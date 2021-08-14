import os
os.system("docker build -t bs4_scraping .")
os.system("docker run -it --name=bs4_container bs4_scraping")
os.system("docker cp bs4_container:data.json .")
os.system("docker rm bs4_container")  

