from django.shortcuts import render, HttpResponse

# Create your views here.
from rest_framework import generics, permissions, response, status
from films.models import Movie, Director, Review, Cast, Video

from films.serializers import MovieSerializer, DirectorSerializer, ReviewSerializer, CastSerializer, ActorSerializer, VideoSerializer
# Create your views here.

from users import authentication

import requests

TMDB_GENRE_LIST = {
    28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentary",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    36: "History",
    27: "Horror",
    10402: "Music",
    9648: "Mystery",
    10749: "Romance",
    878: "Science Fiction",
    10770: "TV Movie",
    53: "Thriller",
    10753: "War",
    37: "Western"
}

class DirectorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DirectorDeleteAPIView(generics.DestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class MovieListCreateAPIView(generics.ListCreateAPIView):
    queryset = Movie.objects.raw("SELECT * FROM films_movie")
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MovieDetailAPIView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



class MovieNameDetailAPIView(generics.ListAPIView):

    lookup_field = 'title'
    def get_queryset(self):
        return Movie.objects.raw(f"SELECT * FROM films_movie WHERE title LIKE '%%{self.kwargs[self.lookup_field]}%%'")
    
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



class MovieDeleteAPIView(generics.DestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer



class MovieUpdateAPIView(generics.UpdateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class CastListCreateAPIView(generics.ListCreateAPIView):
    queryset = Cast.objects.all()
    serializer_class = CastSerializer


class MovieReviewsListCreateAPIView(generics.ListCreateAPIView):
    lookup_field = 'movie_id'

    def get_queryset(self, *args, **kwargs):
        return Review.objects.filter(movie=self.kwargs[self.lookup_field])
    serializer_class = ReviewSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MovieTopNReviewedAPIView(generics.ListAPIView):
    
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Movie.objects.all().order_by('-popularity')[:int(self.request.GET['n'])]
    

class TrendingMoviesAPIView(generics.ListAPIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 
    serializer_class = MovieSerializer

    def get_queryset(self):

        url = "https://api.themoviedb.org/3/trending/movie/day"
        # get trending movies and save them in movies and replace trending movies with them
        api_response = requests.get(url, headers={
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5MzNmMGFjMDZjNWVkNTVhNjdlMGI3YzUwZjA1NmRlOSIsInN1YiI6IjY0Zjk2MDViYTg0YTQ3MDBhZDM3NjNiMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.0jbl7ODxAdDVjksUz3ownYAAkm9SU_rmqayh0iyHszU'
        })
        data = api_response.json()['results']

        Movie.objects.filter(trending=True).update(trending=False)

        for movie in data:
            m_content = {
                'genre':', '.join([TMDB_GENRE_LIST[id] for id in movie['genre_ids']]),
                'title': movie['title'],
                'release_date':movie['release_date'],
                'movie_api_id':movie['id'],
                'director_name': None,
                'description':movie["overview"],
                'tmdb_rating':round(float(movie['vote_average']), 2),
                'trending':True
                }
            print(m_content)
            if not Movie.objects.filter(movie_api_id=movie['id']).exists():
                Movie(**m_content).save()
            else:
                Movie.objects.filter(movie_api_id=movie['id']).update(trending=True)
        
        return Movie.objects.filter(trending=True)[:10]
                
        

class MovieInTheatersAPIView(generics.ListAPIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = MovieSerializer

    def get_queryset(self):
        url = "https://api.themoviedb.org/3/movie/now_playing"
        api_response = requests.get(url, headers={
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5MzNmMGFjMDZjNWVkNTVhNjdlMGI3YzUwZjA1NmRlOSIsInN1YiI6IjY0Zjk2MDViYTg0YTQ3MDBhZDM3NjNiMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.0jbl7ODxAdDVjksUz3ownYAAkm9SU_rmqayh0iyHszU'
        })
        data = api_response.json()['results']

        Movie.objects.filter(in_theatres=True).update(in_theatres=False)

        for movie in data:
            m_content = {
                'genre':', '.join([TMDB_GENRE_LIST.get(id, "") for id in movie['genre_ids']]),
                'title': movie['title'],
                'release_date':movie['release_date'],
                'movie_api_id':movie['id'],
                'director_name': None,
                'description':movie["overview"],
                'tmdb_rating':round(float(movie['vote_average']), 2),
                'in_theatres':True
                }
            print(m_content)
            if not Movie.objects.filter(movie_api_id=movie['id']).exists():
                Movie(**m_content).save()
            else:
                Movie.objects.filter(movie_api_id=movie['id']).update(in_theatres=True)
            
        return Movie.objects.filter(in_theatres=True)[:10]
        

class MovieCastListAPIView(generics.ListAPIView):
    lookup_field = 'movie_id'

    def get_queryset(self, *args, **kwargs):
        cast = Cast.objects.filter(movie=self.kwargs[self.lookup_field]).first()
        print(cast.actors.all())
        return cast.actors.all()
    serializer_class = ActorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MovieVideoListAPIView(generics.ListAPIView):
    lookup_field = 'movie_id'

    def get_queryset(self, *args, **kwargs):
        return Video.objects.filter(movie=self.kwargs[self.lookup_field])
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        