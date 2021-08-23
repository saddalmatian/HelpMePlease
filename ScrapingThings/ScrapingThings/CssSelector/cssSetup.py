import os
os.system("docker build -t css_scraping .")
os.system("docker volume create my_volume4")
os.system("docker run -it -v my_volume4:/getData --name css_container css_scraping")
os.system("docker cp css_container:/getData/data.json .")
os.system("docker rm css_container")  
os.system("docker volume rm my_volume4")

