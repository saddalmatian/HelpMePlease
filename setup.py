import os
os.system("docker build -t bs4_scraping .")
os.system("docker run -it --name=bs4_container_thing bs4_scraping /bin/bash")
# os.system("docker cp bs4_container_thing:/bs4Scraping/data.json .")
# os.system("docker exec -it bs4_container_thing python main.py")
# os.system("docker stop bs4_container_thing")