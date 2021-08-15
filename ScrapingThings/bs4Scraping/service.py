from bs4 import BeautifulSoup # type: ignore
import time,json,requests
from model import PostItem

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
                          "time_post": class_temp.time_post,
                          "comment":class_temp.comment
                      }})

def export_file(list: list):
    """ export the json file from list given"""
    with open("data.json", "w") as f:
        y = json.dumps(list, indent=4)
        f.write(y)

def gather_all_scripts(page_amount: int, website_url: str) -> list:
    """ Get the scripts of the website we want to scrape then put it into a soup"""
    pages=1
    list_temp = []
    temp_source = requests.get(website_url).text
    list_temp.append(temp_source)
    temp_url=website_url
    while(pages<page_amount):
        soup = BeautifulSoup(temp_source,'lxml')
        website_url=temp_url+soup.find("a",class_='morelink')['href']
        temp_source = requests.get(website_url).text
        list_temp.append(temp_source)
        pages+=1

    return list_temp

def scraping_main(pages_amount: int,website_url: str):
    for_extracting_list=[]
    pages=0
    pk=0
    script=gather_all_scripts(pages_amount,website_url)
    start_time = time.time()
    soup=BeautifulSoup(script[pages],'lxml')
    pair_one=soup.find("tr",class_="athing")
    while(pair_one is not None ):
    
        pair_two = pair_one.nextSibling
        id_post = pair_one['id']
        rank = pair_one.contents[1].text
        link = pair_one.contents[4].a['href']
        title = pair_one.contents[4].a.text

        if(pair_two.contents[1].find('span', class_="score") is not None):
            point = pair_two.contents[1].find('span', class_="score").text
        else:
            point = "0 points"
        if(pair_two.contents[1].find('a', class_="hnuser") is not None):
            user = pair_two.contents[1].find('a', class_="hnuser").text
        else:
            user = "unknown!!!"

        time_post = pair_two.contents[1].find('span', class_="age").a.text
        try:
            comment = pair_two.contents[1].find_all('a', {'href':"item?id="+id_post})[1].text.replace("\u00a0"," ")
        except IndexError:
            comment = "Not available"

        temp_postitem = PostItem(
            rank, title, id_post, link, point, user, time_post,comment)
        list_add_things(for_extracting_list,temp_postitem,pk)
        pk+=1
        pair_one = pair_one.find_next("tr", class_="athing")

        if(pair_one is None and pages<pages_amount):     
            pages+=1      
            try:
                soup=BeautifulSoup(script[pages],'lxml')           
                pair_one=soup.find("tr",class_="athing")
            except IndexError:
                print("Finish")
    export_file(for_extracting_list)
    print("--- %s seconds ---" % (time.time() - start_time))


    