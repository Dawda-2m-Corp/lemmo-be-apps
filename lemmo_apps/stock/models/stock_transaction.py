from django.db import models
from core.models import TimeDataStampedModel, CodeModel
from simple_history.models import HistoricalRecords
from lemmo_apps.location.models.facility import Facility
from lemmo_apps.inventory.models.item import Item


class StockTransaction(models.Model):
    TRANSACTION_TYPES = [
        ("RECEIPT", "Receipt"),
        ("ISSUE", "Issue"),
        ("ADJUSTMENT", "Adjustment"),
        ("RETURN", "Return"),
        ("TRANSFER_IN", "Transfer In"),
        ("TRANSFER_OUT", "Transfer Out"),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    quantity = models.IntegerField(help_text="Use negative for issues/returns")
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    reference = models.CharField(max_length=255, null=True, blank=True)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tblStockTransactions"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.transaction_type}: {self.quantity} of {self.item} @ {self.facility}"
        )
