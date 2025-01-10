from django.shortcuts import render
from.models import AnimeUser
from rest_framework import generics,status
from rest_framework.response import Response
from .serializers import AnimeUserserializer
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
# Create your views here.
class UserReg(generics.CreateAPIView):# CreateAPIView is used to POST the Data
    serializer_class = AnimeUserserializer # Sets AnimeUserserializer as Serializer class

    def create(self, request):
        serializer = AnimeUserserializer(data=request.data) # Uses the AnimeUserserializer as serializer class

        serializer.is_valid(raise_exception=True)
        serializer.save() 
        return Response (serializer.data,status=status.HTTP_201_CREATED)


class pagestyle(PageNumberPagination):
    page_size = 1         



class UserData(ListAPIView): # ListAPIView is used to GET the Data 
    queryset = AnimeUser.objects.all() # Fetches all the fields from the AnimeUser Model
    serializer_class = AnimeUserserializer # Uses AnimeUserserializer for Serialization
    pagination_class = pagestyle # Sets pagination for seperate views
