from bs4 import BeautifulSoup
from urllib.parse import quote
import requests
import time
import json

collection_url = "https://steamcommunity.com/workshop/filedetails/?id=2229246849"

response = requests.get(collection_url)

collection = BeautifulSoup(response.text, "html.parser")
mod_elements = collection("div", class_="collectionItemDetails")
urls = [mod_element.find("a")["href"] for mod_element in mod_elements]
mods = []

for url in urls:
    response = requests.get(url)
    mod_page = BeautifulSoup(response.text, "html.parser")

    title = mod_page.find("div", class_="workshopItemTitle").text
    description = mod_page.find("div", class_="workshopItemDescription")
    version = mod_page.find("div", class_="rightDetailsBlock").find_all("a")[-1].text

    mod = {
        "name": title,
        "version": version,
        "url": url,
        "updated": time.asctime(),
    }

    if description("span", class_="bb_removedlink"):
        # print(f"{title} has had links removed ({url})")
        mod["censored"] = "links and comments disabled"
    else:
        mod["censored"] = False

    mods.append(mod)
    print(mod)

requests.post(
    "https://hook.eu1.make.com/bsuctkbg5sukw8cbb44o0df4sojq25hv", json={"mods": mods}
)

with open("censorship.json", mode="w", encoding="utf8") as f:
    json.dump({"mods": mods}, f)
