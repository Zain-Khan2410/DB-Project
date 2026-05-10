import os
import django
import random

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "food_delivery.settings")
django.setup()

from django.contrib.auth import get_user_model
from restaurant.models import Category, Restaurant, MenuItem
from orders.models import Order, OrderItem

User = get_user_model()

def seed_data():
    print("🌱 Starting database seeding...")

    # 1. Create Users
    owner, created = User.objects.get_or_create(
        username="owner1",
        defaults={"email": "owner@example.com", "role": "restaurant_owner"}
    )
    if created:
        owner.set_password("admin123")
        owner.save()
        print(f"✅ Created Owner: {owner.username}")

    customer, created = User.objects.get_or_create(
        username="customer1",
        defaults={"email": "customer@example.com", "role": "customer", "address": "123 Foodie Street, Karachi"}
    )
    if created:
        customer.set_password("admin123")
        customer.save()
        print(f"✅ Created Customer: {customer.username}")

    # 2. Create Categories
    categories_data = [
        ("Burgers", "🍔"),
        ("Pizza", "🍕"),
        ("Desi", "🍲"),
        ("Chinese", "🥢"),
        ("Desserts", "🍰"),
    ]
    categories = []
    for name, icon in categories_data:
        cat, _ = Category.objects.get_or_create(name=name, defaults={"icon": icon})
        categories.append(cat)
    print("✅ Categories created.")

    # 3. Create Restaurants
    restaurants_data = [
        {
            "name": "Burger Knight",
            "description": "The best burgers in town with secret sauces.",
            "address": "DHA Phase 6, Karachi",
            "phone": "+923001112222",
            "category": categories[0],
            "rating": 4.5,
        },
        {
            "name": "Pizza Palace",
            "description": "Authentic Italian wood-fired pizzas.",
            "address": "Gulshan-e-Iqbal, Karachi",
            "phone": "+923003334444",
            "category": categories[1],
            "rating": 4.8,
        },
        {
            "name": "Desi Dhaba",
            "description": "Traditional flavors that feel like home.",
            "address": "North Nazimabad, Karachi",
            "phone": "+923005556666",
            "category": categories[2],
            "rating": 4.2,
        },
    ]

    created_restaurants = []
    for r_data in restaurants_data:
        res, created = Restaurant.objects.get_or_create(
            name=r_data["name"],
            defaults={
                "owner": owner,
                "description": r_data["description"],
                "address": r_data["address"],
                "phone": r_data["phone"],
                "category": r_data["category"],
                "rating": r_data["rating"],
                "delivery_time": random.choice([25, 30, 45]),
                "min_order": random.choice([500, 1000]),
            }
        )
        created_restaurants.append(res)
        if created:
            print(f"✅ Created Restaurant: {res.name}")

    # 4. Create Menu Items
    menu_data = {
        "Burger Knight": [
            ("Zinger Burger", "Crispy chicken with mayo", 450),
            ("Beef Master", "Juicy beef patty with cheese", 650),
            ("French Fries", "Large portion with masala", 250),
        ],
        "Pizza Palace": [
            ("Margherita", "Simple cheese and basil", 1200),
            ("Pepperoni Feast", "Loaded with pepperoni", 1500),
            ("Garlic Bread", "Buttery garlic goodness", 350),
        ],
        "Desi Dhaba": [
            ("Chicken Karahi", "Half kg spicy karahi", 950),
            ("Garlic Naan", "Fresh from the tandoor", 60),
            ("Biryani", "Special Sindhi Biryani", 400),
        ]
    }

    for res in created_restaurants:
        items = menu_data.get(res.name, [])
        for name, desc, price in items:
            MenuItem.objects.get_or_create(
                restaurant=res,
                name=name,
                defaults={"description": desc, "price": price, "category": "Popular"}
            )
    print("✅ Menu items added.")

    # 5. Create a Dummy Order
    if not Order.objects.filter(customer=customer).exists():
        res = created_restaurants[0]
        order = Order.objects.create(
            customer=customer,
            restaurant=res,
            delivery_address=customer.address,
            total_price=700,
            status="delivered"
        )
        item = res.menu_items.first()
        OrderItem.objects.create(
            order=order,
            menu_item=item,
            quantity=1,
            price=item.price
        )
        print(f"✅ Created Dummy Order #{order.pk}")

    print("\n✨ Seeding completed successfully!")
    print(f"🔑 Owner Login: owner1 / admin123")
    print(f"🔑 Customer Login: customer1 / admin123")

if __name__ == "__main__":
    seed_data()
