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