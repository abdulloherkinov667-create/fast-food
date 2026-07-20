from django.conf import settings
from django.contrib import messages
from django.db.models import Sum
from products.models import Order, OrderItem
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import Category, FastFoodProduct, ShopingModel


def menu_home(request):
    categories = Category.objects.all()
    products = FastFoodProduct.objects.filter(is_active=True)

    for product in products:
        product.image_url = product.product_image.url if product.product_image else ""
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


# Savatdagi bitta qatorni butunlay o'chirish uchun (savat.html dagi chelak tugmasi)
@login_required(login_url='login_page')
def delete_product_cart(request, pk):
    product_id = pk
    user_id = request.user.id
    db_cart = ShopingModel.objects.filter(id=product_id, user_id=user_id)

    if db_cart.exists():
        db_cart.delete()
        return redirect('savat_page')
    return redirect('savat_page')


@login_required(login_url='login_page')
def update_cart_quantity(request, pk, action):
    cart_item = get_object_or_404(ShopingModel, id=pk, user=request.user)

    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save(update_fields=['quantity'])
    elif action == 'decrease':
        cart_item.quantity -= 1
        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save(update_fields=['quantity'])

    return redirect('savat_page')


@login_required(login_url='login_page')
def checkout_html(request):
    cart_items = ShopingModel.objects.filter(user=request.user).select_related('product')
    if not cart_items.exists():
        return redirect('savat_page')

    total_price = 0
    for item in cart_items:
        item.line_total = item.product.price * item.quantity
        total_price += item.line_total

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'cash')
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()

        if not phone or not address:
            messages.error(request, "Telefon raqami va manzilni to'ldiring!")
            context = {'cart_items': cart_items, 'total_price': total_price}
            return render(request, 'user_page/checkout.html', context)

        order = Order.objects.create(
            user=request.user,
            phone=phone,
            address=address,
            description=request.POST.get('description', ''),
            payment_method=payment_method,
            card_holder_name=request.POST.get('card_holder_name') if payment_method == 'payme' else None,
            card_number=request.POST.get('card_number') if payment_method == 'payme' else None,
            card_expiry=request.POST.get('card_expiry') if payment_method == 'payme' else None,
            card_cvv=request.POST.get('card_cvv') if payment_method == 'payme' else None,
        )

        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, count=item.quantity)

        cart_items.delete()

        messages.success(request, "✓ Buyurtmangiz muvaffaqiyatli qabul qilindi!")
        return redirect('menu_home')

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'user_page/checkout.html', context)