from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, F, Count, Sum
from django.utils import timezone
from datetime import timedelta

from lemmo_apps.inventory.models.product import Product, ProductBatch
from lemmo_apps.location.models.facility import Facility
from lemmo_apps.stock.models.stock import Stock
from lemmo_apps.authentication.models import User, UserActivity


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get basic statistics
        total_products = Product.objects.count()
        total_facilities = Facility.objects.count()
        total_users = User.objects.count()

        # Get low stock alerts
        low_stock_products = Product.objects.filter(
            stock_quantity__lte=F("min_stock_level")
        ).count()
        out_of_stock_products = Product.objects.filter(stock_quantity=0).count()

        # Get expired batches
        expired_batches = ProductBatch.objects.filter(
            expiration_date__lt=timezone.now().date()
        ).count()

        # Get recent activity
        recent_activities = UserActivity.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).count()

        context.update(
            {
                "total_products": total_products,
                "total_facilities": total_facilities,
                "total_users": total_users,
                "low_stock_products": low_stock_products,
                "out_of_stock_products": out_of_stock_products,
                "expired_batches": expired_batches,
                "recent_activities": recent_activities,
            }
        )

        return context


class DashboardOverviewView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/overview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get overview statistics
        active_products = Product.objects.filter(is_active=True).count()
        active_facilities = Facility.objects.filter(operational_status="ACTIVE").count()
        active_users = User.objects.filter(is_active=True).count()

        # Get healthcare specific stats
        healthcare_professionals = User.objects.filter(
            role__in=["PHARMACIST", "NURSE", "DOCTOR"]
        ).count()

        logistics_staff = User.objects.filter(
            role__in=[
                "LOGISTICS_MANAGER",
                "WAREHOUSE_MANAGER",
                "SUPPLY_CHAIN_SPECIALIST",
                "INVENTORY_CLERK",
                "DISPATCHER",
                "DRIVER",
            ]
        ).count()

        context.update(
            {
                "active_products": active_products,
                "active_facilities": active_facilities,
                "active_users": active_users,
                "healthcare_professionals": healthcare_professionals,
                "logistics_staff": logistics_staff,
            }
        )

        return context


class DashboardAnalyticsView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/analytics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get analytics data
        product_type_stats = Product.objects.values("product_type").annotate(
            count=Count("product_type")
        )
        facility_category_stats = Facility.objects.values("category").annotate(
            count=Count("category")
        )
        user_role_stats = User.objects.values("role").annotate(count=Count("role"))

        # Get time-based analytics
        recent_products = Product.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).count()

        recent_facilities = Facility.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).count()

        context.update(
            {
                "product_type_stats": product_type_stats,
                "facility_category_stats": facility_category_stats,
                "user_role_stats": user_role_stats,
                "recent_products": recent_products,
                "recent_facilities": recent_facilities,
            }
        )

        return context


class DashboardReportsView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/reports.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get report data
        total_stock_value = (
            Product.objects.aggregate(
                total_value=Sum(F("price") * F("stock_quantity"))
            )["total_value"]
            or 0
        )

        low_stock_value = (
            Product.objects.filter(stock_quantity__lte=F("min_stock_level")).aggregate(
                low_stock_value=Sum(F("price") * F("stock_quantity"))
            )["low_stock_value"]
            or 0
        )

        context.update(
            {
                "total_stock_value": total_stock_value,
                "low_stock_value": low_stock_value,
            }
        )

        return context


class InventoryOverviewView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/inventory_overview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get inventory statistics
        total_products = Product.objects.count()
        active_products = Product.objects.filter(is_active=True).count()
        low_stock_products = Product.objects.filter(
            stock_quantity__lte=F("min_stock_level")
        ).count()
        out_of_stock_products = Product.objects.filter(stock_quantity=0).count()

        # Get batch statistics
        total_batches = ProductBatch.objects.count()
        expired_batches = ProductBatch.objects.filter(
            expiration_date__lt=timezone.now().date()
        ).count()

        # Get expiring soon batches
        expiry_threshold = timezone.now().date() + timedelta(days=30)
        expiring_soon_batches = ProductBatch.objects.filter(
            expiration_date__lte=expiry_threshold,
            expiration_date__gte=timezone.now().date(),
        ).count()

        context.update(
            {
                "total_products": total_products,
                "active_products": active_products,
                "low_stock_products": low_stock_products,
                "out_of_stock_products": out_of_stock_products,
                "total_batches": total_batches,
                "expired_batches": expired_batches,
                "expiring_soon_batches": expiring_soon_batches,
            }
        )

        return context


