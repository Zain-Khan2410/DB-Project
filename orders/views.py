from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from restaurant.models import MenuItem, Restaurant
from .models import Order, OrderItem, Review


def get_cart(request):
    return request.session.get("cart", {})

def save_cart(request, cart):
    request.session["cart"] = cart
    # Calculate total items and store in session for easy template access
    total_items = sum(v.get("quantity", 0) for v in cart.get("items", {}).values())
    request.session["cart_count"] = total_items
    request.session.modified = True


@login_required
@require_POST
def add_to_cart(request):
    data     = json.loads(request.body)
    item_id  = str(data.get("item_id"))
    quantity = int(data.get("quantity", 1))

    item = get_object_or_404(MenuItem, pk=item_id, is_available=True)
    cart = get_cart(request)

    if cart and "restaurant_id" in cart:
        if str(cart["restaurant_id"]) != str(item.restaurant_id):
            return JsonResponse({
                "success": False,
                "message": "Clear your cart before ordering from a different restaurant."
            })

    cart.setdefault("restaurant_id", item.restaurant_id)
    cart.setdefault("items", {})

    if item_id in cart["items"]:
        cart["items"][item_id]["quantity"] += quantity
    else:
        cart["items"][item_id] = {
            "name":     item.name,
            "price":    str(item.price),
            "quantity": quantity,
            "image":    item.image.url if item.image else "",
        }

    save_cart(request, cart)
    total_items = sum(v["quantity"] for v in cart["items"].values())
    return JsonResponse({"success": True, "cart_count": total_items})


@login_required
def cart_view(request):
    cart     = get_cart(request)
    items    = []
    subtotal = 0

    if cart.get("items"):
        for item_id, info in cart["items"].items():
            line = float(info["price"]) * info["quantity"]
            subtotal += line
            items.append({**info, "id": item_id, "subtotal": round(line, 2)})

    delivery_fee = 50 if items else 0
    return render(request, "orders/cart.html", {
        "items":        items,
        "subtotal":     round(subtotal, 2),
        "delivery_fee": delivery_fee,
        "grand_total":  round(subtotal + delivery_fee, 2),
    })


@login_required
@require_POST
def update_cart(request):
    data    = json.loads(request.body)
    item_id = str(data.get("item_id"))
    action  = data.get("action")

    cart = get_cart(request)
    if "items" in cart and item_id in cart["items"]:
        if action == "remove" or (action == "decrease" and cart["items"][item_id]["quantity"] <= 1):
            del cart["items"][item_id]
            if not cart["items"]:
                cart = {}
        elif action == "increase":
            cart["items"][item_id]["quantity"] += 1
        elif action == "decrease":
            cart["items"][item_id]["quantity"] -= 1

    save_cart(request, cart)
    return JsonResponse({"success": True})


@login_required
def checkout_view(request):
    cart = get_cart(request)
    if not cart.get("items"):
        messages.error(request, "Your cart is empty.")
        return redirect("orders:cart")

    if request.method == "POST":
        restaurant = get_object_or_404(Restaurant, pk=cart["restaurant_id"])
        subtotal   = sum(float(v["price"]) * v["quantity"] for v in cart["items"].values())

        order = Order.objects.create(
            customer=request.user,
            restaurant=restaurant,
            delivery_address=request.POST.get("address", request.user.address),
            payment_method=request.POST.get("payment_method", "cod"),
            total_price=subtotal,
            delivery_fee=50,
            special_instructions=request.POST.get("special_instructions", ""),
        )

        for item_id, info in cart["items"].items():
            menu_item = MenuItem.objects.get(pk=item_id)
            OrderItem.objects.create(
                order=order, menu_item=menu_item,
                quantity=info["quantity"], price=info["price"],
            )

        request.session["cart"] = {}
        request.session.modified = True
        messages.success(request, f"Order #{order.pk} placed successfully!")
        return redirect("orders:order_detail", pk=order.pk)

    return render(request, "orders/checkout.html", {"cart": cart, "user": request.user})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, customer=request.user)
    return render(request, "orders/order_detail.html", {"order": order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(customer=request.user)
    return render(request, "orders/my_orders.html", {"orders": orders})


@login_required
def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk, customer=request.user)
    if order.status == "pending":
        order.status = "cancelled"
        order.save()
        messages.success(request, "Order cancelled.")
    else:
        messages.error(request, "Cannot cancel this order.")
    return redirect("orders:my_orders")


@login_required
def owner_orders(request):
    if not request.user.is_owner() and not request.user.is_staff:
        return redirect("restaurant:home")
    restaurants = request.user.restaurants.all()
    orders      = Order.objects.filter(restaurant__in=restaurants)
    return render(request, "orders/owner_orders.html", {"orders": orders})


@login_required
@require_POST
def update_order_status(request, pk):
    if request.user.is_staff:
        order = get_object_or_404(Order, pk=pk)
    else:
        order = get_object_or_404(Order, pk=pk, restaurant__owner=request.user)
    new_status = request.POST.get("status")
    valid      = [s[0] for s in Order.STATUS_CHOICES]
    if new_status in valid:
        order.status = new_status
        order.save()
        messages.success(request, f"Status updated to {new_status}.")
    return redirect("orders:owner_orders")


@login_required
def leave_review(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk, customer=request.user, status="delivered")
    if hasattr(order, "review"):
        messages.info(request, "You already reviewed this order.")
        return redirect("orders:my_orders")

    if request.method == "POST":
        Review.objects.create(
            order=order, customer=request.user, restaurant=order.restaurant,
            rating=int(request.POST.get("rating", 5)),
            comment=request.POST.get("comment", ""),
        )
        r       = order.restaurant
        reviews = Review.objects.filter(restaurant=r)
        r.rating = sum(rv.rating for rv in reviews) / reviews.count()
        r.save()
        messages.success(request, "Review submitted!")
        return redirect("orders:my_orders")

    return render(request, "orders/review.html", {"order": order})
