from django.contrib import admin
from root import settings
from django.urls import path
from django.conf.urls.static import static 

from products.views import menu_home
from users.views import RegisterAPIView, logout_page, profile_page, savat_page, register_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', menu_home, name='menu_home'),
    path("profil/", profile_page, name='profile_user'),
    path("register/", register_page, name='register_user'),
    path("logout/", logout_page, name='logout_user'),
    path("savat_page/", savat_page, name='savat_page'),
    
    #api registr
    path('api/register/', RegisterAPIView.as_view(), name='api_register'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)