from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.

shows = [
    ("0", "9:00 AM"),
    ("1", "12:00 PM"),
    ("2", "3:00 PM"),
    ("3", "6:00 PM"),
    ("4", "9:00 PM"),
]

seats = []
count = 1
for i in range(1, 51):
    for ch in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']:
        seats.append((f"{ch}{i%10}", f"{ch}{i%10}"))
        count += 1
  



# Model to store tickets booked by users
class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey("films.Movie", on_delete=models.CASCADE)
    show = models.IntegerField(choices=shows)
    seat = models.CharField(max_length=3, choices=seats)
    ticket_id = models.CharField(max_length=100)
    booked_at = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()

    # same seat cannot be booked for same movie and show
    class Meta:
        unique_together = ['movie', 'show', 'seat']

    

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} - {self.ticket_id}"