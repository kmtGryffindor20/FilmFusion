from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, response, status

from .models import Ticket

from films.models import Movie

from .serializers import TicketSerializer


count = 1
ALL_SEATS = []
for i in range(1, 11):
    for ch in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']:
        ALL_SEATS.append((count, f"{ch}{i}"))
        count += 1

class UserTicketListAPIView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)
    
class TicketDetailAPIView(generics.RetrieveAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Allow only the user who booked the ticket to view it
    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

class TicketCreateAPIView(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        data["user"] = request.user
        print(data)
        movie = Movie.objects.get(id=data["movie"])
        # if movie.in_theatres == False:
        #     return response.Response("This movie is not in theatres", status=status.HTTP_400_BAD_REQUEST)
        data["movie"] = movie
        data["ticket_id"] = f"{movie.title}-{data['show']}-{data['seat']}-{request.user.username}"
        try:
            ticket = Ticket(**data)
            ticket.save()
        
            serialized_data = TicketSerializer(ticket).data
            return response.Response(serialized_data, status=status.HTTP_201_CREATED)
        except:
            return response.Response("You have already booked a ticket for this movie and seat", status=status.HTTP_400_BAD_REQUEST)
        


# view for available seats
class AvailableSeatsListAPIView(generics.ListAPIView):
    lookup_field = 'movie_id'

    serializer_class = TicketSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self, *args, **kwargs):
        movie = Movie.objects.get(id=self.kwargs[self.lookup_field])
        show = self.kwargs['show']
        booked_seats = Ticket.objects.filter(movie=movie, show=show).values_list('seat', flat=True)
        print(booked_seats)
        available_seats = [seat for seat in ALL_SEATS if seat[1] not in booked_seats]
        return available_seats
    
    def list(self, request, *args, **kwargs):
        return response.Response(self.get_queryset(*args, **kwargs), status=status.HTTP_200_OK)