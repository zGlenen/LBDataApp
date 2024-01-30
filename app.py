import csv
from io import TextIOWrapper, BytesIO
from flask import Flask, render_template, request, jsonify
from flask_paginate import Pagination, get_page_parameter
from UserScraper import UserScraper
from DataHandler import DataHandler


app = Flask(__name__)
output_data = []
filtered_films = []

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():

    try:
        data = request.form.get('username')
    except:
        return render_template('error.html')
    
    if not data:
        return render_template('error.html')

    scraper = UserScraper()
    data_handler = DataHandler()

    data_handler.insert_genre_db()

    
    films = scraper.scrape_user(data)
    letterboxd_urls = scraper.get_uris(films)
    data_handler.scrape_data(letterboxd_urls)
    global output_data 
    output_data = data_handler.films
    global filtered_films
    filtered_films = []
    #films_json = jsonify([serialize_films(film) for film in data_handler.films])
    
    return jsonify(True)

@app.route('/dashboard')
def dashboard():
    global output_data

    if not output_data:
        return render_template('error.html')
    
    return render_template('dashboard.html',films=output_data)

@app.route('/films')
def films():
    global output_data
    global filtered_films

    if not output_data:
        return render_template('error.html')
    
    filter_options = request.args
    filtered_films = get_filtered_films(output_data,filter_options)

    sorting_option = request.args.get('sorting_option', default='year_latest', type=str)
    sorted_films = get_sorted_films(sorting_option)

    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 20  # Number of films per page
    offset = (page - 1) * per_page
    paginated_films = sorted_films[offset: offset + per_page]

    pagination = Pagination(page=page, total=len(sorted_films), per_page=per_page, css_framework='bootstrap')

    return render_template('films.html', films=paginated_films, pagination=pagination)

def get_filtered_films(data, filter_options):
    global filtered_films
    if filter_options:
        filtered_films = []
        filtered_films_2 = []
        filtered_films_3 = []
        filtered_films_4 = []
        hasUserRating = False
        hasAvgRating = False
        hasDec = False
        for i in filter_options:
            if i.startswith("user"):
                filtered_films.extend(get_filtered_rating_films(data, i.split("_")[-1]))
                hasUserRating = True
            elif i.startswith("avg"):
                if hasUserRating and not hasAvgRating:
                    filtered_films_2 = (get_filtered_avg_rating_films((filtered_films), i.split("_")[-1]))
                    if not filtered_films_2:
                            return []
                else:
                    filtered_films_2.extend(get_filtered_avg_rating_films((data if not hasUserRating else filtered_films), i.split("_")[-1]))
                    if not filtered_films_2:
                            return []
                hasAvgRating = True
            elif i.startswith("dec"):
                if filtered_films_2:
                    x = filtered_films_2
                elif filtered_films:
                    x = filtered_films
                else:
                    x = data

                if not hasDec:
                    filtered_films_3 = get_filtered_decade(x,i.split("_")[1])
                    hasDec = True
                    if not filtered_films_3:
                            return []
                else:
                    filtered_films_3.extend(get_filtered_decade(x,i.split("_")[1]))
                    if not filtered_films_3:
                            return []
            elif i.startswith("year"):
                #get the decade and add the year to it
                for j in filter_options:
                    if j.startswith("dec"):
                        year = int(j.split("_")[1]) + int(i.split("_")[-1])

                        filtered_films_4 = get_filtered_year(filtered_films_3,year)
                        if not filtered_films_4:
                            return []
        if filtered_films_4:
            filtered_films_4 = list(set(filtered_films_4))
            return filtered_films_4
        if filtered_films_3:
            filtered_films_3 = list(set(filtered_films_3))
            return filtered_films_3
        elif filtered_films_2:
            filtered_films_2 = list(set(filtered_films_2))
            return filtered_films_2
        else:
            filtered_films = list(set(filtered_films))
            
            return filtered_films
    else:
        return data
    
def get_filtered_year(data,year):
    filtered_films = [film for film in data if year == film.year_released ]
    return filtered_films

def get_filtered_decade(data,decade_option):
    decade_start = int(decade_option)
    if decade_start == 1800:
        decade_end = 1899
    else:
        decade_end = decade_start + 9
    filtered_films = [film for film in data if decade_start <= film.year_released <= decade_end]
    return filtered_films

