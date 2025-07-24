from core.models import TimeDataStampedModel, CodeModel
from simple_history.models import HistoricalRecords
from django.db import models
from .product import Product
from .product_management import Batch


class Item(TimeDataStampedModel, CodeModel):
    label = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bar_code = models.TextField(blank=True, null=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="items")
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="items")
    expiry_date = models.DateField(blank=True, null=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.product.name} - {self.label} - {self.batch.name}"

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
        ordering = ["-created_at"]
        unique_together = (("label", "product", "batch"),)
        db_table = "tblProductItems"
