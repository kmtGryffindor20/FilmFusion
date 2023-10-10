import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "film_fusion.settings")
import json
import django
django.setup()

# your imports, e.g. Django models
from films import models

import requests
import time
import pandas as pd

for i in range(0,8):
    df = pd.read_html(f"https://en.wikipedia.org/wiki/List_of_Hindi_films_of_200{i}")

    movies = ""
    for j in range(len(df)):
        if df[j].columns[0] == 'Title':
            movies = df[j]
            break

    api_url = "http://localhost:8000/api/movies/cast_add/"

    movies = movies.dropna(axis=0, subset=['Title'])
    directors = movies['Director']
    directors = directors.unique()
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5MzNmMGFjMDZjNWVkNTVhNjdlMGI3YzUwZjA1NmRlOSIsInN1YiI6IjY0Zjk2MDViYTg0YTQ3MDBhZDM3NjNiMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.0jbl7ODxAdDVjksUz3ownYAAkm9SU_rmqayh0iyHszU"
    }


    movies_db = models.Movie.objects.all()

    session = requests.Session()

    for movie in movies_db[1596:]:
        try:
            cast = movies[(movies['Title'] == movie.title)]['Cast'].values[0]
            if pd.isna(cast):
                cast = None
        except:
            continue

        data = {
                'movie':movie.pk,
                'cast':cast
            }

        response = session.post(url=api_url, json=data)
        print(response.json())
        
        


# for i in range(0, 9):
#     df = pd.read_html(f"https://en.wikipedia.org/wiki/List_of_Hindi_films_of_200{i}")
#     movies_df = ""
#     for j in range(len(df)):
#         if df[j].columns[0] == 'Title':
#             movies_df = df[j]
#             break
#     movies_df = movies_df.dropna(axis=0, subset=['Title'])
#     directors = movies_df['Director']
#     directors = directors.unique()
#     headers = {
#         "accept": "application/json",
#         "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5MzNmMGFjMDZjNWVkNTVhNjdlMGI3YzUwZjA1NmRlOSIsInN1YiI6IjY0Zjk2MDViYTg0YTQ3MDBhZDM3NjNiMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.0jbl7ODxAdDVjksUz3ownYAAkm9SU_rmqayh0iyHszU"
#     }

#     url = "https://api.themoviedb.org/3/search/movie"

#     api_url = "http://localhost:8000/api/movies/"

#     session1 = requests.session()
#     for director in directors:
#         if not pd.isna(director):
#             params = {
#                 'director_name':director
#             }
#             response = session1.post("http://localhost:8000/api/movies/directors/", json=params)
#             print(response.text)

#     session2 = requests.session()
#     for movie in movies_df.values[0:1]:
#         params = {
#             'query': movie[0]
#         }
#         response = session2.get(url, params=params, headers=headers)
#         data = response.json()
#         if data['total_results'] != 0:
#             try:
#                 id = data['results'][0]['id']
#             except:
#                 id = None
#             try:
#                 date = data['results'][0]['release_date']
#             except:
#                 date = None
#             try:
#                 director_name = models.Director.objects.filter(director_name=movie[3]).first().director_name
#             except AttributeError:
#                 director_name = None
#             try:
#                 description = data['results'][0]['overview']
#             except:
#                 description = None
#             tmdb_rating = round(data['results'][0]['vote_average'], 2)
#             if(pd.isna(movie[3])):
#                 genre = None
#             else:
#                 genre = movie[3]

#             data = {
#                 'genre':genre,
#                 'title': movie[0],
#                 'release_date':date,
#                 'movie_api_id':id,
#                 'director_name': director_name,
#                 'description':description,
#                 'tmdb_rating':tmdb_rating
#             }
            
#             response = session1.post(api_url, json=data)
#             try:
#                 print(response.json()['id'])
#             except:
#                 print(response.json())