from django.core.management.base import BaseCommand
from faker import Faker
from lemmo_apps.location.models.facility import (
    Facility,
    FacilityType,
    FacilityDepartment,
    FacilityContact,
)
from lemmo_apps.location.models.location import Location, LocationType
import random
from decimal import Decimal

fake = Faker()


class Command(BaseCommand):
    help = "Generate fake location data for testing"

    def add_arguments(self, parser):
        parser.add_argument(
            "--facility-types",
            type=int,
            default=10,
            help="Number of facility types to create (default: 10)",
        )
        parser.add_argument(
            "--facilities",
            type=int,
            default=50,
            help="Number of facilities to create (default: 50)",
        )
        parser.add_argument(
            "--departments",
            type=int,
            default=100,
            help="Number of facility departments to create (default: 100)",
        )
        parser.add_argument(
            "--contacts",
            type=int,
            default=150,
            help="Number of facility contacts to create (default: 150)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before generating new data",
        )

    def handle(self, *args, **options):
        facility_types_count = options["facility_types"]
        facilities_count = options["facilities"]
        departments_count = options["departments"]
        contacts_count = options["contacts"]
        clear_data = options["clear"]

        if clear_data:
            self.stdout.write("Clearing existing data...")
            FacilityContact.objects.all().delete()
            FacilityDepartment.objects.all().delete()
            Facility.objects.all().delete()
            FacilityType.objects.all().delete()

        # Generate facility types
        self.stdout.write(f"Generating {facility_types_count} facility types...")

        facility_types = []
        type_names = [
            "General Hospital",
            "Specialty Hospital",
            "Community Hospital",
            "Teaching Hospital",
            "Medical Clinic",
            "Urgent Care Center",
            "Primary Care Clinic",
            "Specialty Clinic",
            "Pharmacy",
            "Retail Pharmacy",
            "Hospital Pharmacy",
            "Compounding Pharmacy",
            "Laboratory",
            "Diagnostic Laboratory",
            "Research Laboratory",
            "Blood Bank",
            "Warehouse",
            "Distribution Center",
            "Medical Supply Store",
            "Rehabilitation Center",
        ]

        for i in range(facility_types_count):
            if i < len(type_names):
                name = type_names[i]
            else:
                name = fake.unique.word().title() + " " + fake.word().title()

            facility_type_data = {
                "name": name,
                "description": fake.text(max_nb_chars=200),
                "is_active": random.choice([True, True, True, False]),  # 75% active
            }

            facility_type = FacilityType.objects.create(**facility_type_data)
            facility_types.append(facility_type)

            if (i + 1) % 5 == 0:
                self.stdout.write(f"Created {i + 1} facility types...")

        self.stdout.write(f"Successfully created {len(facility_types)} facility types")

        # Generate facilities
        self.stdout.write(f"Generating {facilities_count} facilities...")

        facilities = []
        facility_categories = [fc[0] for fc in Facility.FACILITY_CATEGORIES]
        operational_statuses = [os[0] for os in Facility.OPERATIONAL_STATUS]

        # Healthcare facility names
        hospital_names = [
            "General Hospital",
            "Memorial Hospital",
            "Regional Medical Center",
            "University Hospital",
            "Community Hospital",
            "Specialty Hospital",
            "Children's Hospital",
            "Women's Hospital",
            "Emergency Center",
            "Trauma Center",
            "Rehabilitation Hospital",
            "Psychiatric Hospital",
        ]

        clinic_names = [
            "Medical Clinic",
            "Family Practice",
            "Urgent Care",
            "Primary Care Center",
            "Specialty Clinic",
            "Outpatient Center",
            "Ambulatory Care",
            "Health Center",
        ]

        pharmacy_names = [
            "Community Pharmacy",
            "Hospital Pharmacy",
            "Retail Pharmacy",
            "Compounding Pharmacy",
            "Specialty Pharmacy",
            "Mail Order Pharmacy",
            "Long-term Care Pharmacy",
        ]

        for i in range(facilities_count):
            facility_type = random.choice(facility_types)
            category = random.choice(facility_categories)

            if category == "HOSPITAL":
                name = random.choice(hospital_names) + " " + fake.city()
            elif category == "CLINIC":
                name = random.choice(clinic_names) + " " + fake.city()
            elif category == "PHARMACY":
                name = random.choice(pharmacy_names) + " " + fake.city()
            else:
                name = fake.unique.company() + " " + fake.city()

            facility_data = {
                "name": name,
                "facility_type": facility_type,
                "category": category,
                "operational_status": random.choice(operational_statuses),
                "address": fake.street_address(),
                "city": fake.city(),
                "state": fake.state(),
                "postal_code": fake.postcode(),
                "country": "USA",
                "phone": fake.phone_number(),
                "email": fake.email(),
                "website": fake.url() if random.choice([True, False]) else None,
                "license_number": f"LIC{fake.unique.random_number(digits=8)}"
                if random.choice([True, False])
                else None,
                "license_expiry_date": fake.date_between(
                    start_date="today", end_date="+2y"
                )
                if random.choice([True, False])
                else None,
                "accreditation": random.choice(["JCAHO", "CARF", "AAAHC", "CMS"])
                if random.choice([True, False])
                else None,
                "bed_count": random.randint(0, 500) if category == "HOSPITAL" else 0,
                "operating_rooms": random.randint(0, 20)
                if category == "HOSPITAL"
                else 0,
                "emergency_rooms": random.randint(0, 10)
                if category == "HOSPITAL"
                else 0,
                "operating_hours": {
                    "monday": "8:00-18:00",
                    "tuesday": "8:00-18:00",
                    "wednesday": "8:00-18:00",
                    "thursday": "8:00-18:00",
                    "friday": "8:00-18:00",
                    "saturday": "9:00-17:00",
                    "sunday": "Closed",
                },
                "emergency_services": random.choice([True, False]),
                "trauma_center_level": random.choice(["I", "II", "III", "IV"])
                if random.choice([True, False])
                else None,
                "specialty_services": random.sample(
                    [
                        "Cardiology",
                        "Neurology",
                        "Oncology",
                        "Orthopedics",
                        "Pediatrics",
                    ],
                    random.randint(1, 3),
                )
                if random.choice([True, False])
                else [],
                "has_pharmacy": random.choice([True, False]),
                "has_laboratory": random.choice([True, False]),
                "has_imaging": random.choice([True, False]),
                "storage_capacity": Decimal(
                    str(random.uniform(100.0, 5000.0))
                ).quantize(Decimal("0.01"))
                if random.choice([True, False])
                else None,
                "refrigeration_capacity": Decimal(
                    str(random.uniform(10.0, 500.0))
                ).quantize(Decimal("0.01"))
                if random.choice([True, False])
                else None,
                "freezer_capacity": Decimal(str(random.uniform(5.0, 200.0))).quantize(
                    Decimal("0.01")
                )
                if random.choice([True, False])
                else None,
                "administrator_name": fake.name(),
                "administrator_phone": fake.phone_number(),
                "administrator_email": fake.email(),
                "tax_id": f"{random.randint(10, 99)}-{random.randint(1000000, 9999999)}"
                if random.choice([True, False])
                else None,
                "medicare_provider_number": f"{random.randint(100000, 999999)}"
                if random.choice([True, False])
                else None,
                "medicaid_provider_number": f"{random.randint(100000, 999999)}"
                if random.choice([True, False])
                else None,
                "latitude": Decimal(str(random.uniform(25.0, 49.0))).quantize(
                    Decimal("0.000001")
                ),
                "longitude": Decimal(str(random.uniform(-125.0, -66.0))).quantize(
                    Decimal("0.000001")
                ),
                "notes": fake.text(max_nb_chars=300)
                if random.choice([True, False])
                else None,
                "is_active": random.choice([True, True, True, False]),  # 75% active
            }

            facility = Facility.objects.create(**facility_data)
            facilities.append(facility)

            if (i + 1) % 10 == 0:
                self.stdout.write(f"Created {i + 1} facilities...")

        self.stdout.write(f"Successfully created {len(facilities)} facilities")

        # Generate facility departments
        self.stdout.write(f"Generating {departments_count} facility departments...")

        department_names = [
            "Emergency Department",
            "Intensive Care Unit",
            "Cardiology",
            "Neurology",
            "Oncology",
            "Orthopedics",
            "Pediatrics",
            "Obstetrics",
            "Gynecology",
            "Radiology",
            "Laboratory",
            "Pharmacy",
            "Rehabilitation",
            "Psychiatry",
            "Surgery",
            "Anesthesiology",
            "Pathology",
            "Dermatology",
            "Ophthalmology",
            "ENT",
            "Urology",
            "Gastroenterology",
            "Endocrinology",
            "Pulmonology",
        ]

        for i in range(departments_count):
            facility = random.choice(facilities)

            department_data = {
                "facility": facility,
                "name": random.choice(department_names),
                "description": fake.text(max_nb_chars=200),
                "department_head": fake.name(),
                "phone": fake.phone_number(),
                "email": fake.email(),
                "is_active": random.choice([True, True, True, False]),  # 75% active
            }

            FacilityDepartment.objects.create(**department_data)

            if (i + 1) % 20 == 0:
                self.stdout.write(f"Created {i + 1} departments...")

        self.stdout.write(
            f"Successfully created {departments_count} facility departments"
        )

        # Generate facility contacts
        self.stdout.write(f"Generating {contacts_count} facility contacts...")

        contact_types = [
            "PRIMARY",
            "SECONDARY",
            "EMERGENCY",
            "ADMINISTRATIVE",
            "TECHNICAL",
        ]

        for i in range(contacts_count):
            facility = random.choice(facilities)

            contact_data = {
                "facility": facility,
                "name": fake.name(),
                "title": fake.job(),
                "contact_type": random.choice(contact_types),
                "phone": fake.phone_number(),
                "email": fake.email(),
                "is_primary": random.choice([True, False]),
            }

            FacilityContact.objects.create(**contact_data)

            if (i + 1) % 30 == 0:
                self.stdout.write(f"Created {i + 1} contacts...")

        self.stdout.write(f"Successfully created {contacts_count} facility contacts")

        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                f"\n✅ Location data generation complete!\n"
                f"📊 Summary:\n"
                f"   • Facility Types: {FacilityType.objects.count()}\n"
                f"   • Facilities: {Facility.objects.count()}\n"
                f"   • Departments: {FacilityDepartment.objects.count()}\n"
                f"   • Contacts: {FacilityContact.objects.count()}\n"
                f"   • Active Facilities: {Facility.objects.filter(is_active=True).count()}\n"
                f"   • Hospitals: {Facility.objects.filter(category='HOSPITAL').count()}\n"
                f"   • Pharmacies: {Facility.objects.filter(category='PHARMACY').count()}\n"
                f"   • Emergency Services: {Facility.objects.filter(emergency_services=True).count()}"
            )
        )
