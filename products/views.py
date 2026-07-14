import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Category, FastFoodProduct, ShopingModel
from django.contrib import messages

# DRF imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ShoppingCartSerializer


def menu_home(request):
    categories = Category.objects.all()
    products = FastFoodProduct.objects.filter(is_active=True)

    for product in products:
        product.image_url = product.product_image.url if product.product_image else ""

    context = {
        'categories': categories,
        'products': products,
        'media_url': settings.MEDIA_URL,
    }
    return render(request, 'menu_home.html', context)



def shoping_cart_create(request):
    # ESKI FUNCTION - DRF API DAN FOYDALANISH KERAK: /api/v1/cart/add/
    pass
    
    # if request.method == 'POST':
    #     # Check if user is authenticated
    #     if not request.user.is_authenticated:
    #         return JsonResponse({
    #             'success': False,
    #             'error': 'Siz tizimga kirmagansiz! Iltimos, login qilib qayta urinib ko\'ring.',
    #             'redirect': '/login/'
    #         }, status=401)
    #     
    #     data = request.POST
    #     product_id = data.get('uzumproduct')
    #     user_id = request.user.id
    #     print(product_id, user_id)
    #     
    #     try:
    #         new_cart = ShopingModel.objects.create(
    #             product_id=product_id,
    #             user_id=user_id
    #         )
    #         new_cart.save()
    #         
    #         return JsonResponse({
    #             'success': True,
    #             'message': 'Mahsulot savatga qo\'shildi!',
    #             'product_id': product_id
    #         })
    #     except Exception as e:
    #         return JsonResponse({
    #             'success': False,
    #             'error': str(e)
    #         }, status=400)


# savatga qoshish apisi
class ShoppingCartCreateAPIView(APIView):
    def post(self, request):
        """Savatga yangi mahsulot qo'shish"""
        if not request.user.is_authenticated:
            return Response({
                'success': False,
                'error': 'Login qilinmadi',
                'redirect': '/login/'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            product_id = request.data.get('product_id')
            
            if not product_id:
                return Response({
                    'success': False,
                    'error': 'ID kerak'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Mahsulot mavjudligini tekshirish
            try:
                product = FastFoodProduct.objects.get(id=product_id)
            except FastFoodProduct.DoesNotExist:
                return Response({
                    'success': False,
                    'error': 'Mahsulot yo\'q'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Savatga qo'shish
            cart_item = ShopingModel.objects.create(
                product_id=product_id,
                user=request.user
            )
            
            serializer = ShoppingCartSerializer(cart_item)
            return Response({
                'success': True,
                'message': 'Mahsulot savatga qo\'shildi!',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)