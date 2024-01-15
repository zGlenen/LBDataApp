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
    def __init__(self,genres,production_countries,runtime,cast,crew):
        self.genres = genres
        self.production_countries = production_countries
        self.runtime = runtime
        self.cast = cast
        self.crew = crew
