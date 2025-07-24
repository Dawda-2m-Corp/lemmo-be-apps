from django.db import models
from .requisition import Requisition
from lemmo_apps.inventory.models.item import Item


class RequisitionItem(models.Model):
    requisition = models.ForeignKey(
        Requisition, on_delete=models.CASCADE, related_name="items"
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    requested_quantity = models.PositiveIntegerField()
    approved_quantity = models.PositiveIntegerField(blank=True, null=True)
    issued_quantity = models.PositiveIntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "tblRequisitionItems"
        unique_together = ("requisition", "item")

    def __str__(self):
        return f"{self.item} x {self.requested_quantity}"
