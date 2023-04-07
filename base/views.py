from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, logout
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from .models import CustomUserModel

# Create your views here.
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def signup(request):
    try:
        request_data = JSONParser().parse(request)
        user = CustomUserModel.objects.create_user(
            email=request_data["email"],
            password=request_data["password"],
            name=request_data["name"],
        )
        user.save()
        token = Token.objects.get(user=user)
        return JsonResponse({"token": str(token)}, status=201)
    except IntegrityError as e:
        return JsonResponse({"error": "Email used already exists"}, status=400)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login_user(request):
    request_data = JSONParser().parse(request)
    user = authenticate(
        request, email=request_data["email"], password=request_data["password"]
    )

    if user is None:
        return JsonResponse(
            {"error": "Unable to login. Incorrect username and/or password."},
            status=400,
        )
    else:
        try:
            token = Token.objects.get(user=user)
        except:
            token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({"token": str(token)}, status=201)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def logout_user(request):
    token = Token.objects.get(user=request.user)
    token.delete()
    logout(request)
    return JsonResponse({"message": "User logged out successfully!"})
