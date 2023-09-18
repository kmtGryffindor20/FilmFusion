from django.shortcuts import render, HttpResponse

# Create your views here.
from rest_framework import generics, mixins, permissions, authentication
from users.models import Profile, User
from django.contrib.auth.models import BaseUserManager
from users.serializers import ProfileSerializer, UserSerializer
from rest_framework.permissions import AllowAny

class ProfileListCreateAPIView(generics.ListCreateAPIView, BaseUserManager):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny,]
        