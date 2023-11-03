from django.urls import path
from . import views

urlpatterns = [
    path('directors/', views.DirectorListCreateAPIView.as_view()),
    path('directors/delete/<int:pk>/', views.DirectorDeleteAPIView.as_view()),
    path('', views.MovieListCreateAPIView.as_view()),
    path('<int:pk>/', views.MovieDetailAPIView.as_view()),
    path('delete/<int:pk>/', views.MovieDeleteAPIView.as_view()),
    path('search/<str:title>/', views.MovieNameDetailAPIView.as_view()),
    path('update/<int:pk>/', views.MovieUpdateAPIView.as_view()),
    path('cast_add/', views.CastListCreateAPIView.as_view()),
    path('<int:movie_id>/reviews/', views.MovieReviewsListCreateAPIView.as_view()),
    path('topN/', views.MovieTopNReviewedAPIView.as_view()),
    path('trending/', views.TrendingMoviesAPIView.as_view()),
    path('in_theaters/', views.MovieInTheatersAPIView.as_view()),

    

]