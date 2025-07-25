from django.db import models
from django.contrib.auth import get_user_model
from core.models import UUIDModel, TimeDataStampedModel
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class Driver(UUIDModel, TimeDataStampedModel):
    LICENSE_TYPES = [
        ("CLASS_A", "Class A - Commercial Vehicle"),
        ("CLASS_B", "Class B - Medium Vehicle"),
        ("CLASS_C", "Class C - Light Vehicle"),
        ("CLASS_D", "Class D - Passenger Vehicle"),
        ("CDL", "Commercial Driver License"),
        ("HAZMAT", "Hazardous Materials"),
        ("MEDICAL", "Medical Transport"),
    ]

    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
        ("SUSPENDED", "Suspended"),
        ("ON_LEAVE", "On Leave"),
        ("TERMINATED", "Terminated"),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="driver_profile"
    )
    driver_id = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")

    # Personal information
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=20)
    emergency_contact = models.CharField(max_length=255)
    emergency_phone = models.CharField(max_length=20)

    # License information
    license_number = models.CharField(max_length=50, unique=True)
    license_type = models.CharField(
        max_length=20, choices=LICENSE_TYPES, default="CLASS_C"
    )
    license_expiry_date = models.DateField()
    license_issuing_state = models.CharField(max_length=50)

    # Healthcare specific
    has_medical_transport_certification = models.BooleanField(default=False)
    has_hazmat_certification = models.BooleanField(default=False)
    has_refrigerated_transport_certification = models.BooleanField(default=False)
    has_emergency_response_training = models.BooleanField(default=False)

    # Employment details
    hire_date = models.DateField()
    department = models.CharField(max_length=100, blank=True, null=True)
    supervisor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="supervised_drivers",
    )

    # Performance metrics
    total_deliveries = models.PositiveIntegerField(default=0)
    successful_deliveries = models.PositiveIntegerField(default=0)
    average_delivery_time = models.PositiveIntegerField(
        blank=True, null=True, help_text="Average delivery time in minutes"
    )
    customer_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Customer rating 0-5",
    )

    # Safety and compliance
    safety_score = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Safety score 0-5",
    )
    last_safety_training = models.DateField(blank=True, null=True)
    next_safety_training = models.DateField(blank=True, null=True)
    medical_exam_date = models.DateField(blank=True, null=True)
    medical_exam_expiry = models.DateField(blank=True, null=True)

    # Current assignment
    assigned_vehicle = models.ForeignKey(
        "Vehicle",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_driver",
    )
    current_location = models.CharField(max_length=255, blank=True, null=True)
    is_available = models.BooleanField(default=True)

    # Notes and metadata
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "tblDrivers"
        ordering = ["user__first_name", "user__last_name"]

    def __str__(self):
        return f"{self.user.full_name} ({self.driver_id})"

    @property
    def is_licensed(self):
        return self.license_expiry_date > timezone.now().date()

    @property
    def is_medical_certified(self):
        return (
            self.medical_exam_expiry
            and self.medical_exam_expiry > timezone.now().date()
        )

    @property
    def is_safety_certified(self):
        return (
            self.next_safety_training
            and self.next_safety_training > timezone.now().date()
        )

    @property
    def success_rate(self):
        if self.total_deliveries > 0:
            return (self.successful_deliveries / self.total_deliveries) * 100
        return 0

    @property
    def is_available_for_assignment(self):
        return (
            self.status == "ACTIVE"
            and self.is_active
            and self.is_available
            and self.is_licensed
            and self.is_medical_certified
        )


class DriverLicense(UUIDModel, TimeDataStampedModel):
    LICENSE_TYPES = [
        ("CLASS_A", "Class A - Commercial Vehicle"),
        ("CLASS_B", "Class B - Medium Vehicle"),
        ("CLASS_C", "Class C - Light Vehicle"),
        ("CLASS_D", "Class D - Passenger Vehicle"),
        ("CDL", "Commercial Driver License"),
        ("HAZMAT", "Hazardous Materials"),
        ("MEDICAL", "Medical Transport"),
    ]

    driver = models.ForeignKey(
        Driver, on_delete=models.CASCADE, related_name="licenses"
    )
    license_type = models.CharField(max_length=20, choices=LICENSE_TYPES)
    license_number = models.CharField(max_length=50)
    issuing_authority = models.CharField(max_length=100)
    issuing_state = models.CharField(max_length=50)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    is_active = models.BooleanField(default=True)

    # Healthcare specific
    allows_medical_transport = models.BooleanField(default=False)
    allows_hazmat_transport = models.BooleanField(default=False)
    allows_refrigerated_transport = models.BooleanField(default=False)

    # Restrictions
    restrictions = models.JSONField(default=list, blank=True)
    endorsements = models.JSONField(default=list, blank=True)

    # Notes
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "tblDriverLicenses"
        ordering = ["-issue_date"]

    def __str__(self):
        return f"{self.driver.user.full_name} - {self.get_license_type_display()}"

    @property
    def is_expired(self):
        return self.expiry_date < timezone.now().date()

    @property
    def is_expiring_soon(self):
        return self.expiry_date <= timezone.now().date() + timedelta(days=30)


class DriverSchedule(UUIDModel, TimeDataStampedModel):
    SCHEDULE_TYPES = [
        ("REGULAR", "Regular Schedule"),
        ("OVERTIME", "Overtime"),
        ("EMERGENCY", "Emergency"),
        ("ON_CALL", "On Call"),
        ("VACATION", "Vacation"),
        ("SICK", "Sick Leave"),
    ]

    driver = models.ForeignKey(
        Driver, on_delete=models.CASCADE, related_name="schedules"
    )
    schedule_type = models.CharField(
        max_length=20, choices=SCHEDULE_TYPES, default="REGULAR"
    )

    # Schedule details
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    # Healthcare specific
    is_emergency_available = models.BooleanField(default=False)
    is_medical_transport_available = models.BooleanField(default=False)
    is_hazmat_available = models.BooleanField(default=False)

    # Assignment
    assigned_vehicle = models.ForeignKey(
        "Vehicle",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="driver_schedules",
    )
    assigned_route = models.ForeignKey(
        "Route",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="driver_schedules",
    )

    # Status
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "tblDriverSchedules"
        ordering = ["-start_date", "start_time"]

    def __str__(self):
        return f"{self.driver.user.full_name} - {self.get_schedule_type_display()} ({self.start_date})"

    @property
    def is_current(self):
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date

    @property
    def is_upcoming(self):
        today = timezone.now().date()
        return self.start_date > today

    @property
    def is_past(self):
        today = timezone.now().date()
        return self.end_date < today
