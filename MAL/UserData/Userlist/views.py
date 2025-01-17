from django.http import JsonResponse
from django.shortcuts import render
from.models import AnimeUser,UserProfile
from rest_framework import generics,status
from rest_framework.response import Response
from .serializers import AnimeUserserializer,Userprofileserializer,Loginserializer
from rest_framework.generics import ListAPIView
from decouple import config
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from UserData.custom_Pagination import Custompagesettings
from.pagination import pagestyle
from.utils import get_tokens_for_user
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from.permission import Isvalid

# Create your views here.
class Registration(generics.ListCreateAPIView):# CreateAPIView is used to POST the Data
    """
    Allows user to Register 
    """
    permission_classes = [Isvalid]
    serializer_class = AnimeUserserializer # Sets AnimeUserserializer as Serializer class
    pagination_class = Custompagesettings
    def create(self, request):# overriding CreateAPIView
        serializer = AnimeUserserializer(data=request.data) # Uses the AnimeUserserializer as serializer class

        serializer.is_valid(raise_exception=True)
        serializer.save() 
        return Response (serializer.data,status=status.HTTP_201_CREATED)
        
    
    def get_queryset(self):
        return AnimeUser.objects.all()
    

# class UserData(ListAPIView): # ListAPIView is used to GET the Data 
#     queryset = AnimeUser.objects.all() # Fetches all the fields from the AnimeUser Model
#     serializer_class = AnimeUserserializer # Uses AnimeUserserializer for Serialization
#     pagination_class = pagestyle # Sets pagination for seperate views


class Update(RetrieveUpdateDestroyAPIView):
    """
    Allows User to update thier Profile.
    """
    queryset = AnimeUser.objects.all()
    serializer_class = AnimeUserserializer
    lookup_field = 'id'


class Create_Profile(generics.ListCreateAPIView):
    serializer_class = Userprofileserializer
    queryset = UserProfile.objects.all()
    pagination_class = pagestyle


# class ViewProfile(ListAPIView): # This is used if there is only Superuser without any Authentication
#     queryset = UserProfile.objects.all()
#     serializer_class = Userprofileserializer
#     pagination_class = Custompagesettings

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

class user_login(generics.GenericAPIView):
    serializer_class = Loginserializer
    permission_classes = [Isvalid]
    def post(self, request):
        # Get username and password from request
        username = request.data.get('username')
        password = request.data.get('password')

        # Check if username and password are provided
        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate the user
        user = authenticate(username=username, password=password)

        # If authentication fails
        if user is None:
            return Response({'error': 'Invalid username or password.'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        

        # Return success response with the access token
        return Response({
            'message': 'Authenticated successfully.',
            'username': user.username,
            'access_token': access_token,
        }, status=status.HTTP_200_OK)