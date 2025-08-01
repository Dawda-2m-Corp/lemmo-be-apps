# Generated by Django 5.2.4 on 2025-07-25 21:28

import django.db.models.deletion
import mptt.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Facility",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("HOSPITAL", "Hospital"),
                            ("CLINIC", "Clinic"),
                            ("PHARMACY", "Pharmacy"),
                            ("LABORATORY", "Laboratory"),
                            ("WAREHOUSE", "Warehouse"),
                            ("DISTRIBUTION_CENTER", "Distribution Center"),
                            ("AMBULATORY_CARE", "Ambulatory Care Center"),
                            ("EMERGENCY_CENTER", "Emergency Center"),
                            ("REHABILITATION", "Rehabilitation Center"),
                            ("LONG_TERM_CARE", "Long-term Care Facility"),
                            ("HOSPICE", "Hospice"),
                            ("OTHER", "Other"),
                        ],
                        default="OTHER",
                        max_length=30,
                    ),
                ),
                (
                    "operational_status",
                    models.CharField(
                        choices=[
                            ("ACTIVE", "Active"),
                            ("INACTIVE", "Inactive"),
                            ("MAINTENANCE", "Under Maintenance"),
                            ("CONSTRUCTION", "Under Construction"),
                            ("CLOSED", "Closed"),
                        ],
                        default="ACTIVE",
                        max_length=20,
                    ),
                ),
                ("address", models.TextField()),
                ("city", models.CharField(max_length=100)),
                ("state", models.CharField(max_length=100)),
                ("postal_code", models.CharField(max_length=20)),
                ("country", models.CharField(default="USA", max_length=100)),
                ("phone", models.CharField(blank=True, max_length=20, null=True)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("website", models.URLField(blank=True, null=True)),
                (
                    "license_number",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("license_expiry_date", models.DateField(blank=True, null=True)),
                (
                    "accreditation",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "bed_count",
                    models.PositiveIntegerField(
                        default=0, help_text="Number of beds for inpatient facilities"
                    ),
                ),
                ("operating_rooms", models.PositiveIntegerField(default=0)),
                ("emergency_rooms", models.PositiveIntegerField(default=0)),
                ("operating_hours", models.JSONField(blank=True, default=dict)),
                ("emergency_services", models.BooleanField(default=False)),
                (
                    "trauma_center_level",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                ("specialty_services", models.JSONField(blank=True, default=list)),
                ("has_pharmacy", models.BooleanField(default=False)),
                ("has_laboratory", models.BooleanField(default=False)),
                ("has_imaging", models.BooleanField(default=False)),
                (
                    "storage_capacity",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text="Storage capacity in cubic meters",
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "refrigeration_capacity",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text="Refrigeration capacity in cubic meters",
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "freezer_capacity",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text="Freezer capacity in cubic meters",
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "administrator_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "administrator_phone",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                (
                    "administrator_email",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                ("tax_id", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "medicare_provider_number",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "medicaid_provider_number",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "latitude",
                    models.DecimalField(
                        blank=True, decimal_places=6, max_digits=9, null=True
                    ),
                ),
                (
                    "longitude",
                    models.DecimalField(
                        blank=True, decimal_places=6, max_digits=9, null=True
                    ),
                ),
                ("notes", models.TextField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Facility",
                "verbose_name_plural": "Facilities",
                "db_table": "tblFacilities",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="FacilityType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Facility Type",
                "verbose_name_plural": "Facility Types",
                "db_table": "tblFacilityTypes",
            },
        ),
        migrations.CreateModel(
            name="LocationType",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("level", models.PositiveIntegerField(default=0)),
            ],
            options={
                "verbose_name": "Location Type",
                "verbose_name_plural": "Location Types",
                "db_table": "tblLocationTypes",
            },
        ),
        migrations.CreateModel(
            name="FacilityContact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("title", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "contact_type",
                    models.CharField(
                        choices=[
                            ("ADMINISTRATIVE", "Administrative"),
                            ("CLINICAL", "Clinical"),
                            ("LOGISTICS", "Logistics"),
                            ("PHARMACY", "Pharmacy"),
                            ("LABORATORY", "Laboratory"),
                            ("EMERGENCY", "Emergency"),
                            ("MAINTENANCE", "Maintenance"),
                            ("SECURITY", "Security"),
                            ("OTHER", "Other"),
                        ],
                        default="ADMINISTRATIVE",
                        max_length=20,
                    ),
                ),
                ("phone", models.CharField(blank=True, max_length=20, null=True)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("is_primary", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("notes", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "facility",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contacts",
                        to="location.facility",
                    ),
                ),
            ],
            options={
                "db_table": "tblFacilityContacts",
                "ordering": ["-is_primary", "name"],
            },
        ),
        migrations.CreateModel(
            name="FacilityDepartment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "department_head",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("phone", models.CharField(blank=True, max_length=20, null=True)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "facility",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="departments",
                        to="location.facility",
                    ),
                ),
            ],
            options={
                "db_table": "tblFacilityDepartments",
                "ordering": ["name"],
            },
        ),
        migrations.AddField(
            model_name="facility",
            name="facility_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="location.facilitytype",
            ),
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("lft", models.PositiveIntegerField(editable=False)),
                ("rght", models.PositiveIntegerField(editable=False)),
                ("tree_id", models.PositiveIntegerField(db_index=True, editable=False)),
                ("level", models.PositiveIntegerField(editable=False)),
                (
                    "parent",
                    mptt.fields.TreeForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="location.location",
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="locations",
                        to="location.locationtype",
                    ),
                ),
            ],
            options={
                "verbose_name": "Location",
                "verbose_name_plural": "Locations",
                "db_table": "tblLocations",
            },
        ),
    ]
