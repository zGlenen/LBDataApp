from FilmDataHandler import FilmDataHandler
import csv
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def open_file(file_name):
    file = open(file_name,"r")
    data = list(csv.reader(file,delimiter=","))
    file.close()
    return data

def write_file(films,file_name):
    file = open(file_name,"w")
    for film in films:
            file.write(film.print()) 
    file.close()

def get_tmdb_film_details(id):
    url = "https://api.themoviedb.org/3/movie/"+id+"?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzYTAwZDZlNGFkNzQyYTY0MTZmNjEwYTE0N2E4ODA2NCIsInN1YiI6IjY1OWVlNWVjOTFiNTMwMDFmZGYxZGMxOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.r1uBAc6yrAsFwJxICmap8RrNk8Cf_w1RIwlrwTu4aPM"
    }

    response = requests.get(url, headers=headers)

    return json.loads(response.text)    

def get_tmdb_film_credits(id):
    url = "https://api.themoviedb.org/3/movie/"+id+"/credits?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzYTAwZDZlNGFkNzQyYTY0MTZmNjEwYTE0N2E4ODA2NCIsInN1YiI6IjY1OWVlNWVjOTFiNTMwMDFmZGYxZGMxOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.r1uBAc6yrAsFwJxICmap8RrNk8Cf_w1RIwlrwTu4aPM"
    }

    response = requests.get(url, headers=headers)

    return json.loads(response.text)    

def parse_json(data):
    for film in data:
        complete_data_details = get_tmdb_film_details(film["ID"])
        complete_data_credits = get_tmdb_film_credits(film["ID"])
        film["genres"] = complete_data_details["genres"] 
        film["production_countries"] = complete_data_details["production_countries"]
        film["runtime"] = complete_data_details["runtime"]
        
        director_info = next(
            (crew for crew in complete_data_credits["crew"] if crew["job"] == "Director"),
            None
        )
        film["director"] = director_info["name"] if director_info else "Unknown Director"

def get_id(data):
    films = []
    count = 0
    for film in data:
         if count > 0:
            page = requests.get(film[3])
            soup = BeautifulSoup(page.content,"html.parser")
            body = soup.find("body", {"class": "film backdropped"})
            if body: 
                tmdb_id = body.get("data-tmdb-id")
                print(film[1] + ": " + tmdb_id)
                films.append({
                  "Title": film[1],
                  "ID": tmdb_id
                })
            else:
                 print(film[1])
         count += 1 
    return films

def main():

    file_name_in = "files/output.csv"
    #file_name_out = "files/output.csv"
    data = open_file(file_name_in)
    
    filmDataHandler = FilmDataHandler([])
    filmDataHandler.populate_films(data)

    films = get_id(data)
    parse_json(films)
    
    print(json.dumps(films, indent=4))
    

    #write_file(filmDataHandler.output_films,file_name_out)

if __name__ == "__main__":
    main()          



# def validate_year(year):
#     if year and year.isdigit():
#         if int(year) > 1888 and datetime(int(year),1,1) < datetime.now():
#             return True
#         else:
#             return False
        
# def validate_date(date):
#     format = "%Y-%m-%d"
#     if date:
#         try:
#             return bool(datetime.strptime(date, format))
#         except ValueError:
#             return False
    

        # # year = 1920
    # # year2 = 1929
    # # filmDataHandler.check_year_released(year,year2)#will have to add specfic logic for individual years, and whole decades down the road

    # # date = datetime(2023, 9, 11)
    # # date2 = datetime(2023, 10, 11)
    # # filmDataHandler.check_date_added(date,date2)

    # print("Welcome to Zack & Luke's dumbass data dump!")
    # print("I've already got your file! How would you like to order it?")

    # answer = 0
    # while (answer != '1' and answer != '2'):
    #     answer = input("Press 1 for year or 2 for date:")

    #     if answer == '1':
    #         ##validate for years
    #         valid = False
    #         while (not valid):
    #             year = input("Epic sauce! Please enter a year: ")
    #             if validate_year(year):
    #                 year2 = input("Awesome! Enter a second year for range:")

    #                 if validate_year(year2):
    #                     filmDataHandler.check_year_released(year,year2)
    #                     valid = True
    #     elif answer == '2': 
    #         ##validate for dates
    #         valid = False
    #         while (not valid):
    #             date = input("Epic sauce! Please enter a date: ")
    #             if validate_date(date):
    #                 date2 = input("Awesome! Enter a second date for range:")
    #                 if validate_date(date2):
    #                     filmDataHandler.check_date_added(date,date2)
    #                     valid = True
    #     else: 
    #         print("Oops try again!")
        

    # print("It's all done! Have an epic day!")