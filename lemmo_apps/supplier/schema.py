import graphene
from graphene_django import DjangoObjectType
from .models.supplier import Supplier, SupplierContact, SupplierRating
from .models.purchase_order import PurchaseOrder, PurchaseOrderItem
from .models.contract import Contract, ContractTerm


class SupplierType(DjangoObjectType):
    class Meta:
        model = Supplier
        fields = "__all__"


class SupplierContactType(DjangoObjectType):
    class Meta:
        model = SupplierContact
        fields = "__all__"


class SupplierRatingType(DjangoObjectType):
    class Meta:
        model = SupplierRating
        fields = "__all__"


class PurchaseOrderType(DjangoObjectType):
    class Meta:
        model = PurchaseOrder
        fields = "__all__"


class PurchaseOrderItemType(DjangoObjectType):
    class Meta:
        model = PurchaseOrderItem
        fields = "__all__"


class ContractType(DjangoObjectType):
    class Meta:
        model = Contract
        fields = "__all__"


class ContractTermType(DjangoObjectType):
    class Meta:
        model = ContractTerm
        fields = "__all__"


class Query(graphene.ObjectType):
    # Supplier queries
    suppliers = graphene.List(
        SupplierType,
        supplier_type=graphene.String(),
        status=graphene.String(),
        is_active=graphene.Boolean(),
        search=graphene.String(),
        is_preferred=graphene.Boolean(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )

    supplier = graphene.Field(SupplierType, id=graphene.UUID(required=True))

    # Supplier contact queries
    supplier_contacts = graphene.List(
        SupplierContactType,
        supplier_id=graphene.UUID(),
        contact_type=graphene.String(),
        is_active=graphene.Boolean(),
    )

    # Supplier rating queries
    supplier_ratings = graphene.List(
        SupplierRatingType,
        supplier_id=graphene.UUID(),
        rating_type=graphene.String(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )

    # Purchase order queries
    purchase_orders = graphene.List(
        PurchaseOrderType,
        supplier_id=graphene.UUID(),
        status=graphene.String(),
        priority=graphene.String(),
        requested_by=graphene.UUID(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )

    purchase_order = graphene.Field(PurchaseOrderType, id=graphene.UUID(required=True))

    purchase_order_by_number = graphene.Field(
        PurchaseOrderType, po_number=graphene.String(required=True)
    )

    # Contract queries
    contracts = graphene.List(
        ContractType,
        supplier_id=graphene.UUID(),
        contract_type=graphene.String(),
        status=graphene.String(),
        is_active=graphene.Boolean(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )

    contract = graphene.Field(ContractType, id=graphene.UUID(required=True))

    contract_by_number = graphene.Field(
        ContractType, contract_number=graphene.String(required=True)
    )

    # Healthcare specific queries
    approved_suppliers = graphene.List(SupplierType)
    preferred_suppliers = graphene.List(SupplierType)
    active_contracts = graphene.List(ContractType)
    expiring_contracts = graphene.List(ContractType)
    pending_orders = graphene.List(PurchaseOrderType)

    # Dashboard statistics
    supplier_stats = graphene.JSONString()
    procurement_stats = graphene.JSONString()

    def resolve_suppliers(
        self,
        info,
        supplier_type=None,
        status=None,
        is_active=None,
        search=None,
        is_preferred=None,
        limit=None,
        offset=None,
    ):
        queryset = Supplier.objects.all()

        if supplier_type:
            queryset = queryset.filter(supplier_type=supplier_type)

        if status:
            queryset = queryset.filter(status=status)

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        if search:
            queryset = queryset.filter(name__icontains=search)

        if is_preferred is not None:
            queryset = queryset.filter(is_preferred=is_preferred)

        if offset:
            queryset = queryset[offset:]

        if limit:
            queryset = queryset[:limit]

        return queryset

    def resolve_supplier(self, info, id):
        return Supplier.objects.get(id=id)

    def resolve_supplier_contacts(
        self, info, supplier_id=None, contact_type=None, is_active=None
    ):
        queryset = SupplierContact.objects.all()

        if supplier_id:
            queryset = queryset.filter(supplier_id=supplier_id)

        if contact_type:
            queryset = queryset.filter(contact_type=contact_type)

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        return queryset

    def resolve_supplier_ratings(
        self, info, supplier_id=None, rating_type=None, limit=None, offset=None
    ):
        queryset = SupplierRating.objects.all()

        if supplier_id:
            queryset = queryset.filter(supplier_id=supplier_id)

        if rating_type:
            queryset = queryset.filter(rating_type=rating_type)

        if offset:
            queryset = queryset[offset:]

        if limit:
            queryset = queryset[:limit]

        return queryset

    def resolve_purchase_orders(
        self,
        info,
        supplier_id=None,
        status=None,
        priority=None,
        requested_by=None,
        limit=None,
        offset=None,
    ):
        queryset = PurchaseOrder.objects.all()

        if supplier_id:
            queryset = queryset.filter(supplier_id=supplier_id)

        if status:
            queryset = queryset.filter(status=status)

        if priority:
            queryset = queryset.filter(priority=priority)

        if requested_by:
            queryset = queryset.filter(requested_by_id=requested_by)

        if offset:
            queryset = queryset[offset:]

        if limit:
            queryset = queryset[:limit]

        return queryset

    def resolve_purchase_order(self, info, id):
        return PurchaseOrder.objects.get(id=id)

    def resolve_purchase_order_by_number(self, info, po_number):
        return PurchaseOrder.objects.get(po_number=po_number)

    def resolve_contracts(
        self,
        info,
        supplier_id=None,
        contract_type=None,
        status=None,
        is_active=None,
        limit=None,
        offset=None,
    ):
        queryset = Contract.objects.all()

        if supplier_id:
            queryset = queryset.filter(supplier_id=supplier_id)

        if contract_type:
            queryset = queryset.filter(contract_type=contract_type)

        if status:
            queryset = queryset.filter(status=status)

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        if offset:
            queryset = queryset[offset:]

        if limit:
            queryset = queryset[:limit]

        return queryset

    def resolve_contract(self, info, id):
        return Contract.objects.get(id=id)

    def resolve_contract_by_number(self, info, contract_number):
        return Contract.objects.get(contract_number=contract_number)

    def resolve_approved_suppliers(self, info):
        return Supplier.objects.filter(status="ACTIVE", is_active=True)

    def resolve_preferred_suppliers(self, info):
        return Supplier.objects.filter(is_preferred=True, is_active=True)

    def resolve_active_contracts(self, info):
        from django.utils import timezone

        today = timezone.now().date()
        return Contract.objects.filter(
            status="ACTIVE", start_date__lte=today, end_date__gte=today
        )

    def resolve_expiring_contracts(self, info):
        from django.utils import timezone
        from datetime import timedelta

        expiry_threshold = timezone.now().date() + timedelta(days=90)
        return Contract.objects.filter(
            status="ACTIVE",
            end_date__lte=expiry_threshold,
            end_date__gte=timezone.now().date(),
        )

    def resolve_pending_orders(self, info):
        return PurchaseOrder.objects.filter(status__in=["DRAFT", "SUBMITTED"])

    def resolve_supplier_stats(self, info):
        from django.db.models import Count, Avg

        total_suppliers = Supplier.objects.count()
        active_suppliers = Supplier.objects.filter(status="ACTIVE").count()
        preferred_suppliers = Supplier.objects.filter(is_preferred=True).count()

        # Average ratings
        avg_quality_rating = (
            Supplier.objects.aggregate(avg_quality=Avg("quality_rating"))["avg_quality"]
            or 0
        )

        avg_reliability_rating = (
            Supplier.objects.aggregate(avg_reliability=Avg("reliability_rating"))[
                "avg_reliability"
            ]
            or 0
        )

        # Supplier type distribution
        type_distribution = (
            Supplier.objects.values("supplier_type")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        return {
            "total_suppliers": total_suppliers,
            "active_suppliers": active_suppliers,
            "preferred_suppliers": preferred_suppliers,
            "avg_quality_rating": float(avg_quality_rating),
            "avg_reliability_rating": float(avg_reliability_rating),
            "type_distribution": list(type_distribution),
        }

    def resolve_procurement_stats(self, info):
        from django.db.models import Count, Sum
        from django.utils import timezone
        from datetime import timedelta

        # Purchase order stats
        total_orders = PurchaseOrder.objects.count()
        pending_orders = PurchaseOrder.objects.filter(
            status__in=["DRAFT", "SUBMITTED"]
        ).count()
        approved_orders = PurchaseOrder.objects.filter(
            status__in=["APPROVED", "ORDERED"]
        ).count()

        # Contract stats
        total_contracts = Contract.objects.count()
        active_contracts = Contract.objects.filter(status="ACTIVE").count()
        expiring_contracts = Contract.objects.filter(
            status="ACTIVE", end_date__lte=timezone.now().date() + timedelta(days=90)
        ).count()

        # Financial stats
        total_order_value = (
            PurchaseOrder.objects.aggregate(total_value=Sum("total_amount"))[
                "total_value"
            ]
            or 0
        )

        return {
            "total_orders": total_orders,
            "pending_orders": pending_orders,
            "approved_orders": approved_orders,
            "total_contracts": total_contracts,
            "active_contracts": active_contracts,
            "expiring_contracts": expiring_contracts,
            "total_order_value": float(total_order_value),
        }


class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
