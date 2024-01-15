import subprocess
from flask import Flask, render_template, request, jsonify
from UserScraper import WebScrapper
from DataHandler import DataHandler


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.form.get('username')

    scraper = WebScrapper()
    data_handler = DataHandler()
    data_handler.insert_genre_db()

    films = scraper.scrape_user(data)
    letterboxd_urls = scraper.get_uris(films)
    
    data_handler.scrape_data(letterboxd_urls)

    films_json = jsonify([film.__dict__ for film in data_handler.films])

    
    return films_json

if __name__ == '__main__':
    app.run(debug=True)
