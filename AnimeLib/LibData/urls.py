from django.urls import path
from .views import UserReg,UserData

urlpatterns=[
    path('',UserReg.as_view()),
    path('test/',UserData.as_view())
]