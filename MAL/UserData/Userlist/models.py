import uuid
from django.db import models
from django.contrib.auth.base_user import BaseUserManager,AbstractBaseUser
# Create your models here.
class UserData(BaseUserManager): # Manager class
    def create_user(self,firstname,lastname,username, email, password=None,**extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        
        user = self.model(username=username,email=self.normalize_email(email),firstname=firstname,lastname=lastname,**extra_fields)
        user.set_password(password) # Hashing password
        user.save()
        return user
    
    def create_superuser(
        self, firstname,lastname, username, email, password=None, **extra_fields
    ):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            firstname=firstname,
            lastname=lastname,
            **extra_fields,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.set_password(password)
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
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['firstname','lastname','username']

    objects = UserData()    

    def __str__(self):
        return self.email
    
    def has_module_perms(self, app_level):
        return True
    
    def has_perm(self, pernm, obj=None):    
        return self.is_admin
     



class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    profile_pic = models.ImageField(upload_to='user/pic', blank=True,null=True)
    bio = models.TextField(max_length=255,blank=True)
    user = models.OneToOneField(AnimeUser,on_delete=models.CASCADE)
    location = models.TextField(max_length=255)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)



