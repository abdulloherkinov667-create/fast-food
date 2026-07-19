from django.conf import settings
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import Category, FastFoodProduct, ShopingModel


def menu_home(request):
    categories = Category.objects.all()
    products = FastFoodProduct.objects.filter(is_active=True)

    for product in products:
        product.image_url = product.product_image.url if product.product_image else ""

    # Foydalanuvchining hozirgi savatidagi mahsulotlar: {"<product_id>": <quantity>}
    # Kalitlar string bo'lishi kerak, chunki JS tomonida JSON.parse qilingandan keyin
    # object kalitlari doim string bo'ladi va biz product.id (int) bilan taqqoslaymiz.
    cart_quantities = {}
    if request.user.is_authenticated:
        cart_quantities = {
            str(product_id): quantity
            for product_id, quantity in ShopingModel.objects.filter(
                user=request.user
            ).values_list('product_id', 'quantity')
        }

    context = {
        'categories': categories,
        'products': products,
        'media_url': settings.MEDIA_URL,
        'cart_quantities': cart_quantities,
    }
    return render(request, 'menu_home.html', context)


@login_required(login_url='login_viuw')
def savat_page(request):
    cart_items = (
        ShopingModel.objects.filter(user=request.user)
        .select_related('product', 'product__category_product')
        .order_by('-id')
    )
    cart_count = cart_items.aggregate(total=Sum('quantity'))['total'] or 0

    context = {
        'cart_items': cart_items,
        'cart_count': cart_count,
    }
    return render(request, 'savat.html', context)


# Savatdagi bitta qatorni butunlay o'chirish uchun (savat.html dagi chelak tugmasi)
@login_required(login_url='login_viuw')
def delete_product_cart(request, pk):
    product_id = pk
    user_id = request.user.id
    db_cart = ShopingModel.objects.filter(id=product_id, user_id=user_id)

    if db_cart.exists():
        db_cart.delete()
        return redirect('savat_page')
    return redirect('savat_page')


def checkout_html(request):
    return render(request, "user_page/checkout.html")