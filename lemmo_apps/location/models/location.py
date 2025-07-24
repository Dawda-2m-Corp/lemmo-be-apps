from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from core.models import UUIDModel  # type: ignore


class LocationType(UUIDModel):
    name = models.CharField(max_length=100, unique=True)
    level = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Location Type"
        verbose_name_plural = "Location Types"
        db_table = "tblLocationTypes"


class Location(MPTTModel, UUIDModel):
    name = models.CharField(max_length=100, unique=True)
    type = models.ForeignKey(
        LocationType, on_delete=models.CASCADE, related_name="locations"
    )
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        db_table = "tblLocations"

    def __str__(self):
        return self.name
