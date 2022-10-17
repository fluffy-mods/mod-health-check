from bs4 import BeautifulSoup
import requests
import time

collection_url = "https://steamcommunity.com/workshop/filedetails/?id=2229246849"

response = requests.get(collection_url)

collection = BeautifulSoup(response.text, "html.parser")
mods = collection("div", class_="collectionItemDetails")
urls = [mod.find("a")["href"] for mod in mods]

for url in urls:
    response = requests.get(url)
    mod = BeautifulSoup(response.text, "html.parser")

    title = mod.find("div", class_="workshopItemTitle").text
    description = mod.find("div", class_="workshopItemDescription")
    version = mod.find(
        "div", class_="rightDetailsBlock").find_all("a")[-1].text

    if description("span", class_="bb_removedlink"):
        # print(f"{title} has had links removed ({url})")
        print(
            f"\"{title}\", \"{time.asctime()}\", \"links removed\", \"{version}\"\n")
    else:
        print(
            f"\"{title}\", \"{time.asctime()}\", \"OK\", \"{version}\"\n")
