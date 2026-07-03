from django.db import models
from products.models import BaseCreateModel


class User(BaseCreateModel):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.full_name