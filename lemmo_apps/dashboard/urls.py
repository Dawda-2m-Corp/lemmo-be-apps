from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = (
    [
        # Dashboard URLs
        path("", views.DashboardView.as_view(), name="dashboard"),
        path("overview/", views.DashboardOverviewView.as_view(), name="overview"),
        path("analytics/", views.DashboardAnalyticsView.as_view(), name="analytics"),
        path("reports/", views.DashboardReportsView.as_view(), name="reports"),
        # Healthcare specific dashboard URLs
        path(
            "inventory-overview/",
            views.InventoryOverviewView.as_view(),
            name="inventory-overview",
        ),
        path(
            "logistics-overview/",
            views.LogisticsOverviewView.as_view(),
            name="logistics-overview",
        ),
        path(
            "supplier-overview/",
            views.SupplierOverviewView.as_view(),
            name="supplier-overview",
        ),
        path(
            "facility-overview/",
            views.FacilityOverviewView.as_view(),
            name="facility-overview",
        ),
        # Alert URLs
        path("alerts/", views.AlertsView.as_view(), name="alerts"),
        path(
            "alerts/low-stock/",
            views.LowStockAlertsView.as_view(),
            name="low-stock-alerts",
        ),
        path(
            "alerts/expiring-products/",
            views.ExpiringProductsAlertsView.as_view(),
            name="expiring-products-alerts",
        ),
        path(
            "alerts/emergency-shipments/",
            views.EmergencyShipmentsAlertsView.as_view(),
            name="emergency-shipments-alerts",
        ),
        path(
            "alerts/maintenance-due/",
            views.MaintenanceDueAlertsView.as_view(),
            name="maintenance-due-alerts",
        ),
        # Report URLs
        path(
            "reports/inventory/",
            views.InventoryReportView.as_view(),
            name="inventory-report",
        ),
        path(
            "reports/logistics/",
            views.LogisticsReportView.as_view(),
            name="logistics-report",
        ),
        path(
            "reports/supplier/",
            views.SupplierReportView.as_view(),
            name="supplier-report",
        ),
        path(
            "reports/facility/",
            views.FacilityReportView.as_view(),
            name="facility-report",
        ),
        path(
            "reports/compliance/",
            views.ComplianceReportView.as_view(),
            name="compliance-report",
        ),
    ],
)
