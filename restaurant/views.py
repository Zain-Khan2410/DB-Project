from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Restaurant, MenuItem, Category


def home(request):
    query       = request.GET.get("q", "")
    category_id = request.GET.get("category", "")
    restaurants = Restaurant.objects.filter(is_active=True)
    categories  = Category.objects.all()

    if query:
        restaurants = restaurants.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    if category_id:
        restaurants = restaurants.filter(category_id=category_id)

    return render(request, "restaurant/home.html", {
        "restaurants": restaurants,
        "categories": categories,
        "query": query,
        "selected_category": category_id,
    })


def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk, is_active=True)
    menu_items = restaurant.menu_items.filter(is_available=True)
    menu_by_category = {}
    for item in menu_items:
        cat = item.category or "Other"
        menu_by_category.setdefault(cat, []).append(item)
    return render(request, "restaurant/detail.html", {
        "restaurant": restaurant,
        "menu_by_category": menu_by_category,
    })


@login_required
def owner_dashboard(request):
    if not request.user.is_owner() and not request.user.is_staff:
        messages.error(request, "Access denied.")
        return redirect("restaurant:home")
    restaurants = Restaurant.objects.filter(owner=request.user)
    return render(request, "restaurant/owner_dashboard.html", {"restaurants": restaurants})


@login_required
def add_restaurant(request):
    if not request.user.is_owner() and not request.user.is_staff:
        return redirect("restaurant:home")
    categories = Category.objects.all()
    if request.method == "POST":
        r = Restaurant(
            owner=request.user,
            name=request.POST["name"],
            description=request.POST.get("description", ""),
            address=request.POST["address"],
            phone=request.POST["phone"],
            delivery_time=request.POST.get("delivery_time", 30),
            min_order=request.POST.get("min_order", 0),
        )
        cat_id = request.POST.get("category")
        if cat_id:
            r.category_id = cat_id
        if request.FILES.get("image"):
            r.image = request.FILES["image"]
        r.save()
        messages.success(request, "Restaurant added!")
        return redirect("restaurant:owner_dashboard")
    return render(request, "restaurant/add_restaurant.html", {"categories": categories})


@login_required
def add_menu_item(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id, owner=request.user)
    if request.method == "POST":
        item = MenuItem(
            restaurant=restaurant,
            name=request.POST["name"],
            description=request.POST.get("description", ""),
            price=request.POST["price"],
            category=request.POST.get("category", ""),
            is_veg=request.POST.get("is_veg") == "on",
        )
        if request.FILES.get("image"):
            item.image = request.FILES["image"]
        item.save()
        messages.success(request, "Menu item added!")
        return redirect("restaurant:owner_dashboard")
    return render(request, "restaurant/add_menu_item.html", {"restaurant": restaurant})


@login_required
def delete_menu_item(request, pk):
    item = get_object_or_404(MenuItem, pk=pk, restaurant__owner=request.user)
    item.delete()
    messages.success(request, "Item deleted.")
    return redirect("restaurant:owner_dashboard")
