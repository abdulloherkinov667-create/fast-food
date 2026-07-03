from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer


def profile_page(request):
    latest_user = User.objects.order_by("-id").first()
    return render(request, "user_page/profil_page.html", {"user": latest_user})


def savat_page(request):
    return render(request, "user_page/savat.html")

def register_page(request):
    return render(request, "user_page/registr.html")


class RegisterAPIView(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "Ro'yxatdan  muvoffiqiyatli o'tdingiz!")
            return Response(
                {
                    "success": True,
                    "message": "Ro'yxatdan  muvoffiqiyatli o'tdingiz!",
                    "redirect_url": reverse("menu_home"),
                },
                status=status.HTTP_201_CREATED,
            )

        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)