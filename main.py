from FilmDataHandler import FilmDataHandler
import csv
from datetime import datetime

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

def validate_year(year):
    if year and year.isdigit():
        if int(year) > 1888 and datetime(int(year),1,1) < datetime.now():
            return True
        else:
            return False
        


def main():

    file_name_in = "files/watched.csv"
    file_name_out = "files/output.csv"
    data = open_file(file_name_in)
    
    filmDataHandler = FilmDataHandler([])
    filmDataHandler.populate_films(data)

    # year = 1920
    # year2 = 1929
    # filmDataHandler.check_year_released(year,year2)#will have to add specfic logic for individual years, and whole decades down the road

    # date = datetime(2023, 9, 11)
    # date2 = datetime(2023, 10, 11)
    # filmDataHandler.check_date_added(date,date2)

    print("Welcome to Zack & Luke's dumbass data dump!")
    print("I've already got your file! How would you like to order it?")

    answer = 0
    while (answer != '1' and answer != '2'):
        answer = input("Press 1 for year or 2 for date:")

        if answer == '1':
            ##validate for years
            valid = False
            while (not valid):
                year = input("Epic sauce! Please enter a year: ")
                if validate_year(year):
                    year2 = input("Awesome! Enter a second year for range:")
                    if year2 == 'b':
                        year2 = year
                    if validate_year(year2):
                        filmDataHandler.check_year_released(year,year2)
                        valid = True
        elif answer == '2': 
            ##validate for dates
            date = input("Epic sauce! Please enter a date: ")
            date2 = input("Awesome! Enter a second date for range or q to end:")
            if date2 == 'q':
                date2 = date
            filmDataHandler.check_date_added(date,date2)
        else: 
            print("Oops try again!")
        

    print("It's all done! Have an epic day!")
    write_file(filmDataHandler.output_films,file_name_out)

if __name__ == "__main__":
    main()          
