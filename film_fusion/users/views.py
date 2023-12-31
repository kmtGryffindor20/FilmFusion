from django.shortcuts import render, HttpResponse

# Create your views here.
from rest_framework import generics, mixins, permissions, authentication, response
from films.models import Review
from users.models import Profile, User
from django.contrib.auth.models import BaseUserManager
from users.serializers import ProfileSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from films.serializers import MovieSerializer, ReviewSerializer

class ProfileListCreateAPIView(generics.ListCreateAPIView, BaseUserManager):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser]


class ProfileDetailAPIView(generics.RetrieveAPIView, BaseUserManager):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny,]

    def perform_create(self, serializer):
        instance = serializer.save()
        user = instance
        Profile.objects.create(user=user).save()
        return instance.save()
        

# View for User Watchlist
class WatchlistListCreateAPIView(generics.ListCreateAPIView):

    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user).first().watchlist.all()

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return response.Response("You must be logged in to view this page", status=401)
        
        movie_id = request.data.get('movie')
        
        if movie_id is None:
            return response.Response("You must provide a movie id", status=400)
        
        Profile.objects.filter(user=request.user).first().watchlist.add(movie_id)
        return self.list(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return response.Response("You must be logged in to view this page", status=401)

        serialized_data = MovieSerializer(self.get_queryset(), many=True).data
        
        return response.Response({"results":serialized_data}, status=200)



class ProfileDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
    
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return response.Response("You must be logged in to view this page", status=401)

        serialized_data = ProfileSerializer(self.get_queryset(), many=True).data
        
        return response.Response({"results":serialized_data}, status=200)
    

class UserReviewsListAPIView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
    
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return response.Response("You must be logged in to view this page", status=401)

        serialized_data = ReviewSerializer(self.get_queryset(), many=True).data
        
        return response.Response({"results":serialized_data}, status=200)
    

class UserWatchlistDeleteAPIView(generics.DestroyAPIView):
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user).first().watchlist.all()
    
    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return response.Response("You must be logged in to view this page", status=401)
        
        movie_id = self.kwargs['movie_id']
        
        if movie_id is None:
            return response.Response("You must provide a movie id", status=400)
        
        profile = Profile.objects.filter(user=request.user).first()
        profile.watchlist.remove(movie_id)
        profile.save()
        return response.Response("Movie removed from watchlist", status=200)
    
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return response.Response("You must be logged in to view this page", status=401)

        serialized_data = MovieSerializer(self.get_queryset(), many=True).data
        
        return response.Response({"results":serialized_data}, status=200)