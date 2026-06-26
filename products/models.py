from django.db import models

class BaseCreateModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        

class Category(BaseCreateModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class FastFoodProduct(BaseCreateModel):
    name = models.CharField(max_length=500)
    price = models.DecimalField("Maxsulot narxi: ", max_digits=10, decimal_places=2)
    ingredients = models.TextField("Tarkibi: ", max_length=4000)
    category_product = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="food_products")
    product_image = models.ImageField(upload_to="products/images/")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"