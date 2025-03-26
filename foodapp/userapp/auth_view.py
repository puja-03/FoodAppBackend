from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .auth_serializer import *
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.utils.timezone import now
from datetime import timedelta
from .utils import *

class RegisterUser(APIView):
    permission_classes = [AllowAny] 
    def post(self, request, role=None):
        valid_roles = {choice[0] for choice in CustomUser.ROLE_CHOICES}
        if role not in valid_roles:
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data.copy()
        data['role'] = role
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                if not user.is_verified:
                    otp = send_otp_email(user.email)
                    return Response({"message": "Check your email to verify your account.", "user": serializer.data}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_verified:
            return Response({'message': 'Please verify your account before logging in.'},
                            status=status.HTTP_403_FORBIDDEN)
        if not user.check_password(password):
            return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
        refresh_token = RefreshToken.for_user(user)
        return Response({
            "message": "Login successful",
            "access_token": str(refresh_token.access_token),
            "refresh_token": str(refresh_token),
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "role": user.role,
            }
        })

class VerifyEmail(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        email = serializer.data['email']
        otp = serializer.data['otp']
        user = CustomUser.objects.filter(email=email).first()
        if user.is_verified:
            return Response({"error": "Email already verified"}, status=status.HTTP_400_BAD_REQUEST)
        if not user or user.otp != otp:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        if now() > user.otp_created_at + timedelta(minutes=10):
            return Response({"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
        refresh_token = RefreshToken.for_user(user)

        user.is_verified = True
        user.save()
        return Response({
            "message": "Email verified successfully",
            "access_token": str(refresh_token.access_token),
            "refresh_token": str(refresh_token),
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "role": user.role,
            }
            })
    

class LogoutUser(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)