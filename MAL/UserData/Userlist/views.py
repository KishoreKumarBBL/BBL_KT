from django.shortcuts import render
from.models import AnimeUser,UserProfile
from rest_framework import generics,status
from rest_framework.response import Response
from .serializers import AnimeUserserializer,Userprofileserializer,Loginserializer,RegisterSerializer
from rest_framework.generics import ListAPIView
from decouple import config
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from UserData.custom_Pagination import Custompagesettings
from.pagination import pagestyle
from.utils import get_tokens_for_user
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from.permission import Isvalid
from django.urls import reverse
from UserData import settings
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden, JsonResponse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from UserData.services.azure_mail_service import send_azure_mail
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.hashers import make_password
import jwt

# Create your views here.
class Registration(generics.ListCreateAPIView):
    """
    Handles both Registration and Email Activation.
    """
    permission_classes = [Isvalid]
    serializer_class = AnimeUserserializer
    pagination_class = Custompagesettings

    def post(self, request, *args, **kwargs):
        """User Registration"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(is_active=False)  # User is initially inactive

        base_url = "http://localhost:8000"
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_url = f"{base_url}/Verify/{uid}/{token}/"

        # Generate Email Content
        html_content = render_to_string(
            "Email_Verification.html", {"activation_url": activation_url}
        )

        subject = "Account Activation"
        from_email = settings.AZURE_SENDER_ADDRESS

        # Send email
        send_azure_mail(subject, html_content, from_email, user.email)

        return Response(
            {
                "message": "Account created successfully. Please check your email to activate your account.",
                "activation_link": activation_url  # For debugging, remove in production
            },
            status=status.HTTP_201_CREATED
        )

   
    
    def get_queryset(self):
        return AnimeUser.objects.all()
    

# class UserData(ListAPIView): # ListAPIView is used to GET the Data 
#     queryset = AnimeUser.objects.all() # Fetches all the fields from the AnimeUser Model
#     serializer_class = AnimeUserserializer # Uses AnimeUserserializer for Serialization
#     pagination_class = pagestyle # Sets pagination for seperate views

class Verify_mail(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        """Handles email verification when user clicks the activation link."""
        try:
            # Decode the user id from uidb64 and get the user
            user_id = urlsafe_base64_decode(uidb64).decode()
            user = AnimeUser.objects.get(pk=user_id)

            # Check if the token is valid
            if not default_token_generator.check_token(user, token):
                return Response(
                    {"error": "Invalid or expired activation token."},
                    status=status.HTTP_400_BAD_REQUEST
                )
                # Activate the user
            user.is_active = True
            user.save()

            # Send an email to the admin notifying that the user was verified
            subject = "User Account Activation"
            user_email = user.username
            html_content = render_to_string(
                "Admin_Notification.html", {"user_email":user_email }
            )

            from_email = settings.AZURE_SENDER_ADDRESS
            to_email = settings.ADMIN_MAIL


            # Send email
            send_azure_mail(subject, html_content, from_email, to_email)

            # Respond back to the user with a success message
            return Response(
                {"message": "Your account has been activated successfully."},
                status=status.HTTP_200_OK
            )
        

        except (AnimeUser.DoesNotExist, ValueError, TypeError):
            return Response(
                {"error": "Invalid activation link."},
                status=status.HTTP_400_BAD_REQUEST
            )


class Update(RetrieveUpdateDestroyAPIView):
    """
    Allows User to update thier Profile.
    """
    queryset = AnimeUser.objects.all()
    serializer_class = AnimeUserserializer
    lookup_field = 'id'


class Create_Profile(generics.ListCreateAPIView):
    serializer_class = Userprofileserializer
    queryset = UserProfile.objects.all()
    pagination_class = pagestyle


# class ViewProfile(ListAPIView): # This is used if there is only Superuser without any Authentication
#     queryset = UserProfile.objects.all()
#     serializer_class = Userprofileserializer
#     pagination_class = Custompagesettings

    # def get_queryset(self):
    #     return super().get_queryset() This should be used if we need to filter the user details or to fetch the Authenticated user details
    
class updateProfile(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = Userprofileserializer
    lookup_field = 'id'
   
 
    # def update(self, request, *args, **kwargs):
    #     user = self.get_object()
    #     serializer = self.get_serializer(instance=user, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)

    #     return Response(serializer.data, status=status.HTTP_200_OK)

class user_login(generics.GenericAPIView):
    serializer_class = Loginserializer
    permission_classes = [Isvalid]
    def post(self, request):
        # Get username and password from request
        username = request.data.get('username')
        password = request.data.get('password')

        # Check if username and password are provided
        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate the user
        user = authenticate(username=username, password=password)

        # If authentication fails
        if user is None:
            return Response({'error': 'Invalid username or password.'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        

        # Return success response with the access token
        return Response({
            'message': 'Authenticated successfully.',
            'username': user.username,
            'access_token': access_token,
        }, status=status.HTTP_200_OK)
    

class UserLogoutView(APIView):
     permission_classes = [AllowAny]  # Allow all users, including unauthenticated ones

     def get(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "You are not logged in."}, status=400)
        # Perform logout logic
        return Response({"message": "Logged out successfully!"})
     


class UserForgotPasswordAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["email"],
            properties={
                "email": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The email send to reset password",
                )
            },
        ),
        responses={
            200: "email send successfully",
            400: "Bad Request: email is required",
            500: "Internal Server Error",
        },
    )
    def post(self, request):
        base_url = "http://localhost:8000"
        email = request.data.get("email")
        try:
            user = AnimeUser.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = f"{base_url}/resetpassword/{uid}/{token}/"
            html_content = render_to_string(
                "forget_password.html", {"reset_url": reset_url}
            )

            subject = "Password Reset"
            from_email = settings.AZURE_SENDER_ADDRESS

            # Send email
            send_azure_mail(subject, html_content, from_email, email)

            return Response(
                {"message": "Password reset email sent",
                 "reset_url": reset_url
                 }, status=status.HTTP_200_OK
            )
        except ObjectDoesNotExist:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )


class UserResetPasswordAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["password", "confirm_password"],
            properties={
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="password"
                ),
                "confirm_password": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="confirm_password",
                ),
            },
        ),
        responses={
            200: "password rest successfully",
            400: "Bad Request: password and confirm_password code are required",
            500: "Internal Server Error",
        },
    )
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = AnimeUser.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                new_password = request.data.get("password")
                confirm_password = request.data.get("confirm_password")

                # Check if passwords match
                if new_password != confirm_password:
                    return Response(
                        {"message": "Passwords do not match"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                user.set_password(new_password)
                user.save()
                return Response(
                    {"message": "Password reset successful"}, status=status.HTTP_200_OK
                )
            return Response(
                {"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED
            )
        except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
            return Response(
                {"message": "Invalid user ID"}, status=status.HTTP_400_BAD_REQUEST
            )