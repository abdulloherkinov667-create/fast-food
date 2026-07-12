import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Category, FastFoodProduct, ShopingModel
from django.contrib import messages


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
    
    if request.method == 'POST':
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'error': 'Siz tizimga kirmagansiz! Iltimos, login qilib qayta urinib ko\'ring.',
                'redirect': '/login/'
            }, status=401)
        
        data = request.POST
        product_id = data.get('uzumproduct')
        user_id = request.user.id
        print(product_id, user_id)
        
        try:
            new_cart = ShopingModel.objects.create(
                product_id=product_id,
                user_id=user_id
            )
            new_cart.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Mahsulot savatga qo\'shildi!',
                'product_id': product_id
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)