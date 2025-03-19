from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .auth_serializer import *
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny


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
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
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
        if not user.check_password(password):
            return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
        refresh_token = RefreshToken.for_user(user)
        return Response({
            "email": user.email,
            "username": user.username,
            "role": user.role,
            "access_token": str(refresh_token.access_token),
            "refresh_token": str(refresh_token)
        })


        