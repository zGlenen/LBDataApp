class Film():

    def __init__(self,date,name,year,letterboxd_uri):
        self.date = date
        self.name = name
        self.year = year
        self.letterboxd_uri = letterboxd_uri

    def print(self):
        #if name contains comma, surround quotes on it
        return "{},{},{},{}\n".format(self.date,self.name,self.year,self.letterboxd_uri)

    