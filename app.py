import csv
from io import TextIOWrapper, BytesIO
from flask import Flask, render_template, request, jsonify
from UserScraper import UserScraper
from DataHandler import DataHandler


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    data = request.form.get('username')

    scraper = UserScraper()
    data_handler = DataHandler()

    data_handler.insert_genre_db()

    
    films = scraper.scrape_user(data)
    letterboxd_urls = scraper.get_uris(films)
    data_handler.scrape_data(letterboxd_urls)

    films_json = jsonify([serialize_films(film) for film in data_handler.films])
    
    return films_json

def serialize_films(film):
    return {
        'title' : film.title
    }

if __name__ == '__main__':
    app.run(debug=True)
