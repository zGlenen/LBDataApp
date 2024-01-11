from FilmDataHandler import FilmDataHandler
import csv


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


def main():

    file_name_in = "files/output.csv"
    data = open_file(file_name_in)
    
    filmDataHandler = FilmDataHandler([])
    filmDataHandler.scrape_data(data)
    filmDataHandler.populate_films()

    print("")


if __name__ == "__main__":
    main()          