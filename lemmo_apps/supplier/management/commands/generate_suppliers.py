from django.core.management.base import BaseCommand
from faker import Faker
from lemmo_apps.supplier.models.supplier import (
    Supplier,
    SupplierContact,
    SupplierRating,
)
from lemmo_apps.supplier.models.purchase_order import PurchaseOrder, PurchaseOrderItem
from lemmo_apps.supplier.models.contract import Contract, ContractTerm
from lemmo_apps.inventory.models.product import Product
from lemmo_apps.location.models.facility import Facility
from django.contrib.auth import get_user_model
from decimal import Decimal
import random
from datetime import timedelta
from django.utils import timezone

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "Generate fake supplier data for testing"

    def add_arguments(self, parser):
        parser.add_argument(
            "--suppliers",
            type=int,
            default=30,
            help="Number of suppliers to create (default: 30)",
        )
        parser.add_argument(
            "--contacts",
            type=int,
            default=60,
            help="Number of supplier contacts to create (default: 60)",
        )
        parser.add_argument(
            "--ratings",
            type=int,
            default=100,
            help="Number of supplier ratings to create (default: 100)",
        )
        parser.add_argument(
            "--purchase-orders",
            type=int,
            default=50,
            help="Number of purchase orders to create (default: 50)",
        )
        parser.add_argument(
            "--contracts",
            type=int,
            default=20,
            help="Number of contracts to create (default: 20)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before generating new data",
        )

    def handle(self, *args, **options):
        suppliers_count = options["suppliers"]
        contacts_count = options["contacts"]
        ratings_count = options["ratings"]
        purchase_orders_count = options["purchase_orders"]
        contracts_count = options["contracts"]
        clear_data = options["clear"]

        if clear_data:
            self.stdout.write("Clearing existing data...")
            ContractTerm.objects.all().delete()
            Contract.objects.all().delete()
            PurchaseOrderItem.objects.all().delete()
            PurchaseOrder.objects.all().delete()
            SupplierRating.objects.all().delete()
            SupplierContact.objects.all().delete()
            Supplier.objects.all().delete()

        # Get existing users, products, and facilities for relationships
        users = list(User.objects.all())
        products = list(Product.objects.all())
        facilities = list(Facility.objects.all())

        if not users:
            self.stdout.write(
                self.style.ERROR("No users found. Please generate users first.")
            )
            return

        if not products:
            self.stdout.write(
                self.style.ERROR("No products found. Please generate products first.")
            )
            return

        if not facilities:
            self.stdout.write(
                self.style.ERROR(
                    "No facilities found. Please generate facilities first."
                )
            )
            return

        # Generate suppliers
        self.stdout.write(f"Generating {suppliers_count} suppliers...")

        suppliers = []
        supplier_types = [st[0] for st in Supplier.SUPPLIER_TYPES]
        supplier_statuses = [ss[0] for ss in Supplier.SUPPLIER_STATUS]
        certification_types = [ct[0] for ct in Supplier.CERTIFICATION_TYPES]

        # Healthcare supplier names
        supplier_names = [
            "Johnson & Johnson",
            "Pfizer",
            "Merck",
            "Novartis",
            "Roche",
            "GlaxoSmithKline",
            "AstraZeneca",
            "Sanofi",
            "Bayer",
            "Abbott",
            "Medtronic",
            "Becton Dickinson",
            "Cardinal Health",
            "McKesson",
            "AmerisourceBergen",
            "Cencora",
            "Henry Schein",
            "Owens & Minor",
            "Medline Industries",
            "B. Braun",
            "Fresenius",
            "Baxter",
            "Stryker",
            "Zimmer Biomet",
            "Boston Scientific",
            "Edwards Lifesciences",
        ]

        for i in range(suppliers_count):
            if i < len(supplier_names):
                name = supplier_names[i]
            else:
                name = fake.unique.company()

            supplier_data = {
                "name": name,
                "supplier_type": random.choice(supplier_types),
                "status": random.choice(supplier_statuses),
                "address": fake.street_address(),
                "city": fake.city(),
                "state": fake.state(),
                "postal_code": fake.postcode(),
                "country": "USA",
                "phone": fake.phone_number(),
                "email": fake.email(),
                "website": fake.url() if random.choice([True, False]) else None,
                "tax_id": f"{random.randint(10, 99)}-{random.randint(1000000, 9999999)}"
                if random.choice([True, False])
                else None,
                "business_license": f"BL{fake.unique.random_number(digits=8)}"
                if random.choice([True, False])
                else None,
                "duns_number": f"{random.randint(100000000, 999999999)}"
                if random.choice([True, False])
                else None,
                "vendor_id": f"V{fake.unique.random_number(digits=6)}"
                if random.choice([True, False])
                else None,
                "fda_registration_number": f"FDA{fake.unique.random_number(digits=8)}"
                if random.choice([True, False])
                else None,
                "dea_registration_number": f"DEA{fake.unique.random_number(digits=8)}"
                if random.choice([True, False])
                else None,
                "certifications": random.sample(
                    certification_types, random.randint(0, 3)
                )
                if random.choice([True, False])
                else [],
                "specialties": random.sample(
                    [
                        "Medications",
                        "Medical Supplies",
                        "Equipment",
                        "Vaccines",
                        "Diagnostics",
                    ],
                    random.randint(1, 3),
                )
                if random.choice([True, False])
                else [],
                "credit_limit": Decimal(
                    str(random.uniform(10000.0, 1000000.0))
                ).quantize(Decimal("0.01"))
                if random.choice([True, False])
                else None,
                "payment_terms": random.choice(
                    ["Net 30", "Net 60", "Net 90", "2/10 Net 30"]
                )
                if random.choice([True, False])
                else None,
                "currency": "USD",
                "average_delivery_time": random.randint(1, 30)
                if random.choice([True, False])
                else None,
                "quality_rating": Decimal(str(random.uniform(3.0, 5.0))).quantize(
                    Decimal("0.01")
                )
                if random.choice([True, False])
                else None,
                "reliability_rating": Decimal(str(random.uniform(3.0, 5.0))).quantize(
                    Decimal("0.01")
                )
                if random.choice([True, False])
                else None,
                "assigned_buyer": random.choice(users)
                if random.choice([True, False])
                else None,
                "notes": fake.text(max_nb_chars=300)
                if random.choice([True, False])
                else None,
                "is_preferred": random.choice([True, False]),
            }

            supplier = Supplier.objects.create(**supplier_data)
            suppliers.append(supplier)

            if (i + 1) % 10 == 0:
                self.stdout.write(f"Created {i + 1} suppliers...")

        self.stdout.write(f"Successfully created {len(suppliers)} suppliers")

        # Generate supplier contacts
        self.stdout.write(f"Generating {contacts_count} supplier contacts...")

        contact_types = ["PRIMARY", "SECONDARY", "SALES", "TECHNICAL", "ACCOUNTS"]

        for i in range(contacts_count):
            supplier = random.choice(suppliers)

            contact_data = {
                "supplier": supplier,
                "name": fake.name(),
                "title": fake.job(),
                "contact_type": random.choice(contact_types),
                "phone": fake.phone_number(),
                "email": fake.email(),
                "is_primary": random.choice([True, False]),
            }

            SupplierContact.objects.create(**contact_data)

            if (i + 1) % 20 == 0:
                self.stdout.write(f"Created {i + 1} contacts...")

        self.stdout.write(f"Successfully created {contacts_count} supplier contacts")

        # Generate supplier ratings
        self.stdout.write(f"Generating {ratings_count} supplier ratings...")

        rating_types = ["QUALITY", "DELIVERY", "PRICE", "SERVICE", "RELIABILITY"]

        for i in range(ratings_count):
            supplier = random.choice(suppliers)

            rating_data = {
                "supplier": supplier,
                "rating_type": random.choice(rating_types),
                "score": random.randint(1, 5),
                "comments": fake.text(max_nb_chars=200)
                if random.choice([True, False])
                else None,
                "date": fake.date_between(start_date="-1y", end_date="today"),
            }

            SupplierRating.objects.create(**rating_data)

            if (i + 1) % 30 == 0:
                self.stdout.write(f"Created {i + 1} ratings...")

        self.stdout.write(f"Successfully created {ratings_count} supplier ratings")

        # Generate purchase orders
        self.stdout.write(f"Generating {purchase_orders_count} purchase orders...")

        po_statuses = [ps[0] for ps in PurchaseOrder.STATUS_CHOICES]
        priorities = [p[0] for p in PurchaseOrder.PRIORITY_CHOICES]

        for i in range(purchase_orders_count):
            supplier = random.choice(suppliers)
            requested_by = random.choice(users)
            approved_by = random.choice(users) if random.choice([True, False]) else None

            po_data = {
                "po_number": f"PO{fake.unique.random_number(digits=8)}",
                "supplier": supplier,
                "status": random.choice(po_statuses),
                "priority": random.choice(priorities),
                "order_date": fake.date_between(start_date="-6m", end_date="today"),
                "expected_delivery_date": fake.date_between(
                    start_date="today", end_date="+3m"
                ),
                "subtotal": Decimal(str(random.uniform(1000.0, 50000.0))).quantize(
                    Decimal("0.01")
                ),
                "tax_amount": Decimal(str(random.uniform(50.0, 2500.0))).quantize(
                    Decimal("0.01")
                ),
                "shipping_amount": Decimal(str(random.uniform(50.0, 500.0))).quantize(
                    Decimal("0.01")
                ),
                "discount_amount": Decimal(str(random.uniform(0.0, 1000.0))).quantize(
                    Decimal("0.01")
                ),
                "total_amount": Decimal(str(random.uniform(1100.0, 53000.0))).quantize(
                    Decimal("0.01")
                ),
                "currency": "USD",
                "requested_by": requested_by,
                "approved_by": approved_by,
                "approval_date": fake.date_between(start_date="-6m", end_date="today")
                if approved_by
                else None,
                "shipping_address": fake.address(),
                "shipping_method": random.choice(
                    ["Ground", "Air", "Express", "Overnight"]
                ),
                "tracking_number": f"TRK{fake.unique.random_number(digits=10)}"
                if random.choice([True, False])
                else None,
                "notes": fake.text(max_nb_chars=300)
                if random.choice([True, False])
                else None,
                "internal_notes": fake.text(max_nb_chars=200)
                if random.choice([True, False])
                else None,
                "supplier_notes": fake.text(max_nb_chars=200)
                if random.choice([True, False])
                else None,
            }

            purchase_order = PurchaseOrder.objects.create(**po_data)

            # Generate purchase order items
            num_items = random.randint(1, 5)
            for j in range(num_items):
                product = random.choice(products)

                item_data = {
                    "purchase_order": purchase_order,
                    "product": product,
                    "quantity": random.randint(10, 100),
                    "unit_price": Decimal(str(random.uniform(5.0, 500.0))).quantize(
                        Decimal("0.01")
                    ),
                    "received_quantity": random.randint(0, 100),
                    "quality_control_passed": random.choice([True, False]),
                    "batch_number": f"B{fake.unique.random_number(digits=6)}"
                    if random.choice([True, False])
                    else None,
                    "notes": fake.text(max_nb_chars=200)
                    if random.choice([True, False])
                    else None,
                }

                PurchaseOrderItem.objects.create(**item_data)

            if (i + 1) % 10 == 0:
                self.stdout.write(f"Created {i + 1} purchase orders...")

        self.stdout.write(
            f"Successfully created {purchase_orders_count} purchase orders"
        )

        # Generate contracts
        self.stdout.write(f"Generating {contracts_count} contracts...")

        contract_types = [ct[0] for ct in Contract.CONTRACT_TYPES]
        contract_statuses = [cs[0] for cs in Contract.STATUS_CHOICES]

        for i in range(contracts_count):
            supplier = random.choice(suppliers)
            created_by = random.choice(users)
            approved_by = random.choice(users) if random.choice([True, False]) else None

            start_date = fake.date_between(start_date="-1y", end_date="+1y")
            end_date = start_date + timedelta(
                days=random.randint(365, 1095)
            )  # 1-3 years

            contract_data = {
                "contract_number": f"CON{fake.unique.random_number(digits=8)}",
                "supplier": supplier,
                "contract_type": random.choice(contract_types),
                "status": random.choice(contract_statuses),
                "start_date": start_date,
                "end_date": end_date,
                "renewal_date": end_date - timedelta(days=30)
                if random.choice([True, False])
                else None,
                "total_value": Decimal(
                    str(random.uniform(50000.0, 1000000.0))
                ).quantize(Decimal("0.01"))
                if random.choice([True, False])
                else None,
                "currency": "USD",
                "payment_terms": random.choice(
                    ["Net 30", "Net 60", "Net 90", "2/10 Net 30"]
                )
                if random.choice([True, False])
                else None,
                "payment_schedule": {
                    "frequency": random.choice(["Monthly", "Quarterly", "Annually"]),
                    "advance_payment": random.choice([True, False]),
                }
                if random.choice([True, False])
                else {},
                "title": fake.sentence(nb_words=6),
                "description": fake.text(max_nb_chars=500),
                "terms_and_conditions": fake.text(max_nb_chars=1000)
                if random.choice([True, False])
                else None,
                "created_by": created_by,
                "approved_by": approved_by,
                "approval_date": fake.date_between(
                    start_date=start_date, end_date=start_date + timedelta(days=30)
                )
                if approved_by
                else None,
                "performance_score": Decimal(str(random.uniform(3.0, 5.0))).quantize(
                    Decimal("0.01")
                )
                if random.choice([True, False])
                else None,
                "compliance_score": Decimal(str(random.uniform(3.0, 5.0))).quantize(
                    Decimal("0.01")
                )
                if random.choice([True, False])
                else None,
                "notes": fake.text(max_nb_chars=300)
                if random.choice([True, False])
                else None,
                "internal_notes": fake.text(max_nb_chars=200)
                if random.choice([True, False])
                else None,
            }

            contract = Contract.objects.create(**contract_data)

            # Generate contract terms
            num_terms = random.randint(1, 3)
            term_types = [tt[0] for tt in ContractTerm.TERM_TYPES]

            for j in range(num_terms):
                term_data = {
                    "contract": contract,
                    "term_type": random.choice(term_types),
                    "description": fake.text(max_nb_chars=200),
                    "value": fake.text(max_nb_chars=100),
                    "effective_date": fake.date_between(
                        start_date=start_date, end_date=end_date
                    ),
                    "is_compliant": random.choice(
                        [True, True, True, False]
                    ),  # 75% compliant
                    "compliance_notes": fake.text(max_nb_chars=200)
                    if random.choice([True, False])
                    else None,
                }

                ContractTerm.objects.create(**term_data)

            if (i + 1) % 5 == 0:
                self.stdout.write(f"Created {i + 1} contracts...")

        self.stdout.write(f"Successfully created {contracts_count} contracts")

        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                f"\n✅ Supplier data generation complete!\n"
                f"📊 Summary:\n"
                f"   • Suppliers: {Supplier.objects.count()}\n"
                f"   • Contacts: {SupplierContact.objects.count()}\n"
                f"   • Ratings: {SupplierRating.objects.count()}\n"
                f"   • Purchase Orders: {PurchaseOrder.objects.count()}\n"
                f"   • Purchase Order Items: {PurchaseOrderItem.objects.count()}\n"
                f"   • Contracts: {Contract.objects.count()}\n"
                f"   • Contract Terms: {ContractTerm.objects.count()}\n"
                f"   • Active Suppliers: {Supplier.objects.filter(status='ACTIVE').count()}\n"
                f"   • Preferred Suppliers: {Supplier.objects.filter(is_preferred=True).count()}\n"
                f"   • FDA Registered: {Supplier.objects.filter(fda_registration_number__isnull=False).count()}"
            )
        )
