class Film():

    def __init__(self,date,name,year,letterboxd_uri,id,details):
        self.date = date
        self.name = name
        self.year = year
        self.letterboxd_uri = letterboxd_uri
        self.id = id
        self.details = details

    def __str__(self):
        return f"ID: {self.id} {self.name} ({self.year}) - {self.letterboxd_uri}\n"