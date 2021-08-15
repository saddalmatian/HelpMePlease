import os
os.system("docker build -t bs4_scraping .")
os.system("docker volume create my_volume")
os.system("docker run -it -v my_volume:/getData --name bs4_container bs4_scraping")
os.system("docker cp bs4_container:/getData/data.json .")
os.system("docker rm bs4_container")  
os.system("docker volume rm my_volume")

