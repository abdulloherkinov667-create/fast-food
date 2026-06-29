from django.contrib import admin
from .models import Category, FastFoodProduct

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id','created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('-created_at',)


@admin.register(FastFoodProduct)
class FastFoodProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'price', 'count', 'category_product', 'is_active', 'created_at')
    list_filter = ('category_product', 'is_active', 'created_at')
    search_fields = ('name', 'ingredients')
    list_editable = ('price', 'count', 'is_active')
    ordering = ('-created_at',)