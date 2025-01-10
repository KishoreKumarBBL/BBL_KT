from django.db import models
from django.contrib.auth.base_user import BaseUserManager,AbstractBaseUser
# Create your models here.
class UserData(BaseUserManager): # Manager class
    def create_user(self,firstname,lastname,username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        
        user = self.model(username=username,email=self.normalize_email(email),firstname=firstname,lastname=lastname)
        user.set_password(password)
        user.save()
        return user

class AnimeUser(AbstractBaseUser): # User class
    username = models.CharField(max_length=255,unique=True)
    email = models.EmailField(max_length=255,unique=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['firstname','lastname','username']

objects = UserData()     