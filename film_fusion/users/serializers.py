from rest_framework import serializers

from .models import Profile, User

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

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user