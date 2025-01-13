from rest_framework import serializers
from .models import AnimeUser,UserProfile

class AnimeUserserializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=5, max_length=15, write_only=True)
    firstname = serializers.CharField(required=True)
    lastname = serializers.CharField(required=True)

    class Meta:
        model = AnimeUser
        fields = ['id','username', 'firstname', 'lastname', 'email', 'password','created_at']

    # Validation for username
    def validate_username(self, value):
        user_name = self.instance.username if self.instance else None
        if AnimeUser.objects.filter(username=value).exclude(username=user_name).exists(): #checks if username already exists!
            raise serializers.ValidationError("Username already exists!")
        if not value.isalnum():
            raise serializers.ValidationError("Username should contain only alphanumeric characters!")
        return value
    
    # Validation for email
    def validate_email(self, value):
        user_id = self.instance.id if self.instance else None
        if AnimeUser.objects.filter(email=value).exclude(id=user_id).exists():# checks if the email already exists
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

class Userprofileserializer(serializers.ModelSerializer):
    profileimg = serializers.FileField(required=True,)
    location = serializers.CharField(required=False)
    bio = serializers.CharField(required=True)
    class Meta:
        model = UserProfile
        fields = '__all__'
        # exclude = (
        #     "created_at",
        #     "updated_at",
        #     "is_deleted"
        # )

        