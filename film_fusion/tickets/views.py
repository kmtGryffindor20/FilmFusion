from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, response, status

from .models import Ticket

from films.models import Movie

from .serializers import TicketSerializer


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
        
