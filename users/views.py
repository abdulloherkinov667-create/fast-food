from django.contrib import messages
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from products.models import ShopingModel
from products.serializers import RegisterSerializer

from products.serializers import LoginSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Users
from products.models import Order


def profile_page(request):
    profile_user = None
    if request.user and request.user.is_authenticated:
        profile_user = request.user
    else:
        profile_user_id = request.session.get("profile_user_id")
        if profile_user_id:
            profile_user = Users.objects.filter(id=profile_user_id).first()

    last_orders = []
    total_orders_count = 0
    total_items_count = 0

    if profile_user:
        orders_qs = Order.objects.filter(user=profile_user).order_by('-created_at').prefetch_related('items')
        total_orders_count = orders_qs.count()
        total_items_count = sum(o.items.count() for o in orders_qs)
        last_orders = orders_qs[:2]  # faqat oxirgi 2 ta

    context = {
        "user": profile_user,
        "last_orders": last_orders,
        "has_orders": total_orders_count > 0,
        "total_orders_count": total_orders_count,
        "total_items_count": total_items_count,
    }
    return render(request, "user_page/profil_page.html", context)


@login_required(login_url='login_page')
def order_history_page(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at').prefetch_related('items')
    context = {
        "orders": orders,
        "has_orders": orders.exists(),
    }
    return render(request, "user_page/buyurtma_tarixi.html", context)


@login_required(login_url='login_page') 
def savat_page(request):
    cart_items = ShopingModel.objects.filter(user=request.user)
    total_price = 0
    total_count = 0
    for item in cart_items:
        item.line_total = item.product.price * item.quantity
        total_price += item.line_total
        total_count += item.quantity
    context = {'cart_items': cart_items, 'cart_count': total_count, 'total_price': total_price}
    return render(request, 'user_page/savat.html', context) 


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
                {"message": "Ro'yxatdan o'tdingiz!"}, 
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
                {"message": "Tizimga kirdingiz!"}, 
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def logout_user(request):
    """Log out the current user and redirect to home."""
    if request.method == "POST":
        logout(request)
        messages.success(request, "Tizimdan chiqdingiz.")
    return redirect("menu_home")

def buyurtma_tarixi(request):
    return render(request, 'user_page/buyurtma_tarixi.html')