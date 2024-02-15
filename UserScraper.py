import requests
from bs4 import BeautifulSoup
from datetime import datetime

class UserScraper:
    def __init__(self, base_url="https://letterboxd.com/"):
        self.base_url = base_url
        self.type = None

    def scrape_user(self, username, type):
        films = []
        self.type = type

        last_page_number = self.get_last_page_number(username)

        for page_number in range(1, last_page_number + 1):
            url_addon = f"page/{page_number}" if page_number > 1 else ""
            url = f"{self.base_url}{username}/{self.type}/{url_addon}"

            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")

            if self.type == 'films/diary':
                tr_elements = soup.find_all("tr", class_="diary-entry-row")
                for tr in tr_elements:
                    div_element = tr.find('div', class_='linked-film-poster')
                    film_name = div_element.get('data-film-slug')
                    rating_span = tr.find('span', class_='rating')
                    rating = rating_span.get_text(strip=True) if rating_span else None
                    date_td = tr.find('td', class_='td-day')
                    date_href = date_td.find('a', href=True)
                    date_parts = date_href['href'].split('/')
                    year, month, day = date_parts[5], date_parts[6], date_parts[7]
                    
                    # Combine year, month, and day into a single string in 'YYYY/MM/DD' format
                    date_str = f"{year}/{month}/{day}"
                    
                    # Convert the date string to a datetime object
                    date_obj = datetime.strptime(date_str, '%Y/%m/%d')
                    films.append((film_name, rating, date_obj))
            else:
                li_elements = soup.find_all("li", class_="poster-container")

                for li in li_elements:
                    div_element = li.find('div', class_='really-lazy-load',)
                    name = div_element.get('data-film-slug')
                    rating_span = li.find('span', class_='rating')
                    rating = rating_span.get_text(strip=True) if rating_span else None
                    films.append((name,rating,None))

        return films

    def get_last_page_number(self, username):
        url = f"{self.base_url}{username}/{type}/"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        last_page_element = soup.select_one('.paginate-pages ul li.paginate-page:last-child a')
        return int(last_page_element.text) if last_page_element else 1

    def get_uris(self, films):

        x = []
        for slug, rating, date in films:
            slug = f"{self.base_url}film/{slug}/"
            x.append((slug,rating,date))
        return x
