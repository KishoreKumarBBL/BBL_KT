import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin

class Users (BaseUserManager):
    """ Helps to Register user in this site """
    def create_user (self, 
                     username,
                     first_name,
                     last_name, 
                     email, 
                     password=None,
                     **extra_fields):
        """ This create the user in the site Database """
        if not username:
            raise ValueError('Users must have an username')
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(username = username, email= self.normalize_email(email), first_name = first_name,
                          last_name = last_name)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(
            self, username, email, password, first_name, last_name, **extra_fields
    ):
        """ This creates a superuser in the site Database """
        user = self.create_user(username= username, 
                                email=self.normalize_email(email), 
                                first_name=first_name,
                                last_name=last_name)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        return user

class Siteusers(AbstractBaseUser,PermissionsMixin):
    """ This is the user model for the site """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['first_name','last_name','username']

    objects = Users()    

    def __str__(self):
        return self.email



class products(models.Model):
    """ This is the product model """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prd_img = models.ImageField(upload_to='prdts/Images', null=True)
    prd_name = models.CharField(max_length=100)
    prd_price = models.DecimalField(max_digits=10, decimal_places=2)
    prd_desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

