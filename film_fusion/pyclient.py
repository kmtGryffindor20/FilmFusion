import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "film_fusion.settings")

import django
django.setup()

# # your imports, e.g. Django models
from films import models

import requests

movies = models.Movie.objects.all()
url = "https://api.themoviedb.org/3/movie/"

session = requests.session()
session1 = requests.session()
headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5MzNmMGFjMDZjNWVkNTVhNjdlMGI3YzUwZjA1NmRlOSIsInN1YiI6IjY0Zjk2MDViYTg0YTQ3MDBhZDM3NjNiMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.0jbl7ODxAdDVjksUz3ownYAAkm9SU_rmqayh0iyHszU"
    }
# # update movie model with total reviews
# for i in range(len(movies)):
#     movie_id = movies[i].movie_api_id
#     response = session.get(url+f"{movie_id}/credits", headers=headers)
#     data = response.json()
#     if not models.Cast.objects.filter(movie=movies[i]).exists():
#         models.Cast.objects.create(movie=movies[i])
#     try:
#         cast = data['cast']
#         crew = data['crew']
#     except:
#         cast = [{"id":-1, "name":None}]
    
#     for j in range(len(cast)):
#         actor_id = cast[j]['id']
#         actor_name = cast[j]['name']
#         actor = models.Actors.objects.get_or_create(actor_api_id=actor_id, actor_name=actor_name)
#         try:
#             actor.save()
#         except:
#             pass
#         this_cast = models.Cast.objects.get(movie=movies[i])
#         if not this_cast.actors.filter(actor_api_id=actor_id).exists():
#             this_cast.actors.add(actor[0])
   

    
#     for j in range(len(crew)):
#         if crew[j]['job'] == "Director":
#             director_name = crew[j]['name']
#             director = models.Director.objects.get_or_create(director_name=director_name)
#             try:
#                 director.save()
#             except:
#                 pass
#             movies[i].director_name = director[0]
#             movies[i].save()
#             print(director_name)
#             break



# for i in range(len(movies)):
#     movie_id = movies[i].movie_api_id
#     response = session.get(url+f"{movie_id}/videos", headers=headers)
#     data = response.json()
#     try:
#         videos = data['results']
#     except:
#         videos = [{"key":None, "name":None}]
#     for j in range(len(videos)):
#         key = videos[j]['key']
#         try:
#             name = videos[j]['name'][:50]
#         except:
#             name = None
#         video_type = videos[j].get('type', None)
#         if video_type == "Trailer" or video_type == "Teaser":  
#             video = models.Video.objects.get_or_create(key=key, name=name, movie=movies[i])
#         else:
#             continue
#         try:
#             video.save()
#         except:
#             pass
#         print(key, name)

uri = "http://127.0.0.1:8000/api/auth/"
data = {
    "username":"KMT",
    "password":"testing@123"
}
response = session1.post(uri, json=data)
print(response.json())
token = response.json()['token']

headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

# url = "http://127.0.0.1:8000/api/users/watchlist/"
# # response = session1.post(url, headers=headers, json={"movie":2})
# # print(response.json())

# response = session1.get(url, headers=headers)
# print(response.json())


url = "http://127.0.0.1:8000/api/movies/reviews/1/"

# # post a review
# data = {
#     "rating":5,
#     "review_text":"This is a test review"
# }
# response = session.post(url, headers=headers, json=data)
# print(response.json())

# response = session.get(url)
# print(response.json())


# book ticket
url = "http://127.0.0.1:8000/api/tickets/create/"
data = {
    "movie":2,
    "show":1,
    "seat":'Z1',
    "price":100
}
response = session.post(url, headers=headers, json=data)
print(response.json())