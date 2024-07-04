from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes
from .serializers import CustomUserSerializer, LoginSerializer
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from myApp.authentication import UserAuthentication
@api_view(['POST'])
def register(request):
    serializer = CustomUserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    try:
        serializer.save()
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@authentication_classes([UserAuthentication])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(data={"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    user = CustomUser.objects.filter(email=email).first()
    
    if not user or not check_password(password, user.password):
        return Response(data={"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    refresh = RefreshToken.for_user(user)
    return Response({
        "message": "Login successful",
        "token": str(refresh.access_token),
    }, status=status.HTTP_200_OK)  # Use HTTP_200_OK for successful login