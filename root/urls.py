from django.contrib import admin
from root import settings
from django.urls import path
from django.conf.urls.static import static 

from products.views import menu_home
from users.views import profile_page, savat_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', menu_home, name='menu_home'),
    path("profil/", profile_page, name='profile_user'),
    path("savat_page/", savat_page, name='savat_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)