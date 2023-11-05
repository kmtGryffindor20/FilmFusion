from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProfileListCreateAPIView.as_view()),
    path('register/', views.UserListCreateAPIView.as_view()),
    path('watchlist/', views.WatchlistListCreateAPIView.as_view()),
    path('profile/', views.ProfileDetailAPIView.as_view()),
    path('reviews/', views.UserReviewsListAPIView.as_view()),
    path('watchlist/delete/<int:movie_id>', views.UserWatchlistDeleteAPIView.as_view())
]