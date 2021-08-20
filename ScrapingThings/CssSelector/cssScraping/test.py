import lxml.html  # type: ignore
import requests
website_url = "https://news.ycombinator.com/"
current_page = 1
temp_list = []

html = requests.get(website_url)
doc = lxml.html.fromstring(html.content)
temp_list.append(html.content)
main_url = website_url
while(current_page < 5):
    next_page_path = doc.cssselect('a[class="morelink"]')[0].get('href')
    website_url = main_url+next_page_path
    html = requests.get(website_url)
    doc = lxml.html.fromstring(html.content)
    temp_list.append(html.content)
    current_page += 1

script = temp_list
doc = lxml.html.fromstring((script)[1])
athing_select = doc.cssselect("tr.athing")
athing_sibling_select = doc.cssselect("tr.athing ~ tr > td.subtext")
index = 0
try:
    while(bool(athing_select[index])):
        
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
            comment = athing_sibling_select[index].cssselect("a")[3].text
        except IndexError:
            comment = "None"
        index += 1
except IndexError:
    print("Finishied Scraping!!!")

