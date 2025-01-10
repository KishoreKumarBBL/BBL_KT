from django.urls import path
from .views import UserRegistration,UserData

urlpatterns=[
    path('',UserRegistration.as_view()),
    path('test/',UserData.as_view())
]