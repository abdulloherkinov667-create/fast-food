from django.conf import settings
from django.db import models
from root.models import BaseCreateModel
from users.models import Users
from django.core.validators import MinValueValidator

class Category(BaseCreateModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class FastFoodProduct(BaseCreateModel):
    name = models.CharField(max_length=500)
    price = models.DecimalField("Maxsulot narxi: ", max_digits=10, decimal_places=2)
    ingredients = models.TextField("Tarkibi: ", max_length=4000)
    count = models.PositiveIntegerField(default=1, verbose_name="necha dona borr")    
    category_product = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="food_products")
    product_image = models.ImageField(upload_to="products/images/")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        
        
class ShopingModel(BaseCreateModel):
    product = models.ForeignKey(FastFoodProduct, on_delete=models.CASCADE, related_name='cart_list')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_carts')
    quantity = models.PositiveIntegerField(default=1) # <- Buni qo'shish kerak!
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"
    
    
#order model
class Order(BaseCreateModel):
    class OrderStatusChoice(models.TextChoices):
        PENDING = 'Kutilmoqda', 'Kutilmoqda'          # Buyurtma tushdi, lekin hali ko'rilmadi
        CONFIRMED = 'Tasdiqlandi', 'Tasdiqlandi'     # Admin buyurtmani ko'rib, tasdiqladi
        PROCESSING = 'Tayyorlanmoqda', 'Tayyorlanmoqda' # Omborxonada qadoqlanmoqda
        SHIPPED = 'Yo‘lga chiqdi', 'Yo‘lga chiqdi'       # Kuryerga berildi yoki pochta yo'lida
        DELIVERED = 'Yetkazildi', 'Yetkazildi'      # Mijoz mahsulotni qabul qilib oldi
        CANCELLED = 'Bekor qilindi', 'Bekor qilindi'   # Mijoz yoki admin tomonidan bekor qilindi
        RETURNED = 'Qaytarildi', 'Qaytarildi'
    
    class PaymentMethodChoice(models.TextChoices):
        CASH = 'cash', 'Naqd pul'
        PAYME = 'payme', 'Payme'
        
    
    
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='orders')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(verbose_name="Zakar borishi kk bo'lgan manzil", blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    is_status = models.CharField(
        max_length=30,
        choices=OrderStatusChoice.choices,
        default=OrderStatusChoice.PENDING
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethodChoice.choices,
        default=PaymentMethodChoice.CASH,
        verbose_name="To'lov usuli"
    )
    card_holder_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Karta egasi")
    card_number = models.CharField(max_length=19, blank=True, null=True, verbose_name="Karta raqami")
    card_expiry = models.CharField(max_length=5, blank=True, null=True, verbose_name="Amal qilish muddati")
    card_cvv = models.CharField(max_length=3, blank=True, null=True, verbose_name="CVV")

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    @property
    def total_order_price(self):
        return sum(item.item_total_price for item in self.items.all())
    
    def __str__(self):
        return self.user.username
    
    
#order item model
class OrderItem(BaseCreateModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(FastFoodProduct, on_delete=models.SET_NULL, related_name="order_items", null=True)
    product_name = models.CharField(max_length=500, blank=True)
    price = models.BigIntegerField(help_text="Sotib olingan vaqtdagi narxi", editable=False)
    count = models.IntegerField(validators=[MinValueValidator(1)])

    @property
    def item_total_price(self):
        return self.price * self.count

    def __str__(self):
        return self.product_name or "O'chirilgan mahsulot"

    def save(self, *args, **kwargs):
        if self.product:
            self.price = self.product.price
            if not self.product_name:
                self.product_name = self.product.name
        return super().save(*args, **kwargs)