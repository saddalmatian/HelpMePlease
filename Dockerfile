FROM python:3

ADD ./ScrapingThings .
WORKDIR /
RUN pip install -r requirements.txt

CMD [ "python","/bs4Scraping/main.py" ]

