class Film():
    def __init__(self,date_added,title,year_released,letterboxd_uri,id,details):
        self.date_added = date_added
        self.title = title
        self.year_released = year_released
        self.letterboxd_uri = letterboxd_uri
        self.id = id
        self.details = details
        

    def __str__(self):
        return f"ID: {self.id} {self.title} ({self.year_released}) - {self.letterboxd_uri}"

class Genre:
    def __init__(self,id,name):
        self.id = id
        self.name = name

class Person:
    def __init__(self,id,name,job=None,character=None):
        self.id = id
        self.name = name
        self.job = job
        self.character = character


class FilmDetails:
    def __init__(self,genres,production_countries,runtime,cast,crew,image_url,rating,user_rating):
        self.genres = genres
        self.production_countries = production_countries
        self.runtime = runtime
        self.cast = cast
        self.crew = crew
        self.image_url = image_url
        self.rating = rating
        self.user_rating = user_rating
