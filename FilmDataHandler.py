from Film import Film
from datetime import datetime
from bs4 import BeautifulSoup
import sqlite3
import requests
import json

class FilmDataHandler:
    def __init__(self,films):
        self.films = films
        self.output_films = []
        self.unreadable_films = []

    def print_films(self):
        for film in self.output_films:
            if film:
                print(film)
            
    def check_record_exists(self,url,cursor):
        statement = "SELECT * FROM film WHERE letterboxd_url = '" + url + "'"
        cursor.execute(statement)
        row = cursor.fetchone()
        if row:
            details = self.parse_api(row[0])
            self.films.append(Film(row[4],row[1],row[2],url,row[0],details))
            return True  # Record exists
        else:
            return False  # Record doesn't exist

    def scrape_data(self,data):

        conn = sqlite3.connect('database/FilmDataDB.db')
        cursor = conn.cursor()
        for film in data:

            date_added = film[0]
            release_year = film[2]
            title = film[1]
            url = film[3]

            if date_added != 'Date':
                if not self.check_record_exists(url,cursor):
                    conn.commit()
                    page = requests.get(url)
                    soup = BeautifulSoup(page.content,"html.parser")

                    tmdb_link = soup.find("a", {"class": "micro-button track-event", "data-track-action": "TMDb", "target": "_blank"})
                    
                    if tmdb_link:
                        tmdb_url = tmdb_link.get("href")
                        if "tv" not in tmdb_url:  # Check if "tv" is in the href
                            tmdb_id = tmdb_url.split("/")[-2]  # Extract TMDB ID from the URL
                            print(title + ": " + tmdb_id)
                            
                            cursor.execute("INSERT INTO film (film_id, title, release_year, date_added, letterboxd_url) VALUES (?,?,?,?,?)",
                                        (tmdb_id, title, release_year, date_added, url))
                            
                            details = self.parse_api(tmdb_id)
                            if details != 1:
                                self.films.append(Film(date_added,title,release_year,url,tmdb_id,details))
                            else:
                                self.unreadable_films.append(f"{title} : {release_year} : NOT IN DB")
                        else:
                            #not readaable as they are a TV show
                            self.unreadable_films.append(f"{title} : {release_year} : TV SHOW")
                    else:
                        print(f"{title} {release_year}: Could Not Find TMDb Link")
        conn.commit()
        conn.close()
    
    def get_tmdb_film_details(self,id):
        url = "https://api.themoviedb.org/3/movie/" + str(id)+ "?language=en-US"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzYTAwZDZlNGFkNzQyYTY0MTZmNjEwYTE0N2E4ODA2NCIsInN1YiI6IjY1OWVlNWVjOTFiNTMwMDFmZGYxZGMxOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.r1uBAc6yrAsFwJxICmap8RrNk8Cf_w1RIwlrwTu4aPM"
        }

        response = requests.get(url, headers=headers)


        return json.loads(response.text)    

    def get_tmdb_film_credits(self,id):
        url = "https://api.themoviedb.org/3/movie/"+str(id)+"/credits?language=en-US"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzYTAwZDZlNGFkNzQyYTY0MTZmNjEwYTE0N2E4ODA2NCIsInN1YiI6IjY1OWVlNWVjOTFiNTMwMDFmZGYxZGMxOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.r1uBAc6yrAsFwJxICmap8RrNk8Cf_w1RIwlrwTu4aPM"
        }

        response = requests.get(url, headers=headers)

        return json.loads(response.text) 
    
    def parse_api(self,id):

        film = {}

        complete_data_details = self.get_tmdb_film_details(id)
        complete_data_credits = self.get_tmdb_film_credits(id)

        if 'success' not in complete_data_details:
            film["genres"] = complete_data_details["genres"] 
            film["production_countries"] = complete_data_details["production_countries"]
            film["runtime"] = complete_data_details["runtime"]
            director_info = next(
                (crew for crew in complete_data_credits["crew"] if crew["job"] == "Director"),
                None
            )
            film["director"] = director_info["name"] if director_info else "Unknown Director"
        else:
            film = 1

        return film

    def check_year_released(self,year,year2):
        firstLine = True
        for film in self.films:
            if not firstLine:
                if int(film.year) >= int(year) and int(film.year) <= int(year2):
                    self.output_films.append(Film(film.date,film.name,film.year,film.letterboxd_uri))
            firstLine = False

    def check_date_added(self,date,date2):
        firstLine = True
        for film in self.films:
            if not firstLine:
                if datetime.strptime(film.date,'%Y-%m-%d') >= datetime.strptime(date,'%Y-%m-%d') and datetime.strptime(film.date,'%Y-%m-%d') <= datetime.strptime(date2,'%Y-%m-%d'):
                    self.output_films.append(Film(film.date,film.name,film.year,film.letterboxd_uri))
            firstLine = False

    def get_film_by_genre(self, genre):
        count = 0
        for film in self.films:
            if film.details != 1 and "genres" in film.details:
                for g in film.details["genres"]:
                    if g.get("name") == genre:
                        count += 1
                        self.output_films.append(film)
        return count > 0

    def get_genre_stats(self, year=0):
        genre_list = {}

        for film in self.films:
            if year == 0 or year == film.year:
                if film.details != 1 and "genres" in film.details:
                    for g in film.details["genres"]:
                        if g["name"] in genre_list:
                            genre_list[g["name"]] += 1
                        else:
                            genre_list[g["name"]] = 1
        return genre_list
