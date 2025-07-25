from django.db import models
from django.conf import settings
from core.models import UUIDModel, TimeDataStampedModel
from simple_history.models import HistoricalRecords
from lemmo_apps.location.models.facility import Facility


class Shipment(UUIDModel, TimeDataStampedModel):
    SHIPMENT_TYPES = [
        ("INBOUND", "Inbound"),
        ("OUTBOUND", "Outbound"),
        ("INTERNAL", "Internal Transfer"),
        ("EMERGENCY", "Emergency"),
        ("REGULAR", "Regular"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("ASSIGNED", "Assigned"),
        ("PICKED_UP", "Picked Up"),
        ("IN_TRANSIT", "In Transit"),
        ("DELIVERED", "Delivered"),
        ("FAILED", "Delivery Failed"),
        ("CANCELLED", "Cancelled"),
        ("RETURNED", "Returned"),
    ]

    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("NORMAL", "Normal"),
        ("HIGH", "High"),
        ("URGENT", "Urgent"),
        ("EMERGENCY", "Emergency"),
    ]

    shipment_number = models.CharField(max_length=50, unique=True)
    shipment_type = models.CharField(
        max_length=20, choices=SHIPMENT_TYPES, default="OUTBOUND"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default="NORMAL"
    )

    # Origin and destination
    origin_facility = models.ForeignKey(
        Facility, on_delete=models.CASCADE, related_name="outbound_shipments"
    )
    destination_facility = models.ForeignKey(
        Facility, on_delete=models.CASCADE, related_name="inbound_shipments"
    )

    # Healthcare specific
    requires_refrigeration = models.BooleanField(default=False)
    temperature_requirements = models.CharField(max_length=100, blank=True, null=True)
    is_hazardous = models.BooleanField(default=False)
    is_fragile = models.BooleanField(default=False)
    requires_special_handling = models.BooleanField(default=False)

    # Dimensions and weight
    total_weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Total weight in kg",
    )
    total_volume = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Total volume in cubic meters",
    )
    package_count = models.PositiveIntegerField(default=0)

    # Scheduling
    pickup_date = models.DateField(blank=True, null=True)
    pickup_time = models.TimeField(blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    delivery_time = models.TimeField(blank=True, null=True)
    actual_pickup_date = models.DateTimeField(blank=True, null=True)
    actual_delivery_date = models.DateTimeField(blank=True, null=True)

    # Assignment
    assigned_driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_shipments",
    )
    assigned_vehicle = models.ForeignKey(
        "Vehicle",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_shipments",
    )

    # Tracking
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    current_location = models.CharField(max_length=255, blank=True, null=True)
    estimated_delivery_time = models.DateTimeField(blank=True, null=True)

    # Financial
    shipping_cost = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    insurance_cost = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    total_cost = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    # Notes and metadata
    special_instructions = models.TextField(blank=True, null=True)
    delivery_notes = models.TextField(blank=True, null=True)
    failure_reason = models.TextField(blank=True, null=True)

    # Timestamps
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_shipments",
    )
    assigned_at = models.DateTimeField(blank=True, null=True)
    picked_up_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Shipment"
        verbose_name_plural = "Shipments"
        db_table = "tblShipments"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Shipment-{self.shipment_number}"

    @property
    def is_assigned(self):
        return bool(self.assigned_driver and self.assigned_vehicle)

    @property
    def is_in_transit(self):
        return self.status in ["PICKED_UP", "IN_TRANSIT"]

    @property
    def is_delivered(self):
        return self.status == "DELIVERED"

    @property
    def is_failed(self):
        return self.status == "FAILED"

    @property
    def is_cancelled(self):
        return self.status == "CANCELLED"

    @property
    def total_items(self):
        return self.items.count()

    def calculate_totals(self):
        """Calculate shipment totals"""
        total_weight = sum(item.weight for item in self.items.all() if item.weight)
        total_volume = sum(item.volume for item in self.items.all() if item.volume)
        package_count = self.items.count()

        self.total_weight = total_weight
        self.total_volume = total_volume
        self.package_count = package_count

        # Calculate total cost
        total_cost = (self.shipping_cost or 0) + (self.insurance_cost or 0)
        self.total_cost = total_cost

        self.save()


class ShipmentItem(models.Model):
    shipment = models.ForeignKey(
        Shipment, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(
        "lemmo_apps.inventory.Product", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()

    # Physical properties
    weight = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True, help_text="Weight in kg"
    )
    volume = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Volume in cubic meters",
    )
    dimensions = models.CharField(
        max_length=100, blank=True, null=True, help_text="LxWxH in cm"
    )

    # Healthcare specific
    batch_number = models.CharField(max_length=100, blank=True, null=True)
    lot_number = models.CharField(max_length=100, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    requires_refrigeration = models.BooleanField(default=False)
    temperature_requirements = models.CharField(max_length=100, blank=True, null=True)

    # Status tracking
    is_picked_up = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    quality_check_passed = models.BooleanField(default=True)
    quality_notes = models.TextField(blank=True, null=True)

    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tblShipmentItems"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.shipment.shipment_number} - {self.product.name}"

    @property
    def is_expired(self):
        from django.utils import timezone

        if not self.expiration_date:
            return False
        return self.expiration_date < timezone.now().date()

    @property
    def is_expiring_soon(self):
        from django.utils import timezone
        from datetime import timedelta

        if not self.expiration_date:
            return False
        return self.expiration_date <= (timezone.now().date() + timedelta(days=30))


class ShipmentTracking(models.Model):
    TRACKING_EVENTS = [
        ("CREATED", "Shipment Created"),
        ("ASSIGNED", "Assigned to Driver"),
        ("PICKED_UP", "Picked Up"),
        ("IN_TRANSIT", "In Transit"),
        ("OUT_FOR_DELIVERY", "Out for Delivery"),
        ("DELIVERED", "Delivered"),
        ("FAILED", "Delivery Failed"),
        ("RETURNED", "Returned"),
        ("CANCELLED", "Cancelled"),
        ("LOCATION_UPDATE", "Location Update"),
        ("DELAY", "Delay"),
        ("EXCEPTION", "Exception"),
    ]

    shipment = models.ForeignKey(
        Shipment, on_delete=models.CASCADE, related_name="tracking_events"
    )
    event_type = models.CharField(max_length=20, choices=TRACKING_EVENTS)
    event_time = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )

    # Additional data
    temperature = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Temperature in Celsius",
    )
    humidity = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Humidity percentage",
    )
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tracking_events",
    )
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "tblShipmentTracking"
        ordering = ["-event_time"]

    def __str__(self):
        return (
            f"{self.shipment.shipment_number} - {self.event_type} at {self.event_time}"
        )
