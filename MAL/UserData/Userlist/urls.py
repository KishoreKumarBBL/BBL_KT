from django.urls import path, re_path
from .views import Registration,UserData,Update,Create_Profile,ViewProfile,updateProfile


urlpatterns=[
    path('Register/',Registration.as_view(),name='CreateUser'),
    path('Register/view/',UserData.as_view(), name='userData'),
    path('Register/update/<uuid:id>/',Update.as_view(), name='Update'),
    path('api/profile/',Create_Profile.as_view(), name='Profile'),
    path('api/profile/view/',ViewProfile.as_view(), name= 'ProfileView'),
    path('api/profile/update/<uuid:id>/',updateProfile.as_view(), name='ProfileUpdate')
    
   

]