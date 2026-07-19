from rest_framework import serializers
from .models import FastFoodProduct

class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = FastFoodProduct
        fields = ['id', 'name', 'price', 'ingredients', 'category_product', 'image_url', 'is_active']

    def get_image_url(self, obj):
        return obj.product_image.url if obj.product_image else None


from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

# 1. Ro'yxatdan o'tish Serializeri
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'phone_number', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )
        return user
    

# 2. Login Serializeri (Faqat username va password tekshiradi)
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Foydalanuvchi nomi yoki parol noto'g'ri!")
        else:
            raise serializers.ValidationError("Barcha maydonlarni to'ldiring!")

        data["user"] = user
        return data


# 3. Savat (Shopping Cart) Serializeri
from rest_framework import serializers

from .models import ShopingModel


class ShoppingCartSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(
        source='product.price', max_digits=10, decimal_places=2, read_only=True
    )
    item_total_price = serializers.SerializerMethodField()

    class Meta:
        model = ShopingModel
        fields = [
            'id',
            'product',
            'product_name',
            'product_price',
            'quantity',
            'item_total_price',
        ]
    def get_item_total_price(self, obj):
        return obj.product.price * obj.quantity