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
    num_of_stats = 5
    
    utility = Util(num_of_stats)
    filmDataHandler = FilmDataHandler([])
    #filmDataHandler.insert_genre_db()
    filmDataHandler.scrape_data(data)

    #Sort by genre
    genre = "Horror"
    if filmDataHandler.get_film_by_genre(genre):
        print(f"\nFilms in list with {genre} genre: ")
        count = filmDataHandler.print_films()
        print(f"You've seen {count} {genre} movies!\n")

    #get year of greatest occurance of that genre
        common_year = filmDataHandler.get_most_common_release_year()
        filmDataHandler.get_film_by_genre(genre,common_year)
        count = filmDataHandler.print_films()
        print(f"You've seen {count} {genre} movies in {common_year}!")

    else: 
        print(f"There are no films in the list with {genre} genre")

    #Get all genre stats
    genre_dict = filmDataHandler.get_genre_stats()
    print("\nGenre stats of every movie you've seen:")
    for a,b in genre_dict.items():
         print(f"{a} ({b})")

    #Get top genre stats
    genre_dict = utility.get_highest_values_in_object(genre_dict)
    print(f"\nTop {num_of_stats} Genre stats across movies you've seen:")
    for a,b in genre_dict.items():
         print(f"{a} ({b})")
    
    #FYI films that cannot be added
    if (filmDataHandler.unreadable_films):
        print("\nFollowing film(s) are unreadble:")
        for i in filmDataHandler.unreadable_films:
            print(i)

if __name__ == "__main__":
    main()          