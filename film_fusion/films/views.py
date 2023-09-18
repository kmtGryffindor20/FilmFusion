from django.shortcuts import render, HttpResponse

# Create your views here.
from rest_framework import generics
from films.models import Movie, Director, Review

from films.serializers import MovieSerializer, DirectorSerializer, ReviewSerializer
# Create your views here.


class DirectorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

class MovieListCreateAPIView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieDetailAPIView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieDeleteAPIView(generics.DestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer