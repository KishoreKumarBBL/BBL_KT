from django.shortcuts import render
from.models import AnimeUser
from rest_framework import generics,status
from rest_framework.response import Response
from .serializers import AnimeUserserializer
from rest_framework.generics import ListAPIView
# Create your views here.
class UserRegistration(generics.CreateAPIView):
    serializer_class = AnimeUserserializer

    def create(self, request):
        serializer = AnimeUserserializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response (serializer.data,status=status.HTTP_201_CREATED)

class UserLogin(generics.GenericAPIView):
     def post (self, request):
         user=request.data

class UserData(ListAPIView):
    queryset = AnimeUser.objects.all()
    serializer_class = AnimeUserserializer
    
