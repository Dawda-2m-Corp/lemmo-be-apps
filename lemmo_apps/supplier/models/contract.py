from django.db import models
from django.conf import settings
from core.models import UUIDModel, TimeDataStampedModel
from simple_history.models import HistoricalRecords


class Contract(UUIDModel, TimeDataStampedModel):
    CONTRACT_TYPES = [
        ("SERVICE", "Service Contract"),
        ("SUPPLY", "Supply Contract"),
        ("MAINTENANCE", "Maintenance Contract"),
        ("LICENSE", "License Agreement"),
        ("CONSULTING", "Consulting Agreement"),
        ("FRAMEWORK", "Framework Agreement"),
    ]

    STATUS_CHOICES = [
        ("DRAFT", "Draft"),
        ("ACTIVE", "Active"),
        ("EXPIRED", "Expired"),
        ("TERMINATED", "Terminated"),
        ("RENEWED", "Renewed"),
        ("PENDING_RENEWAL", "Pending Renewal"),
    ]

    contract_number = models.CharField(max_length=50, unique=True)
    supplier = models.ForeignKey(
        "Supplier", on_delete=models.CASCADE, related_name="contracts"
    )
    contract_type = models.CharField(
        max_length=20, choices=CONTRACT_TYPES, default="SUPPLY"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="DRAFT")

    # Contract period
    start_date = models.DateField()
    end_date = models.DateField()
    renewal_date = models.DateField(blank=True, null=True)

    # Financial terms
    total_value = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True
    )
    currency = models.CharField(max_length=3, default="USD")
    payment_terms = models.CharField(max_length=100, blank=True, null=True)
    payment_schedule = models.JSONField(default=dict, blank=True)

    # Contract details
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    terms_and_conditions = models.TextField(blank=True, null=True)

    # Approval workflow
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_contracts",
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_contracts",
    )
    approval_date = models.DateTimeField(blank=True, null=True)

    # Performance metrics
    performance_score = models.DecimalField(
        max_digits=3, decimal_places=2, blank=True, null=True
    )
    compliance_score = models.DecimalField(
        max_digits=3, decimal_places=2, blank=True, null=True
    )

    # Documents
    contract_document = models.FileField(upload_to="contracts/", blank=True, null=True)
    attachments = models.JSONField(default=list, blank=True)

    # Metadata
    notes = models.TextField(blank=True, null=True)
    internal_notes = models.TextField(blank=True, null=True)

    # Timestamps
    signed_at = models.DateTimeField(blank=True, null=True)
    terminated_at = models.DateTimeField(blank=True, null=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"
        db_table = "tblContracts"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.contract_number} - {self.supplier.name}"

    @property
    def is_active(self):
        from django.utils import timezone

        today = timezone.now().date()
        return self.status == "ACTIVE" and self.start_date <= today <= self.end_date

    @property
    def is_expired(self):
        from django.utils import timezone

        return self.end_date < timezone.now().date()

    @property
    def is_approved(self):
        return self.status in ["ACTIVE", "EXPIRED", "RENEWED"]

    @property
    def days_until_expiry(self):
        from django.utils import timezone
        from datetime import timedelta

        return (self.end_date - timezone.now().date()).days

    @property
    def is_expiring_soon(self):
        return 0 <= self.days_until_expiry <= 90


class ContractTerm(models.Model):
    TERM_TYPES = [
        ("SERVICE_LEVEL", "Service Level Agreement"),
        ("QUALITY_STANDARDS", "Quality Standards"),
        ("DELIVERY_TERMS", "Delivery Terms"),
        ("PRICING", "Pricing Terms"),
        ("PAYMENT", "Payment Terms"),
        ("LIABILITY", "Liability Terms"),
        ("TERMINATION", "Termination Terms"),
        ("CONFIDENTIALITY", "Confidentiality Terms"),
        ("INTELLECTUAL_PROPERTY", "Intellectual Property"),
        ("OTHER", "Other"),
    ]

    contract = models.ForeignKey(
        Contract, on_delete=models.CASCADE, related_name="terms"
    )
    term_type = models.CharField(max_length=30, choices=TERM_TYPES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_required = models.BooleanField(default=True)
    is_compliant = models.BooleanField(default=True)
    compliance_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tblContractTerms"
        ordering = ["term_type", "title"]

    def __str__(self):
        return f"{self.contract.contract_number} - {self.title}"
