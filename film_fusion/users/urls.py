from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProfileListCreateAPIView.as_view()),
    path('register/', views.UserListCreateAPIView.as_view()),
]