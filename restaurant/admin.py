from django.contrib import admin
from .models import Restaurant, MenuItem, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "icon")

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display  = ("name", "owner", "category", "rating", "delivery_time", "is_active")
    list_filter   = ("is_active", "category")
    search_fields = ("name",)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display  = ("name", "restaurant", "price", "category", "is_available", "is_veg")
    list_filter   = ("is_available", "is_veg")
    search_fields = ("name",)
