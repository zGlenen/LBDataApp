from Film import Film
from datetime import datetime

class FilmDataHandler:
    def __init__(self,films):
        self.films = films
        self.output_films = []

    def populate_films(self,data):
        for line in data:
            if line != "":
                self.films.append(Film(line[0],line[1],line[2],line[3]))

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