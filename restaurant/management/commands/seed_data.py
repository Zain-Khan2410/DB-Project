from django.core.management.base import BaseCommand
from accounts.models import User
from restaurant.models import Category, Restaurant, MenuItem


class Command(BaseCommand):
    help = "Seed demo data"

    def handle(self, *args, **kwargs):
        cats_data = [
            ("Burgers", "🍔"), ("Pizza", "🍕"), ("Biryani", "🍛"),
            ("Chinese", "🥡"), ("Desserts", "🍰"), ("Drinks", "🥤"),
        ]
        cats = {}
        for name, icon in cats_data:
            cat, _ = Category.objects.get_or_create(name=name, defaults={"icon": icon})
            cats[name] = cat

        owner, created = User.objects.get_or_create(
            username="owner1",
            defaults={"email": "owner@foodrush.pk", "role": "restaurant_owner",
                      "phone": "0300-1234567", "address": "Karachi, Pakistan"}
        )
        if created:
            owner.set_password("owner123")
            owner.save()
            self.stdout.write("  Created owner: owner1 / owner123")

        cust, created = User.objects.get_or_create(
            username="customer1",
            defaults={"email": "customer@foodrush.pk", "role": "customer",
                      "phone": "0321-9876543", "address": "DHA Phase 5, Karachi"}
        )
        if created:
            cust.set_password("cust123")
            cust.save()
            self.stdout.write("  Created customer: customer1 / cust123")

        restaurants = [
            {
                "name": "Burger Barn",
                "description": "Best smash burgers in town. Fresh, juicy, and loaded.",
                "address": "Clifton Block 5, Karachi", "phone": "021-1111111",
                "category": "Burgers", "rating": 4.5, "delivery_time": 25, "min_order": 300,
                "menu": [
                    ("Classic Smash Burger", "Double patty, cheese, lettuce, tomato", 450, "Burgers", False),
                    ("BBQ Crunch Burger",    "Crispy chicken, BBQ sauce, coleslaw",   550, "Burgers", False),
                    ("Veg Delight Burger",   "Grilled veggie patty, avocado spread",  400, "Burgers", True),
                    ("Loaded Fries",         "Cheese sauce, jalapenos, ranch dip",    250, "Sides",   True),
                    ("Oreo Shake",           "Thick and creamy Oreo milkshake",       280, "Drinks",  True),
                ],
            },
            {
                "name": "Pizza Pronto",
                "description": "Wood-fired pizzas with premium toppings.",
                "address": "Gulshan-e-Iqbal, Karachi", "phone": "021-2222222",
                "category": "Pizza", "rating": 4.2, "delivery_time": 35, "min_order": 500,
                "menu": [
                    ("Margherita Classic", "Tomato, mozzarella, fresh basil",       650, "Pizzas",   True),
                    ("BBQ Chicken Feast",  "BBQ sauce, chicken, onions, peppers",   850, "Pizzas",   False),
                    ("Spicy Pepperoni",    "Double pepperoni, chilli flakes",       900, "Pizzas",   False),
                    ("Garlic Bread",       "Herb butter garlic bread with dip",     200, "Sides",    True),
                    ("Tiramisu",           "Classic Italian dessert",               350, "Desserts", True),
                ],
            },
            {
                "name": "Biryani House",
                "description": "Authentic Karachi dum biryani since 1985.",
                "address": "Saddar, Karachi", "phone": "021-3333333",
                "category": "Biryani", "rating": 4.8, "delivery_time": 40, "min_order": 400,
                "menu": [
                    ("Chicken Biryani", "Full plate, raita included",      380, "Biryani",  False),
                    ("Beef Biryani",    "Slow-cooked beef, saffron rice",  450, "Biryani",  False),
                    ("Mutton Biryani",  "Tender mutton on the bone",       550, "Biryani",  False),
                    ("Veg Biryani",     "Basmati, vegetables, masala",     300, "Biryani",  True),
                    ("Shahi Tukra",     "Traditional Pakistani dessert",   180, "Desserts", True),
                ],
            },
        ]

        for rdata in restaurants:
            r, created = Restaurant.objects.get_or_create(
                name=rdata["name"],
                defaults={
                    "owner": owner, "description": rdata["description"],
                    "address": rdata["address"], "phone": rdata["phone"],
                    "category": cats[rdata["category"]], "rating": rdata["rating"],
                    "delivery_time": rdata["delivery_time"], "min_order": rdata["min_order"],
                }
            )
            if created:
                self.stdout.write(f"  Restaurant: {r.name}")
                for name, desc, price, cat, is_veg in rdata["menu"]:
                    MenuItem.objects.create(
                        restaurant=r, name=name, description=desc,
                        price=price, category=cat, is_veg=is_veg
                    )

        self.stdout.write(self.style.SUCCESS("\nDemo data seeded!"))
        self.stdout.write("  Owner:    owner1    / owner123")
        self.stdout.write("  Customer: customer1 / cust123")
