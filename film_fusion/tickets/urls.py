from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.UserTicketListAPIView.as_view()),
    path('create/', views.TicketCreateAPIView.as_view()),
    path('<int:pk>/', views.TicketDetailAPIView.as_view()),
    path('available/<int:movie_id>/<int:show>/', views.AvailableSeatsListAPIView.as_view()),
]