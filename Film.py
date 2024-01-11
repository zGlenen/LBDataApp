class Film():

    def __init__(self,date,name,year,letterboxd_uri,id,details):
        self.date = date
        self.name = name
        self.year = year
        self.letterboxd_uri = letterboxd_uri
        self.id = id
        self.details = details

    def print(self):
        #if name contains comma, surround quotes on it
        return "{},{},{},{}\n".format(self.date,self.name,self.year,self.letterboxd_uri)

    