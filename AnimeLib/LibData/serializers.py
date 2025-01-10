from rest_framework import serializers
from .models import AnimeUser

class AnimeUserserializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=5, max_length=10, write_only=True)
    firstname = serializers.CharField(required=True)
    lastname = serializers.CharField(required=True)

    class Meta:
        model = AnimeUser
        fields = ['username', 'firstname', 'lastname', 'email', 'password']

    # Validation for username
    def validate_username(self, value):
        if AnimeUser.objects.filter(username=value).exists(): #checks if username already exists!
            raise serializers.ValidationError("Username already exists!")
        if not value.isalnum():
            raise serializers.ValidationError("Username should contain only alphanumeric characters!")
        return value
    
    # Validation for email
    def validate_email(self, value):
        if AnimeUser.objects.filter(email=value).exists():# checks if the email already exists
            raise serializers.ValidationError("Email already exists!")
        return value

    # Can be used to validate one or more fields.
    def validate(self, data):
        firstname = data.get('firstname', '')#fetches the firstname from validate_data
        if firstname and firstname.isupper(): # checks if firstname exist and is uppercase
            raise serializers.ValidationError({'firstname': 'First name should not be in uppercase.'})
        return data # returns the validate data

    # Creating a new AnimeUser instance
    def create(self, validated_data):
        user = AnimeUser.objects.create(
            username=validated_data['username'],
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user
