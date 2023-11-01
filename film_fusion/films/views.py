from django.shortcuts import render, HttpResponse

# Create your views here.
from rest_framework import generics, permissions
from films.models import Movie, Director, Review, Cast

from films.serializers import MovieSerializer, DirectorSerializer, ReviewSerializer, CastSerializer
# Create your views here.

from users import authentication

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
        return Movie.objects.all().order_by('-tmdb_rating')[:int(self.request.GET['n'])]

    