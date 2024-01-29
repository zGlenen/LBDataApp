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

    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10  # Number of films per page
    offset = (page - 1) * per_page
    paginated_films = sorted_films[offset: offset + per_page]

    pagination = Pagination(page=page, total=len(sorted_films), per_page=per_page, css_framework='bootstrap')

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
    elif sorting_option == 'longest':
        sorted_films = sorted(data, key=lambda film: film.details.runtime, reverse=True)
    elif sorting_option == 'shortest':
        sorted_films = sorted(data, key=lambda film: film.details.runtime)
    else:
        # Default sorting option
        sorted_films = data

    return sorted_films

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
