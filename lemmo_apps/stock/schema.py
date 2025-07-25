import graphene
from graphene_django import DjangoObjectType
from .models.stock import Stock
from .models.stock_transaction import StockTransaction
from django.db.models import F


class StockType(DjangoObjectType):
    class Meta:
        model = Stock
        fields = "__all__"


class StockTransactionType(DjangoObjectType):
    class Meta:
        model = StockTransaction
        fields = "__all__"


class Query(graphene.ObjectType):
    # Stock queries
    stock = graphene.List(
        StockType,
        product_id=graphene.UUID(),
        facility_id=graphene.UUID(),
        is_active=graphene.Boolean(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )

    stock_item = graphene.Field(StockType, id=graphene.UUID(required=True))

    # Stock transaction queries
    stock_transactions = graphene.List(
        StockTransactionType,
        stock_id=graphene.UUID(),
        transaction_type=graphene.String(),
        facility_id=graphene.UUID(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )

    stock_transaction = graphene.Field(
        StockTransactionType, id=graphene.UUID(required=True)
    )

    # Healthcare specific queries
    low_stock = graphene.List(StockType)
    out_of_stock = graphene.List(StockType)
    overstocked = graphene.List(StockType)
    expiring_stock = graphene.List(StockType)
    expired_stock = graphene.List(StockType)

    # Dashboard statistics
    stock_stats = graphene.JSONString()
    transaction_stats = graphene.JSONString()

    def resolve_stock(
        self,
        info,
        product_id=None,
        facility_id=None,
        is_active=None,
        limit=None,
        offset=None,
    ):
        queryset = Stock.objects.all()

        if product_id:
            queryset = queryset.filter(product_id=product_id)

        if facility_id:
            queryset = queryset.filter(facility_id=facility_id)

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        if offset:
            queryset = queryset[offset:]

        if limit:
            queryset = queryset[:limit]

        return queryset

    def resolve_stock_item(self, info, id):
        return Stock.objects.get(id=id)

    def resolve_stock_transactions(
        self,
        info,
        stock_id=None,
        transaction_type=None,
        facility_id=None,
        limit=None,
        offset=None,
    ):
        queryset = StockTransaction.objects.all()

        if stock_id:
            queryset = queryset.filter(stock_id=stock_id)

        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)

        if facility_id:
            queryset = queryset.filter(facility_id=facility_id)

        if offset:
            queryset = queryset[offset:]

        if limit:
            queryset = queryset[:limit]

        return queryset

    def resolve_stock_transaction(self, info, id):
        return StockTransaction.objects.get(id=id)

    def resolve_low_stock(self, info):
        return Stock.objects.filter(quantity__lte=F("reorder_point"), is_active=True)

    def resolve_out_of_stock(self, info):
        return Stock.objects.filter(quantity=0, is_active=True)

    def resolve_overstocked(self, info):
        return Stock.objects.filter(quantity__gt=F("max_stock_level"), is_active=True)

    def resolve_expiring_stock(self, info):
        from django.utils import timezone
        from datetime import timedelta

        expiry_threshold = timezone.now().date() + timedelta(days=30)
        return Stock.objects.filter(
            expiration_date__lte=expiry_threshold,
            expiration_date__gte=timezone.now().date(),
            is_active=True,
        )

    def resolve_expired_stock(self, info):
        from django.utils import timezone

        return Stock.objects.filter(
            expiration_date__lt=timezone.now().date(), is_active=True
        )

    def resolve_stock_stats(self, info):
        from django.db.models import Count, Sum, Avg
        from django.db.models import F

        total_stock_items = Stock.objects.count()
        active_stock_items = Stock.objects.filter(is_active=True).count()
        low_stock_items = Stock.objects.filter(
            quantity__lte=F("reorder_point"), is_active=True
        ).count()
        out_of_stock_items = Stock.objects.filter(quantity=0, is_active=True).count()
        overstocked_items = Stock.objects.filter(
            quantity__gt=F("max_stock_level"), is_active=True
        ).count()

        # Total stock value
        total_stock_value = (
            Stock.objects.aggregate(total_value=Sum(F("quantity") * F("unit_cost")))[
                "total_value"
            ]
            or 0
        )

        # Average stock level
        avg_stock_level = (
            Stock.objects.aggregate(avg_quantity=Avg("quantity"))["avg_quantity"] or 0
        )

        return {
            "total_stock_items": total_stock_items,
            "active_stock_items": active_stock_items,
            "low_stock_items": low_stock_items,
            "out_of_stock_items": out_of_stock_items,
            "overstocked_items": overstocked_items,
            "total_stock_value": float(total_stock_value),
            "avg_stock_level": float(avg_stock_level),
        }

    def resolve_transaction_stats(self, info):
        from django.db.models import Count, Sum
        from django.utils import timezone
        from datetime import timedelta

        total_transactions = StockTransaction.objects.count()

        # Transaction type distribution
        transaction_type_distribution = (
            StockTransaction.objects.values("transaction_type")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        # Recent transactions
        last_30_days = timezone.now() - timedelta(days=30)
        recent_transactions = StockTransaction.objects.filter(
            created_at__gte=last_30_days
        ).count()

        # Transaction value stats
        total_transaction_value = (
            StockTransaction.objects.aggregate(total_value=Sum("total_amount"))[
                "total_value"
            ]
            or 0
        )

        return {
            "total_transactions": total_transactions,
            "recent_transactions": recent_transactions,
            "total_transaction_value": float(total_transaction_value),
            "transaction_type_distribution": list(transaction_type_distribution),
        }


class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
