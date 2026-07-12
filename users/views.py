from django.contrib import messages
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from products.serializers import RegisterSerializer

from products.serializers import LoginSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Users

def profile_page(request):
    # Prefer Django authentication user when available, fallback to session-stored id
    profile_user = None
    if request.user and request.user.is_authenticated:
        profile_user = request.user
    else:
        profile_user_id = request.session.get("profile_user_id")
        if profile_user_id:
            profile_user = Users.objects.filter(id=profile_user_id).first()

    return render(request, "user_page/profil_page.html", {"user": profile_user})


def savat_page(request):
    return render(request, "user_page/savat.html")


def registratsiya_page(request):
    return render(request, "loginlar/registratsiya.html")


def login_page(request):
    return render(request, "loginlar/login.html")


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Muvaffaqiyatli ro'yxatdan o'tdingiz! Login sahifasiga yo'naltiriladi."}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)  # Session orqali tizimga kirish
            return Response(
                {"message": "Tizimga muvaffaqiyatli kirdingiz! Asosiy sahifaga yo'naltiriladi."}, 
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def logout_user(request):
    """Log out the current user and redirect to home."""
    if request.method == "POST":
        logout(request)
        messages.success(request, "Tizimdan chiqdingiz.")
    return redirect("menu_home")