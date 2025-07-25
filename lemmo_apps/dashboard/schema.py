import graphene
from graphene_django import DjangoObjectType
from django.db.models import F
from datetime import timedelta


class Query(graphene.ObjectType):
    # Dashboard overview queries
    dashboard_overview = graphene.JSONString()
    inventory_overview = graphene.JSONString()
    logistics_overview = graphene.JSONString()
    supplier_overview = graphene.JSONString()
    facility_overview = graphene.JSONString()

    # Alert queries
    alerts = graphene.JSONString()
    low_stock_alerts = graphene.JSONString()
    expiring_products_alerts = graphene.JSONString()
    emergency_shipments_alerts = graphene.JSONString()
    maintenance_due_alerts = graphene.JSONString()

    # Report queries
    inventory_report = graphene.JSONString()
    logistics_report = graphene.JSONString()
    supplier_report = graphene.JSONString()
    facility_report = graphene.JSONString()
    compliance_report = graphene.JSONString()

    def resolve_dashboard_overview(self, info):
        from django.db.models import Count, Sum
        from django.utils import timezone
        from datetime import timedelta

        # Import models
        from lemmo_apps.inventory.models.product import Product
        from lemmo_apps.logistics.models.shipment import Shipment
        from lemmo_apps.supplier.models.supplier import Supplier
        from lemmo_apps.location.models.facility import Facility
        from lemmo_apps.requisition.models.requisition import Requisition

        # Basic stats
        total_products = Product.objects.count()
        active_shipments = Shipment.objects.filter(
            status__in=["PENDING", "ASSIGNED", "PICKED_UP", "IN_TRANSIT"]
        ).count()
        total_suppliers = Supplier.objects.count()
        total_facilities = Facility.objects.count()
        pending_requisitions = Requisition.objects.filter(status="PENDING").count()

        # Recent activity
        last_7_days = timezone.now() - timedelta(days=7)
        recent_products = Product.objects.filter(created_at__gte=last_7_days).count()
        recent_shipments = Shipment.objects.filter(created_at__gte=last_7_days).count()

        return {
            "total_products": total_products,
            "active_shipments": active_shipments,
            "total_suppliers": total_suppliers,
            "total_facilities": total_facilities,
            "pending_requisitions": pending_requisitions,
            "recent_products": recent_products,
            "recent_shipments": recent_shipments,
        }

    def resolve_inventory_overview(self, info):
        from django.db.models import Count, Sum
        from lemmo_apps.inventory.models.product import Product

        total_products = Product.objects.count()
        active_products = Product.objects.filter(is_active=True).count()
        low_stock_products = Product.objects.filter(
            stock_quantity__lte=F("reorder_point")
        ).count()
        out_of_stock_products = Product.objects.filter(stock_quantity=0).count()

        # Product type distribution
        product_type_distribution = (
            Product.objects.values("product_type")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        return {
            "total_products": total_products,
            "active_products": active_products,
            "low_stock_products": low_stock_products,
            "out_of_stock_products": out_of_stock_products,
            "product_type_distribution": list(product_type_distribution),
        }

    def resolve_logistics_overview(self, info):
        from django.db.models import Count
        from lemmo_apps.logistics.models.vehicle import Vehicle
        from lemmo_apps.logistics.models.shipment import Shipment

        total_vehicles = Vehicle.objects.count()
        active_vehicles = Vehicle.objects.filter(status="ACTIVE").count()
        total_shipments = Shipment.objects.count()
        active_shipments = Shipment.objects.filter(
            status__in=["PENDING", "ASSIGNED", "PICKED_UP", "IN_TRANSIT"]
        ).count()
        delivered_shipments = Shipment.objects.filter(status="DELIVERED").count()

        return {
            "total_vehicles": total_vehicles,
            "active_vehicles": active_vehicles,
            "total_shipments": total_shipments,
            "active_shipments": active_shipments,
            "delivered_shipments": delivered_shipments,
        }

    def resolve_supplier_overview(self, info):
        from django.db.models import Count, Avg
        from lemmo_apps.supplier.models.supplier import Supplier
        from lemmo_apps.supplier.models.purchase_order import PurchaseOrder

        total_suppliers = Supplier.objects.count()
        active_suppliers = Supplier.objects.filter(status="ACTIVE").count()
        preferred_suppliers = Supplier.objects.filter(is_preferred=True).count()
        total_orders = PurchaseOrder.objects.count()
        pending_orders = PurchaseOrder.objects.filter(
            status__in=["DRAFT", "SUBMITTED"]
        ).count()

        # Average ratings
        avg_quality_rating = (
            Supplier.objects.aggregate(avg_quality=Avg("quality_rating"))["avg_quality"]
            or 0
        )

        return {
            "total_suppliers": total_suppliers,
            "active_suppliers": active_suppliers,
            "preferred_suppliers": preferred_suppliers,
            "total_orders": total_orders,
            "pending_orders": pending_orders,
            "avg_quality_rating": float(avg_quality_rating),
        }

    def resolve_facility_overview(self, info):
        from django.db.models import Count
        from lemmo_apps.location.models.facility import Facility

        total_facilities = Facility.objects.count()
        active_facilities = Facility.objects.filter(is_active=True).count()
        operational_facilities = Facility.objects.filter(
            operational_status="ACTIVE"
        ).count()

        # Facility type distribution
        facility_type_distribution = (
            Facility.objects.values("category")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        return {
            "total_facilities": total_facilities,
            "active_facilities": active_facilities,
            "operational_facilities": operational_facilities,
            "facility_type_distribution": list(facility_type_distribution),
        }

    def resolve_alerts(self, info):
        from django.db.models import F
        from lemmo_apps.inventory.models.product import Product
        from lemmo_apps.logistics.models.vehicle import Vehicle
        from lemmo_apps.supplier.models.contract import Contract
        from django.utils import timezone

        # Low stock alerts
        low_stock_count = Product.objects.filter(
            stock_quantity__lte=F("reorder_point")
        ).count()

        # Expiring products alerts
        expiring_products_count = Product.objects.filter(
            expiration_date__lte=timezone.now().date() + timedelta(days=30)
        ).count()

        # Maintenance due alerts
        maintenance_due_count = Vehicle.objects.filter(
            next_maintenance_date__lte=timezone.now().date()
        ).count()

        # Expiring contracts alerts
        expiring_contracts_count = Contract.objects.filter(
            status="ACTIVE", end_date__lte=timezone.now().date() + timedelta(days=90)
        ).count()

        return {
            "low_stock_count": low_stock_count,
            "expiring_products_count": expiring_products_count,
            "maintenance_due_count": maintenance_due_count,
            "expiring_contracts_count": expiring_contracts_count,
            "total_alerts": low_stock_count
            + expiring_products_count
            + maintenance_due_count
            + expiring_contracts_count,
        }

    def resolve_low_stock_alerts(self, info):
        from django.db.models import F
        from lemmo_apps.inventory.models.product import Product

        low_stock_products = Product.objects.filter(
            stock_quantity__lte=F("reorder_point")
        ).values("id", "name", "stock_quantity", "reorder_point")

        return {
            "count": low_stock_products.count(),
            "products": list(low_stock_products),
        }

    def resolve_expiring_products_alerts(self, info):
        from lemmo_apps.inventory.models.product import Product
        from django.utils import timezone
        from datetime import timedelta

        expiring_products = Product.objects.filter(
            expiration_date__lte=timezone.now().date() + timedelta(days=30)
        ).values("id", "name", "expiration_date")

        return {"count": expiring_products.count(), "products": list(expiring_products)}

    def resolve_emergency_shipments_alerts(self, info):
        from lemmo_apps.logistics.models.shipment import Shipment

        emergency_shipments = Shipment.objects.filter(priority="EMERGENCY").values(
            "id",
            "shipment_number",
            "origin_facility__name",
            "destination_facility__name",
        )

        return {
            "count": emergency_shipments.count(),
            "shipments": list(emergency_shipments),
        }

    def resolve_maintenance_due_alerts(self, info):
        from lemmo_apps.logistics.models.vehicle import Vehicle
        from django.utils import timezone

        maintenance_due_vehicles = Vehicle.objects.filter(
            next_maintenance_date__lte=timezone.now().date()
        ).values("id", "vehicle_id", "make", "model", "next_maintenance_date")

        return {
            "count": maintenance_due_vehicles.count(),
            "vehicles": list(maintenance_due_vehicles),
        }

    def resolve_inventory_report(self, info):
        from django.db.models import Count, Sum, Avg
        from django.db.models import F
        from lemmo_apps.inventory.models.product import Product

        total_products = Product.objects.count()
        total_stock_value = (
            Product.objects.aggregate(
                total_value=Sum(F("stock_quantity") * F("price"))
            )["total_value"]
            or 0
        )

        # Stock level analysis
        low_stock_count = Product.objects.filter(
            stock_quantity__lte=F("reorder_point")
        ).count()
        out_of_stock_count = Product.objects.filter(stock_quantity=0).count()
        overstocked_count = Product.objects.filter(
            stock_quantity__gt=F("max_stock_level")
        ).count()

        return {
            "total_products": total_products,
            "total_stock_value": float(total_stock_value),
            "low_stock_count": low_stock_count,
            "out_of_stock_count": out_of_stock_count,
            "overstocked_count": overstocked_count,
        }

    def resolve_logistics_report(self, info):
        from django.db.models import Count, Avg
        from lemmo_apps.logistics.models.vehicle import Vehicle
        from lemmo_apps.logistics.models.shipment import Shipment

        total_vehicles = Vehicle.objects.count()
        active_vehicles = Vehicle.objects.filter(status="ACTIVE").count()
        total_shipments = Shipment.objects.count()
        delivered_shipments = Shipment.objects.filter(status="DELIVERED").count()

        # Delivery success rate
        delivery_success_rate = (
            (delivered_shipments / total_shipments * 100) if total_shipments > 0 else 0
        )

        return {
            "total_vehicles": total_vehicles,
            "active_vehicles": active_vehicles,
            "total_shipments": total_shipments,
            "delivered_shipments": delivered_shipments,
            "delivery_success_rate": float(delivery_success_rate),
        }

    def resolve_supplier_report(self, info):
        from django.db.models import Count, Avg
        from lemmo_apps.supplier.models.supplier import Supplier
        from lemmo_apps.supplier.models.purchase_order import PurchaseOrder

        total_suppliers = Supplier.objects.count()
        active_suppliers = Supplier.objects.filter(status="ACTIVE").count()
        total_orders = PurchaseOrder.objects.count()

        # Average supplier rating
        avg_rating = (
            Supplier.objects.aggregate(avg_rating=Avg("quality_rating"))["avg_rating"]
            or 0
        )

        return {
            "total_suppliers": total_suppliers,
            "active_suppliers": active_suppliers,
            "total_orders": total_orders,
            "avg_rating": float(avg_rating),
        }

    def resolve_facility_report(self, info):
        from django.db.models import Count
        from lemmo_apps.location.models.facility import Facility

        total_facilities = Facility.objects.count()
        active_facilities = Facility.objects.filter(is_active=True).count()
        operational_facilities = Facility.objects.filter(
            operational_status="ACTIVE"
        ).count()

        return {
            "total_facilities": total_facilities,
            "active_facilities": active_facilities,
            "operational_facilities": operational_facilities,
        }

    def resolve_compliance_report(self, info):
        from django.db.models import Count
        from lemmo_apps.inventory.models.product import Product
        from lemmo_apps.supplier.models.supplier import Supplier
        from lemmo_apps.location.models.facility import Facility

        # FDA compliance
        fda_approved_products = Product.objects.filter(fda_approved=True).count()
        total_products = Product.objects.count()
        fda_compliance_rate = (
            (fda_approved_products / total_products * 100) if total_products > 0 else 0
        )

        # Supplier compliance
        certified_suppliers = Supplier.objects.filter(is_certified=True).count()
        total_suppliers = Supplier.objects.count()
        supplier_compliance_rate = (
            (certified_suppliers / total_suppliers * 100) if total_suppliers > 0 else 0
        )

        # Facility compliance
        licensed_facilities = Facility.objects.filter(
            license_number__isnull=False
        ).count()
        total_facilities = Facility.objects.count()
        facility_compliance_rate = (
            (licensed_facilities / total_facilities * 100)
            if total_facilities > 0
            else 0
        )

        return {
            "fda_compliance_rate": float(fda_compliance_rate),
            "supplier_compliance_rate": float(supplier_compliance_rate),
            "facility_compliance_rate": float(facility_compliance_rate),
            "fda_approved_products": fda_approved_products,
            "certified_suppliers": certified_suppliers,
            "licensed_facilities": licensed_facilities,
        }


class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
