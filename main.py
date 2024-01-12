from FilmDataHandler import FilmDataHandler
from Util import Util
import csv

def open_file(file_name):
    file = open(file_name,"r",encoding='utf-8')
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
    num_of_stats = 3
    
    utility = Util(num_of_stats)
    filmDataHandler = FilmDataHandler([])
    filmDataHandler.scrape_data(data)

    #Sort by genre
    genre = "Horror"
    if filmDataHandler.get_film_by_genre(genre):
        print(f"Films in list with {genre} genre: ")
        filmDataHandler.print_films()
    else: 
        print(f"There are no films in the list with {genre} genre")

    #Sort genre by most watched
    genre_dict = filmDataHandler.get_genre_stats()
    genre_dict = utility.get_highest_values_in_object(genre_dict)
    print("Genre stats across films in list given:")
    for a,b in genre_dict.items():
         print(f"{a} ({b})")
    
    #FYI films that cannot be added
    if (filmDataHandler.unreadable_films):
        print("Following film(s) are unreadble:")
        for i in filmDataHandler.unreadable_films:
            print(i)



if __name__ == "__main__":
    main()          