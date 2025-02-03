from rest_framework import serializers
from .models import Siteusers



class Siteuserserializer(serializers.ModelSerializer):
    username = serializers.CharField(required = True,)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=5, max_length=15, write_only=True)
    confirm_password =serializers.CharField(min_length=5, max_length=15, write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = Siteusers
        fields = ('id','username', 'email', 'password','confirm_password', 'first_name', 'last_name','created_at')

    def validate_username(self, value):
        user_name = self.instance.username if self.instance else None
        if Siteusers.objects.filter(username=value).exclude(username=user_name).exists(): #checks if username already exists!
            raise serializers.ValidationError("Username already exists!")
        if not value.isalnum():
            raise serializers.ValidationError("Username should contain only alphanumeric characters!")
        return value
    
    # Validation for email
    def validate_email(self, value):
        user_id = self.instance.id if self.instance else None
        if Siteusers.objects.filter(email=value).exclude(id=user_id).exists():# checks if the email already exists
            raise serializers.ValidationError("Email already exists!")
        return value
       
    def validate(self, value):
        if value['password'] != value['confirm_password']:
         raise serializers.ValidationError({'password': 'Passwords do not match'})
        first_name = value.get('first_name', '')
        if first_name and first_name.isupper(): # checks if firstname exist and is uppercase
             serializers.ValidationError({'firstname': 'First name should not be in uppercase.'})
            
        return value
    
    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        user = Siteusers.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user
    