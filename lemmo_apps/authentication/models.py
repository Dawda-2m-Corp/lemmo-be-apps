from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils import timezone
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("ADMIN", "Administrator"),
        ("PHARMACIST", "Pharmacist"),
        ("NURSE", "Nurse"),
        ("DOCTOR", "Doctor"),
        ("LOGISTICS_MANAGER", "Logistics Manager"),
        ("WAREHOUSE_MANAGER", "Warehouse Manager"),
        ("SUPPLY_CHAIN_SPECIALIST", "Supply Chain Specialist"),
        ("INVENTORY_CLERK", "Inventory Clerk"),
        ("DISPATCHER", "Dispatcher"),
        ("DRIVER", "Driver"),
    ]

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(
        max_length=30, choices=ROLE_CHOICES, default="INVENTORY_CLERK"
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    employee_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    license_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Professional license number if applicable",
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.email}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_healthcare_professional(self):
        return self.role in ["PHARMACIST", "NURSE", "DOCTOR"]

    @property
    def is_logistics_staff(self):
        return self.role in [
            "LOGISTICS_MANAGER",
            "WAREHOUSE_MANAGER",
            "SUPPLY_CHAIN_SPECIALIST",
            "INVENTORY_CLERK",
            "DISPATCHER",
            "DRIVER",
        ]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]
        db_table = "tblUsers"


class UserSession(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sessions")
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "tblUserSessions"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Session for {self.user.email}"


class UserActivity(models.Model):
    ACTIVITY_TYPES = [
        ("LOGIN", "Login"),
        ("LOGOUT", "Logout"),
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
        ("VIEW", "View"),
        ("APPROVE", "Approve"),
        ("REJECT", "Reject"),
        ("DISPATCH", "Dispatch"),
        ("RECEIVE", "Receive"),
    ]

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activities")
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tblUserActivities"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.activity_type} - {self.created_at}"
