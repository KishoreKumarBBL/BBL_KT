from django.urls import path
from .views import UserReg,UserData,Update,Profile,ViewProfile

urlpatterns=[
    path('',UserReg.as_view()),
    path('api/',UserData.as_view()),
    path('api/update/<int:pk>',Update.as_view()),
    path('profile/',Profile.as_view()),
    path('profile/view/',ViewProfile.as_view()),

]