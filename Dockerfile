FROM python:3
ADD ./ScrapingThings .
RUN pip install -r requirements.txt

CMD [ "python3","bs4Scraping/main.py" ]

