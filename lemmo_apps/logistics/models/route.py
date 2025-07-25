from django.db import models
from django.contrib.auth import get_user_model
from core.models import UUIDModel, TimeDataStampedModel
from lemmo_apps.location.models.facility import Facility

User = get_user_model()


class Route(UUIDModel, TimeDataStampedModel):
    ROUTE_TYPES = [
        ("DELIVERY", "Delivery Route"),
        ("PICKUP", "Pickup Route"),
        ("COMBINED", "Combined Route"),
        ("EMERGENCY", "Emergency Route"),
    ]

    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
        ("MAINTENANCE", "Under Maintenance"),
        ("PLANNED", "Planned"),
    ]

    name = models.CharField(max_length=255)
    route_type = models.CharField(
        max_length=20, choices=ROUTE_TYPES, default="DELIVERY"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")
    description = models.TextField(blank=True, null=True)

    # Route details
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    estimated_distance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Distance in kilometers",
    )
    estimated_duration = models.PositiveIntegerField(
        blank=True, null=True, help_text="Duration in minutes"
    )

    # Healthcare specific
    requires_refrigeration = models.BooleanField(default=False)
    temperature_requirements = models.CharField(max_length=100, blank=True, null=True)
    is_hazardous_route = models.BooleanField(default=False)
    requires_special_handling = models.BooleanField(default=False)

    # Assignment
    assigned_driver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_routes",
    )
    assigned_vehicle = models.ForeignKey(
        "Vehicle",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_routes",
    )

    # Scheduling
    scheduled_departure_time = models.DateTimeField(blank=True, null=True)
    scheduled_arrival_time = models.DateTimeField(blank=True, null=True)
    actual_departure_time = models.DateTimeField(blank=True, null=True)
    actual_arrival_time = models.DateTimeField(blank=True, null=True)

    # Performance
    average_completion_time = models.PositiveIntegerField(
        blank=True, null=True, help_text="Average completion time in minutes"
    )
    success_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Success rate percentage",
    )

    # Metadata
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "tblRoutes"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_route_type_display()})"

    @property
    def is_operational(self):
        return self.status == "ACTIVE" and self.is_active

    @property
    def is_assigned(self):
        return self.assigned_driver is not None and self.assigned_vehicle is not None

    @property
    def total_stops(self):
        return self.stops.count()

    @property
    def completed_stops(self):
        return self.stops.filter(status="COMPLETED").count()


class RouteStop(UUIDModel, TimeDataStampedModel):
    STOP_TYPES = [
        ("PICKUP", "Pickup"),
        ("DELIVERY", "Delivery"),
        ("REFUEL", "Refuel"),
        ("REST", "Rest"),
        ("MAINTENANCE", "Maintenance"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
        ("SKIPPED", "Skipped"),
        ("FAILED", "Failed"),
    ]

    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="stops")
    stop_type = models.CharField(max_length=20, choices=STOP_TYPES, default="DELIVERY")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    # Location
    facility = models.ForeignKey(
        Facility, on_delete=models.CASCADE, related_name="route_stops"
    )
    address = models.TextField()
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )

    # Timing
    sequence_order = models.PositiveIntegerField(
        help_text="Order of stops in the route"
    )
    estimated_arrival_time = models.DateTimeField(blank=True, null=True)
    estimated_departure_time = models.DateTimeField(blank=True, null=True)
    actual_arrival_time = models.DateTimeField(blank=True, null=True)
    actual_departure_time = models.DateTimeField(blank=True, null=True)

    # Healthcare specific
    requires_refrigeration = models.BooleanField(default=False)
    temperature_requirements = models.CharField(max_length=100, blank=True, null=True)
    is_hazardous_stop = models.BooleanField(default=False)
    requires_special_handling = models.BooleanField(default=False)

    # Instructions
    special_instructions = models.TextField(blank=True, null=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)

    # Performance
    stop_duration = models.PositiveIntegerField(
        blank=True, null=True, help_text="Duration in minutes"
    )
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "tblRouteStops"
        ordering = ["route", "sequence_order"]
        unique_together = ["route", "sequence_order"]

    def __str__(self):
        return f"{self.route.name} - Stop {self.sequence_order} ({self.facility.name})"

    @property
    def is_completed(self):
        return self.status == "COMPLETED"

    @property
    def is_pending(self):
        return self.status == "PENDING"

    @property
    def is_in_progress(self):
        return self.status == "IN_PROGRESS"


class DeliveryZone(UUIDModel, TimeDataStampedModel):
    ZONE_TYPES = [
        ("URBAN", "Urban"),
        ("SUBURBAN", "Suburban"),
        ("RURAL", "Rural"),
        ("REMOTE", "Remote"),
        ("EMERGENCY", "Emergency"),
    ]

    name = models.CharField(max_length=255)
    zone_type = models.CharField(max_length=20, choices=ZONE_TYPES, default="URBAN")
    description = models.TextField(blank=True, null=True)

    # Geographic boundaries
    center_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    center_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    radius_km = models.DecimalField(
        max_digits=8, decimal_places=2, help_text="Radius in kilometers"
    )

    # Healthcare specific
    has_emergency_services = models.BooleanField(default=False)
    has_pharmacy = models.BooleanField(default=False)
    has_hospital = models.BooleanField(default=False)
    has_laboratory = models.BooleanField(default=False)

    # Delivery constraints
    max_delivery_time_hours = models.PositiveIntegerField(
        default=24, help_text="Maximum delivery time in hours"
    )
    requires_special_vehicle = models.BooleanField(default=False)
    requires_refrigerated_delivery = models.BooleanField(default=False)

    # Performance metrics
    average_delivery_time = models.PositiveIntegerField(
        blank=True, null=True, help_text="Average delivery time in minutes"
    )
    success_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Success rate percentage",
    )

    # Assignment
    assigned_drivers = models.ManyToManyField(
        User, blank=True, related_name="assigned_delivery_zones"
    )
    assigned_vehicles = models.ManyToManyField(
        "Vehicle", blank=True, related_name="assigned_delivery_zones"
    )

    # Metadata
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "tblDeliveryZones"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_zone_type_display()})"

    @property
    def is_operational(self):
        return self.is_active

    @property
    def has_assignments(self):
        return self.assigned_drivers.exists() or self.assigned_vehicles.exists()

    @property
    def total_facilities(self):
        return self.facilities.count()
