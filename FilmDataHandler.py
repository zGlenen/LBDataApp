from Film import Film
from FilmDetails import FilmDetails, Genre, Person
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
        statement = "SELECT film.film_id, film.title, film.release_year, film.letterboxd_url, film.date_added, GROUP_CONCAT(DISTINCT g.name) AS genres, GROUP_CONCAT(DISTINCT fc.country) AS countries, film.runtime FROM film INNER JOIN film_genre AS fg ON film.film_id = fg.film_id INNER JOIN genre AS g ON fg.genre_id = g.id INNER JOIN film_country AS fc ON fc.film_id = film.film_id WHERE film.letterboxd_url = ? GROUP BY film.film_id;"
        cursor.execute(statement, (url,))
        row = cursor.fetchone()

        if row:

            id = row[0]
            title = row[1]
            release_year = row[2]
            date_added = row[4]
            letterboxd_url = row[3]
            genres = row[5].split(",")
            production_countries = row[6].split(",")
            runtime = row[7]
            cast = []
            crew = []
            
            statement = "SELECT pcast.person_id, p.name, pcast.character FROM film_person_cast AS pcast INNER JOIN person AS p ON pcast.person_id = p.id WHERE film_id = ? "
            cursor.execute(statement, (id,))
            cast_row = cursor.fetchall()
            for c in cast_row:
                p_id = c[0]
                p_name = c[1]
                p_character = c[2]
                cast.append(Person(p_id,p_name,character=p_character))

            statement = "SELECT pcrew.person_id, p.name, pcrew.job FROM film_person_crew AS pcrew INNER JOIN person AS p ON pcrew.person_id = p.id WHERE film_id = ?"
            cursor.execute(statement, (id,))
            crew_row = cursor.fetchall()
            for c in crew_row:
                p_id = c[0]
                p_name = c[1]
                p_job = c[2]
                crew.append(Person(p_id,p_name,job=p_job))

            self.films.append(Film(date_added,title,release_year,letterboxd_url,id,FilmDetails(genres,production_countries,runtime,cast,crew)))
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
                        details = self.parse_api(tmdb_id,cursor)

                        if details:
                            cursor.execute("INSERT INTO film (film_id, title, release_year, date_added, letterboxd_url, runtime) VALUES (?,?,?,?,?,?)",
                            (tmdb_id, title, release_year, date_added, url, details.runtime))
                            conn.commit()
                            for g in details.genres:
                                cursor.execute("INSERT INTO film_genre (film_id, genre_id) VALUES (?,?)",(tmdb_id,int(g.id)))
                            for c in details.production_countries:
                                cursor.execute("INSERT INTO film_country (film_id, country) VALUES (?,?)",(tmdb_id,c))

                            for p in details.cast:
                                cursor.execute("SELECT * FROM film_person_cast WHERE film_id = ? AND person_id = ?", (tmdb_id, p.id))
                                existing_record = cursor.fetchone()
                                
                                if existing_record is None:
                                    cursor.execute("INSERT INTO film_person_cast (film_id, person_id, character) VALUES (?, ?, ?)", (tmdb_id, p.id, p.character))
                                else:
                                    print(f"Record with film_id={tmdb_id} and person_id={p.id} already exists.")

                            for p in details.crew:
                                cursor.execute("SELECT * FROM film_person_crew WHERE film_id = ? AND person_id = ?", (tmdb_id, p.id))
                                existing_record = cursor.fetchone()
                                
                                if existing_record is None:
                                    cursor.execute("INSERT INTO film_person_crew (film_id, person_id, job) VALUES (?, ?, ?)", (tmdb_id, p.id, p.job))
                                else:
                                    print(f"Record with film_id={tmdb_id} and person_id={p.id} already exists.")

                        
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
    def parse_api(self,id,cursor):
        complete_data_details = self.get_tmdb_film_details(id)
        complete_data_credits = self.get_tmdb_film_credits(id)

        if 'success' not in complete_data_details:
            people = self.insert_person_db(complete_data_credits,cursor)

            runtime = complete_data_details["runtime"]  
            genres = []
            production_countries = []
            cast = []
            crew = []

            for g in complete_data_details["genres"]:
                g_id = g["id"]
                g_name = g["name"]
                genres.append(Genre(g_id,g_name))     
                
            for c in complete_data_details["production_countries"]:
                pc_name = c["name"]
                production_countries.append(pc_name)

            for p in people:
                p_id = p["id"]
                p_name = p["name"]
                if "character" in p:
                    p_character = p["character"]
                    cast.append(Person(p_id,p_name,character=p_character))
                else:
                    p_job = p["job"]
                    crew.append(Person(p_id,p_name,job=p_job))
        else:
            return None

        return FilmDetails(genres,production_countries,runtime,cast,crew)

    def get_film_by_genre(self, genre,year=0):
        self.output_films.clear()
        count = 0
        for film in self.films:
            if year == 0 or film.year_released == year:
                if film.details:
                    for g in film.details.genres:
                        if g == genre:
                            count += 1
                            self.output_films.append(film)
        return count > 0

    def get_genre_stats(self, year=0):
        genre_list = {}

        for film in self.films:
            if year == 0 or year == film.year_released:
                if film.details:
                    for g in film.details.genres:
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

    def insert_person_db(self,credits,cursor):
        people = credits['cast']
        people.extend(credits['crew'])

        for p in people:
            statement = "SELECT * from person WHERE person.id = ?"
            cursor.execute(statement, (p["id"],))
            row = cursor.fetchone()

            if not row:
                cursor.execute("INSERT INTO person (id, name) VALUES (?,?)",(int(p["id"]),(p["name"])))
                print(f"{p['name']} has been entered into the db")
    
        return people

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
