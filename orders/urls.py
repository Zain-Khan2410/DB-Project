from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("cart/",                    views.cart_view,           name="cart"),
    path("cart/add/",                views.add_to_cart,         name="add_to_cart"),
    path("cart/update/",             views.update_cart,         name="update_cart"),
    path("checkout/",                views.checkout_view,       name="checkout"),
    path("my-orders/",               views.my_orders,           name="my_orders"),
    path("<int:pk>/",                views.order_detail,        name="order_detail"),
    path("<int:pk>/cancel/",         views.cancel_order,        name="cancel_order"),
    path("owner/",                   views.owner_orders,        name="owner_orders"),
    path("owner/<int:pk>/status/",   views.update_order_status, name="update_order_status"),
    path("<int:order_pk>/review/",   views.leave_review,        name="leave_review"),
]
