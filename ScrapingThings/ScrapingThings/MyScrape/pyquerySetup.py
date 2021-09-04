import os
os.system("docker build -t myscrape_scraping .")
os.system("docker volume create my_volume5")
os.system("docker run -it -v my_volume5:/getData --name myscrape_container myscrape_scraping")
os.system("docker cp myscrape_container:/getData/data.json .")
os.system("docker rm myscrape_container")  
os.system("docker volume rm my_volume5")

