from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from .serializers import (
    ContactSerializer,
    CustomUserSerializer,
    LoginSerializer,
    NoticeSerializer,
    NoteSerializer,
    AssignmentSerializer,
    AssignmentSubmissionSerializer
)
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models import CustomUser, Notice,Assignment,AssignmentSubmission
from rest_framework_simplejwt.tokens import RefreshToken
from myApp.authentication import UserAuthentication


@api_view(["POST"])
def register(request):
    serializer = CustomUserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    try:
        serializer.save()
    except Exception as e:
        return Response(
            {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
# @authentication_classes([UserAuthentication])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            data={"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )

    email = serializer.validated_data["email"]
    password = serializer.validated_data["password"]
    user = CustomUser.objects.filter(email=email).first()

    if not user or not check_password(password, user.password):
        return Response(
            data={"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )

    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "user": user.username,
            "role": user.role,
            "message": "Login successful",
            "token": str(refresh.access_token),
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def contact(request):
    serializer = ContactSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {"message": "Invalid format"}, status=status.HTTP_400_BAD_REQUEST
        )
    try:
        serializer.save()
    except Exception as e:
        return Response(
            {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return Response({"Message": "Data Saved"}, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT"])
@authentication_classes([UserAuthentication])
def user_profile_view(request):
    try:
        user = request.user
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST", "GET"])
@authentication_classes([UserAuthentication])
def notice_view(request):
    if request.method == "POST":
        serializer = NoticeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response({"message": "Notice saved"}, status=status.HTTP_201_CREATED)
    elif request.method == "GET":
        notices = Notice.objects.all()
        serializer = NoticeSerializer(notices, many=True)
        return Response(serializer.data)

@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([UserAuthentication])
def notice_update(request, id):
    try:
        notice_instance = Notice.objects.get(id=id)
    except Notice.DoesNotExist:
        return Response(
            {"message": "Notice not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = NoticeSerializer(notice_instance)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = NoticeSerializer(notice_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        notice_instance.delete()
        return Response({"message": "Notice deleted"}, status=status.HTTP_204_NO_CONTENT)
    

@api_view(['POST','GET'])
@authentication_classes([UserAuthentication])
def assignment_creation(request):
    if request.method == "GET":
        assignments = Assignment.objects.all()
        serializer = AssignmentSerializer(assignments, many=True)
        return Response({"Message": serializer.data}, status=status.HTTP_200_OK)
    elif request.method == "POST":
        request.data['teacher'] = request.user.id 
        serializer = AssignmentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"Message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"Message": "Uploaded"}, status=status.HTTP_201_CREATED)