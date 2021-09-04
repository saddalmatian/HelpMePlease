from os import pardir
import requests
from model import Pal, PostItem
import requests
import json
import time


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
    html = requests.get(website_url)
    pal=Pal(html.content.decode("utf-8"))
    main_url=website_url
    list_temp.append(pal)
    while(current_page<page_amount):
        next_page = pal.findBy("a","class.morelink")[0].text()
        website_url = main_url+next_page
        r = requests.get(website_url)
        pal=Pal(html.content.decode("utf-8"))
        list_temp.append(pal)
        current_page += 1
    
    return list_temp

def scraping_main(pages_amount: int,website_url: str):
    """Main Scraping Function"""
    for_extracting_list=[]
    page_select=0
    
    script=gather_all_scripts(pages_amount,website_url)
    start_time = time.time()
    pal=script[page_select]
    position=0
    trAthing=pal.findBy("tr","class.athing")[position]
    trAthingSibling=trAthing.getSibling("tr")[0]
    try:
        while(page_select<pages_amount):
            
            id_post = trAthing.get("id")
            rank = trAthing.findBy("span","class.rank")[0].text()
            title = trAthing.findBy("a","class.storylink")[0].text()
            link = trAthing.findBy("a","class.storylink")[0].get("href")
            try:
                point = trAthingSibling.findBy("span","class.score")[0].text()
            except IndexError:
                point = "none"
           
            try:
                user = trAthingSibling.findBy("a","class.hnuser")[0].text()
            except IndexError:
                user = "Unknown"
            try:
                time_post = trAthingSibling.findBy("span","class.age")[0].text()
            except IndexError:
                time_post = "Unknown"
            try:
                comment = trAthingSibling.findBy("a","href.item?id="+id_post)[1].text().replace("&nbsp;"," ")
            except IndexError:
                comment = "None"
            temp_postitem = PostItem(
            rank, title, id_post, link, point, user, time_post,comment)
            list_add_things(for_extracting_list,temp_postitem,position)
            position+=1
            try:
                trAthing=pal.findBy("tr","class.athing")[position]
                trAthingSibling=trAthing.getSibling("tr")[0]    
            except IndexError:
                position=0
                page_select+=1
                pal=script[page_select]
                trAthing=pal.findBy("tr","class.athing")[position]
                trAthingSibling=trAthing.getSibling("tr")[0]   
            
    except IndexError:
        print("Finish")

    export_file(for_extracting_list)    
    print("--- %s seconds ---" % (time.time() - start_time))