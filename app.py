import csv
from io import TextIOWrapper, BytesIO
from flask import Flask, render_template, request, jsonify
from flask_paginate import Pagination, get_page_parameter
from UserScraper import UserScraper
from DataHandler import DataHandler


app = Flask(__name__)
output_data_for_films = []
output_data_for_cast = []
output_data_for_crew = []
output_data_for_dashboard = {}
filtered_films = []
is_filtered = False

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
    global output_data_for_films 
    output_data_for_films = data_handler.films
    global output_data_for_cast
    global output_data_for_crew
    output_data_for_cast = data_handler.get_people_for_search("cast")
    output_data_for_crew = data_handler.get_people_for_search("crew")

    
    return jsonify(True)

@app.route('/dashboard')
def dashboard():
    global output_data_for_films
    global output_data_for_dashboard
    global output_data_for_cast

    if not output_data_for_films:
        return render_template('error.html')
    
    output_data_for_dashboard['totalFilms'] = len(output_data_for_films) 
    output_data_for_dashboard['totalRuntime'] = get_total_runtime(output_data_for_films)
    output_data_for_dashboard['totalGenreCount'] = get_total_genre_count(output_data_for_films)
    output_data_for_dashboard['totalDecadeCount'] = get_total_decade_count(output_data_for_films)
    output_data_for_dashboard['totalAvgRatingCount'] = get_total_avg_rating_count(output_data_for_films)
    output_data_for_dashboard['totalRatingCount'] = get_total_rating_count(output_data_for_films)
    output_data_for_dashboard['totalYearCount'] = get_total_year_count(output_data_for_films)
    output_data_for_dashboard['totalRuntimeCount'] = get_total_runtime_count(output_data_for_films)
    output_data_for_dashboard['totalCountryCount'] = get_total_country_count(output_data_for_films)
    # output_data_for_dashboard['totalActorCount'] = get_total_actor_count(output_data_for_cast) OVER MAX CAP?????????

    return render_template('dashboard.html',data=output_data_for_dashboard)

@app.route('/people_search')
def people_search():
    global output_data_for_people

    if not output_data_for_films:
        return render_template('error.html')
    
    return render_template('people_search.html',people=output_data_for_people)

@app.route('/films')
def films():
    global output_data_for_films
    global filtered_films
    global is_filtered

    if not output_data_for_films:
        return render_template('error.html')
    
    sorting_option = request.args.get('sorting_option', default='year_latest', type=str)
    sorted_films = get_sorted_films(filtered_films if filtered_films else output_data_for_films,sorting_option)
    
    filter_options = request.args
    filtered_films = get_filtered_films(output_data_for_films,filter_options)

    

    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 20  # Number of films per page
    offset = (page - 1) * per_page
    if is_filtered:
        paginated_films = filtered_films[offset: offset + per_page]
    else:
        paginated_films = sorted_films[offset: offset + per_page]


    pagination = Pagination(page=page, total=len(filtered_films if is_filtered else sorted_films), per_page=per_page, css_framework='bootstrap')

    return render_template('films.html', films=paginated_films, pagination=pagination, og_films=output_data_for_films)

def get_total_actor_count(data):
    actor_count = {}

    for person in data:
        if person['name'] in actor_count:
            actor_count[person['name']] += 1
        else:
            actor_count[person['name']] = 1

    sorted_actor_count = dict(sorted(actor_count.items(), key=lambda x: x[1], reverse=True))

    return actor_count

def get_total_country_count(data):
    country_count = {}

    for film in data:
        for c in film.details.production_countries:
            if c in country_count:
                country_count[c] += 1
            else:
                country_count[c] = 1

    return country_count

def get_total_runtime_count(data):
    runtime_count = {}

    for film in data:
        if str(film.details.runtime) in runtime_count:
            runtime_count[str(film.details.runtime)] += 1
        else:
            runtime_count[str(film.details.runtime)] = 1
    
    return runtime_count

def get_total_year_count(data):
    year_count = {}

    for film in data:
        if str(film.year_released) in year_count:
            year_count[str(film.year_released)] += 1
        else:
            year_count[str(film.year_released)] = 1
    
    return year_count

def get_total_avg_rating_count(data):
    rating_count = {}

    for film in data:
        if str(film.details.rating) in rating_count:
            rating_count[str(film.details.rating)] += 1
        else:
            rating_count[str(film.details.rating)] = 1

    return rating_count

def get_total_rating_count(data):
    rating_count = {}

    for film in data:
        if film.details.user_rating in rating_count:
            rating_count[film.details.user_rating] += 1
        else:
            rating_count[film.details.user_rating] = 1

    return rating_count

def get_total_decade_count(data):
    decade_count = {}
    decade = 0
    for film in data:
        if str(film.year_released).startswith('202'):
            decade = 2020
        elif str(film.year_released).startswith('201'):
            decade = 2010
        elif str(film.year_released).startswith('200'):
            decade = 2000
        elif str(film.year_released).startswith('199'):
            decade = 1990
        elif str(film.year_released).startswith('198'):
            decade = 1980
        elif str(film.year_released).startswith('197'):
            decade = 1970
        elif str(film.year_released).startswith('196'):
            decade = 1960
        elif str(film.year_released).startswith('195'):
            decade = 1950
        elif str(film.year_released).startswith('194'):
            decade = 1940
        elif str(film.year_released).startswith('193'):
            decade = 1930
        elif str(film.year_released).startswith('192'):
            decade = 1920
        elif str(film.year_released).startswith('191'):
            decade = 1910
        elif str(film.year_released).startswith('190'):
            decade = 1900
        elif str(film.year_released).startswith('18'):
            decade = 1800

        if str(decade) in decade_count:
            decade_count[str(decade)] += 1
        else:
            decade_count[str(decade)] = 1
    
    return decade_count

