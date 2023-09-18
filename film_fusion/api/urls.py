from django.urls import path, include

from . import views

urlpatterns = [
   path('movies/', include('films.urls')),
   path('users/', include('users.urls'))
]