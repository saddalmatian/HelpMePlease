from bs4 import BeautifulSoup
import bs4  # type: ignore
from .model import PostItem
import requests
import json
import time



def list_add_things(list_temp: list, class_temp: PostItem, pk: int):
    """ append model element into a temp list to export json file with pk is id """
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


def gather_all_scripts(amount: int, url: str) -> list:
    """ Get the scripts of the website we want to scrape then put it into a soup"""
    list_temp = []
    temp_source = requests.get(url).text
    list_temp.append(temp_source)
    if(amount > 1):
        for x in range(2, amount+1):
            temp_source = requests.get(
                url+"news?p="+str(x)).text
            list_temp.append(temp_source)
    return list_temp


def soup_find_specific(tag: str, name_class: str, a_soup: bs4.BeautifulSoup) -> bs4.element.ResultSet:
    """ Faster way to use find function in bs4 """
    return a_soup.find_all(tag, class_=name_class)


def scraping_web(amount: int, url: str):
    """Start scraping web with given amount page and the url of that page"""
    my_scripts_list = []  # type: list[str]
    # Temp list for all of things
    script = gather_all_scripts(amount, url)
    start_time = time.time()
    # Declare all needed variable
    soup = BeautifulSoup(script[0], 'lxml')
    tr_element = soup_find_specific("tr", "athing", soup)
    td_element = soup_find_specific("td", "subtext", soup)
    current_page = 0
    pk = 0
    index = 0

    """Start scraping"""
    while(current_page < amount):
        """Get all the things we need"""
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
        temp_postitem = PostItem(
            rank, title, id_post, link, point, user, time_post)

        """Append things into list for extracting json file"""
        list_add_things(my_scripts_list, temp_postitem, pk)

        pk += 1
        if(index < len(tr_element)-1):
            index += 1
        else:
            try:
                current_page += 1
                index = 0
                soup = BeautifulSoup(script[current_page], 'lxml')
                tr_element = soup_find_specific("tr", "athing", soup)
                td_element = soup_find_specific("td", "subtext", soup)
            except IndexError:
                print("Finished all in:")

    export_file(my_scripts_list)

    print("--- %s seconds ---" % (time.time() - start_time))
