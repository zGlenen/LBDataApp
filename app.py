import csv
from io import TextIOWrapper, BytesIO
from flask import Flask, render_template, request, jsonify
from flask_paginate import Pagination, get_page_parameter
from UserScraper import UserScraper
from DataHandler import DataHandler


app = Flask(__name__)
output_data = []

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

    if not output_data:
        return render_template('error.html')
    
    sorting_option = request.args.get('sorting_option', default='year_latest', type=str)
    sorted_films = get_sorted_films(output_data,sorting_option)

    filter_option_rating = request.args.get('rating_option', default='any', type=str)
    filtered_films = get_filtered_rating_films(sorted_films,filter_option_rating)

    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 20  # Number of films per page
    offset = (page - 1) * per_page
    paginated_films = filtered_films[offset: offset + per_page]

    pagination = Pagination(page=page, total=len(filtered_films), per_page=per_page, css_framework='bootstrap')

    return render_template('films.html', films=paginated_films, pagination=pagination)

def get_sorted_films(data,sorting_option):
    
    if sorting_option == 'year_latest':
        sorted_films = sorted(data, key=lambda film: film.year_released, reverse=True)
    elif sorting_option == 'year_earliest':
        sorted_films = sorted(data, key=lambda film: film.year_released)
    elif sorting_option == 'rating_highest':
        sorted_films = sorted(data, key=lambda film: film.details.rating, reverse=True)
    elif sorting_option == 'rating_lowest':
        sorted_films = sorted(data, key=lambda film: film.details.rating)
    elif sorting_option == 'user_rating_highest':
        sorted_films = sort_by_user_rating(data, reverse=True)
    elif sorting_option == 'user_rating_lowest':
        sorted_films = sort_by_user_rating(data)
    elif sorting_option == 'longest':
        sorted_films = sorted(data, key=lambda film: film.details.runtime, reverse=True)
    elif sorting_option == 'shortest':
        sorted_films = sorted(data, key=lambda film: film.details.runtime)
    else:
        # Default sorting option
        sorted_films = data

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
