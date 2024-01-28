from bs4 import BeautifulSoup
import requests

url = 'https://boxd.it/21Xw7h'

page = requests.get(url)
soup = BeautifulSoup(page.content,"html.parser")

span_el = soup.find("span", class_="film-title-wrapper")

a_el = span_el.find("a")

href = a_el.get("href")

print(href)