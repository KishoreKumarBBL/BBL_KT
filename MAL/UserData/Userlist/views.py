from django.http import JsonResponse
from django.shortcuts import render
from.models import AnimeUser,UserProfile
from rest_framework import generics,status
from rest_framework.response import Response
from .serializers import AnimeUserserializer,Userprofileserializer
from rest_framework.generics import ListAPIView
from decouple import config
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from UserData.customPagination import Custompagesettings
from.pagination import pagestyle
from.utils import get_tokens_for_user
from rest_framework.views import APIView
from django.contrib.auth import authenticate
# from rest_framework.permissions import IsAuthenticated
# Create your views here.
class Registration(generics.CreateAPIView):# CreateAPIView is used to POST the Data
    serializer_class = AnimeUserserializer # Sets AnimeUserserializer as Serializer class

    def create(self, request):# overriding CreateAPIView
        serializer = AnimeUserserializer(data=request.data) # Uses the AnimeUserserializer as serializer class

        serializer.is_valid(raise_exception=True)
        serializer.save() 
        return Response (serializer.data,status=status.HTTP_201_CREATED)
    

class UserData(ListAPIView): # ListAPIView is used to GET the Data 
    queryset = AnimeUser.objects.all() # Fetches all the fields from the AnimeUser Model
    serializer_class = AnimeUserserializer # Uses AnimeUserserializer for Serialization
    pagination_class = pagestyle # Sets pagination for seperate views


class Update(RetrieveUpdateDestroyAPIView):
    queryset = AnimeUser.objects.all()
    serializer_class = AnimeUserserializer
    lookup_field = 'id'


class Create_Profile(generics.CreateAPIView):
    serializer_class = Userprofileserializer
    queryset = UserProfile.objects.all()


class ViewProfile(ListAPIView): # This is used if there is only Superuser without any Authentication
    queryset = UserProfile.objects.all()
    serializer_class = Userprofileserializer
    pagination_class = Custompagesettings

    # def get_queryset(self):
    #     return super().get_queryset() This should be used if we need to filter the user details or to fetch the Authenticated user details
    
class updateProfile(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = Userprofileserializer
    lookup_field = 'id'
   
 
    # def update(self, request, *args, **kwargs):
    #     user = self.get_object()
    #     serializer = self.get_serializer(instance=user, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)

    #     return Response(serializer.data, status=status.HTTP_200_OK)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:  # Check for missing username or password
            return JsonResponse({'error': 'Username and password are required'}, status=400)

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is None or not isinstance(user, AnimeUser):  # Ensure the user is an instance of AnimeUser
            return JsonResponse({'error': 'Invalid username or password'}, status=400)

        # Generate tokens
        tokens = get_tokens_for_user(user)
        return JsonResponse(tokens)

    return JsonResponse({'error': 'Invalid request method, use POST.'}, status=405)