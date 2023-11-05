from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
   path('auth/', views.CustomAuthToken.as_view()),
   path('movies/', include('films.urls')),
   path('users/', include('users.urls'))
]