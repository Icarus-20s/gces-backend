from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CustomUserSerializer, LoginSerializer
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models import CustomUser

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


@api_view(['post'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(data={"message":"invalid"},status=status.HTTP_400_BAD_REQUEST)
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    user = CustomUser.objects.filter(email=email).first()
    if not user:
        return Response(data={"message":"invalid"},status=status.HTTP_400_BAD_REQUEST)
    if not check_password(password=password, encoded=user.password):
        return Response(data={"message":"not ok"},status=status.HTTP_401_UNAUTHORIZED)
    return Response(data={"message":"ok"},status=status.HTTP_202_ACCEPTED)




