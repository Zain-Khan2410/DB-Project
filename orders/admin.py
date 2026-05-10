from django.contrib import admin
from .models import Order, OrderItem, Review

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("pk", "customer", "restaurant", "status", "total_price", "created_at")
    list_filter  = ("status", "payment_method")
    inlines      = [OrderItemInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("customer", "restaurant", "rating", "created_at")
