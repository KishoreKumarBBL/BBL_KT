from django.urls import path, re_path
from .views import (Registration,
                    Update,Create_Profile, UserResetPasswordAPIView,
                    updateProfile,
                    user_login,
                    UserLogoutView,
                    UserForgotPasswordAPIView,
                    Verify_mail
                    )
app_name = 'userlist'

urlpatterns=[
    path('Register/',Registration.as_view(),name='CreateUser'),
    path('Register/<uuid:id>', Update.as_view()),
    path('Verify/<uidb64>/<token>/',Verify_mail.as_view(),name='EmailVerify'),
    path('api/profile/<uuid:id>/',updateProfile.as_view(), name='ProfileUpdate'),
    path('api/profile/',Create_Profile.as_view()),
    path('api/login/',user_login.as_view(), name='Login'),
    path('forgotpassword/', UserForgotPasswordAPIView.as_view(),name='emailregister'),
    path('resetpassword/<uidb64>/<token>/',UserResetPasswordAPIView.as_view(),name='verify-email')
   

]