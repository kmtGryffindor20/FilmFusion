from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from films.models import Movie
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='ptofile_pics')
    watchlist = models.ManyToManyField(Movie, blank=True)

    def save(self, **kwargs):
        super().save()
        image = Image.open(self.image.path)
        if image.height > 300 or image.width > 300:
            out_size = (300, 300)
            image.thumbnail(out_size)
            image.save(self.image.path)

    def get_username(self):
        return self.user.username
    def get_email(self):
        return self.user.email
    
