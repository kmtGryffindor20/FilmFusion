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
        