from django.db import models
from django.conf import settings
from core.models import UUIDModel, TimeDataStampedModel
from simple_history.models import HistoricalRecords


class Supplier(UUIDModel, TimeDataStampedModel):
    SUPPLIER_TYPES = [
        ("MANUFACTURER", "Manufacturer"),
        ("DISTRIBUTOR", "Distributor"),
        ("WHOLESALER", "Wholesaler"),
        ("SPECIALTY", "Specialty Supplier"),
        ("LOCAL", "Local Supplier"),
        ("INTERNATIONAL", "International Supplier"),
    ]

    SUPPLIER_STATUS = [
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
        ("SUSPENDED", "Suspended"),
        ("BLACKLISTED", "Blacklisted"),
        ("PENDING_APPROVAL", "Pending Approval"),
    ]

    CERTIFICATION_TYPES = [
        ("FDA", "FDA Approved"),
        ("ISO_9001", "ISO 9001"),
        ("ISO_13485", "ISO 13485"),
        ("CE", "CE Marking"),
        ("GMP", "Good Manufacturing Practice"),
        ("HACCP", "HACCP"),
        ("OTHER", "Other"),
    ]

    name = models.CharField(max_length=255)
    supplier_type = models.CharField(
        max_length=20, choices=SUPPLIER_TYPES, default="DISTRIBUTOR"
    )
    status = models.CharField(
        max_length=20, choices=SUPPLIER_STATUS, default="PENDING_APPROVAL"
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

    # Business Information
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    business_license = models.CharField(max_length=100, blank=True, null=True)
    duns_number = models.CharField(
        max_length=20, blank=True, null=True, help_text="Dun & Bradstreet Number"
    )
    vendor_id = models.CharField(max_length=50, blank=True, null=True)

    # Healthcare specific
    fda_registration_number = models.CharField(max_length=50, blank=True, null=True)
    dea_registration_number = models.CharField(max_length=50, blank=True, null=True)
    certifications = models.JSONField(default=list, blank=True)
    specialties = models.JSONField(
        default=list, blank=True, help_text="Product categories they specialize in"
    )

    # Financial
    credit_limit = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True
    )
    payment_terms = models.CharField(max_length=100, blank=True, null=True)
    currency = models.CharField(max_length=3, default="USD")

    # Performance metrics
    average_delivery_time = models.PositiveIntegerField(
        blank=True, null=True, help_text="Average delivery time in days"
    )
    quality_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Quality rating 0-5",
    )
    reliability_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Reliability rating 0-5",
    )

    # Administrative
    assigned_buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_suppliers",
    )
    notes = models.TextField(blank=True, null=True)
    is_preferred = models.BooleanField(default=False)

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"
        db_table = "tblSuppliers"
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def full_address(self):
        return f"{self.address}, {self.city}, {self.state} {self.postal_code}, {self.country}"

    @property
    def is_approved(self):
        return self.status == "ACTIVE"

    @property
    def average_rating(self):
        if self.quality_rating and self.reliability_rating:
            return (self.quality_rating + self.reliability_rating) / 2
        return None


class SupplierContact(models.Model):
    CONTACT_TYPES = [
        ("SALES", "Sales Representative"),
        ("TECHNICAL", "Technical Support"),
        ("ACCOUNTING", "Accounting"),
        ("LOGISTICS", "Logistics"),
        ("QUALITY", "Quality Assurance"),
        ("REGULATORY", "Regulatory Affairs"),
        ("GENERAL", "General"),
    ]

    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, related_name="contacts"
    )
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    contact_type = models.CharField(
        max_length=20, choices=CONTACT_TYPES, default="GENERAL"
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tblSupplierContacts"
        ordering = ["-is_primary", "name"]

    def __str__(self):
        return f"{self.supplier.name} - {self.name} ({self.title})"


class SupplierRating(models.Model):
    RATING_TYPES = [
        ("QUALITY", "Quality"),
        ("DELIVERY", "Delivery"),
        ("PRICE", "Price"),
        ("SERVICE", "Customer Service"),
        ("COMMUNICATION", "Communication"),
        ("OVERALL", "Overall"),
    ]

    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, related_name="ratings"
    )
    rated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating_type = models.CharField(max_length=20, choices=RATING_TYPES)
    rating = models.PositiveIntegerField(help_text="Rating from 1-5")
    comments = models.TextField(blank=True, null=True)
    date_rated = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tblSupplierRatings"
        ordering = ["-date_rated"]
        unique_together = ["supplier", "rated_by", "rating_type"]

    def __str__(self):
        return f"{self.supplier.name} - {self.rating_type} - {self.rating}/5"
