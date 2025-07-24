from .location import Location
from core.models import UUIDModel, CodeModel
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class FacilityType(CodeModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Health Facility Type"
        verbose_name_plural = "Health Facility Types"
        db_table = "tblHealthFacilityTypes"

    def __str__(self):
        return self.name


class Facility(UUIDModel):
    name = models.CharField(max_length=100, unique=True)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="health_facilities"
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = PhoneNumberField(blank=True)
    facility_type = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Health Facility"
        verbose_name_plural = "Health Facilities"
        db_table = "tblHealthFacilities"

    def __str__(self):
        return self.name
