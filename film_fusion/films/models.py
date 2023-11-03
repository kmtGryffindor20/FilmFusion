from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Director(models.Model):
    director_name = models.CharField(max_length=30, unique=True)

class Movie(models.Model):
    title = models.CharField(max_length=120)
    movie_api_id = models.IntegerField(null=True, unique=True)
    release_date = models.DateField(null=True)
    genre = models.CharField(max_length=80, null=True)
    director_name = models.ForeignKey(Director, to_field="director_name", on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True, null=True)
    tmdb_rating = models.DecimalField(decimal_places=2, max_digits=4, default=0)
    


class Cast(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE)
    cast = models.TextField(blank=True, null=True)

    def get_moviename(self):
        return self.movie.title

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.DecimalField(decimal_places=1, max_digits=2)
    review_text = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)

    def get_moviename(self):
        return self.movie.title


class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)


class TrendingMovies(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
