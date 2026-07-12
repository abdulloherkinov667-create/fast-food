from django.contrib import admin
from users.models import Users


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone_number', 'date_joined')
    search_fields = ('username', 'phone_number')