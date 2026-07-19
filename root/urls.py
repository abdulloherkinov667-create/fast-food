from django.contrib import admin
from root import settings
from django.urls import path
from django.conf.urls.static import static 

from products.views import menu_home
from users.views import profile_page, savat_page, registratsiya_page, login_page, logout_user
from products.views import delete_product_cart
from users.views import RegisterView, LoginView
from products.profduct_api import ShoppingCartCreateAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', menu_home, name='menu_home'),
    path("profil/", profile_page, name='profile_user'),
    path("savat_page/", savat_page, name='savat_page'),
    path('registratsiya/', registratsiya_page, name='registratsiya_page'),
    path('login/', login_page, name='login_page'),
    path('logout/', logout_user, name='logout_user'),
    
    # api auth    
    path('api/v1/auth/register/', RegisterView.as_view(), name='api_register'),
    path('api/v1/auth/login/', LoginView.as_view(), name='api_login'),
    path('cart/delete/<int:pk>/', delete_product_cart, name='delete_product_cart'),
    
    # API - Savat
    path('api/v1/cart/add/', ShoppingCartCreateAPIView.as_view(), name='api_cart_add'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)