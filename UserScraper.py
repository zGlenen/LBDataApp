import requests
from bs4 import BeautifulSoup
from DataHandler import DataHandler


class WebScrapper:
    def scrape_user(self,username):

        url = f"https://letterboxd.com/{username}/films/"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        data = []

        last_page_element = soup.select_one('.paginate-pages ul li.paginate-page:last-child a')
        if last_page_element:
            last_page_number = int(last_page_element.text)
        else:
            last_page_number = 1

        for i in range(1,last_page_number+1):
            url_addon = ""
            if i > 1:
                url_addon = f"page/{i}"
            page = requests.get(url + url_addon)
            soup = BeautifulSoup(page.content, "html.parser")

            li_elements = soup.find_all("li", class_="poster-container")

            for li in li_elements:
                div_element = li.find('div', class_='really-lazy-load',)

                name = div_element.get('data-film-slug')
                data.append(f"{name}")

        return data
    
    def get_uris(self,films):
        data = []
        for slug in films:
            letterboxd_url = f"https://letterboxd.com/film/{slug}/"
            data.append(letterboxd_url)
        return data
    
