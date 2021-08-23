import os
os.system("docker build -t pyquery_scraping .")
os.system("docker volume create my_volume3")
os.system("docker run -it -v my_volume3:/getData --name pyquery_container pyquery_scraping")
os.system("docker cp pyquery_container:/getData/data.json .")
os.system("docker rm pyquery_container")  
os.system("docker volume rm my_volume3")

