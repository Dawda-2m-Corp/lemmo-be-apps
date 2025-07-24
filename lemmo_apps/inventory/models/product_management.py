from django.db import models
from core.models import TimeDataStampedModel, CodeModel
from simple_history.models import HistoricalRecords


class Batch(CodeModel, TimeDataStampedModel):
    name = models.CharField(max_length=200)
    expiry_date = models.DateField(blank=True, null=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Batch"
        verbose_name_plural = "Batches"
        ordering = ["-created_at"]
        db_table = "tblItemBatches"

    def __str__(self):
        return f"{self.name} (exp: {self.expiry_date})"
