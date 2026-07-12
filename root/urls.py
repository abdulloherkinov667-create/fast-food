from django.contrib import admin
from root import settings
from django.urls import path
from django.conf.urls.static import static 

from products.views import menu_home
from users.views import profile_page, savat_page, registratsiya_page, login_page, logout_user
from products.views import shoping_cart_create
from users.views import RegisterView, LoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', menu_home, name='menu_home'),
    path("profil/", profile_page, name='profile_user'),
    path("savat_page/", savat_page, name='savat_page'),
    path('shoping_cart_create/', shoping_cart_create, name='shoping_cart_create'),
    path('registratsiya/', registratsiya_page, name='registratsiya_page'),
    path('login/', login_page, name='login_page'),
    path('logout/', logout_user, name='logout_user'),
    
    # api auth    
    path('api/v1/auth/register/', RegisterView.as_view(), name='api_register'),
    path('api/v1/auth/login/', LoginView.as_view(), name='api_login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)