import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "film_fusion.settings")

import django
django.setup()

# your imports, e.g. Django models
from films import models

import requests
import time
import pandas as pd

df = pd.read_html("https://en.wikipedia.org/wiki/List_of_Hindi_films_of_2011")

jan_mar = df[2]
apr_jun = df[3]
jul_sep = df[4]
oct_dec = df[5]

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

directors = jan_mar['Director']._append([apr_jun['Director'], jul_sep['Director'], oct_dec['Director']])

# for director in directors:
#     params = {
#         'director_name':director
#     }
#     response = requests.post("http://localhost:8000/api/movies/directors/", json=params)

for movie in movies.values:
    params = {
        'query': movie[2]
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    if data['total_results'] != 0:
        id = data['results'][0]['id'] or None
        date = data['results'][0]['release_date'] or None
        director_name = models.Director.objects.filter(director_name=movie[4]).first().director_name
        description = data['results'][0]['overview'] or None
        tmdb_rating = data['results'][0]['vote_average']

        data = {
            'genre':movie[3],
            'title': movie[2],
            'release_date':date,
            'movie_api_id':id,
            'director_name': director_name,
            'description':description,
            'tmdb_rating':tmdb_rating
        }
        
        requests.post(api_url, json=data)
    