import lxml.html # type: ignore
import requests
import time,json
from model import PostItem

def export_file(list: list):
    """ export the json file from list given"""
    with open("getData/data.json", "w") as f:
        y = json.dumps(list, indent=4)
        f.write(y)

from requests.models import ChunkedEncodingError

def list_add_things(list_temp: list, class_temp: PostItem, position: int):
    """ append model element into a temp list to export json file with position is specific id """
    list_temp.append({"model": "myapp.bs4Scraping",
                      "pk": position,
                      "fields": {
                          "rank": class_temp.rank,
                          "title": class_temp.title,
                          "id_post": class_temp.id_post,
                          "link": class_temp.link,
                          "point": class_temp.point,
                          "user": class_temp.user,
                          "time_post": class_temp.time_post,
                          "comment":class_temp.comment
                      }})


def path_append(current_path: str, appended_path: str) -> str:
    """Find child of current path"""
    return current_path+appended_path


def gather_html(page_amount: int, website_url: str) -> list:
    """Get html content list of website with given amount"""
    current_page = 1
    temp_list = []

    html = requests.get(website_url)
    doc = lxml.html.fromstring(html.content)
    temp_list.append(html.content)
    main_url = website_url
    while(current_page < page_amount):
        next_page_path = doc.xpath('//tr/td/a[@class="morelink"]/@href')
        website_url = main_url+next_page_path[0]
        html = requests.get(website_url)
        doc = lxml.html.fromstring(html.content)
        temp_list.append(html.content)
        current_page += 1
    return temp_list


def scraping_main(page_amount: int, url: str):
    """Main Scraping Function"""
    for_extracting_list=[]# type: list[str]
    position=0
    pair = 1
    
    script=gather_html(page_amount,url)
    start_time = time.time()

    athing_path = '//tr[@class="athing"]['+str(pair)+']'
    athing_path_sibling = path_append(athing_path, '/following::tr[1]')
    doc = lxml.html.fromstring((script)[0])
    current_page = 0
    while(bool(doc.xpath(athing_path)) is not False):

        id_post = doc.xpath(path_append(athing_path, '/@id'))[0]
        rank = doc.xpath(path_append(
            athing_path, '/td/span[@class="rank"]/text()'))[0]
        title = doc.xpath(path_append(
            athing_path, '/td/a[@class="storylink"]/text()'))[0]
        link = doc.xpath(path_append(
            athing_path, '/td/a[@class="storylink"]/@href'))[0]

        try:
            point = doc.xpath(path_append(athing_path_sibling,
                                          '/td/span[@class="score"]/text()'))[0]
        except IndexError:
            point = "None"
        try:
            user = doc.xpath(path_append(athing_path_sibling,
                                         '/td/a[@class="hnuser"]/text()'))[0]
        except IndexError:
            user = "Unknown"
        try:
            time_post = doc.xpath(path_append(
                athing_path_sibling, '/td/span[@class="age"]/a/text()'))[0]
        except IndexError:
            time_post = "Unknown"
        try:
            comment = doc.xpath(path_append(athing_path_sibling,
                                            '/td/a[3]/text()'))[0].replace("\u00a0"," ")
        except IndexError:
            comment = "None"
        pair += 1

        temp_postitem = PostItem(
            rank, title, id_post, link, point, user, time_post,comment)
        list_add_things(for_extracting_list,temp_postitem,position)
        position+=1

        athing_path = '//tr[@class="athing"]['+str(pair)+']'
        athing_path_sibling = path_append(athing_path, '/following::tr[1]')
        if(bool(doc.xpath(athing_path)) is False):
            current_page += 1
            try:
                doc = lxml.html.fromstring(
                    (script)[current_page])
                pair = 1
                athing_path = '//tr[@class="athing"]['+str(pair)+']'
                athing_path_sibling = path_append(
                    athing_path, '/following::tr[1]')

            except IndexError:
                print("Finished")

    export_file(for_extracting_list)
    print("--- %s seconds ---" % (time.time() - start_time))


scraping_main(5, "https://news.ycombinator.com/")
