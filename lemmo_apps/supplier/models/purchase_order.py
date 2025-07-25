from django.db import models
from django.conf import settings
from core.models import UUIDModel, TimeDataStampedModel
from simple_history.models import HistoricalRecords
from lemmo_apps.inventory.models.product import Product


class PurchaseOrder(UUIDModel, TimeDataStampedModel):
    STATUS_CHOICES = [
        ("DRAFT", "Draft"),
        ("SUBMITTED", "Submitted"),
        ("APPROVED", "Approved"),
        ("ORDERED", "Ordered"),
        ("PARTIALLY_RECEIVED", "Partially Received"),
        ("FULLY_RECEIVED", "Fully Received"),
        ("CANCELLED", "Cancelled"),
        ("CLOSED", "Closed"),
    ]

    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("NORMAL", "Normal"),
        ("HIGH", "High"),
        ("URGENT", "Urgent"),
        ("EMERGENCY", "Emergency"),
    ]

    po_number = models.CharField(max_length=50, unique=True)
    supplier = models.ForeignKey(
        "Supplier", on_delete=models.CASCADE, related_name="purchase_orders"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="DRAFT")
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default="NORMAL"
    )

    # Order details
    order_date = models.DateField(auto_now_add=True)
    expected_delivery_date = models.DateField(blank=True, null=True)
    actual_delivery_date = models.DateField(blank=True, null=True)

    # Financial
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    shipping_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default="USD")

    # Approval workflow
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="requested_purchase_orders",
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_purchase_orders",
    )
    approval_date = models.DateTimeField(blank=True, null=True)

    # Shipping
    shipping_address = models.TextField(blank=True, null=True)
    shipping_method = models.CharField(max_length=100, blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)

    # Notes and metadata
    notes = models.TextField(blank=True, null=True)
    internal_notes = models.TextField(blank=True, null=True)
    supplier_notes = models.TextField(blank=True, null=True)

    # Timestamps
    submitted_at = models.DateTimeField(blank=True, null=True)
    ordered_at = models.DateTimeField(blank=True, null=True)
    received_at = models.DateTimeField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Purchase Order"
        verbose_name_plural = "Purchase Orders"
        db_table = "tblPurchaseOrders"
        ordering = ["-created_at"]

    def __str__(self):
        return f"PO-{self.po_number} - {self.supplier.name}"

    @property
    def is_approved(self):
        return self.status in [
            "APPROVED",
            "ORDERED",
            "PARTIALLY_RECEIVED",
            "FULLY_RECEIVED",
            "CLOSED",
        ]

    @property
    def is_received(self):
        return self.status in ["PARTIALLY_RECEIVED", "FULLY_RECEIVED", "CLOSED"]

    @property
    def is_cancelled(self):
        return self.status == "CANCELLED"

    @property
    def total_items(self):
        return self.items.count()

    @property
    def received_items(self):
        return self.items.filter(quantity_received__gt=0).count()

    def calculate_totals(self):
        """Calculate order totals"""
        subtotal = sum(item.total_price for item in self.items.all())
        self.subtotal = subtotal
        self.total_amount = (
            subtotal + self.tax_amount + self.shipping_amount - self.discount_amount
        )
        self.save()


class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(
        PurchaseOrder, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier_product_code = models.CharField(max_length=100, blank=True, null=True)

    # Quantities
    quantity_ordered = models.PositiveIntegerField()
    quantity_received = models.PositiveIntegerField(default=0)
    quantity_cancelled = models.PositiveIntegerField(default=0)

    # Pricing
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=15, decimal_places=2)

    # Delivery
    expected_delivery_date = models.DateField(blank=True, null=True)
    actual_delivery_date = models.DateField(blank=True, null=True)

    # Quality control
    quality_control_passed = models.BooleanField(default=True)
    quality_notes = models.TextField(blank=True, null=True)

    # Batch information
    batch_number = models.CharField(max_length=100, blank=True, null=True)
    lot_number = models.CharField(max_length=100, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)

    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tblPurchaseOrderItems"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.purchase_order.po_number} - {self.product.name}"

    @property
    def quantity_outstanding(self):
        return self.quantity_ordered - self.quantity_received - self.quantity_cancelled

    @property
    def is_fully_received(self):
        return self.quantity_received == self.quantity_ordered

    @property
    def is_partially_received(self):
        return 0 < self.quantity_received < self.quantity_ordered

    def save(self, *args, **kwargs):
        # Calculate total price
        self.total_price = self.quantity_ordered * self.unit_price
        super().save(*args, **kwargs)
        # Update purchase order totals
        self.purchase_order.calculate_totals()
