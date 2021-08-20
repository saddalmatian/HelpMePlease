import os
os.system("docker build -t lxml_scraping .")
os.system("docker volume create my_volume2")
os.system("docker run -it -v my_volume2:/getData --name lxml_container lxml_scraping")
os.system("docker cp lxml_container:/getData/data.json .")
os.system("docker rm lxml_container")  
os.system("docker volume rm my_volume2")

