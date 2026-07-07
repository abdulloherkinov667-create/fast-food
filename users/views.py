from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer


def profile_page(request):
    profile_user_id = request.session.get("profile_user_id")
    profile_user = None

    if profile_user_id:
        profile_user = User.objects.filter(id=profile_user_id).first()

    return render(request, "user_page/profil_page.html", {"user": profile_user})


def savat_page(request):
    return render(request, "user_page/savat.html")

def register_page(request):
    return render(request, "user_page/registr.html")


def logout_page(request):
    if request.method == "POST":
        request.session.flush()
        messages.success(request, "Tizimdan chiqdingiz.")
    return redirect("register_user")


class RegisterAPIView(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            request.session["profile_user_id"] = user.id
            request.session.modified = True
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