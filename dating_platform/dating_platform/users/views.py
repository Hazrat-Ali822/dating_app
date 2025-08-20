from django.contrib.auth import get_user_model  # Import this at the top
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from .models import UserProfile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt


# Get the User model
User = get_user_model()

# Signup View
@csrf_exempt
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        date_of_birth = request.POST['date_of_birth']
        gender = request.POST['gender']
        country = request.POST['country']
        interests = request.POST.getlist('interests[]')
        marital_status = request.POST['marital_status']
        wedding_timeline = request.POST['wedding_timeline']
        profession = request.POST['profession']

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({"detail": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Create User instance
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Create UserProfile instance and link it to the user
        profile = UserProfile.objects.create(
            user=user,  # Correct assignment of the user instance
            date_of_birth=date_of_birth,
            gender=gender,
            country=country,
            interests=interests,
            marital_status=marital_status,
            wedding_timeline=wedding_timeline,
            profession=profession
        )
        
        return redirect('login')

    return render(request, 'index.html')
@csrf_exempt
# In your views.py
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            # Return token as part of response
            return JsonResponse({"access_token": str(access_token)}, status=200)
        else:
            return JsonResponse({"detail": "Unauthorized"}, status=401)

    return render(request, 'login.html')


# User Discovery Feed
@api_view(['GET'])
def discover(request):
    if request.user.is_authenticated:
        current_user = request.user
        user_profile = current_user.profile
        matching_users = UserProfile.objects.exclude(user=current_user)

        matched_users = []

        for user in matching_users:
            reason = None
            
            # Check for matching interests
            if any(interest in user_profile.interests for interest in user.interests):
                reason = f"You both like {', '.join([interest for interest in user_profile.interests if interest in user.interests])}"
            
            # Check for matching marital status
            if not reason and user.marital_status == user_profile.marital_status:
                reason = f"You both have the same marital status: {user.marital_status}"
            
            # Check for matching profession
            if not reason and user.profession == user_profile.profession:
                reason = f"You both have the same profession: {user.profession}"

            # If a match is found, add the user to matched_users
            if reason:
                matched_users.append({
                    'user': user.user.username,
                    'reason': reason
                })

        # If no matches found, show diverse users of the opposite gender
        if not matched_users:
            diverse_users = []
            for user in matching_users:
                # Check if opposite gender
                if (current_user.profile.gender == 'Male' and user.gender == 'Female') or (current_user.profile.gender == 'Female' and user.gender == 'Male'):
                    diverse_users.append({
                        'user': user.user.username,
                        'reason': "No matching criteria, but here are users of the opposite gender."
                    })

            matched_users = diverse_users

        return Response({'matched_users': matched_users}, status=status.HTTP_200_OK)

    return JsonResponse({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)