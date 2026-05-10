from django.db import models
from accounts.models import User
from restaurant.models import Restaurant, MenuItem


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending",    "Pending"),
        ("confirmed",  "Confirmed"),
        ("preparing",  "Preparing"),
        ("on_the_way", "On the Way"),
        ("delivered",  "Delivered"),
        ("cancelled",  "Cancelled"),
    ]
    PAYMENT_CHOICES = [
        ("cod",    "Cash on Delivery"),
        ("card",   "Credit/Debit Card"),
        ("wallet", "Digital Wallet"),
    ]

    customer             = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    restaurant           = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    status               = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    payment_method       = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default="cod")
    delivery_address     = models.TextField()
    total_price          = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_fee         = models.DecimalField(max_digits=6,  decimal_places=2, default=50)
    special_instructions = models.TextField(blank=True)
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk} — {self.customer.username}"

    def grand_total(self):
        return self.total_price + self.delivery_fee


class OrderItem(models.Model):
    order     = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity  = models.PositiveIntegerField(default=1)
    price     = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name}"

    def subtotal(self):
        return self.price * self.quantity


class Review(models.Model):
    order      = models.OneToOneField(Order, on_delete=models.CASCADE)
    customer   = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rating     = models.PositiveSmallIntegerField(default=5)
    comment    = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.customer.username} for {self.restaurant.name}"
