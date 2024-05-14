from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

User = get_user_model()


def default_cart_data():
    return {}


class Cart(models.Model):
    user = models.OneToOneField(User, related_name="cart", on_delete=models.CASCADE, editable=False)
    data = models.JSONField(default=default_cart_data, editable=False)

    def __str__(self):
        return f"{self.user.username} cart"
