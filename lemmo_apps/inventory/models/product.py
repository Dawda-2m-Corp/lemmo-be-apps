from django.db import models
from simple_history.models import HistoricalRecords
from core.models import CodeModel


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"
        db_table = "tblProductCategories"

    def __str__(self):
        return self.name


class Product(CodeModel):
    PRODUCT_TYPES = [
        ("MEDICATION", "Medication"),
        ("MEDICAL_SUPPLY", "Medical Supply"),
        ("EQUIPMENT", "Equipment"),
        ("CONSUMABLE", "Consumable"),
        ("VACCINE", "Vaccine"),
        ("DIAGNOSTIC", "Diagnostic"),
        ("NUTRITIONAL", "Nutritional"),
        ("OTHER", "Other"),
    ]

    STORAGE_TYPES = [
        ("ROOM_TEMP", "Room Temperature"),
        ("REFRIGERATED", "Refrigerated (2-8°C)"),
        ("FROZEN", "Frozen (-20°C)"),
        ("ULTRA_COLD", "Ultra Cold (-70°C)"),
        ("CONTROLLED", "Controlled Temperature"),
    ]

    CONTROLLED_SUBSTANCE_TYPES = [
        ("NONE", "Not Controlled"),
        ("SCHEDULE_I", "Schedule I"),
        ("SCHEDULE_II", "Schedule II"),
        ("SCHEDULE_III", "Schedule III"),
        ("SCHEDULE_IV", "Schedule IV"),
        ("SCHEDULE_V", "Schedule V"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True, blank=True
    )
    product_type = models.CharField(
        max_length=20, choices=PRODUCT_TYPES, default="OTHER"
    )
    unit_of_measure = models.CharField(
        max_length=50, help_text="e.g., tablets, vials, units"
    )
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)

    # Healthcare specific fields
    generic_name = models.CharField(max_length=255, blank=True, null=True)
    brand_name = models.CharField(max_length=255, blank=True, null=True)
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    ndc_code = models.CharField(
        max_length=20, blank=True, null=True, help_text="National Drug Code"
    )
    rx_required = models.BooleanField(default=False)
    controlled_substance = models.CharField(
        max_length=20, choices=CONTROLLED_SUBSTANCE_TYPES, default="NONE"
    )
    storage_type = models.CharField(
        max_length=20, choices=STORAGE_TYPES, default="ROOM_TEMP"
    )
    storage_notes = models.TextField(blank=True, null=True)
    expiration_date_required = models.BooleanField(default=True)
    lot_number_required = models.BooleanField(default=True)
    min_stock_level = models.PositiveIntegerField(default=0)
    max_stock_level = models.PositiveIntegerField(default=1000)
    reorder_point = models.PositiveIntegerField(default=10)

    # Regulatory information
    fda_approved = models.BooleanField(default=False)
    fda_approval_date = models.DateField(blank=True, null=True)
    requires_prescription = models.BooleanField(default=False)
    requires_special_handling = models.BooleanField(default=False)
    hazardous_material = models.BooleanField(default=False)
    temperature_sensitive = models.BooleanField(default=False)

    # Dimensions and weight for logistics
    weight_grams = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    dimensions_cm = models.CharField(
        max_length=50, blank=True, null=True, help_text="LxWxH in cm"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.reorder_point

    @property
    def is_out_of_stock(self):
        return self.stock_quantity == 0

    @property
    def is_overstocked(self):
        return self.stock_quantity > self.max_stock_level

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        db_table = "tblProducts"
        ordering = ["name"]


class ProductBatch(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="batches"
    )
    batch_number = models.CharField(max_length=100, unique=True)
    lot_number = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.PositiveIntegerField()
    remaining_quantity = models.PositiveIntegerField()
    manufacturing_date = models.DateField()
    expiration_date = models.DateField()
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.CharField(max_length=255, blank=True, null=True)
    supplier_batch_number = models.CharField(max_length=100, blank=True, null=True)
    quality_control_passed = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Product Batch"
        verbose_name_plural = "Product Batches"
        db_table = "tblProductBatches"
        ordering = ["-expiration_date"]

    def __str__(self):
        return f"{self.product.name} - Batch {self.batch_number}"

    @property
    def is_expired(self):
        from django.utils import timezone

        return self.expiration_date < timezone.now().date()

    @property
    def is_expiring_soon(self):
        from django.utils import timezone
        from datetime import timedelta

        return self.expiration_date <= (timezone.now().date() + timedelta(days=30))


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="product_images/")
    caption = models.CharField(max_length=255, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tblProductImages"
        ordering = ["-is_primary", "created_at"]

    def __str__(self):
        return f"Image for {self.product.name}"
