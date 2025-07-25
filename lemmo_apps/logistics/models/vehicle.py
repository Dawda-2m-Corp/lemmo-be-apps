from django.db import models
from django.conf import settings
from core.models import UUIDModel, TimeDataStampedModel
from simple_history.models import HistoricalRecords


class Vehicle(UUIDModel, TimeDataStampedModel):
    VEHICLE_TYPES = [
        ("VAN", "Van"),
        ("TRUCK", "Truck"),
        ("REFRIGERATED_TRUCK", "Refrigerated Truck"),
        ("AMBULANCE", "Ambulance"),
        ("MOTORCYCLE", "Motorcycle"),
        ("CAR", "Car"),
        ("PICKUP", "Pickup Truck"),
        ("TRAILER", "Trailer"),
        ("OTHER", "Other"),
    ]

    VEHICLE_STATUS = [
        ("ACTIVE", "Active"),
        ("MAINTENANCE", "Under Maintenance"),
        ("OUT_OF_SERVICE", "Out of Service"),
        ("RETIRED", "Retired"),
        ("RESERVED", "Reserved"),
    ]

    FUEL_TYPES = [
        ("GASOLINE", "Gasoline"),
        ("DIESEL", "Diesel"),
        ("ELECTRIC", "Electric"),
        ("HYBRID", "Hybrid"),
        ("CNG", "Compressed Natural Gas"),
        ("LPG", "Liquefied Petroleum Gas"),
    ]

    vehicle_id = models.CharField(max_length=50, unique=True)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES, default="VAN")
    status = models.CharField(max_length=20, choices=VEHICLE_STATUS, default="ACTIVE")

    # Vehicle details
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    license_plate = models.CharField(max_length=20, unique=True)
    vin = models.CharField(
        max_length=17, blank=True, null=True, help_text="Vehicle Identification Number"
    )
    color = models.CharField(max_length=50, blank=True, null=True)

    # Capacity and specifications
    capacity_volume = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Capacity in cubic meters",
    )
    capacity_weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Capacity in kg",
    )
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPES, default="GASOLINE")
    fuel_capacity = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Fuel capacity in liters",
    )

    # Healthcare specific
    is_refrigerated = models.BooleanField(default=False)
    temperature_range = models.CharField(
        max_length=50, blank=True, null=True, help_text="Temperature range in Celsius"
    )
    has_gps_tracking = models.BooleanField(default=True)
    has_temperature_monitoring = models.BooleanField(default=False)
    has_security_system = models.BooleanField(default=False)

    # Insurance and registration
    insurance_number = models.CharField(max_length=100, blank=True, null=True)
    insurance_expiry = models.DateField(blank=True, null=True)
    registration_expiry = models.DateField(blank=True, null=True)
    inspection_expiry = models.DateField(blank=True, null=True)

    # Operational
    assigned_driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_vehicle",
    )
    home_location = models.CharField(max_length=255, blank=True, null=True)
    current_location = models.CharField(max_length=255, blank=True, null=True)

    # Financial
    purchase_date = models.DateField(blank=True, null=True)
    purchase_price = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    current_value = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )

    # Maintenance
    last_maintenance_date = models.DateField(blank=True, null=True)
    next_maintenance_date = models.DateField(blank=True, null=True)
    total_mileage = models.PositiveIntegerField(
        default=0, help_text="Total mileage in kilometers"
    )

    # Metadata
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"
        db_table = "tblVehicles"
        ordering = ["vehicle_id"]

    def __str__(self):
        return f"{self.vehicle_id} - {self.make} {self.model}"

    @property
    def is_operational(self):
        return self.status == "ACTIVE" and self.is_active

    @property
    def is_available(self):
        return self.status == "ACTIVE" and not self.assigned_driver

    @property
    def is_licensed(self):
        return bool(self.license_plate and self.registration_expiry)

    @property
    def is_insured(self):
        return bool(self.insurance_number and self.insurance_expiry)

    @property
    def is_registration_expired(self):
        from django.utils import timezone

        if not self.registration_expiry:
            return False
        return self.registration_expiry < timezone.now().date()

    @property
    def is_insurance_expired(self):
        from django.utils import timezone

        if not self.insurance_expiry:
            return False
        return self.insurance_expiry < timezone.now().date()

    @property
    def is_maintenance_due(self):
        from django.utils import timezone

        if not self.next_maintenance_date:
            return False
        return self.next_maintenance_date <= timezone.now().date()


class VehicleMaintenance(models.Model):
    MAINTENANCE_TYPES = [
        ("PREVENTIVE", "Preventive Maintenance"),
        ("CORRECTIVE", "Corrective Maintenance"),
        ("EMERGENCY", "Emergency Repair"),
        ("INSPECTION", "Inspection"),
        ("UPGRADE", "Upgrade"),
        ("OTHER", "Other"),
    ]

    STATUS_CHOICES = [
        ("SCHEDULED", "Scheduled"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]

    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="maintenance_records"
    )
    maintenance_type = models.CharField(
        max_length=20, choices=MAINTENANCE_TYPES, default="PREVENTIVE"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="SCHEDULED"
    )

    # Maintenance details
    title = models.CharField(max_length=255)
    description = models.TextField()
    scheduled_date = models.DateField()
    completed_date = models.DateField(blank=True, null=True)

    # Service provider
    service_provider = models.CharField(max_length=255, blank=True, null=True)
    service_provider_contact = models.CharField(max_length=255, blank=True, null=True)

    # Costs
    estimated_cost = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    actual_cost = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    # Mileage
    mileage_at_service = models.PositiveIntegerField(blank=True, null=True)

    # Parts and labor
    parts_used = models.JSONField(default=list, blank=True)
    labor_hours = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )

    # Quality control
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="performed_maintenance",
    )
    quality_check_passed = models.BooleanField(default=True)
    quality_notes = models.TextField(blank=True, null=True)

    # Follow-up
    next_maintenance_date = models.DateField(blank=True, null=True)
    next_maintenance_mileage = models.PositiveIntegerField(blank=True, null=True)

    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tblVehicleMaintenance"
        ordering = ["-scheduled_date"]

    def __str__(self):
        return f"{self.vehicle.vehicle_id} - {self.title}"


class VehicleDriver(models.Model):
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="driver_assignments"
    )
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vehicle_assignments",
    )
    assigned_date = models.DateField(auto_now_add=True)
    unassigned_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tblVehicleDrivers"
        ordering = ["-assigned_date"]

    def __str__(self):
        return f"{self.vehicle.vehicle_id} - {self.driver.email}"
