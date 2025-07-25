from django.db import models
from core.models import UUIDModel


class FacilityType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Facility Type"
        verbose_name_plural = "Facility Types"
        db_table = "tblFacilityTypes"

    def __str__(self):
        return self.name


class Facility(UUIDModel):
    FACILITY_CATEGORIES = [
        ("HOSPITAL", "Hospital"),
        ("CLINIC", "Clinic"),
        ("PHARMACY", "Pharmacy"),
        ("LABORATORY", "Laboratory"),
        ("WAREHOUSE", "Warehouse"),
        ("DISTRIBUTION_CENTER", "Distribution Center"),
        ("AMBULATORY_CARE", "Ambulatory Care Center"),
        ("EMERGENCY_CENTER", "Emergency Center"),
        ("REHABILITATION", "Rehabilitation Center"),
        ("LONG_TERM_CARE", "Long-term Care Facility"),
        ("HOSPICE", "Hospice"),
        ("OTHER", "Other"),
    ]

    OPERATIONAL_STATUS = [
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
        ("MAINTENANCE", "Under Maintenance"),
        ("CONSTRUCTION", "Under Construction"),
        ("CLOSED", "Closed"),
    ]

    name = models.CharField(max_length=255)
    facility_type = models.ForeignKey(
        FacilityType, on_delete=models.SET_NULL, null=True, blank=True
    )
    category = models.CharField(
        max_length=30, choices=FACILITY_CATEGORIES, default="OTHER"
    )
    operational_status = models.CharField(
        max_length=20, choices=OPERATIONAL_STATUS, default="ACTIVE"
    )

    # Contact Information
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="USA")
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    # Healthcare specific fields
    license_number = models.CharField(max_length=100, blank=True, null=True)
    license_expiry_date = models.DateField(blank=True, null=True)
    accreditation = models.CharField(max_length=255, blank=True, null=True)
    bed_count = models.PositiveIntegerField(
        default=0, help_text="Number of beds for inpatient facilities"
    )
    operating_rooms = models.PositiveIntegerField(default=0)
    emergency_rooms = models.PositiveIntegerField(default=0)

    # Operational details
    operating_hours = models.JSONField(default=dict, blank=True)
    emergency_services = models.BooleanField(default=False)
    trauma_center_level = models.CharField(max_length=20, blank=True, null=True)
    specialty_services = models.JSONField(default=list, blank=True)

    # Logistics and storage
    has_pharmacy = models.BooleanField(default=False)
    has_laboratory = models.BooleanField(default=False)
    has_imaging = models.BooleanField(default=False)
    storage_capacity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Storage capacity in cubic meters",
    )
    refrigeration_capacity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Refrigeration capacity in cubic meters",
    )
    freezer_capacity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Freezer capacity in cubic meters",
    )

    # Administrative
    administrator_name = models.CharField(max_length=255, blank=True, null=True)
    administrator_phone = models.CharField(max_length=20, blank=True, null=True)
    administrator_email = models.EmailField(blank=True, null=True)

    # Financial
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    medicare_provider_number = models.CharField(max_length=50, blank=True, null=True)
    medicaid_provider_number = models.CharField(max_length=50, blank=True, null=True)

    # Geographic
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )

    # Metadata
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Facility"
        verbose_name_plural = "Facilities"
        db_table = "tblFacilities"
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def full_address(self):
        return f"{self.address}, {self.city}, {self.state} {self.postal_code}, {self.country}"

    @property
    def is_licensed(self):
        return bool(self.license_number and self.license_expiry_date)

    @property
    def is_license_expired(self):
        from django.utils import timezone

        if not self.license_expiry_date:
            return False
        return self.license_expiry_date < timezone.now().date()

    @property
    def is_operational(self):
        return self.operational_status == "ACTIVE" and self.is_active


class FacilityDepartment(models.Model):
    facility = models.ForeignKey(
        Facility, on_delete=models.CASCADE, related_name="departments"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    department_head = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tblFacilityDepartments"
        ordering = ["name"]

    def __str__(self):
        return f"{self.facility.name} - {self.name}"


class FacilityContact(models.Model):
    CONTACT_TYPES = [
        ("ADMINISTRATIVE", "Administrative"),
        ("CLINICAL", "Clinical"),
        ("LOGISTICS", "Logistics"),
        ("PHARMACY", "Pharmacy"),
        ("LABORATORY", "Laboratory"),
        ("EMERGENCY", "Emergency"),
        ("MAINTENANCE", "Maintenance"),
        ("SECURITY", "Security"),
        ("OTHER", "Other"),
    ]

    facility = models.ForeignKey(
        Facility, on_delete=models.CASCADE, related_name="contacts"
    )
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    contact_type = models.CharField(
        max_length=20, choices=CONTACT_TYPES, default="ADMINISTRATIVE"
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tblFacilityContacts"
        ordering = ["-is_primary", "name"]

    def __str__(self):
        return f"{self.facility.name} - {self.name} ({self.title})"
