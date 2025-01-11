from django.shortcuts import render
from.models import AnimeUser,UserProfile
from rest_framework import generics,status
from rest_framework.response import Response
from .serializers import AnimeUserserializer,Userprofileserializer
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from decouple import config
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import authtoken
# Create your views here.
class UserReg(generics.CreateAPIView):# CreateAPIView is used to POST the Data
    serializer_class = AnimeUserserializer # Sets AnimeUserserializer as Serializer class

    def create(self, request):# overriding CreateAPIView
        serializer = AnimeUserserializer(data=request.data) # Uses the AnimeUserserializer as serializer class

        serializer.is_valid(raise_exception=True)
        serializer.save() 
        return Response (serializer.data,status=status.HTTP_201_CREATED)


class pagestyle(PageNumberPagination):
    page_size = config("page_size")
    page_query_param = config("page_param")       



class UserData(ListAPIView): # ListAPIView is used to GET the Data 
    queryset = AnimeUser.objects.all() # Fetches all the fields from the AnimeUser Model
    serializer_class = AnimeUserserializer # Uses AnimeUserserializer for Serialization
    pagination_class = pagestyle # Sets pagination for seperate views


class Update(RetrieveUpdateDestroyAPIView):
    queryset = AnimeUser.objects.all()
    serializer_class = AnimeUserserializer


class Profile(generics.CreateAPIView):
    serializer_class = Userprofileserializer
    queryset = UserProfile.objects.all()


class ViewProfile(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = Userprofileserializer