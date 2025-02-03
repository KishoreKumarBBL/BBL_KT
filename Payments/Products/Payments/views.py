# from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from.models import Siteusers
from .serializers import Siteuserserializer
from rest_framework import generics

# Create your views here.
class Register(generics.ListCreateAPIView):
    serializer_class = Siteuserserializer
    def get_queryset(self):
        return Siteusers.objects.all()
    
    def post(self, request, *args, **kwargs):
         serializer = self.get_serializer(data=request.data)
         serializer.is_valid(raise_exception=True)
         user = serializer.save(is_active=False)
         return Response({"user": Siteuserserializer(user).data}, status=status.HTTP_201_CREATED)

class Deleteuser(generics.RetrieveUpdateDestroyAPIView):
    queryset = Siteusers.objects.all()
    serializer_class = Siteuserserializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if 'password' in serializer.validated_data:
            instance.set_password(serializer.validated_data.pop('password'))   # Hash password

        serializer.save()  # Save the instance

        return Response(serializer.data, status=status.HTTP_200_OK)