class LogisticsOverviewView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/logistics_overview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get logistics statistics
        total_vehicles = 0  # Would need to import Vehicle model
        active_vehicles = 0
        total_drivers = 0  # Would need to import Driver model
        active_drivers = 0

        context.update(
            {
                "total_vehicles": total_vehicles,
                "active_vehicles": active_vehicles,
                "total_drivers": total_drivers,
                "active_drivers": active_drivers,
            }
        )

        return context


class SupplierOverviewView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/supplier_overview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get supplier statistics
        total_suppliers = 0  # Would need to import Supplier model
        active_suppliers = 0
        preferred_suppliers = 0

        context.update(
            {
                "total_suppliers": total_suppliers,
                "active_suppliers": active_suppliers,
                "preferred_suppliers": preferred_suppliers,
            }
        )

        return context


class FacilityOverviewView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/facility_overview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get facility statistics
        total_facilities = Facility.objects.count()
        active_facilities = Facility.objects.filter(operational_status="ACTIVE").count()

        # Get facility type distribution
        facility_type_stats = Facility.objects.values("facility_type__name").annotate(
            count=Count("facility_type")
        )

        # Get category distribution
        category_stats = Facility.objects.values("category").annotate(
            count=Count("category")
        )

        context.update(
            {
                "total_facilities": total_facilities,
                "active_facilities": active_facilities,
                "facility_type_stats": facility_type_stats,
                "category_stats": category_stats,
            }
        )

        return context


class AlertsView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/alerts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all alerts
        low_stock_products = Product.objects.filter(
            stock_quantity__lte=F("min_stock_level")
        )
        out_of_stock_products = Product.objects.filter(stock_quantity=0)
        expired_batches = ProductBatch.objects.filter(
            expiration_date__lt=timezone.now().date()
        )

        context.update(
            {
                "low_stock_products": low_stock_products,
                "out_of_stock_products": out_of_stock_products,
                "expired_batches": expired_batches,
            }
        )

        return context


class LowStockAlertsView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "dashboard/low_stock_alerts.html"
    context_object_name = "low_stock_products"

    def get_queryset(self):
        return Product.objects.filter(stock_quantity__lte=F("min_stock_level"))


class ExpiringProductsAlertsView(LoginRequiredMixin, ListView):
    model = ProductBatch
    template_name = "dashboard/expiring_products_alerts.html"
    context_object_name = "expiring_batches"

    def get_queryset(self):
        expiry_threshold = timezone.now().date() + timedelta(days=30)
        return ProductBatch.objects.filter(
            expiration_date__lte=expiry_threshold,
            expiration_date__gte=timezone.now().date(),
        )


class EmergencyShipmentsAlertsView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/emergency_shipments_alerts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # This would need to be implemented based on your shipment model
        # For now, returning empty context
        context.update(
            {
                "emergency_shipments": [],
            }
        )

        return context


class MaintenanceDueAlertsView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/maintenance_due_alerts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # This would need to be implemented based on your maintenance model
        # For now, returning empty context
        context.update(
            {
                "maintenance_due_items": [],
            }
        )

        return context


class InventoryReportView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/inventory_report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get inventory report data
        total_products = Product.objects.count()
        total_stock_value = (
            Product.objects.aggregate(
                total_value=Sum(F("price") * F("stock_quantity"))
            )["total_value"]
            or 0
        )

        # Get product type distribution
        product_type_stats = Product.objects.values("product_type").annotate(
            count=Count("product_type"),
            total_value=Sum(F("price") * F("stock_quantity")),
        )

        context.update(
            {
                "total_products": total_products,
                "total_stock_value": total_stock_value,
                "product_type_stats": product_type_stats,
            }
        )

        return context
