from django.core.management.base import BaseCommand
from products.models import Category, FastFoodProduct


class Command(BaseCommand):
    help = "Bazaga restoran kategoriyalari va mahsulotlarni qo'shadi"

    def handle(self, *args, **options):
        self.stdout.write("Ma'lumotlar qo'shilmoqda...")

        # ==================== KATEGORIYALAR ====================
        categories_data = [
            "Burgerlar",
            "Pitsa",
            "Hot-Doglar",
            "Gazaklar",
            "Salatlar",
            "Tovuq taomlar",
            "Lavash va Shaverma",
            "Ichimliklar",
            "Desertlar",
            "Sho'rvalar",
        ]

        categories = {}
        for name in categories_data:
            cat, created = Category.objects.get_or_create(name=name)
            categories[name] = cat
            status = "[+] Yaratildi" if created else "[=] Mavjud"
            self.stdout.write(f"  {status}: {name}")

        # ==================== MAHSULOTLAR ====================
        products_data = [
            # --- Burgerlar ---
            {
                "name": "Classic Cheeseburger",
                "price": 32000,
                "ingredients": "Mol go'shti kotleti, cheddar pishloqi, pomidor, salat bargi, piyoz, xantal sous, sezam bulochka",
                "count": 50,
                "category": "Burgerlar",
                "image": "products/images/cheeseburger.png",
            },
            {
                "name": "Double Burger",
                "price": 45000,
                "ingredients": "2x mol go'shti kotleti, bekon, cheddar pishloq, tuzlangan bodring, piyoz halqalari, maxsus sous",
                "count": 40,
                "category": "Burgerlar",
                "image": "products/images/double_burger.png",
            },
            {
                "name": "Chicken Burger",
                "price": 35000,
                "ingredients": "Qarsildoq tovuq filesi, salat bargi, mayanez, pomidor, briosh bulochka",
                "count": 45,
                "category": "Burgerlar",
                "image": "products/images/chicken_burger.png",
            },
            {
                "name": "BBQ Burger",
                "price": 42000,
                "ingredients": "Mol go'shti kotleti, bekon, BBQ sousi, karamelizatsiya qilingan piyoz, xantal pishloq",
                "count": 35,
                "category": "Burgerlar",
                "image": "products/images/cheeseburger.png",
            },
            # --- Pitsa ---
            {
                "name": "Pizza Margarita",
                "price": 55000,
                "ingredients": "Mozzarella pishloq, pomidor sousi, yangi rayhon barglari, zaytun moyi",
                "count": 30,
                "category": "Pitsa",
                "image": "products/images/pizza_margarita.png",
            },
            {
                "name": "Pizza Pepperoni",
                "price": 62000,
                "ingredients": "Pepperoni kolbasa, mozzarella pishloq, pomidor sousi, oregano",
                "count": 30,
                "category": "Pitsa",
                "image": "products/images/pizza_pepperoni.png",
            },
            {
                "name": "Pizza 4 Pishloq",
                "price": 68000,
                "ingredients": "Mozzarella, parmezan, gorgonzola, cheddar pishloqlari, krem sous",
                "count": 25,
                "category": "Pitsa",
                "image": "products/images/pizza_margarita.png",
            },
            {
                "name": "Pizza Go'shtli",
                "price": 72000,
                "ingredients": "Mol go'shti, tovuq, kolbasa, bekon, mozzarella, pomidor sousi, qalampir",
                "count": 20,
                "category": "Pitsa",
                "image": "products/images/pizza_pepperoni.png",
            },
            # --- Hot-Doglar ---
            {
                "name": "Classic Hot-Dog",
                "price": 18000,
                "ingredients": "Sosiska, gorchitsa, ketchup, tuzlangan bodring, piyoz, bulochka",
                "count": 60,
                "category": "Hot-Doglar",
                "image": "products/images/hot_dog.png",
            },
            {
                "name": "Mega Hot-Dog",
                "price": 25000,
                "ingredients": "2x sosiska, pishloq sousi, jalapeno, qarsildoq piyoz, gorchitsa sous",
                "count": 40,
                "category": "Hot-Doglar",
                "image": "products/images/hot_dog.png",
            },
            # --- Gazaklar ---
            {
                "name": "Fri Kartoshka (Standart)",
                "price": 15000,
                "ingredients": "Oltin qarsildoq kartoshka, tuz, ketchup",
                "count": 100,
                "category": "Gazaklar",
                "image": "products/images/cheeseburger.png",
            },
            {
                "name": "Fri Kartoshka (Katta)",
                "price": 22000,
                "ingredients": "Katta porsiya oltin kartoshka, tuz, 2x sous (ketchup, mayanez)",
                "count": 80,
                "category": "Gazaklar",
                "image": "products/images/cheeseburger.png",
            },
            {
                "name": "Chicken Nagetslar (6 dona)",
                "price": 24000,
                "ingredients": "6 dona qarsildoq tovuq nagetslari, BBQ va mayanez souslari",
                "count": 70,
                "category": "Gazaklar",
                "image": "products/images/chicken_burger.png",
            },
            {
                "name": "Chicken Nagetslar (12 dona)",
                "price": 42000,
                "ingredients": "12 dona qarsildoq tovuq nagetslari, 3 xil sous (BBQ, mayanez, sweet chili)",
                "count": 50,
                "category": "Gazaklar",
                "image": "products/images/chicken_burger.png",
            },
            {
                "name": "Piyoz Halqalari",
                "price": 18000,
                "ingredients": "Qarsildoq piyoz halqalari, ranch sousi",
                "count": 60,
                "category": "Gazaklar",
                "image": "products/images/double_burger.png",
            },
            # --- Salatlar ---
            {
                "name": "Sezar Salat",
                "price": 35000,
                "ingredients": "Rimcha salat, parmezan pishloq, krutonlar, tovuq filesi, Sezar sousi",
                "count": 30,
                "category": "Salatlar",
                "image": "products/images/pizza_margarita.png",
            },
            {
                "name": "Ovqatxona Salat",
                "price": 15000,
                "ingredients": "Pomidor, bodring, piyoz, ko'k qalampir, zaytun moyi, limon sharbati",
                "count": 50,
                "category": "Salatlar",
                "image": "products/images/pizza_margarita.png",
            },
            # --- Tovuq taomlar ---
            {
                "name": "Qarsildoq Tovuq Qanotlari (8 dona)",
                "price": 38000,
                "ingredients": "8 dona qarsildoq tovuq qanotlari, maxsus ziravorlar, sous",
                "count": 40,
                "category": "Tovuq taomlar",
                "image": "products/images/chicken_burger.png",
            },
            {
                "name": "Tovuq Stiks (6 dona)",
                "price": 32000,
                "ingredients": "6 dona tovuq stikslari, qarsildoq panir, 2 xil sous",
                "count": 45,
                "category": "Tovuq taomlar",
                "image": "products/images/chicken_burger.png",
            },
            {
                "name": "Grillangan Tovuq",
                "price": 48000,
                "ingredients": "Butun grillangan tovuq, maxsus marinad, ziravorlar, sous",
                "count": 20,
                "category": "Tovuq taomlar",
                "image": "products/images/chicken_burger.png",
            },
            # --- Lavash va Shaverma ---
            {
                "name": "Shaverma Classic",
                "price": 28000,
                "ingredients": "Tovuq go'shti, salat, pomidor, bodring, mayanez, ketchup, lavash",
                "count": 60,
                "category": "Lavash va Shaverma",
                "image": "products/images/hot_dog.png",
            },
            {
                "name": "Shaverma Double",
                "price": 38000,
                "ingredients": "2x tovuq go'shti, pishloq, salat, pomidor, bodring, maxsus sous, lavash",
                "count": 40,
                "category": "Lavash va Shaverma",
                "image": "products/images/hot_dog.png",
            },
            {
                "name": "Lavash Go'shtli",
                "price": 35000,
                "ingredients": "Mol go'shti, sabzavotlar, pishloq, sous, yupqa lavash",
                "count": 35,
                "category": "Lavash va Shaverma",
                "image": "products/images/hot_dog.png",
            },
            # --- Ichimliklar ---
            {
                "name": "Coca-Cola (0.5L)",
                "price": 8000,
                "ingredients": "Coca-Cola 0.5 litrlik shisha",
                "count": 200,
                "category": "Ichimliklar",
                "image": "products/images/pizza_pepperoni.png",
            },
            {
                "name": "Fanta (0.5L)",
                "price": 8000,
                "ingredients": "Fanta apelsin 0.5 litrlik shisha",
                "count": 150,
                "category": "Ichimliklar",
                "image": "products/images/pizza_pepperoni.png",
            },
            {
                "name": "Sprite (0.5L)",
                "price": 8000,
                "ingredients": "Sprite 0.5 litrlik shisha",
                "count": 150,
                "category": "Ichimliklar",
                "image": "products/images/pizza_pepperoni.png",
            },
            {
                "name": "Limonad (Uy)",
                "price": 12000,
                "ingredients": "Yangi siqilgan limon sharbati, shakar siropi, yalpiz, muz",
                "count": 80,
                "category": "Ichimliklar",
                "image": "products/images/pizza_pepperoni.png",
            },
            {
                "name": "Mojito (Alkogolik emas)",
                "price": 18000,
                "ingredients": "Laym, yalpiz, shakar siropi, soda suvi, muz",
                "count": 60,
                "category": "Ichimliklar",
                "image": "products/images/pizza_pepperoni.png",
            },
            {
                "name": "Choy (Qora/Ko'k)",
                "price": 5000,
                "ingredients": "Tabiiy choy barglari, limon, asal",
                "count": 200,
                "category": "Ichimliklar",
                "image": "products/images/pizza_pepperoni.png",
            },
            # --- Desertlar ---
            {
                "name": "Tiramisu",
                "price": 28000,
                "ingredients": "Maskarpone pishloq, espresso kofe, kakao kukuni, biskvit",
                "count": 25,
                "category": "Desertlar",
                "image": "products/images/pizza_margarita.png",
            },
            {
                "name": "Shokoladli Fondant",
                "price": 25000,
                "ingredients": "Quyuq shokolad markazi, biskvit, muzqaymoq bilan",
                "count": 30,
                "category": "Desertlar",
                "image": "products/images/pizza_margarita.png",
            },
            {
                "name": "Cheesecake",
                "price": 30000,
                "ingredients": "Krem pishloq, pechenye asosi, qulupnay sousi",
                "count": 20,
                "category": "Desertlar",
                "image": "products/images/pizza_margarita.png",
            },
            # --- Sho'rvalar ---
            {
                "name": "Mastava",
                "price": 22000,
                "ingredients": "Mol go'shti, guruch, sabzavotlar, ziravorlar, qatiq bilan",
                "count": 40,
                "category": "Sho'rvalar",
                "image": "products/images/double_burger.png",
            },
            {
                "name": "Tovuq Sho'rva",
                "price": 20000,
                "ingredients": "Tovuq go'shti, makaron, sabzi, piyoz, ukrop",
                "count": 45,
                "category": "Sho'rvalar",
                "image": "products/images/double_burger.png",
            },
            {
                "name": "Lag'mon",
                "price": 30000,
                "ingredients": "Qo'l bilan tortilgan makaron, mol go'shti, sabzavotlar, maxsus ziravorlar",
                "count": 35,
                "category": "Sho'rvalar",
                "image": "products/images/double_burger.png",
            },
        ]

        created_count = 0
        existing_count = 0

        for item in products_data:
            category = categories[item["category"]]
            product, created = FastFoodProduct.objects.get_or_create(
                name=item["name"],
                defaults={
                    "price": item["price"],
                    "ingredients": item["ingredients"],
                    "count": item["count"],
                    "category_product": category,
                    "product_image": item["image"],
                    "is_active": True,
                },
            )
            if created:
                created_count += 1
                self.stdout.write(f"  [+] {item['name']} - {item['price']} so'm")
            else:
                existing_count += 1
                self.stdout.write(f"  [=] Mavjud: {item['name']}")

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"Tayyor! {created_count} ta yangi mahsulot qo'shildi, "
            f"{existing_count} ta allaqachon mavjud edi."
        ))
        self.stdout.write(self.style.SUCCESS(
            f"Jami: {Category.objects.count()} ta kategoriya, "
            f"{FastFoodProduct.objects.count()} ta mahsulot"
        ))
