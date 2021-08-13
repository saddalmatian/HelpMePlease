from bs4 import BeautifulSoup  # type: ignore
import model
import requests
import json
import time

from requests import models


def list_add_things(list_temp: list, class_temp: model.PostItem, pk: int):
    """ append things into a temp list to export all"""
    list_temp.append({"model": "myapp.bs4Scraping",
                      "pk": pk,
                      "fields": {
                          "rank": class_temp.rank,
                          "title": class_temp.title,
                          "id_post": class_temp.id_post,
                          "link": class_temp.link,
                          "point": class_temp.point,
                          "user": class_temp.user,
                          "time_post": class_temp.time_post
                      }})

def export_file(list: list):
    """ export the json file from list given"""
    with open("data.json", "w") as f:
        y = json.dumps(list, indent=4)
        f.write(y)


def tr_soup(amount: int, url: str) -> list:
    """ Return the list page scripts with given amount and it's url """
    list_temp=[]
    temp_source = requests.get(url).text
    list_temp.append(temp_source)
    if(amount > 1):
        for x in range(2, amount+1):
            temp_source = requests.get(
                url+"news?p="+str(x)).text
            list_temp.append(temp_source)
    return list_temp


def scraping_web(amount: int, url: str):
    """Start scraping web with given amount page and the url of that page"""
    page_tobe_scraped = tr_soup(amount, url)
    my_scripts_list = [] # type: list[str]
    # Temp list for all of things
    start_time = time.time()
    # Declare all needed variable
    pages = len(page_tobe_scraped)
    soup = BeautifulSoup(page_tobe_scraped[0], 'lxml')
    tr_element = soup.find_all("tr", class_="athing")
    td_element = soup.find_all("td", class_="subtext")
    zone = len(tr_element)
    current_page = 0
    pk = 0
    index = 0
    """Start scraping"""
    while(current_page < pages):

        rank = tr_element[index].find("span", class_="rank").text
        title = tr_element[index].find("a", class_="storylink").text
        link = tr_element[index].find("a", class_="storylink")['href']
        id_post = tr_element[index]['id']

        if td_element[index].find("span", {"id": "score_"+tr_element[index]['id']}) is None:
            point = "null"
        else:
            point = td_element[index].find(
                "span", {"id": "score_"+tr_element[index]['id']}).text

        if(td_element[index].find("a", class_="hnuser") is None):
            user = "unknown"
        else:
            user = td_element[index].find("a", class_="hnuser").text

        if(td_element[index].find("a", {"href": "item?id="+str(id_post)}) is None):
            time_post = "unknown"
        else:
            time_post = td_element[index].find(
                "a", {"href": "item?id="+str(id_post)}).text
        temp_postitem = model.PostItem(rank,title,id_post,link,point,user,time_post)

        """Append things into list"""
        list_add_things(my_scripts_list,temp_postitem,pk)  
        
        pk += 1
        if(index < zone-1):       
            index += 1
        else:
            try:
                current_page += 1
                index = 0
                soup = BeautifulSoup(page_tobe_scraped[current_page], 'lxml')
                tr_element = soup.find_all("tr", class_="athing")
                td_element = soup.find_all("td", class_="subtext")
            except IndexError:
                print("Finished all in:")

    export_file(my_scripts_list)

    print("--- %s seconds ---" % (time.time() - start_time))
