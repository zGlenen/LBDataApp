import requests
from bs4 import BeautifulSoup

def format_title(film_name):
    film_name = film_name.lower()
    return film_name.replace(" ","-")

film_name = "Big Easy Express"
base_URL = "https://letterboxd.com/film"
film_URL = "/" + format_title(film_name) + "/"
page = requests.get(base_URL + film_URL)
soup = BeautifulSoup(page.content,"html.parser")

body = soup.find("body", {"class": "film backdropped"})

tmdb_id = body.get("data-tmdb-id")

print("ID:",tmdb_id)

