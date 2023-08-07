from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, QueryDict
from django.contrib.auth import authenticate, logout
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.contrib.auth.forms import PasswordResetForm
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from .token_handlers import get_token_on_login
from .models import CustomUser

# Create your views here.
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def signup(request):
    try:
        request_data = JSONParser().parse(request)
        user = CustomUser.objects.create_user(
            email=request_data["email"],
            password=request_data["password"],
            name=request_data["name"],
        )
        user.save()
        token = Token.objects.get(user=user)
        return JsonResponse({"token": str(token)}, status=201)
    except IntegrityError as e:
        return JsonResponse({"error": "Email already exists!"}, status=400)


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
        token = get_token_on_login(user)
        return JsonResponse({"token": str(token), "name": user.name}, status=201)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def logout_user(request):
    token = Token.objects.get(user=request.user)
    token.delete()
    logout(request)
    return JsonResponse({"message": "User logged out successfully!"}, status=200)


token_generator = PasswordResetTokenGenerator()


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def reset_password(request):
    request_data = request.data
    form = PasswordResetForm(data=request_data)

    if form.is_valid():
        try:
            user = CustomUser.objects.get(email=request_data["email"])
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User account email not found!"}, status=406)
        else:
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = token_generator.make_token(user)
            opts = {
                "use_https": request.is_secure(),
                "request": request,
                "from_email": "gachjude@gmail.com",
                "subject_template_name": "accounts/password_reset_subject.txt",
                "email_template_name": "accounts/password_reset_email.html",
                "extra_email_context": {
                    "site_name": "Jotify",
                    "domain": "localhost:3000",
                    "protocol": "http",
                    "uid": uid,
                    "token": token,
                },
            }
            form.save(**opts)
            return JsonResponse(
                {
                    "message": "Check your email for password reset link",
                },
                status=202,
            )
    return JsonResponse({"error": "Invalid form value(s)."}, status=400)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def confirm_password_reset(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = CustomUser.objects.get(pk=int(uid))
    except (CustomUser.DoesNotExist, TypeError, ValueError, OverflowError):
        user = None
    else:
        if token_generator.check_token(user, token) and user is not None:
            request_data = JSONParser().parse(request)
            user.set_password(request_data["new_password"])
            user.save()
            logout(request)
            return JsonResponse(
                {"message": "Your new password has been set."}, status=202
            )
        else:
            return JsonResponse({"message": "Bad Request!"}, status=406)
