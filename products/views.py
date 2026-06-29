from django.shortcuts import render
from .models import Category, FastFoodProduct

def menu_home(request):
    categories = Category.objects.all()
    products = FastFoodProduct.objects.filter(is_active=True)
    
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'menu_home.html', context)