from core.models import TimeDataStampedModel, UUIDModel
from django.conf import settings
from django.db import models
from lemmo_apps.location.models.facility import Facility
from simple_history.models import HistoricalRecords


class Requisition(TimeDataStampedModel, UUIDModel):
    STATUS_CHOICES = [
        ("DRAFT", "Draft"),
        ("SUBMITTED", "Submitted"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("FULFILLED", "Fulfilled"),
        ("CANCELLED", "Cancelled"),
    ]

    facility = models.ForeignKey(
        Facility, on_delete=models.CASCADE, related_name="requisitions"
    )
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    request_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="DRAFT")
    comment = models.TextField(blank=True, null=True)

    history = HistoricalRecords()

    class Meta:
        db_table = "tblRequisitions"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Requisition #{self.id} from {self.facility.name}"
