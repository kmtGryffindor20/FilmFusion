import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "film_fusion.settings")

import django
django.setup()

# your imports, e.g. Django models
from films import models

import requests
import time
import pandas as pd

for i in range(8, 24):
    if i < 10:
        i = f"0{i}"
    df = pd.read_html(f"https://en.wikipedia.org/wiki/List_of_Hindi_films_of_20{i}")

    jan_mar = ""
    apr_jun = ""
    jul_sep = ""
    oct_dec = ""

    for j in range(len(df)):
        if df[j].columns[0] == 'Opening':
            jan_mar = df[j]
            apr_jun = df[j+1]
            jul_sep = df[j+2]
            oct_dec = df[j+3]
            break

    jan_mar = jan_mar.dropna(axis=0, subset=['Title'])
    apr_jun = apr_jun.dropna(axis=0, subset=['Title'])
    jul_sep = jul_sep.dropna(axis=0, subset=['Title'])
    oct_dec = oct_dec.dropna(axis=0, subset=['Title'])

    directors = jan_mar['Director']._append([apr_jun['Director'], jul_sep['Director'], oct_dec['Director']])
    directors = directors.unique()

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5MzNmMGFjMDZjNWVkNTVhNjdlMGI3YzUwZjA1NmRlOSIsInN1YiI6IjY0Zjk2MDViYTg0YTQ3MDBhZDM3NjNiMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.0jbl7ODxAdDVjksUz3ownYAAkm9SU_rmqayh0iyHszU"
    }

    url = "https://api.themoviedb.org/3/search/movie"

    api_url = "http://localhost:8000/api/movies/"


    movies = jan_mar._append([apr_jun, jul_sep, oct_dec])

    session1 = requests.session()
    # for director in directors:
    #     if not pd.isna(director):
    #         params = {
    #             'director_name':director
    #         }
    #         response = session1.post("http://localhost:8000/api/movies/directors/", json=params)
    #         print(response.text)

    session2 = requests.session()
    for movie in movies.values[0:1]:
        params = {
            'query': movie[2]
        }
        response = session2.get(url, params=params, headers=headers)
        data = response.json()
        if data['total_results'] != 0:
            try:
                id = data['results'][0]['id']
            except:
                id = None
            try:
                date = data['results'][0]['release_date']
            except:
                date = None
            try:
                director_name = models.Director.objects.filter(director_name=movie[3]).first().director_name
            except AttributeError:
                director_name = None
            try:
                description = data['results'][0]['overview']
            except:
                description = None
            tmdb_rating = round(data['results'][0]['vote_average'], 2)
            if(pd.isna(movie[5])):
                genre = None
            else:
                genre = movie[5]

            data = {
                'genre':genre,
                'title': movie[2],
                'release_date':date,
                'movie_api_id':id,
                'director_name': director_name,
                'description':description,
                'tmdb_rating':tmdb_rating
            }
            
            response = session1.post(api_url, json=data)
            try:
                print(response.json()['id'])
            except:
                print(response.json())
        