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
        next_page_path = doc.cssselect('a[class="morelink"]')[0].get('href')
        website_url = main_url+next_page_path
        html = requests.get(website_url)
        doc = lxml.html.fromstring(html.content)
        temp_list.append(html.content)
        current_page += 1
    return temp_list


def scraping_main(page_amount: int, url: str):
    """Main Scraping Function"""
    for_extracting_list=[]# type: list[str]
    position=0

    script=gather_html(page_amount,url)
    start_time = time.time()
    current_page = 0

    doc = lxml.html.fromstring((script)[0])
    athing_select = doc.cssselect("tr.athing")
    athing_sibling_select = doc.cssselect("tr.athing ~ tr > td.subtext")
    index = 0
    try:
        while(athing_select[index] is not None):
            
            id_post = athing_select[index].get('id')
            rank = athing_select[index].cssselect('td > span.rank')[
                0].text.replace('.', '')
            title = athing_select[index].cssselect('td > a.storylink')[0].text
            link = athing_select[index].cssselect(
                'td > a.storylink')[0].get('href')

            try:
                point = athing_sibling_select[index].cssselect('span.score')[0].text
            except IndexError:
                point = "none"
            try:
                user = athing_sibling_select[index].cssselect('a.hnuser')[0].text
            except IndexError:
                user = "Unknown"
            try:
                time_post = athing_sibling_select[index].cssselect('span.age > a')[0].text
            except IndexError:
                time_post = "Unknown"
            try:
                comment = athing_sibling_select[index].cssselect("a")[3].text.replace("\u00a0"," ")
            except IndexError:
                comment = "None"
            temp_postitem = PostItem(
            rank, title, id_post, link, point, user, time_post,comment)
            list_add_things(for_extracting_list,temp_postitem,position)
            position+=1
            index += 1
            try:
                temp=athing_select[index]         
            except IndexError:
                current_page+=1
                doc = lxml.html.fromstring((script)[current_page])
                index=0
                athing_select = doc.cssselect("tr.athing")
                athing_sibling_select = doc.cssselect("tr.athing ~ tr > td.subtext")

    except IndexError:
        print("Finishied Scraping!!!")

    export_file(for_extracting_list)
    print("--- %s seconds ---" % (time.time() - start_time))

