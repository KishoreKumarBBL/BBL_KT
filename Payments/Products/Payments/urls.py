from django.urls import path
from . views import Register,Deleteuser


urlpatterns = [
    path('api/Register/', Register.as_view(), name='Registration'),
    path('api/Register/<uuid:id>/',Deleteuser.as_view(), name='DeleteUser')
]