def get_sorted_films(sorting_option):
    global filtered_films
    global output_data

    f = []

    if filtered_films:
        f = filtered_films

    if sorting_option == 'year_latest':
        sorted_films = sorted(f, key=lambda film: film.year_released, reverse=True)
    elif sorting_option == 'year_earliest':
        sorted_films = sorted(f, key=lambda film: film.year_released)
    elif sorting_option == 'rating_highest':
        sorted_films = sorted(f, key=lambda film: film.details.rating, reverse=True)
    elif sorting_option == 'rating_lowest':
        sorted_films = sorted(f, key=lambda film: film.details.rating)
    elif sorting_option == 'user_rating_highest':
        sorted_films = sort_by_user_rating(f, reverse=True)
    elif sorting_option == 'user_rating_lowest':
        sorted_films = sort_by_user_rating(f)
    elif sorting_option == 'longest':
        sorted_films = sorted(f, key=lambda film: film.details.runtime, reverse=True)
    elif sorting_option == 'shortest':
        sorted_films = sorted(f, key=lambda film: film.details.runtime)
    else:
        # Default sorting option
        sorted_films = f

    return sorted_films

def get_filtered_rating_films(data,rating_option):

    if rating_option == '0':
        filtered_films = [film for film in data if convert_star_rating_to_numeric(film.details.user_rating) == 0]  
    elif rating_option == '1':
        filtered_films = [film for film in data if convert_star_rating_to_numeric(film.details.user_rating) == 1/2]  
    elif rating_option == '2':
        filtered_films = [film for film in data if convert_star_rating_to_numeric(film.details.user_rating) == 2/2]  
    elif rating_option == '3':
        filtered_films = [film for film in data if convert_star_rating_to_numeric(film.details.user_rating) == 3/2]  
    elif rating_option == '4':
        filtered_films = [film for film in data if convert_star_rating_to_numeric(film.details.user_rating) == 4/2]  
    elif rating_option == '5':
        filtered_films = [film for film in data if convert_star_rating_to_numeric(film.details.user_rating) == 5/2]  
    elif rating_option == '6':
        filtered_films = [film for film in data if convert_star_rating_to_numeric(film.details.user_rating) == 6/2]  
    elif rating_option == '7':
        filtered_films = [film for film in data if convert_star_rating_to_numeric(film.details.user_rating) == 7/2]  
    elif rating_option == '8':
        filtered_films = [film for film in data if convert_star_rating_to_numeric(film.details.user_rating) == 8/2]  
    elif rating_option == '9':
        filtered_films = [film for film in data if convert_star_rating_to_numeric(film.details.user_rating) == 9/2]  
    elif rating_option == '10':
        filtered_films = [film for film in data if convert_star_rating_to_numeric(film.details.user_rating) == 10/2]  
    else:
        # Default sorting option
        filtered_films = data

    return filtered_films

def get_filtered_avg_rating_films(data, avg_rating_option):
    if avg_rating_option == 'any':
        return data
    
    avg_rating_option = float(avg_rating_option) / 2  # Convert to float if it's not already
    upper_bound = avg_rating_option + 0.49  # Calculate the upper bound of the range

    if avg_rating_option == 0:
        filtered_films = [film for film in data if 0 <= film.details.rating < 0.5]
    elif 0.5 <= avg_rating_option < 5:
        filtered_films = [film for film in data if avg_rating_option <= film.details.rating < upper_bound]
    elif avg_rating_option == 5:
        filtered_films = [film for film in data if 4.5 <= film.details.rating <= 5]
    else:
        # Default option
        filtered_films = data

    return filtered_films


def convert_star_rating_to_numeric(star_rating):
    # Count the number of stars
    if star_rating:
        num_stars = star_rating.count('★')
        # Count the number of half stars
        num_half_stars = star_rating.count('½')
        # Calculate the total rating
        total_rating = num_stars + 0.5 * num_half_stars
    else:
        total_rating = 0
    return total_rating

def sort_by_user_rating(films, reverse=False):
    return sorted(films, key=lambda film: convert_star_rating_to_numeric(film.details.user_rating), reverse=reverse)


def serialize_films(film):
    return {
        'id' : film.id,
        'title' : film.title,
        'letterboxd_uri' : film.letterboxd_uri,
        'year_released' : film.year_released,
        'runtime' : film.details.runtime,
        'genres' : film.details.genres,
        'production_countries' : film.details.production_countries
    }

if __name__ == '__main__':
    app.run(debug=True)
