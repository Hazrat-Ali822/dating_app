from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['date_of_birth', 'gender', 'country', 'interests', 'marital_status', 'wedding_timeline', 'profession']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = get_user_model()  # This will reference your custom User model
        fields = ['username', 'email', 'password', 'profile']

    def create(self, validated_data):
        # Extract profile data from validated data
        profile_data = validated_data.pop('profile')
        
        # Create the User instance
        user = get_user_model().objects.create_user(**validated_data)
        
        # Create UserProfile instance with the created user
        UserProfile.objects.create(user=user, **profile_data)
        
        return user

