from FilmDetails import FilmDetails, Genre, Person, Film
from bs4 import BeautifulSoup
from collections import Counter
import sqlite3
import requests
import json
import re
from datetime import datetime 
username = "reedmac"
base_url="https://letterboxd.com/"
films = []

def get_last_page_number(username):
    url = f"{base_url}{username}/films/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    last_page_element = soup.select_one('.paginate-pages ul li.paginate-page:last-child a')
    return int(last_page_element.text) if last_page_element else 1

last_page_number = get_last_page_number(username)

for page_number in range(1, last_page_number + 1):
    url_addon = f"page/{page_number}" if page_number > 1 else ""
    url = f"{base_url}{username}/films/diary/{url_addon}"

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    with open('files/page_content.html', 'w') as f:
        f.write(str(soup.prettify().encode('ascii', 'ignore').decode('ascii')))

#     li_elements = soup.find_all("li", class_="poster-container")

#     for li in li_elements:
#         div_element = li.find('div', class_='really-lazy-load',)
#         name = div_element.get('data-film-slug')
#         rating_span = li.find('span', class_='rating')
#         rating = rating_span.get_text(strip=True) if rating_span else None
#         films.append((name,rating))

# print(films)

