from rest_framework import serializers
from .models import AnimeUser,UserProfile
from django.contrib.auth import authenticate

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
    profile_pic = serializers.FileField(required=False,)
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

class Loginserializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = AnimeUser
        fields =['username','password','token']

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid username or password")
        return data


from uuid import UUID
class RegisterSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = AnimeUser
        fields = ('id', 'username', 'firstname','lastname','email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def get_id(self, obj):
        # Convert UUID to string
        if isinstance(obj.id, UUID):
            return str(obj.id)
        return obj.id

    def create(self, validated_data):
        user = AnimeUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            is_active=False  # User is inactive until email is verified
        )
        return user    
        