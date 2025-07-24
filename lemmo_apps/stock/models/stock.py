from django.db import models
from core.models import TimeDataStampedModel, CodeModel
from simple_history.models import HistoricalRecords
from lemmo_apps.location.models.facility import Facility
from lemmo_apps.inventory.models.item import Item


class Stock(TimeDataStampedModel):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="stock_levels"
    )
    facility = models.ForeignKey(
        Facility, on_delete=models.CASCADE, related_name="stock_levels"
    )
    quantity = models.PositiveIntegerField(default=0)
    minimum_stock_level = models.PositiveIntegerField(default=0)
    maximum_stock_level = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("item", "facility")
        db_table = "tblStock"

    def __str__(self):
        return f"{self.item} @ {self.facility} = {self.quantity}"
