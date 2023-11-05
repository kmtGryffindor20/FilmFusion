from rest_framework import serializers
from django.contrib.auth import password_validation
from .models import Profile, User
from films.serializers import MovieSerializer

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'username',
            'email',
            'image'
        ]

    def get_username(self, obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, Profile):
            return None
        return obj.get_username()
    def get_email(self, obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, Profile):
            return None
        return obj.get_email()
   

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]

    def validate_password(self, value):
        password_validation.validate_password(value) 
        return value

    def create(self, validated_data):
        user = super().create(validated_data)
        if password_validation.validate_password(validated_data['password'], user) is None:
            user.set_password(validated_data['password'])
            user.save()
            return user
        
  