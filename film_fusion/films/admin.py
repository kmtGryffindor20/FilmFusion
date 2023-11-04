from django.contrib import admin

# Register your models here.
from .models import Movie, Review, Director, Cast, Actors

admin.site.register([Movie, Review, Director, Cast, Actors])