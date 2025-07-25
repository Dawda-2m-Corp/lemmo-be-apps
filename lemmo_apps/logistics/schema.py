import graphene
from graphene_django import DjangoObjectType
from .models.vehicle import Vehicle, VehicleMaintenance, VehicleDriver
from .models.shipment import Shipment, ShipmentItem, ShipmentTracking


class VehicleType(DjangoObjectType):
    class Meta:
        model = Vehicle
        fields = "__all__"


class VehicleMaintenanceType(DjangoObjectType):
    class Meta:
        model = VehicleMaintenance
        fields = "__all__"


class VehicleDriverType(DjangoObjectType):
    class Meta:
        model = VehicleDriver
        fields = "__all__"


class ShipmentType(DjangoObjectType):
    class Meta:
        model = Shipment
        fields = "__all__"


class ShipmentItemType(DjangoObjectType):
    class Meta:
        model = ShipmentItem
        fields = "__all__"


class ShipmentTrackingType(DjangoObjectType):
    class Meta:
        model = ShipmentTracking
        fields = "__all__"


class Query(graphene.ObjectType):
    # Vehicle queries
    vehicles = graphene.List(
        VehicleType,
        vehicle_type=graphene.String(),
        status=graphene.String(),
        is_active=graphene.Boolean(),
        is_refrigerated=graphene.Boolean(),
        has_gps_tracking=graphene.Boolean(),
        assigned_driver=graphene.UUID(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )

    vehicle = graphene.Field(VehicleType, id=graphene.UUID(required=True))

    vehicle_by_id = graphene.Field(
        VehicleType, vehicle_id=graphene.String(required=True)
    )

    # Vehicle maintenance queries
    vehicle_maintenance = graphene.List(
        VehicleMaintenanceType,
        vehicle_id=graphene.UUID(),
        maintenance_type=graphene.String(),
        status=graphene.String(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )

    # Vehicle driver queries
    vehicle_drivers = graphene.List(
        VehicleDriverType,
        vehicle_id=graphene.UUID(),
        driver_id=graphene.UUID(),
        is_active=graphene.Boolean(),
    )

    # Shipment queries
    shipments = graphene.List(
        ShipmentType,
        shipment_type=graphene.String(),
        status=graphene.String(),
        priority=graphene.String(),
        origin_facility=graphene.UUID(),
        destination_facility=graphene.UUID(),
        assigned_driver=graphene.UUID(),
        assigned_vehicle=graphene.UUID(),
        requires_refrigeration=graphene.Boolean(),
        is_hazardous=graphene.Boolean(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )

    shipment = graphene.Field(ShipmentType, id=graphene.UUID(required=True))

    shipment_by_number = graphene.Field(
        ShipmentType, shipment_number=graphene.String(required=True)
    )

    # Shipment item queries
    shipment_items = graphene.List(
        ShipmentItemType,
        shipment_id=graphene.UUID(),
        product_id=graphene.UUID(),
        is_delivered=graphene.Boolean(),
        quality_check_passed=graphene.Boolean(),
    )

    # Shipment tracking queries
    shipment_tracking = graphene.List(
        ShipmentTrackingType,
        shipment_id=graphene.UUID(),
        event_type=graphene.String(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )

    # Healthcare specific queries
    refrigerated_vehicles = graphene.List(VehicleType)
    available_vehicles = graphene.List(VehicleType)
    active_shipments = graphene.List(ShipmentType)
    emergency_shipments = graphene.List(ShipmentType)
    pending_shipments = graphene.List(ShipmentType)
    in_transit_shipments = graphene.List(ShipmentType)

    # Dashboard statistics
    logistics_stats = graphene.JSONString()
    fleet_stats = graphene.JSONString()

    def resolve_vehicles(
        self,
        info,
        vehicle_type=None,
        status=None,
        is_active=None,
        is_refrigerated=None,
        has_gps_tracking=None,
        assigned_driver=None,
        limit=None,
        offset=None,
    ):
        queryset = Vehicle.objects.all()

        if vehicle_type:
            queryset = queryset.filter(vehicle_type=vehicle_type)

        if status:
            queryset = queryset.filter(status=status)

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        if is_refrigerated is not None:
            queryset = queryset.filter(is_refrigerated=is_refrigerated)

        if has_gps_tracking is not None:
            queryset = queryset.filter(has_gps_tracking=has_gps_tracking)

        if assigned_driver:
            queryset = queryset.filter(assigned_driver_id=assigned_driver)

        if offset:
            queryset = queryset[offset:]

        if limit:
            queryset = queryset[:limit]

        return queryset

    def resolve_vehicle(self, info, id):
        return Vehicle.objects.get(id=id)

    def resolve_vehicle_by_id(self, info, vehicle_id):
        return Vehicle.objects.get(vehicle_id=vehicle_id)

    def resolve_vehicle_maintenance(
        self,
        info,
        vehicle_id=None,
        maintenance_type=None,
        status=None,
        limit=None,
        offset=None,
    ):
        queryset = VehicleMaintenance.objects.all()

        if vehicle_id:
            queryset = queryset.filter(vehicle_id=vehicle_id)

        if maintenance_type:
            queryset = queryset.filter(maintenance_type=maintenance_type)

        if status:
            queryset = queryset.filter(status=status)

        if offset:
            queryset = queryset[offset:]

        if limit:
            queryset = queryset[:limit]

        return queryset

    def resolve_vehicle_drivers(
        self, info, vehicle_id=None, driver_id=None, is_active=None
    ):
        queryset = VehicleDriver.objects.all()

        if vehicle_id:
            queryset = queryset.filter(vehicle_id=vehicle_id)

        if driver_id:
            queryset = queryset.filter(driver_id=driver_id)

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        return queryset

    def resolve_shipments(
        self,
        info,
        shipment_type=None,
        status=None,
        priority=None,
        origin_facility=None,
        destination_facility=None,
        assigned_driver=None,
        assigned_vehicle=None,
        requires_refrigeration=None,
        is_hazardous=None,
        limit=None,
        offset=None,
    ):
        queryset = Shipment.objects.all()

        if shipment_type:
            queryset = queryset.filter(shipment_type=shipment_type)

        if status:
            queryset = queryset.filter(status=status)

        if priority:
            queryset = queryset.filter(priority=priority)

        if origin_facility:
            queryset = queryset.filter(origin_facility_id=origin_facility)

        if destination_facility:
            queryset = queryset.filter(destination_facility_id=destination_facility)

        if assigned_driver:
            queryset = queryset.filter(assigned_driver_id=assigned_driver)

        if assigned_vehicle:
            queryset = queryset.filter(assigned_vehicle_id=assigned_vehicle)

        if requires_refrigeration is not None:
            queryset = queryset.filter(requires_refrigeration=requires_refrigeration)

        if is_hazardous is not None:
            queryset = queryset.filter(is_hazardous=is_hazardous)

        if offset:
            queryset = queryset[offset:]

        if limit:
            queryset = queryset[:limit]

        return queryset

    def resolve_shipment(self, info, id):
        return Shipment.objects.get(id=id)

    def resolve_shipment_by_number(self, info, shipment_number):
        return Shipment.objects.get(shipment_number=shipment_number)

    def resolve_shipment_items(
        self,
        info,
        shipment_id=None,
        product_id=None,
        is_delivered=None,
        quality_check_passed=None,
    ):
        queryset = ShipmentItem.objects.all()

        if shipment_id:
            queryset = queryset.filter(shipment_id=shipment_id)

        if product_id:
            queryset = queryset.filter(product_id=product_id)

        if is_delivered is not None:
            queryset = queryset.filter(is_delivered=is_delivered)

        if quality_check_passed is not None:
            queryset = queryset.filter(quality_check_passed=quality_check_passed)

        return queryset

    def resolve_shipment_tracking(
        self, info, shipment_id=None, event_type=None, limit=None, offset=None
    ):
        queryset = ShipmentTracking.objects.all()

        if shipment_id:
            queryset = queryset.filter(shipment_id=shipment_id)

        if event_type:
            queryset = queryset.filter(event_type=event_type)

        if offset:
            queryset = queryset[offset:]

        if limit:
            queryset = queryset[:limit]

        return queryset

    def resolve_refrigerated_vehicles(self, info):
        return Vehicle.objects.filter(is_refrigerated=True, is_active=True)

    def resolve_available_vehicles(self, info):
        return Vehicle.objects.filter(status="ACTIVE", assigned_driver__isnull=True)

    def resolve_active_shipments(self, info):
        return Shipment.objects.filter(
            status__in=["PENDING", "ASSIGNED", "PICKED_UP", "IN_TRANSIT"]
        )

    def resolve_emergency_shipments(self, info):
        return Shipment.objects.filter(priority="EMERGENCY")

    def resolve_pending_shipments(self, info):
        return Shipment.objects.filter(status="PENDING")

    def resolve_in_transit_shipments(self, info):
        return Shipment.objects.filter(status__in=["PICKED_UP", "IN_TRANSIT"])

    def resolve_logistics_stats(self, info):
        from django.db.models import Count, Sum
        from django.utils import timezone
        from datetime import timedelta

        # Vehicle stats
        total_vehicles = Vehicle.objects.count()
        active_vehicles = Vehicle.objects.filter(status="ACTIVE").count()
        refrigerated_vehicles = Vehicle.objects.filter(is_refrigerated=True).count()
        available_vehicles = Vehicle.objects.filter(
            status="ACTIVE", assigned_driver__isnull=True
        ).count()

        # Shipment stats
        total_shipments = Shipment.objects.count()
        active_shipments = Shipment.objects.filter(
            status__in=["PENDING", "ASSIGNED", "PICKED_UP", "IN_TRANSIT"]
        ).count()
        delivered_shipments = Shipment.objects.filter(status="DELIVERED").count()
        emergency_shipments = Shipment.objects.filter(priority="EMERGENCY").count()

        # Recent shipments
        last_30_days = timezone.now() - timedelta(days=30)
        recent_shipments = Shipment.objects.filter(created_at__gte=last_30_days).count()

        return {
            "total_vehicles": total_vehicles,
            "active_vehicles": active_vehicles,
            "refrigerated_vehicles": refrigerated_vehicles,
            "available_vehicles": available_vehicles,
            "total_shipments": total_shipments,
            "active_shipments": active_shipments,
            "delivered_shipments": delivered_shipments,
            "emergency_shipments": emergency_shipments,
            "recent_shipments": recent_shipments,
        }

    def resolve_fleet_stats(self, info):
        from django.db.models import Count, Avg
        from django.utils import timezone

        # Vehicle type distribution
        vehicle_type_distribution = (
            Vehicle.objects.values("vehicle_type")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        # Vehicle status distribution
        vehicle_status_distribution = (
            Vehicle.objects.values("status")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        # Maintenance stats
        maintenance_due = Vehicle.objects.filter(
            next_maintenance_date__lte=timezone.now().date()
        ).count()

        # Average mileage
        avg_mileage = (
            Vehicle.objects.aggregate(avg_mileage=Avg("total_mileage"))["avg_mileage"]
            or 0
        )

        return {
            "vehicle_type_distribution": list(vehicle_type_distribution),
            "vehicle_status_distribution": list(vehicle_status_distribution),
            "maintenance_due": maintenance_due,
            "avg_mileage": float(avg_mileage),
        }


class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
