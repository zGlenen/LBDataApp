from Film import Film
from bs4 import BeautifulSoup
from collections import Counter
import sqlite3
import requests
import json

class FilmDataHandler:
    TMDB_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzYTAwZDZlNGFkNzQyYTY0MTZmNjEwYTE0N2E4ODA2NCIsInN1YiI6IjY1OWVlNWVjOTFiNTMwMDFmZGYxZGMxOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.r1uBAc6yrAsFwJxICmap8RrNk8Cf_w1RIwlrwTu4aPM"

    def __init__(self,films):
        self.films = films
        self.output_films = []
        self.unreadable_films = []

    def print_films(self):
        count = 0
        for film in self.output_films:
            if film:
                count += 1
                print(film)
        return count
            
    #Select record from DB using letterboxd url from CSV (will be unique), if it does exist add it to the object list
    def check_record_exists(self,url,cursor):
        exists = False
        statement = "SELECT film.film_id, film.title, film.release_year, film.letterboxd_url, film.date_added, GROUP_CONCAT(DISTINCT g.name) AS genres, GROUP_CONCAT(DISTINCT fc.country) AS countries FROM film INNER JOIN film_genre AS fg ON film.film_id = fg.film_id INNER JOIN genre AS g ON fg.genre_id = g.id INNER JOIN film_country AS fc ON fc.film_id = film.film_id WHERE film.letterboxd_url = ? GROUP BY film.film_id;"
        cursor.execute(statement, (url,))
        row = cursor.fetchone()

        if row:
            details = {
                "genres" : row[5].split(","),
                "production_countries" : row[6].split(",")
            }
            self.films.append(Film(row[4],row[1],row[2],url,row[0],details))
            exists = True  
        
        return exists  

    #Using letterboxd url from CSV get tmdb ID from the button on website
    def scrape_data(self,data):

        conn = sqlite3.connect('database/FilmDataDB.db')
        cursor = conn.cursor()

        for film in data:
            date_added, release_year, title, url = film[0], film[2], film[1], film[3]

            if date_added != 'Date' and not self.check_record_exists(url,cursor):                
                page = requests.get(url)
                soup = BeautifulSoup(page.content,"html.parser")
                tmdb_link = soup.find("a", {"class": "micro-button track-event", "data-track-action": "TMDb", "target": "_blank"})
                
                if tmdb_link:
                    tmdb_url = tmdb_link.get("href")

                    if "tv" not in tmdb_url:  
                        tmdb_id = tmdb_url.split("/")[-2]  # Extract TMDB ID from the URL
                        details = self.parse_api(tmdb_id)

                        if details != 1:
                            cursor.execute("INSERT INTO film (film_id, title, release_year, date_added, letterboxd_url) VALUES (?,?,?,?,?)",
                            (tmdb_id, title, release_year, date_added, url))
                            conn.commit()
                            for g in details["genres"]:
                                cursor.execute("INSERT INTO film_genre (film_id, genre_id) VALUES (?,?)",(tmdb_id,int(g["id"])))
                            for c in details["production_countries"]:
                                cursor.execute("INSERT INTO film_country (film_id, country) VALUES (?,?)",(tmdb_id,c["name"]))

                            tempOb = {
                                "genres" : [],
                                "production_countries" : []
                            }
                            for g in details["genres"]:
                                tempOb["genres"].append(g["name"])
                            details["genres"] = tempOb["genres"]

                            for c in details["production_countries"]:
                                tempOb["production_countries"].append(c["name"])
                            details["production_countries"] = tempOb["production_countries"]

                            self.films.append(Film(date_added,title,release_year,url,tmdb_id,details))
                            print(title + ": " + tmdb_id + " : ")
                            print(details)

                        else:
                            self.unreadable_films.append(f"{title} : {release_year} : NOT IN DB")
                    else:
                        #not readaable as they are a TV show
                        self.unreadable_films.append(f"{title} : {release_year} : TV SHOW")
                else:
                    print(f"{title} {release_year}: Could Not Find TMDb Link")

        conn.commit()
        conn.close()
    
    #Get general details from api
    def get_tmdb_film_details(self,id):
        url = "https://api.themoviedb.org/3/movie/" + str(id)+ "?language=en-US"

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.TMDB_API_KEY}"
        }

        response = requests.get(url, headers=headers)


        return json.loads(response.text)    

    #Get person details from api
    def get_tmdb_film_credits(self,id):
        url = "https://api.themoviedb.org/3/movie/"+str(id)+"/credits?language=en-US"

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.TMDB_API_KEY}"
        }
        response = requests.get(url, headers=headers)

        return json.loads(response.text) 
    
    #Get API info for a single movie using ID
    def parse_api(self,id):

        film = {}

        complete_data_details = self.get_tmdb_film_details(id)
        complete_data_credits = self.get_tmdb_film_credits(id)

        if 'success' not in complete_data_details:
            film["genres"] = complete_data_details["genres"] 
            film["production_countries"] = complete_data_details["production_countries"]
            # film["runtime"] = complete_data_details["runtime"]  #can go into the film table
            # director_info = next((crew for crew in complete_data_credits["crew"] if crew["job"] == "Director"),None)
            # film["director"] = director_info["name"] if director_info else "Unknown Director"
        else:
            film = 1

        return film

    def get_film_by_genre(self, genre,year=0):
        self.output_films.clear()
        count = 0
        for film in self.films:
            if year == 0 or film.year_released == year:
                if film.details != 1 and "genres" in film.details:
                    for g in film.details["genres"]:
                        if g == genre:
                            count += 1
                            self.output_films.append(film)
        return count > 0

    def get_genre_stats(self, year=0):
        genre_list = {}

        for film in self.films:
            if year == 0 or year == film.year:
                if film.details != 1 and "genres" in film.details:
                    for g in film.details["genres"]:
                        if g in genre_list:
                            genre_list[g] += 1
                        else:
                            genre_list[g] = 1
        return genre_list

    def get_most_common_release_year(self):
        if not self.output_films:
            return None

        release_years = [film.year_released for film in self.output_films]
        counter = Counter(release_years)

        most_common_release_year = counter.most_common(1)[0][0]
        return most_common_release_year
    #only needed to run once
    def insert_genre_db(self):
        conn = sqlite3.connect('database/FilmDataDB.db')
        cursor = conn.cursor()

        url = "https://api.themoviedb.org/3/genre/movie/list"

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.TMDB_API_KEY}"
        }

        response = requests.get(url, headers=headers)

        genres = json.loads(response.text)

        for i in genres["genres"]:

            cursor.execute("INSERT INTO genre (id, name) VALUES (?,?)",(i["id"],i["name"]))
                       
        conn.commit()
        conn.close()
