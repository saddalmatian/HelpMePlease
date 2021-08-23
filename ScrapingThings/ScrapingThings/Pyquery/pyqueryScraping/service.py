from pyquery import PyQuery # type: ignore
from model import PostItem
import json,time,requests

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

def export_file(list: list):
    """ export the json file from list given"""
    with open("getData/data.json", "w") as f:
        y = json.dumps(list, indent=4)
        f.write(y)

def gather_all_scripts(page_amount: int, website_url: str) -> list:
    list_temp = []
    current_page = 1
    r = requests.get(website_url)
    html = PyQuery(r.text)
    main_url=website_url
    list_temp.append(html)
    while(current_page<page_amount):
        next_page_path = html('a[class="morelink"]').attr('href')
        website_url = main_url+next_page_path
        r = requests.get(website_url)
        html = PyQuery(r.text)
        list_temp.append(html)
        current_page += 1
    
    return list_temp

def scraping_main(pages_amount: int,website_url: str):
    start_time = time.time()
    """Main Scraping Function"""
    for_extracting_list=[]# type: list[str]
    position=0
    pair = 1
    
    script=gather_all_scripts(pages_amount,website_url)
    start_time = time.time()
    pair=0
    current_page = 0
    athing_path = script[current_page]('tr[class="athing"]').eq(pair)
    athing_path_sibling = athing_path.next()
    while(bool(athing_path)is True):
        id_post = athing_path.attr('id')
        rank = athing_path('span[class="rank"]').text()
        title = athing_path('a[class="storylink"]').text()
        link = athing_path('a[class="storylink"]').attr('href')
        if(bool(athing_path_sibling('span[class="score"]'))==True):
            point = athing_path_sibling('span[class="score"]').text()
        else:
            point = "none"
        if(bool(athing_path_sibling('a[class="hnuser"]'))==True):
            user = athing_path_sibling('a[class="hnuser"]').text()
        else:
            user = "unknown"
        
        if(bool(athing_path_sibling('span[class="age"]'))==True):
            time_post = athing_path_sibling('span[class="age"]').text()
        else:
            time_post = "unknown"
        if(bool(athing_path_sibling('a').eq(3))==True):
            comment = athing_path_sibling('a').eq(3).text().replace("\u00a0"," ")
        else:
            comment = "None"
        pair+=1
        temp_postitem = PostItem(
                rank, title, id_post, link, point, user, time_post,comment)
        
        list_add_things(for_extracting_list,temp_postitem,position)
        position+=1
        athing_path = script[current_page]('tr[class="athing"]').eq(pair)
        athing_path_sibling = athing_path.next()
        if(bool(athing_path) is False):
            current_page += 1
            try:
                pair = 0
                athing_path = script[current_page]('tr[class="athing"]').eq(pair)
                athing_path_sibling = athing_path.next()
            except IndexError:
                print("Finished")
    export_file(for_extracting_list)

    print("--- %s seconds ---" % (time.time() - start_time))



    