from bs4 import BeautifulSoup # type: ignore
from model import PostItem
import time
import json
import requests


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
    """ Get the scripts of the website we want to scrape then put it into a soup"""
    page_select=1
    list_temp = []
    temp_source = requests.get(website_url).text
    list_temp.append(temp_source)
    temp_url=website_url
    while(page_select<page_amount):
        soup = BeautifulSoup(temp_source,'html.parser')
        website_url=temp_url+soup.find("a",class_='morelink')['href']
        temp_source = requests.get(website_url).text
        list_temp.append(temp_source)
        page_select+=1

    return list_temp

def scraping_main(pages_amount: int,website_url: str):
    """Main Scraping Function"""
    for_extracting_list=[]
    page_select=0
    position=0
    script=gather_all_scripts(pages_amount,website_url)
    start_time = time.time()
    soup=BeautifulSoup(script[page_select],'html.parser')
    athing_class=soup.find("tr",class_="athing")
    while(athing_class is not None ):
    
        athing_class_sibling = athing_class.nextSibling
        id_post = athing_class['id']
        rank = athing_class.contents[1].text
        link = athing_class.contents[4].a['href']
        title = athing_class.contents[4].a.text

        if(athing_class_sibling.contents[1].find('span', class_="score") is not None):
            point = athing_class_sibling.contents[1].find('span', class_="score").text
        else:
            point = "0 points"
        if(athing_class_sibling.contents[1].find('a', class_="hnuser") is not None):
            user = athing_class_sibling.contents[1].find('a', class_="hnuser").text
        else:
            user = "unknown!!!"

        time_post = athing_class_sibling.contents[1].find('span', class_="age").a.text
        try:
            comment = athing_class_sibling.contents[1].find_all('a', {'href':"item?id="+id_post})[1].text.replace("\u00a0"," ")
        except IndexError:
            comment = "Not available"

        temp_postitem = PostItem(
            rank, title, id_post, link, point, user, time_post,comment)
        list_add_things(for_extracting_list,temp_postitem,position)
        position+=1
        athing_class = athing_class.find_next("tr", class_="athing")

        if(athing_class is None and page_select<pages_amount):     
            page_select+=1      
            try:
                soup=BeautifulSoup(script[page_select],'html.parser')           
                athing_class=soup.find("tr",class_="athing")
            except IndexError:
                print("Finish")
    export_file(for_extracting_list)
    print("--- %s seconds ---" % (time.time() - start_time))


    