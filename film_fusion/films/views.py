from django.shortcuts import render, HttpResponse

# Create your views here.
from rest_framework import generics, permissions, response, status
from films.models import Actors, Movie, Director, Review, Cast, Video, Recommendation

from films.serializers import MovieSerializer, DirectorSerializer, ReviewSerializer, CastSerializer, ActorSerializer, VideoSerializer, RecommendationSerializer
# Create your views here.
from users.models import Profile, User

from users import authentication

import requests

TMDB_GENRE_LIST = {
    28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentary",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    36: "History",
    27: "Horror",
    10402: "Music",
    9648: "Mystery",
    10749: "Romance",
    878: "Science Fiction",
    10770: "TV Movie",
    53: "Thriller",
    10753: "War",
    37: "Western"
}

class DirectorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DirectorDeleteAPIView(generics.DestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class MovieListCreateAPIView(generics.ListCreateAPIView):
    queryset = Movie.objects.raw("SELECT * FROM films_movie")
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MovieDetailAPIView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



class MovieNameDetailAPIView(generics.ListAPIView):

    lookup_field = 'title'
    def get_queryset(self):
        return Movie.objects.raw(f"SELECT * FROM films_movie WHERE title LIKE '%%{self.kwargs[self.lookup_field]}%%'")
    
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



class MovieDeleteAPIView(generics.DestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer



class MovieUpdateAPIView(generics.UpdateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class CastListCreateAPIView(generics.ListCreateAPIView):
    queryset = Cast.objects.all()
    serializer_class = CastSerializer


class MovieReviewsListCreateAPIView(generics.ListCreateAPIView):
    lookup_field = 'movie_id'

    def get_queryset(self, *args, **kwargs):
        return Review.objects.filter(movie=self.kwargs[self.lookup_field])
    serializer_class = ReviewSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MovieTopNReviewedAPIView(generics.ListAPIView):
    
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Movie.objects.all().order_by('-popularity')[:int(self.request.GET['n'])]
    

class TrendingMoviesAPIView(generics.ListAPIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 
    serializer_class = MovieSerializer

    def get_queryset(self):

        url = "https://api.themoviedb.org/3/trending/movie/day"
        # get trending movies and save them in movies and replace trending movies with them
        api_response = requests.get(url, headers={
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5MzNmMGFjMDZjNWVkNTVhNjdlMGI3YzUwZjA1NmRlOSIsInN1YiI6IjY0Zjk2MDViYTg0YTQ3MDBhZDM3NjNiMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.0jbl7ODxAdDVjksUz3ownYAAkm9SU_rmqayh0iyHszU'
        })
        data = api_response.json()['results']

        Movie.objects.filter(trending=True).update(trending=False)

        for movie in data:
            m_content = {
                'genre':', '.join([TMDB_GENRE_LIST[id] for id in movie['genre_ids']]),
                'title': movie['title'],
                'release_date':movie['release_date'],
                'movie_api_id':movie['id'],
                'director_name': None,
                'description':movie["overview"],
                'tmdb_rating':round(float(movie['vote_average']), 2),
                'trending':True
                }
            print(m_content)
            if not Movie.objects.filter(movie_api_id=movie['id']).exists():
                Movie(**m_content).save()
            else:
                Movie.objects.filter(movie_api_id=movie['id']).update(trending=True)
        
        return Movie.objects.filter(trending=True)[:10]
                
        

class MovieInTheatersAPIView(generics.ListAPIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = MovieSerializer

    def get_queryset(self):
        url = "https://api.themoviedb.org/3/movie/now_playing"
        api_response = requests.get(url, headers={
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5MzNmMGFjMDZjNWVkNTVhNjdlMGI3YzUwZjA1NmRlOSIsInN1YiI6IjY0Zjk2MDViYTg0YTQ3MDBhZDM3NjNiMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.0jbl7ODxAdDVjksUz3ownYAAkm9SU_rmqayh0iyHszU'
        })
        data = api_response.json()['results']

        Movie.objects.filter(in_theatres=True).update(in_theatres=False)

        for movie in data:
            m_content = {
                'genre':', '.join([TMDB_GENRE_LIST.get(id, "") for id in movie['genre_ids']]),
                'title': movie['title'],
                'release_date':movie['release_date'],
                'movie_api_id':movie['id'],
                'director_name': None,
                'description':movie["overview"],
                'tmdb_rating':round(float(movie['vote_average']), 2),
                'in_theatres':True
                }
            print(m_content)
            if not Movie.objects.filter(movie_api_id=movie['id']).exists():
                Movie(**m_content).save()
            else:
                Movie.objects.filter(movie_api_id=movie['id']).update(in_theatres=True)
            
        return Movie.objects.filter(in_theatres=True)[:10]
        

class MovieCastListAPIView(generics.ListAPIView):
    lookup_field = 'movie_id'

    def get_queryset(self, *args, **kwargs):
        cast = Cast.objects.filter(movie=self.kwargs[self.lookup_field]).first()
        print(cast.actors.all())
        return cast.actors.all()
    serializer_class = ActorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MovieVideoListAPIView(generics.ListAPIView):
    lookup_field = 'movie_id'

    def get_queryset(self, *args, **kwargs):
        return Video.objects.filter(movie=self.kwargs[self.lookup_field])
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        

# Movie Reviews view
class MovieReviewsListCreateAPIView(generics.ListCreateAPIView):
    lookup_field = 'movie_id'

    def get_queryset(self, *args, **kwargs):
        return Review.objects.filter(movie=self.kwargs[self.lookup_field])
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return response.Response("You must be logged in to view this page", status=401)
        
        movie_id = self.kwargs[self.lookup_field]
        
        if movie_id is None:
            return response.Response("You must provide a movie id", status=400)
        
        Review.objects.get_or_create(user=request.user, movie=Movie.objects.get(id=movie_id), rating=request.data.get('rating'), review_text=request.data.get('review_text'))[0].save()
        return self.list(request, *args, **kwargs)

    serializer_class = ReviewSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



# Recommend Movies similar to user's watchlist
class RecommendMoviesAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = RecommendationSerializer

    url = "https://api.themoviedb.org/3/movie/"

    def get_queryset(self):
        
        # Get Similar Movies and save them in movies and replace similar movies with them
        for movie_id in Profile.objects.filter(user=self.request.user).first().watchlist.all():

            headers = {
                "accept": "application/json",
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5MzNmMGFjMDZjNWVkNTVhNjdlMGI3YzUwZjA1NmRlOSIsInN1YiI6IjY0Zjk2MDViYTg0YTQ3MDBhZDM3NjNiMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.0jbl7ODxAdDVjksUz3ownYAAkm9SU_rmqayh0iyHszU"
            }
            api_response = requests.get(self.url+f"{movie_id.movie_api_id}/similar", headers=headers)
            data = api_response.json()['results']
            session = requests.session()
            

            for movie in data[:2]:
                m_content = {
                    'genre':', '.join([TMDB_GENRE_LIST.get(id, "") for id in movie.get('genre_ids', [])]),
                    'title': movie.get('title', None),
                    'release_date':movie.get('release_date', None),
                    'movie_api_id':movie.get('id', None),
                    'director_name': None,
                    'description':movie.get("overview", None),
                    'tmdb_rating':round(float(movie.get('vote_average',0)), 2),
                    'trending':False
                    }
                if not Movie.objects.filter(movie_api_id=movie['id']).exists():
                    try:
                        Movie(**m_content).save()
                    except:
                        pass
                else:
                    Movie.objects.filter(movie_api_id=movie['id']).update(trending=True)
                
                api_response = session.get(self.url+f"{movie['id']}/credits", headers=headers)
                n_data = api_response.json()    
                try:
                    cast = n_data['cast']
                    crew = n_data['crew']
                except:
                    cast = [{"id":-1, "name":None}]

                try:
                    if not Cast.objects.filter(movie=Movie.objects.get(movie_api_id=movie['id'])).exists():
                        Cast.objects.create(movie=Movie.objects.get(movie_api_id=movie['id']))
                except:
                    pass
                    
                
                for j in range(len(cast)):
                    actor_id = cast[j]['id']
                    actor_name = cast[j]['name']
                    actor = Actors.objects.get_or_create(actor_api_id=actor_id, actor_name=actor_name)
                    try:
                        actor.save()
                    except:
                        pass
                    try:
                        this_cast = Cast.objects.get(movie=Movie.objects.get(movie_api_id=movie['id']))
                    except:
                        continue
                    if not this_cast.actors.filter(actor_api_id=actor_id).exists():
                        this_cast.actors.add(actor[0])
                
                for j in range(len(crew)):
                    if crew[j]['job'] == "Director":
                        director_name = crew[j]['name']
                        director = Director.objects.get_or_create(director_name=director_name)
                        try:
                            director.save()
                        except:
                            pass
                        try:
                            Movie.objects.filter(movie_api_id=movie['id']).update(director_name=director[0])
                        except:
                            pass
                        break
                
                api_response = session.get(self.url+f"{movie['id']}/videos", headers=headers)
                ndata = api_response.json()
                try:
                    videos = ndata['results']
                except:
                    videos = [{"key":None, "name":None}]
                for j in range(len(videos)):
                    key = videos[j]['key']
                    try:
                        name = videos[j]['name'][:50]
                    except:
                        name = None
                    video_type = videos[j].get('type', None)
                    if video_type == "Trailer" or video_type == "Teaser":  
                        try:
                            video = Video.objects.get_or_create(key=key, name=name, movie=Movie.objects.get(movie_api_id=movie['id']))
                        except:
                            continue
                    else:
                        continue
                    try:
                        video.save()
                    except:
                        pass
                
                try:
                    Recommendation.objects.get_or_create(user=self.request.user, movie_id=Movie.objects.get(movie_api_id=movie['id']))[0].save()
                except:
                    pass
            
        return Recommendation.objects.filter(user=self.request.user)[:10]

    def get(self, request, *args, **kwargs):

        recommendations = self.get_queryset()
        serialized_data = {"results":[]}
        for recommendation in recommendations:
            serialized_data["results"].append(MovieSerializer(recommendation.movie_id).data)

        return response.Response(serialized_data, status=200)