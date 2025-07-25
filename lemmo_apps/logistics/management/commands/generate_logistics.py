from django.core.management.base import BaseCommand
from faker import Faker
from lemmo_apps.logistics.models.vehicle import (
    Vehicle,
    VehicleMaintenance,
    VehicleDriver,
)
from lemmo_apps.logistics.models.route import Route, RouteStop, DeliveryZone
from lemmo_apps.logistics.models.shipment import (
    Shipment,
    ShipmentItem,
    ShipmentTracking,
)
from lemmo_apps.logistics.models.driver import Driver, DriverLicense, DriverSchedule
from lemmo_apps.location.models.facility import Facility
from lemmo_apps.inventory.models.product import Product
from django.contrib.auth import get_user_model
from decimal import Decimal
import random
from datetime import timedelta
from django.utils import timezone

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "Generate fake logistics data for testing"

    def add_arguments(self, parser):
        parser.add_argument(
            "--vehicles",
            type=int,
            default=20,
            help="Number of vehicles to create (default: 20)",
        )
        parser.add_argument(
            "--drivers",
            type=int,
            default=15,
            help="Number of drivers to create (default: 15)",
        )
        parser.add_argument(
            "--routes",
            type=int,
            default=30,
            help="Number of routes to create (default: 30)",
        )
        parser.add_argument(
            "--shipments",
            type=int,
            default=50,
            help="Number of shipments to create (default: 50)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before generating new data",
        )

    def handle(self, *args, **options):
        vehicles_count = options["vehicles"]
        drivers_count = options["drivers"]
        routes_count = options["routes"]
        shipments_count = options["shipments"]
        clear_data = options["clear"]

        if clear_data:
            self.stdout.write("Clearing existing data...")
            ShipmentTracking.objects.all().delete()
            ShipmentItem.objects.all().delete()
            Shipment.objects.all().delete()
            RouteStop.objects.all().delete()
            Route.objects.all().delete()
            DeliveryZone.objects.all().delete()
            DriverSchedule.objects.all().delete()
            DriverLicense.objects.all().delete()
            Driver.objects.all().delete()
            VehicleMaintenance.objects.all().delete()
            VehicleDriver.objects.all().delete()
            Vehicle.objects.all().delete()

        # Get existing users and facilities for relationships
        users = list(User.objects.all())
        facilities = list(Facility.objects.all())

        if not users:
            self.stdout.write(
                self.style.ERROR("No users found. Please generate users first.")
            )
            return

        if not facilities:
            self.stdout.write(
                self.style.ERROR(
                    "No facilities found. Please generate facilities first."
                )
            )
            return

        # Generate vehicles
        self.stdout.write(f"Generating {vehicles_count} vehicles...")

        vehicles = []
        vehicle_types = [vt[0] for vt in Vehicle.VEHICLE_TYPES]
        vehicle_statuses = [vs[0] for vs in Vehicle.VEHICLE_STATUS]
        fuel_types = [ft[0] for ft in Vehicle.FUEL_TYPES]

        # Vehicle makes and models
        vehicle_makes = [
            "Ford",
            "Chevrolet",
            "Toyota",
            "Honda",
            "Nissan",
            "Mercedes-Benz",
            "BMW",
            "Volkswagen",
        ]
        vehicle_models = {
            "VAN": ["Transit", "Sprinter", "Express", "E-Series"],
            "TRUCK": ["F-150", "Silverado", "Tundra", "Titan"],
            "REFRIGERATED_TRUCK": ["Reefer", "Cold Chain", "Temperature Controlled"],
            "AMBULANCE": ["Type I", "Type II", "Type III"],
            "MOTORCYCLE": ["Harley-Davidson", "Honda", "Yamaha", "Kawasaki"],
            "CAR": ["Sedan", "SUV", "Hatchback"],
            "PICKUP": ["F-250", "Silverado 2500", "Tundra"],
            "TRAILER": ["Flatbed", "Enclosed", "Refrigerated"],
        }

        for i in range(vehicles_count):
            vehicle_type = random.choice(vehicle_types)
            make = random.choice(vehicle_makes)
            model = random.choice(vehicle_models.get(vehicle_type, ["Standard"]))

            vehicle_data = {
                "vehicle_id": f"V{fake.unique.random_number(digits=6)}",
                "vehicle_type": vehicle_type,
                "status": random.choice(vehicle_statuses),
                "make": make,
                "model": model,
                "year": random.randint(2015, 2024),
                "license_plate": f"{random.choice(['ABC', 'XYZ', 'DEF', 'GHI'])}{random.randint(100, 999)}",
                "vin": fake.unique.random_number(digits=17),
                "color": random.choice(
                    ["White", "Black", "Silver", "Blue", "Red", "Gray"]
                ),
                "capacity_volume": Decimal(str(random.uniform(10.0, 100.0))).quantize(
                    Decimal("0.01")
                )
                if random.choice([True, False])
                else None,
                "capacity_weight": Decimal(
                    str(random.uniform(1000.0, 10000.0))
                ).quantize(Decimal("0.01"))
                if random.choice([True, False])
                else None,
                "fuel_type": random.choice(fuel_types),
                "fuel_capacity": Decimal(str(random.uniform(50.0, 200.0))).quantize(
                    Decimal("0.01")
                )
                if random.choice([True, False])
                else None,
                "is_refrigerated": random.choice([True, False]),
                "temperature_range": f"{random.randint(-20, 10)}°C to {random.randint(10, 25)}°C"
                if random.choice([True, False])
                else None,
                "has_gps_tracking": random.choice(
                    [True, True, True, False]
                ),  # 75% have GPS
                "has_temperature_monitoring": random.choice([True, False]),
                "has_security_system": random.choice([True, False]),
                "insurance_number": f"INS{fake.unique.random_number(digits=8)}"
                if random.choice([True, False])
                else None,
                "insurance_expiry": fake.date_between(
                    start_date="today", end_date="+2y"
                )
                if random.choice([True, False])
                else None,
                "registration_expiry": fake.date_between(
                    start_date="today", end_date="+1y"
                )
                if random.choice([True, False])
                else None,
                "inspection_expiry": fake.date_between(
                    start_date="today", end_date="+6m"
                )
                if random.choice([True, False])
                else None,
                "home_location": fake.city(),
                "current_location": fake.city(),
                "purchase_date": fake.date_between(start_date="-5y", end_date="-1y"),
                "purchase_price": Decimal(
                    str(random.uniform(20000.0, 150000.0))
                ).quantize(Decimal("0.01"))
                if random.choice([True, False])
                else None,
                "current_value": Decimal(
                    str(random.uniform(15000.0, 120000.0))
                ).quantize(Decimal("0.01"))
                if random.choice([True, False])
                else None,
                "last_maintenance_date": fake.date_between(
                    start_date="-6m", end_date="-1m"
                )
                if random.choice([True, False])
                else None,
                "next_maintenance_date": fake.date_between(
                    start_date="today", end_date="+6m"
                )
                if random.choice([True, False])
                else None,
                "total_mileage": random.randint(1000, 100000),
                "notes": fake.text(max_nb_chars=300)
                if random.choice([True, False])
                else None,
                "is_active": random.choice([True, True, True, False]),  # 75% active
            }

            vehicle = Vehicle.objects.create(**vehicle_data)
            vehicles.append(vehicle)

            if (i + 1) % 5 == 0:
                self.stdout.write(f"Created {i + 1} vehicles...")

        self.stdout.write(f"Successfully created {len(vehicles)} vehicles")

        # Generate drivers
        self.stdout.write(f"Generating {drivers_count} drivers...")

        drivers = []
        license_types = [lt[0] for lt in Driver.LICENSE_TYPES]
        driver_statuses = [ds[0] for ds in Driver.STATUS_CHOICES]

        for i in range(drivers_count):
            user = random.choice(users)

            driver_data = {
                "user": user,
                "driver_id": f"D{fake.unique.random_number(digits=6)}",
                "status": random.choice(driver_statuses),
                "date_of_birth": fake.date_of_birth(minimum_age=21, maximum_age=65),
                "phone_number": fake.phone_number(),
                "emergency_contact": fake.name(),
                "emergency_phone": fake.phone_number(),
                "license_number": f"DL{fake.unique.random_number(digits=8)}",
                "license_type": random.choice(license_types),
                "license_expiry_date": fake.date_between(
                    start_date="today", end_date="+5y"
                ),
                "license_issuing_state": fake.state(),
                "has_medical_transport_certification": random.choice([True, False]),
                "has_hazmat_certification": random.choice([True, False]),
                "has_refrigerated_transport_certification": random.choice(
                    [True, False]
                ),
                "has_emergency_response_training": random.choice([True, False]),
                "hire_date": fake.date_between(start_date="-5y", end_date="-6m"),
                "department": random.choice(
                    ["Logistics", "Transportation", "Delivery", "Emergency Services"]
                ),
                "supervisor": random.choice(users)
                if random.choice([True, False])
                else None,
                "total_deliveries": random.randint(0, 1000),
                "successful_deliveries": random.randint(0, 950),
                "average_delivery_time": random.randint(30, 180)
                if random.choice([True, False])
                else None,
                "customer_rating": Decimal(str(random.uniform(3.0, 5.0))).quantize(
                    Decimal("0.01")
                )
                if random.choice([True, False])
                else None,
                "safety_score": Decimal(str(random.uniform(3.0, 5.0))).quantize(
                    Decimal("0.01")
                )
                if random.choice([True, False])
                else None,
                "last_safety_training": fake.date_between(
                    start_date="-1y", end_date="-1m"
                )
                if random.choice([True, False])
                else None,
                "next_safety_training": fake.date_between(
                    start_date="today", end_date="+1y"
                )
                if random.choice([True, False])
                else None,
                "medical_exam_date": fake.date_between(start_date="-1y", end_date="-1m")
                if random.choice([True, False])
                else None,
                "medical_exam_expiry": fake.date_between(
                    start_date="today", end_date="+2y"
                )
                if random.choice([True, False])
                else None,
                "assigned_vehicle": random.choice(vehicles)
                if random.choice([True, False])
                else None,
                "current_location": fake.city(),
                "is_available": random.choice(
                    [True, True, True, False]
                ),  # 75% available
                "notes": fake.text(max_nb_chars=300)
                if random.choice([True, False])
                else None,
                "is_active": random.choice([True, True, True, False]),  # 75% active
            }

            driver = Driver.objects.create(**driver_data)
            drivers.append(driver)

            if (i + 1) % 5 == 0:
                self.stdout.write(f"Created {i + 1} drivers...")

        self.stdout.write(f"Successfully created {len(drivers)} drivers")

        # Generate routes
        self.stdout.write(f"Generating {routes_count} routes...")

        routes = []
        route_types = [rt[0] for rt in Route.ROUTE_TYPES]
        route_statuses = [rs[0] for rs in Route.STATUS_CHOICES]

        for i in range(routes_count):
            route_data = {
                "name": f"Route {fake.unique.random_number(digits=4)}",
                "route_type": random.choice(route_types),
                "status": random.choice(route_statuses),
                "description": fake.text(max_nb_chars=200),
                "start_location": fake.city(),
                "end_location": fake.city(),
                "estimated_distance": Decimal(
                    str(random.uniform(10.0, 500.0))
                ).quantize(Decimal("0.01")),
                "estimated_duration": random.randint(30, 480),  # 30 minutes to 8 hours
                "requires_refrigeration": random.choice([True, False]),
                "temperature_requirements": f"{random.randint(-20, 10)}°C to {random.randint(10, 25)}°C"
                if random.choice([True, False])
                else None,
                "is_hazardous_route": random.choice([True, False]),
                "requires_special_handling": random.choice([True, False]),
                "assigned_driver": random.choice(drivers)
                if random.choice([True, False])
                else None,
                "assigned_vehicle": random.choice(vehicles)
                if random.choice([True, False])
                else None,
                "scheduled_departure_time": fake.date_time_between(
                    start_date="-1d", end_date="+7d"
                )
                if random.choice([True, False])
                else None,
                "scheduled_arrival_time": fake.date_time_between(
                    start_date="+1d", end_date="+8d"
                )
                if random.choice([True, False])
                else None,
                "average_completion_time": random.randint(60, 360)
                if random.choice([True, False])
                else None,
                "success_rate": Decimal(str(random.uniform(80.0, 99.0))).quantize(
                    Decimal("0.01")
                )
                if random.choice([True, False])
                else None,
                "notes": fake.text(max_nb_chars=300)
                if random.choice([True, False])
                else None,
                "is_active": random.choice([True, True, True, False]),  # 75% active
            }

            route = Route.objects.create(**route_data)
            routes.append(route)

            # Generate route stops
            num_stops = random.randint(2, 8)
            for j in range(num_stops):
                facility = random.choice(facilities)

                stop_data = {
                    "route": route,
                    "stop_type": random.choice(
                        ["PICKUP", "DELIVERY", "REFUEL", "REST"]
                    ),
                    "status": random.choice(
                        ["PENDING", "IN_PROGRESS", "COMPLETED", "SKIPPED"]
                    ),
                    "facility": facility,
                    "address": facility.address,
                    "latitude": facility.latitude,
                    "longitude": facility.longitude,
                    "sequence_order": j + 1,
                    "estimated_arrival_time": fake.date_time_between(
                        start_date="+1d", end_date="+7d"
                    )
                    if random.choice([True, False])
                    else None,
                    "estimated_departure_time": fake.date_time_between(
                        start_date="+1d", end_date="+7d"
                    )
                    if random.choice([True, False])
                    else None,
                    "requires_refrigeration": random.choice([True, False]),
                    "temperature_requirements": f"{random.randint(-20, 10)}°C to {random.randint(10, 25)}°C"
                    if random.choice([True, False])
                    else None,
                    "is_hazardous_stop": random.choice([True, False]),
                    "requires_special_handling": random.choice([True, False]),
                    "special_instructions": fake.text(max_nb_chars=200)
                    if random.choice([True, False])
                    else None,
                    "contact_person": fake.name(),
                    "contact_phone": fake.phone_number(),
                    "stop_duration": random.randint(15, 120)
                    if random.choice([True, False])
                    else None,
                    "notes": fake.text(max_nb_chars=200)
                    if random.choice([True, False])
                    else None,
                }

                RouteStop.objects.create(**stop_data)

            if (i + 1) % 10 == 0:
                self.stdout.write(f"Created {i + 1} routes...")

        self.stdout.write(f"Successfully created {len(routes)} routes")

        # Generate shipments
        self.stdout.write(f"Generating {shipments_count} shipments...")

        shipment_types = [st[0] for st in Shipment.SHIPMENT_TYPES]
        shipment_statuses = [ss[0] for ss in Shipment.STATUS_CHOICES]
        priorities = [p[0] for p in Shipment.PRIORITY_CHOICES]

        for i in range(shipments_count):
            origin_facility = random.choice(facilities)
            destination_facility = random.choice(facilities)

            shipment_data = {
                "shipment_number": f"SH{fake.unique.random_number(digits=8)}",
                "shipment_type": random.choice(shipment_types),
                "status": random.choice(shipment_statuses),
                "priority": random.choice(priorities),
                "origin_facility": origin_facility,
                "destination_facility": destination_facility,
                "requires_refrigeration": random.choice([True, False]),
                "temperature_requirements": f"{random.randint(-20, 10)}°C to {random.randint(10, 25)}°C"
                if random.choice([True, False])
                else None,
                "is_hazardous": random.choice([True, False]),
                "is_fragile": random.choice([True, False]),
                "requires_special_handling": random.choice([True, False]),
                "total_weight": Decimal(str(random.uniform(1.0, 1000.0))).quantize(
                    Decimal("0.01")
                )
                if random.choice([True, False])
                else None,
                "total_volume": Decimal(str(random.uniform(0.1, 100.0))).quantize(
                    Decimal("0.01")
                )
                if random.choice([True, False])
                else None,
                "package_count": random.randint(1, 50),
                "pickup_date": fake.date_between(start_date="-1m", end_date="+1m"),
                "pickup_time": fake.time(),
                "delivery_date": fake.date_between(start_date="today", end_date="+1m"),
                "delivery_time": fake.time(),
                "assigned_driver": random.choice(drivers)
                if random.choice([True, False])
                else None,
                "assigned_vehicle": random.choice(vehicles)
                if random.choice([True, False])
                else None,
                "tracking_number": f"TRK{fake.unique.random_number(digits=10)}"
                if random.choice([True, False])
                else None,
                "current_location": fake.city(),
                "estimated_delivery_time": fake.date_time_between(
                    start_date="+1d", end_date="+7d"
                )
                if random.choice([True, False])
                else None,
                "shipping_cost": Decimal(str(random.uniform(50.0, 500.0))).quantize(
                    Decimal("0.01")
                )
                if random.choice([True, False])
                else None,
                "insurance_cost": Decimal(str(random.uniform(10.0, 100.0))).quantize(
                    Decimal("0.01")
                )
                if random.choice([True, False])
                else None,
                "total_cost": Decimal(str(random.uniform(60.0, 600.0))).quantize(
                    Decimal("0.01")
                )
                if random.choice([True, False])
                else None,
                "special_instructions": fake.text(max_nb_chars=300)
                if random.choice([True, False])
                else None,
                "delivery_notes": fake.text(max_nb_chars=200)
                if random.choice([True, False])
                else None,
                "created_by": random.choice(users),
            }

            shipment = Shipment.objects.create(**shipment_data)

            # Generate shipment items
            num_items = random.randint(1, 5)
            for j in range(num_items):
                item_data = {
                    "shipment": shipment,
                    "product_name": fake.word().title(),
                    "quantity": random.randint(1, 100),
                    "unit_price": Decimal(str(random.uniform(5.0, 500.0))).quantize(
                        Decimal("0.01")
                    ),
                    "total_price": Decimal(str(random.uniform(5.0, 5000.0))).quantize(
                        Decimal("0.01")
                    ),
                    "weight_kg": Decimal(str(random.uniform(0.1, 50.0))).quantize(
                        Decimal("0.01")
                    )
                    if random.choice([True, False])
                    else None,
                    "dimensions_cm": f"{random.randint(1, 50)}x{random.randint(1, 30)}x{random.randint(1, 20)}"
                    if random.choice([True, False])
                    else None,
                    "requires_refrigeration": random.choice([True, False]),
                    "is_hazardous": random.choice([True, False]),
                    "is_fragile": random.choice([True, False]),
                    "special_handling_instructions": fake.text(max_nb_chars=200)
                    if random.choice([True, False])
                    else None,
                    "batch_number": f"B{fake.unique.random_number(digits=6)}"
                    if random.choice([True, False])
                    else None,
                    "expiration_date": fake.date_between(
                        start_date="today", end_date="+2y"
                    )
                    if random.choice([True, False])
                    else None,
                    "notes": fake.text(max_nb_chars=200)
                    if random.choice([True, False])
                    else None,
                }

                ShipmentItem.objects.create(**item_data)

            # Generate shipment tracking events
            num_events = random.randint(1, 5)
            event_types = [
                "PICKED_UP",
                "IN_TRANSIT",
                "DELIVERED",
                "DELAYED",
                "OUT_FOR_DELIVERY",
            ]

            for j in range(num_events):
                tracking_data = {
                    "shipment": shipment,
                    "event_type": random.choice(event_types),
                    "location": fake.city(),
                    "description": fake.text(max_nb_chars=200),
                    "metadata": {
                        "temperature": random.randint(-20, 25)
                        if random.choice([True, False])
                        else None,
                        "humidity": random.randint(30, 80)
                        if random.choice([True, False])
                        else None,
                        "driver_notes": fake.text(max_nb_chars=100)
                        if random.choice([True, False])
                        else None,
                    },
                }

                ShipmentTracking.objects.create(**tracking_data)

            if (i + 1) % 10 == 0:
                self.stdout.write(f"Created {i + 1} shipments...")

        self.stdout.write(f"Successfully created {len(routes)} shipments")

        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                f"\n✅ Logistics data generation complete!\n"
                f"📊 Summary:\n"
                f"   • Vehicles: {Vehicle.objects.count()}\n"
                f"   • Drivers: {Driver.objects.count()}\n"
                f"   • Routes: {Route.objects.count()}\n"
                f"   • Route Stops: {RouteStop.objects.count()}\n"
                f"   • Shipments: {Shipment.objects.count()}\n"
                f"   • Shipment Items: {ShipmentItem.objects.count()}\n"
                f"   • Shipment Tracking: {ShipmentTracking.objects.count()}\n"
                f"   • Active Vehicles: {Vehicle.objects.filter(status='ACTIVE').count()}\n"
                f"   • Refrigerated Vehicles: {Vehicle.objects.filter(is_refrigerated=True).count()}\n"
                f"   • Available Drivers: {Driver.objects.filter(is_available=True).count()}\n"
                f"   • Emergency Shipments: {Shipment.objects.filter(priority='EMERGENCY').count()}"
            )
        )
