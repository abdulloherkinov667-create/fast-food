from django.contrib import admin
from .models import Category, FastFoodProduct
from products.models import ShopingModel, Order, OrderItem

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
    
    
@admin.register(ShopingModel)
class ShopingModelAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('product__name', 'user__username')
    ordering = ('-created_at',)
    
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'phone', 'address', 'is_status', 'created_at')
    list_filter = ('is_status', 'created_at')
    search_fields = ('user__username', 'phone', 'address')
    ordering = ('-created_at',)
    
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'price', 'count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('order__id', 'product__name')
    ordering = ('-created_at',)