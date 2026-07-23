from django.contrib import admin
from root import settings
from django.urls import path
from django.conf.urls.static import static 

from products.views import menu_home, checkout_html
from users.views import profile_page, savat_page, registratsiya_page, login_page, logout_user, RegisterView, LoginView, order_history_page, buyurtma_tarixi
from products.views import delete_product_cart, update_cart_quantity  

from products.profduct_api import ShoppingCartCreateAPIView, OrderCreateApiViuw


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', menu_home, name='menu_home'),
    path("profil/", profile_page, name='profile_user'),
    path("savat_page/", savat_page, name='savat_page'),
    path('registratsiya/', registratsiya_page, name='registratsiya_page'),
    path('login/', login_page, name='login_page'),
    path('logout/', logout_user, name='logout_user'),
    path('checkout_html/', checkout_html, name='checkout_html'),
    path('cart/update/<int:pk>/<str:action>/', update_cart_quantity, name='update_cart_quantity'),
    path('cart/update/<int:pk>/<str:action>/', update_cart_quantity, name='update_cart_quantity'),
    path("profil/buyurtmalar/", order_history_page, name='order_history_page'),
    path("buyurtma_tarixi/", buyurtma_tarixi, name='buyurtma_tarixi'),

    
    
    # api auth    
    path('api/v1/auth/register/', RegisterView.as_view(), name='api_register'),
    path('api/v1/auth/login/', LoginView.as_view(), name='api_login'),
    path('cart/delete/<int:pk>/', delete_product_cart, name='delete_product_cart'),
    
    #api rasmiylashtirish
    path('api/v1/cart/add/', ShoppingCartCreateAPIView.as_view(), name='api_cart_add'),
    path('api/v1/order/create/', OrderCreateApiViuw.as_view(), name='api_order_create'),
    
    # API - Savat
    path('api/v1/cart/add/', ShoppingCartCreateAPIView.as_view(), name='api_cart_add'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)