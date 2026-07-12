from django.contrib.auth.models import AbstractUser
from django.db import models

class Users(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Telefon raqami")

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

    @property
    def full_name(self):
        """Return a friendly full name for templates (fallback to username)."""
        full = f"{self.first_name} {self.last_name}".strip()
        return full if full else self.username

    def __str__(self):
        return self.username