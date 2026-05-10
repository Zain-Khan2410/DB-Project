from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ("customer", "Customer"),
        ("restaurant_owner", "Restaurant Owner"),
        ("admin", "Admin"),
    ]
    role        = models.CharField(max_length=20, choices=ROLE_CHOICES, default="customer")
    phone       = models.CharField(max_length=20, blank=True)
    address     = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to="profiles/", blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    def is_customer(self):
        return self.role == "customer"

    def is_owner(self):
        return self.role == "restaurant_owner"
