from django.db import models
from accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, default="🍽️")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    owner         = models.ForeignKey(User, on_delete=models.CASCADE, related_name="restaurants")
    name          = models.CharField(max_length=200)
    description   = models.TextField(blank=True)
    address       = models.TextField()
    phone         = models.CharField(max_length=15)
    image         = models.ImageField(upload_to="restaurants/", blank=True, null=True)
    category      = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    is_active     = models.BooleanField(default=True)
    rating        = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    delivery_time = models.PositiveIntegerField(default=30, help_text="minutes")
    min_order     = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    restaurant   = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menu_items")
    name         = models.CharField(max_length=200)
    description  = models.TextField(blank=True)
    price        = models.DecimalField(max_digits=8, decimal_places=2)
    image        = models.ImageField(upload_to="menu_items/", blank=True, null=True)
    category     = models.CharField(max_length=100, blank=True)
    is_available = models.BooleanField(default=True)
    is_veg       = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.restaurant.name}"
