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

    def check_record_exists(self,url,cursor):
        statement = "SELECT * FROM film WHERE letterboxd_url = '" + url + "'"
        cursor.execute(statement)
        row = cursor.fetchone()
        if row:
            return True  # Record exists
        else:
            return False  # Record doesn't exist

    def scrape_data(self,data):

        conn = sqlite3.connect('database/FilmDataDB.db')
        cursor = conn.cursor()
        for film in data:
            if film[0] != 'Date':
                if not self.check_record_exists(film[3],cursor):
                    conn.commit()
                    page = requests.get(film[3])
                    soup = BeautifulSoup(page.content,"html.parser")
                    body = soup.find("body", {"class": "film backdropped"})
                    if body: 
                        tmdb_id = body.get("data-tmdb-id")
                        print(film[1] + ": " + tmdb_id)
                        cursor.execute("INSERT INTO film (film_id,title,release_year,date_added,letterboxd_url) VALUES (?,?,?,?,?)",(tmdb_id,film[1],film[2],film[0],film[3]))
                    else:
                        print(film[1] + " has not been entered into the database and cannot be accessed.")
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
    
    def parse_api(self,line):

        film = {}

        complete_data_details = self.get_tmdb_film_details(line[0])
        complete_data_credits = self.get_tmdb_film_credits(line[0])

        film["genres"] = complete_data_details["genres"] 
        film["production_countries"] = complete_data_details["production_countries"]
        film["runtime"] = complete_data_details["runtime"]
        
        director_info = next(
            (crew for crew in complete_data_credits["crew"] if crew["job"] == "Director"),
            None
        )
        film["director"] = director_info["name"] if director_info else "Unknown Director"

        return film

    def populate_films(self):
        conn = sqlite3.connect('database/FilmDataDB.db')
        cursor = conn.cursor()

        statement = "SELECT * FROM film"
        cursor.execute(statement)
        rows = cursor.fetchall()

        for line in rows:
            if line != "":
                details = self.parse_api(line)
                self.films.append(Film(line[4],line[1],line[2],line[3],line[0],details))

        conn.commit()
        conn.close()

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