from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from films.models import Movie
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    watchlist = models.ManyToManyField(Movie, blank=True)

    def save(self, **kwargs):
        super().save()
        

    def get_username(self):
        return self.user.username
    def get_email(self):
        return self.user.email
    
