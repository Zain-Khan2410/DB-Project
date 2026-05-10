from django.urls import path
from . import views

app_name = "restaurant"

urlpatterns = [
    path("",                               views.home,             name="home"),
    path("<int:pk>/",                      views.restaurant_detail,name="detail"),
    path("dashboard/",                     views.owner_dashboard,  name="owner_dashboard"),
    path("add/",                           views.add_restaurant,   name="add_restaurant"),
    path("<int:restaurant_id>/menu/add/",  views.add_menu_item,    name="add_menu_item"),
    path("menu/<int:pk>/delete/",          views.delete_menu_item, name="delete_menu_item"),
]
