from django.urls import path
from .views import UserReg,UserData,Update,Create_Profile,ViewProfile

urlpatterns=[
    path('',UserReg.as_view(),name='CreateUser'),
    path('api/',UserData.as_view(), name='userData'),
    path('api/update/<uuid:id>/',Update.as_view(), name='Update'),
    path('api/profile/',Create_Profile.as_view(), name='Profile'),
    path('api/profile/view/',ViewProfile.as_view(), name= 'ProfileView'),
    
   

]