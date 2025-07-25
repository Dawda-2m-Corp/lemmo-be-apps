from django.urls import path
from . import views

app_name = "logistics"

urlpatterns = [
    # Vehicle URLs
    path("vehicles/", views.VehicleListView.as_view(), name="vehicle-list"),
    path(
        "vehicles/<uuid:pk>/", views.VehicleDetailView.as_view(), name="vehicle-detail"
    ),
    path("vehicles/create/", views.VehicleCreateView.as_view(), name="vehicle-create"),
    path(
        "vehicles/<uuid:pk>/update/",
        views.VehicleUpdateView.as_view(),
        name="vehicle-update",
    ),
    path(
        "vehicles/<uuid:pk>/delete/",
        views.VehicleDeleteView.as_view(),
        name="vehicle-delete",
    ),
    path(
        "vehicles/<uuid:pk>/assign-driver/",
        views.VehicleAssignDriverView.as_view(),
        name="vehicle-assign-driver",
    ),
    path(
        "vehicles/<uuid:pk>/unassign-driver/",
        views.VehicleUnassignDriverView.as_view(),
        name="vehicle-unassign-driver",
    ),
    # Vehicle Maintenance
    path(
        "vehicles/<uuid:vehicle_id>/maintenance/",
        views.VehicleMaintenanceListView.as_view(),
        name="vehicle-maintenance",
    ),
    path(
        "maintenance/<uuid:pk>/",
        views.VehicleMaintenanceDetailView.as_view(),
        name="maintenance-detail",
    ),
    path(
        "maintenance/create/",
        views.VehicleMaintenanceCreateView.as_view(),
        name="maintenance-create",
    ),
    path(
        "maintenance/<uuid:pk>/update/",
        views.VehicleMaintenanceUpdateView.as_view(),
        name="maintenance-update",
    ),
    path(
        "maintenance/<uuid:pk>/delete/",
        views.VehicleMaintenanceDeleteView.as_view(),
        name="maintenance-delete",
    ),
    path(
        "maintenance/<uuid:pk>/complete/",
        views.VehicleMaintenanceCompleteView.as_view(),
        name="maintenance-complete",
    ),
    # Vehicle Drivers
    path(
        "vehicles/<uuid:vehicle_id>/drivers/",
        views.VehicleDriverListView.as_view(),
        name="vehicle-drivers",
    ),
    path(
        "vehicle-drivers/<uuid:pk>/",
        views.VehicleDriverDetailView.as_view(),
        name="vehicle-driver-detail",
    ),
    path(
        "vehicle-drivers/create/",
        views.VehicleDriverCreateView.as_view(),
        name="vehicle-driver-create",
    ),
    path(
        "vehicle-drivers/<uuid:pk>/update/",
        views.VehicleDriverUpdateView.as_view(),
        name="vehicle-driver-update",
    ),
    path(
        "vehicle-drivers/<uuid:pk>/delete/",
        views.VehicleDriverDeleteView.as_view(),
        name="vehicle-driver-delete",
    ),
    # Shipment URLs
    path("shipments/", views.ShipmentListView.as_view(), name="shipment-list"),
    path(
        "shipments/<uuid:pk>/",
        views.ShipmentDetailView.as_view(),
        name="shipment-detail",
    ),
    path(
        "shipments/create/", views.ShipmentCreateView.as_view(), name="shipment-create"
    ),
    path(
        "shipments/<uuid:pk>/update/",
        views.ShipmentUpdateView.as_view(),
        name="shipment-update",
    ),
    path(
        "shipments/<uuid:pk>/delete/",
        views.ShipmentDeleteView.as_view(),
        name="shipment-delete",
    ),
    path(
        "shipments/<uuid:pk>/assign/",
        views.ShipmentAssignView.as_view(),
        name="shipment-assign",
    ),
    path(
        "shipments/<uuid:pk>/pickup/",
        views.ShipmentPickupView.as_view(),
        name="shipment-pickup",
    ),
    path(
        "shipments/<uuid:pk>/deliver/",
        views.ShipmentDeliverView.as_view(),
        name="shipment-deliver",
    ),
    path(
        "shipments/<uuid:pk>/track/",
        views.ShipmentTrackView.as_view(),
        name="shipment-track",
    ),
    # Shipment Items
    path(
        "shipments/<uuid:shipment_id>/items/",
        views.ShipmentItemListView.as_view(),
        name="shipment-items",
    ),
    path(
        "shipment-items/<uuid:pk>/",
        views.ShipmentItemDetailView.as_view(),
        name="shipment-item-detail",
    ),
    path(
        "shipment-items/create/",
        views.ShipmentItemCreateView.as_view(),
        name="shipment-item-create",
    ),
    path(
        "shipment-items/<uuid:pk>/update/",
        views.ShipmentItemUpdateView.as_view(),
        name="shipment-item-update",
    ),
    path(
        "shipment-items/<uuid:pk>/delete/",
        views.ShipmentItemDeleteView.as_view(),
        name="shipment-item-delete",
    ),
    # Shipment Tracking
    path(
        "shipments/<uuid:shipment_id>/tracking/",
        views.ShipmentTrackingListView.as_view(),
        name="shipment-tracking",
    ),
    path(
        "shipment-tracking/<uuid:pk>/",
        views.ShipmentTrackingDetailView.as_view(),
        name="tracking-detail",
    ),
    path(
        "shipment-tracking/create/",
        views.ShipmentTrackingCreateView.as_view(),
        name="tracking-create",
    ),
    path(
        "shipment-tracking/<uuid:pk>/update/",
        views.ShipmentTrackingUpdateView.as_view(),
        name="tracking-update",
    ),
    path(
        "shipment-tracking/<uuid:pk>/delete/",
        views.ShipmentTrackingDeleteView.as_view(),
        name="tracking-delete",
    ),
    # Healthcare specific URLs
    path(
        "refrigerated-vehicles/",
        views.RefrigeratedVehiclesView.as_view(),
        name="refrigerated-vehicles",
    ),
    path(
        "available-vehicles/",
        views.AvailableVehiclesView.as_view(),
        name="available-vehicles",
    ),
    path(
        "active-shipments/",
        views.ActiveShipmentsView.as_view(),
        name="active-shipments",
    ),
    path(
        "emergency-shipments/",
        views.EmergencyShipmentsView.as_view(),
        name="emergency-shipments",
    ),
    path(
        "pending-shipments/",
        views.PendingShipmentsView.as_view(),
        name="pending-shipments",
    ),
    path(
        "in-transit-shipments/",
        views.InTransitShipmentsView.as_view(),
        name="in-transit-shipments",
    ),
    # Analytics URLs
    path(
        "logistics-stats/", views.LogisticsStatsView.as_view(), name="logistics-stats"
    ),
    path("fleet-stats/", views.FleetStatsView.as_view(), name="fleet-stats"),
]
