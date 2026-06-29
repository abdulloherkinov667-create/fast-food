from django.conf import settings
from django.shortcuts import render
from .models import Category, FastFoodProduct


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