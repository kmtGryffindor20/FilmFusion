from rest_framework import serializers

from .models import Movie, Director, Review, Cast

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'movie_api_id',
            'release_date',
            'genre',
            'director_name',
            'description',
            'tmdb_rating',
        ]

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = [
            'id',
            'director_name'
        ]

class ReviewSerializer(serializers.ModelSerializer):
    moviename = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'movie',
            'moviename',
            'rating',
            'review_text',
            'review_date'
        ]
    
    def get_moviename(self, obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, Review):
            return None
        return obj.get_moviename()
    

class CastSerializer(serializers.ModelSerializer):
    moviename = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Cast

        fields = [
            'id',
            'movie',
            'moviename',
            'actors'
        ]

    def get_moviename(self, obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, Cast):
            return None
        return obj.get_moviename()
    

