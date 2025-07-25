from django.core.management.base import BaseCommand
from faker import Faker
from lemmo_apps.inventory.models.product import (
    Product,
    ProductCategory,
    ProductBatch,
    ProductImage,
)
from decimal import Decimal
import random
from datetime import timedelta
from django.utils import timezone
from django.db import models

fake = Faker()


class Command(BaseCommand):
    help = "Generate fake inventory data for testing"

    def add_arguments(self, parser):
        parser.add_argument(
            "--categories",
            type=int,
            default=20,
            help="Number of product categories to create (default: 20)",
        )
        parser.add_argument(
            "--products",
            type=int,
            default=100,
            help="Number of products to create (default: 100)",
        )
        parser.add_argument(
            "--batches",
            type=int,
            default=200,
            help="Number of product batches to create (default: 200)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before generating new data",
        )

    def handle(self, *args, **options):
        categories_count = options["categories"]
        products_count = options["products"]
        batches_count = options["batches"]
        clear_data = options["clear"]

        if clear_data:
            self.stdout.write("Clearing existing data...")
            ProductImage.objects.all().delete()
            ProductBatch.objects.all().delete()
            Product.objects.all().delete()
            ProductCategory.objects.all().delete()

        # Generate product categories
        self.stdout.write(f"Generating {categories_count} product categories...")

        categories = []
        category_names = [
            "Medications",
            "Medical Supplies",
            "Equipment",
            "Consumables",
            "Vaccines",
            "Diagnostics",
            "Nutritional",
            "Surgical Instruments",
            "Personal Protective Equipment",
            "Laboratory Supplies",
            "Emergency Equipment",
            "Rehabilitation Equipment",
            "Monitoring Devices",
            "Therapeutic Devices",
            "Sterilization Equipment",
            "Imaging Supplies",
            "Dental Supplies",
            "Ophthalmic Supplies",
            "Cardiology Equipment",
            "Neurology Equipment",
        ]

        for i in range(categories_count):
            if i < len(category_names):
                name = category_names[i]
            else:
                name = fake.unique.word().title() + " " + fake.word().title()

            category_data = {
                "name": name,
                "description": fake.text(max_nb_chars=200),
                "parent": random.choice([None] + categories) if categories else None,
                "is_active": random.choice([True, True, True, False]),  # 75% active
            }

            category = ProductCategory.objects.create(**category_data)
            categories.append(category)

            if (i + 1) % 5 == 0:
                self.stdout.write(f"Created {i + 1} categories...")

        self.stdout.write(f"Successfully created {len(categories)} product categories")

        # Generate products
        self.stdout.write(f"Generating {products_count} products...")

        products = []
        product_types = [pt[0] for pt in Product.PRODUCT_TYPES]
        storage_types = [st[0] for st in Product.STORAGE_TYPES]
        controlled_substance_types = [
            cst[0] for cst in Product.CONTROLLED_SUBSTANCE_TYPES
        ]

        # Healthcare product names
        medication_names = [
            "Aspirin",
            "Ibuprofen",
            "Acetaminophen",
            "Amoxicillin",
            "Omeprazole",
            "Lisinopril",
            "Metformin",
            "Atorvastatin",
            "Amlodipine",
            "Losartan",
            "Hydrochlorothiazide",
            "Sertraline",
            "Albuterol",
            "Fluticasone",
            "Cetirizine",
            "Loratadine",
            "Dextromethorphan",
            "Guaifenesin",
            "Pseudoephedrine",
            "Diphenhydramine",
        ]

        medical_supplies = [
            "Surgical Masks",
            "Nitrile Gloves",
            "Syringes",
            "Needles",
            "Bandages",
            "Gauze Pads",
            "Medical Tape",
            "Thermometers",
            "Blood Pressure Cuffs",
            "Stethoscopes",
            "IV Bags",
            "Catheters",
            "Sutures",
            "Surgical Scissors",
            "Forceps",
            "Scalpels",
            "Surgical Gowns",
            "Face Shields",
            "Goggles",
        ]

        for i in range(products_count):
            product_type = random.choice(product_types)

            if product_type == "MEDICATION":
                name = random.choice(medication_names)
                generic_name = name
                brand_name = fake.company() + " " + name
            elif product_type == "MEDICAL_SUPPLY":
                name = random.choice(medical_supplies)
                generic_name = None
                brand_name = None
            else:
                name = fake.unique.word().title() + " " + fake.word().title()
                generic_name = None
                brand_name = None

            product_data = {
                "name": name,
                "description": fake.text(max_nb_chars=300),
                "category": random.choice(categories),
                "product_type": product_type,
                "unit_of_measure": random.choice(
                    ["tablets", "vials", "units", "boxes", "pairs", "pieces"]
                ),
                "is_active": random.choice([True, True, True, False]),  # 75% active
                "price": Decimal(str(random.uniform(5.0, 500.0))).quantize(
                    Decimal("0.01")
                ),
                "stock_quantity": random.randint(0, 1000),
                "generic_name": generic_name,
                "brand_name": brand_name,
                "manufacturer": fake.company(),
                "ndc_code": f"{random.randint(10000, 99999)}-{random.randint(1000, 9999)}-{random.randint(10, 99)}"
                if random.choice([True, False])
                else None,
                "rx_required": random.choice([True, False]),
                "controlled_substance": random.choice(controlled_substance_types),
                "storage_type": random.choice(storage_types),
                "storage_notes": fake.text(max_nb_chars=200)
                if random.choice([True, False])
                else None,
                "expiration_date_required": random.choice(
                    [True, True, False]
                ),  # 67% require expiration
                "lot_number_required": random.choice(
                    [True, True, False]
                ),  # 67% require lot numbers
                "min_stock_level": random.randint(5, 50),
                "max_stock_level": random.randint(100, 2000),
                "reorder_point": random.randint(10, 100),
                "fda_approved": random.choice([True, False]),
                "fda_approval_date": fake.date_between(
                    start_date="-5y", end_date="today"
                )
                if random.choice([True, False])
                else None,
                "requires_prescription": random.choice([True, False]),
                "requires_special_handling": random.choice([True, False]),
                "hazardous_material": random.choice([True, False]),
                "temperature_sensitive": random.choice([True, False]),
                "weight_grams": Decimal(str(random.uniform(1.0, 1000.0))).quantize(
                    Decimal("0.01")
                )
                if random.choice([True, False])
                else None,
                "dimensions_cm": f"{random.randint(1, 50)}x{random.randint(1, 30)}x{random.randint(1, 20)}"
                if random.choice([True, False])
                else None,
            }

            product = Product.objects.create(**product_data)
            products.append(product)

            if (i + 1) % 20 == 0:
                self.stdout.write(f"Created {i + 1} products...")

        self.stdout.write(f"Successfully created {len(products)} products")

        # Generate product batches
        self.stdout.write(f"Generating {batches_count} product batches...")

        for i in range(batches_count):
            product = random.choice(products)

            # Generate realistic dates
            manufacturing_date = fake.date_between(start_date="-2y", end_date="-1m")
            expiration_date = manufacturing_date + timedelta(
                days=random.randint(365, 1095)
            )  # 1-3 years

            batch_data = {
                "product": product,
                "batch_number": f"B{fake.unique.random_number(digits=8)}",
                "lot_number": f"L{fake.unique.random_number(digits=6)}"
                if random.choice([True, False])
                else None,
                "quantity": random.randint(50, 1000),
                "remaining_quantity": random.randint(0, 1000),
                "manufacturing_date": manufacturing_date,
                "expiration_date": expiration_date,
                "cost_per_unit": Decimal(str(random.uniform(1.0, 100.0))).quantize(
                    Decimal("0.01")
                ),
                "supplier": fake.company(),
                "supplier_batch_number": f"SB{fake.unique.random_number(digits=6)}"
                if random.choice([True, False])
                else None,
                "quality_control_passed": random.choice(
                    [True, True, True, False]
                ),  # 75% pass
                "notes": fake.text(max_nb_chars=200)
                if random.choice([True, False])
                else None,
            }

            ProductBatch.objects.create(**batch_data)

            if (i + 1) % 50 == 0:
                self.stdout.write(f"Created {i + 1} batches...")

        self.stdout.write(f"Successfully created {batches_count} product batches")

        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                f"\n✅ Inventory data generation complete!\n"
                f"📊 Summary:\n"
                f"   • Categories: {ProductCategory.objects.count()}\n"
                f"   • Products: {Product.objects.count()}\n"
                f"   • Batches: {ProductBatch.objects.count()}\n"
                f"   • Active Products: {Product.objects.filter(is_active=True).count()}\n"
                f"   • Low Stock Products: {Product.objects.filter(stock_quantity__lte=models.F('min_stock_level')).count()}\n"
                f"   • Expired Batches: {ProductBatch.objects.filter(expiration_date__lt=timezone.now().date()).count()}"
            )
        )
