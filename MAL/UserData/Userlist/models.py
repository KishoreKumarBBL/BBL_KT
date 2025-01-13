import uuid
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
        user.set_password(password) # Hashing password
        user.save()
        return user
    

class AnimeUser(AbstractBaseUser): # User class
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255,unique=True)
    email = models.EmailField(max_length=255,unique=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['firstname','lastname','username']

objects = UserData()    

def __str__(self):
    return self.email



class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    profileimg = models.ImageField(upload_to='user/pic', blank=True,null=True)
    bio = models.TextField(max_length=255,blank=True)
    user = models.OneToOneField(AnimeUser,on_delete=models.CASCADE)
    location = models.TextField(max_length=255)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)



