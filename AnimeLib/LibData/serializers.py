from rest_framework import serializers
from.models import AnimeUser

class AnimeUserserializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, unique=True)
    email = serializers.EmailField(required=True, unique=True)
    password = serializers.CharField(required=True)
    firstname = serializers.CharField(required=True)
    lastname = serializers.CharField(required=True)

    class Meta:
        model = AnimeUser
        fields = ['username','firstname','lastname','email','password']

def validate(self,data):
    firstname = data.get('firstname','')
    username = data.get('username','')

    if firstname and firstname.isupper():
        raise serializers.ValidationError('First name should not be in uppercase')
    
    if not username.isalnum():
        raise serializers.ValidationError('Username should contain alphanumeric only!')
    return data 

def create(self,validate_data):
    return AnimeUser.objects.UserData(**validate_data)