def get_total_genre_count(data):
    genre_count = {}
    for film in data:
        for g in film.details.genres:
            if g in genre_count:
                genre_count[g] += 1
            else:
                genre_count[g] = 1
    return genre_count

def get_total_runtime(output_data_for_films):
    total = 0
    for f in output_data_for_films:
        total += f.details.runtime
    return total

def get_filtered_films(data, filter_options):
    global filtered_films
    global is_filtered
    if filter_options:
        filtered_films = []
        filtered_films_2 = []
        filtered_films_3 = []
        filtered_films_4 = []
        filtered_films_5 = []
        filtered_films_6 = []
        filtered_films_7 = []
        hasUserRating = False
        hasAvgRating = False
        hasDec = False
        hasRun = False
        hasGen = False
        for i in filter_options:
            if i.startswith("user"):
                is_filtered = True
                filtered_films.extend(get_filtered_rating_films(data, i.split("_")[-1]))
                hasUserRating = True
            elif i.startswith("avg"):
                is_filtered = True
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
                is_filtered = True
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
                is_filtered = True
                for j in filter_options:
                    if j.startswith("dec"):
                        year = int(j.split("_")[1]) + int(i.split("_")[-1])

                        filtered_films_4 = get_filtered_year(filtered_films_3,year)
                        if not filtered_films_4:
                            return []
            elif i.startswith("run"):
                is_filtered = True
                if filtered_films_4:
                    dataToUse = filtered_films_4
                elif filtered_films_3:
                    dataToUse = filtered_films_3
                elif filtered_films_2:
                    dataToUse = filtered_films_2
                elif filtered_films:
                    dataToUse = filtered_films
                else:
                    dataToUse = data
                
                if not hasRun:
                    filtered_films_5 = get_filtered_runtime(dataToUse,i.split("_")[1])
                    hasRun = True
                    if not filtered_films_5:
                        return []
                else:
                    filtered_films_5.extend(get_filtered_runtime(dataToUse,i.split("_")[1]))
                    if not filtered_films_5:
                        return []
            elif i.startswith("gen"):
                is_filtered = True
                if filtered_films_6:
                    dataToUse = filtered_films_6
                elif filtered_films_5:
                    dataToUse = filtered_films_5
                elif filtered_films_4:
                    dataToUse = filtered_films_4
                elif filtered_films_3:
                    dataToUse = filtered_films_3
                elif filtered_films_2:
                    dataToUse = filtered_films_2
                elif filtered_films:
                    dataToUse = filtered_films
                else:
                    dataToUse = data

                
                filtered_films_6 = get_filtered_genre(dataToUse,i.split("_")[1]) 
                if not filtered_films_6:
                        return []
            elif i.startswith("country"):
                is_filtered = True
                if filtered_films_7:
                    dataToUse = filtered_films_7
                elif filtered_films_6:
                    dataToUse = filtered_films_6
                elif filtered_films_5:
                    dataToUse = filtered_films_5
                elif filtered_films_4:
                    dataToUse = filtered_films_4
                elif filtered_films_3:
                    dataToUse = filtered_films_3
                elif filtered_films_2:
                    dataToUse = filtered_films_2
                elif filtered_films:
                    dataToUse = filtered_films
                else:
                    dataToUse = data

                filtered_films_7 = get_filtered_country(dataToUse,i.split("_")[1])
                if not filtered_films_7:
                        return []

        if filtered_films_7:
            filtered_films_7 = list(set(filtered_films_7))
            return filtered_films_7
        if filtered_films_6:
            filtered_films_6 = list(set(filtered_films_6))
            return filtered_films_6
        if filtered_films_5:
            filtered_films_5 = list(set(filtered_films_5))
            return filtered_films_5
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
    
def get_filtered_country(data,country):
    filtered_films = [film for film in data if country in film.details.production_countries]
    return filtered_films

def get_filtered_genre(data,genre):
    filtered_films = [film for film in data if genre in film.details.genres]
    return filtered_films

def get_filtered_runtime(data,time):
    time = int(time)
    if time == 120:
        toptime = time + 60
    elif time == 180:
        toptime = 10000
    else:
        toptime = time + 30

    filtered_films = [film for film in data if toptime > int(film.details.runtime) >= time ]
    return filtered_films

def get_filtered_year(data,year):
    filtered_films = [film for film in data if year == film.year_released ]
    return filtered_films

def get_filtered_decade(data,decade_option):
    decade_start = int(decade_option)
    if decade_start == 1800:
        decade_end = 1899
    else:
        decade_end = decade_start + 9
    filtered_films = [film for film in data if decade_start <= int(film.year_released) <= decade_end]
    return filtered_films

def get_sorted_films(f,sorting_option):
    if sorting_option == 'year_latest':
        sorted_films = sorted(f, key=lambda film: int(film.year_released), reverse=True)
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
