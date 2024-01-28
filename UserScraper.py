import requests
from bs4 import BeautifulSoup

class UserScraper:
    def __init__(self, base_url="https://letterboxd.com/"):
        self.base_url = base_url

    def scrape_user(self, username):
        films = []

        last_page_number = self.get_last_page_number(username)

        for page_number in range(1, last_page_number + 1):
            url_addon = f"page/{page_number}" if page_number > 1 else ""
            url = f"{self.base_url}{username}/films/{url_addon}"

            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")

            li_elements = soup.find_all("li", class_="poster-container")

            for li in li_elements:
                div_element = li.find('div', class_='really-lazy-load',)
                name = div_element.get('data-film-slug')
                films.append(name)

        return films

    def get_last_page_number(self, username):
        url = f"{self.base_url}{username}/films/"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        last_page_element = soup.select_one('.paginate-pages ul li.paginate-page:last-child a')
        return int(last_page_element.text) if last_page_element else 1

    def get_uris(self, films):
        return [f"{self.base_url}film/{slug}/" for slug in films]
