import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q
from lemmo_apps.inventory.models.product import ProductBatch


class ProductBatchType(DjangoObjectType):
    class Meta:
        model = ProductBatch
        fields = "__all__"


class BatchQuery(graphene.ObjectType):
    batches = graphene.List(
        ProductBatchType,
        product_id=graphene.UUID(),
        is_expired=graphene.Boolean(),
        is_expiring_soon=graphene.Boolean(),
        supplier=graphene.String(),
        quality_control_passed=graphene.Boolean(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )

    batch = graphene.Field(ProductBatchType, id=graphene.UUID(required=True))

    batch_by_number = graphene.Field(
        ProductBatchType, batch_number=graphene.String(required=True)
    )

    # Healthcare specific queries
    expired_batches = graphene.List(ProductBatchType)
    expiring_soon_batches = graphene.List(ProductBatchType)
    quality_control_failed = graphene.List(ProductBatchType)

    # Dashboard statistics
    batch_stats = graphene.JSONString()

    def resolve_batches(
        self,
        info,
        product_id=None,
        is_expired=None,
        is_expiring_soon=None,
        supplier=None,
        quality_control_passed=None,
        limit=None,
        offset=None,
    ):
        from django.utils import timezone
        from datetime import timedelta

        queryset = ProductBatch.objects.all()

        if product_id:
            queryset = queryset.filter(product_id=product_id)

        if is_expired is not None:
            if is_expired:
                queryset = queryset.filter(expiration_date__lt=timezone.now().date())
            else:
                queryset = queryset.filter(expiration_date__gte=timezone.now().date())

        if is_expiring_soon is not None:
            expiry_threshold = timezone.now().date() + timedelta(days=30)
            if is_expiring_soon:
                queryset = queryset.filter(
                    expiration_date__lte=expiry_threshold,
                    expiration_date__gte=timezone.now().date(),
                )
            else:
                queryset = queryset.filter(
                    Q(expiration_date__gt=expiry_threshold)
                    | Q(expiration_date__lt=timezone.now().date())
                )

        if supplier:
            queryset = queryset.filter(supplier__icontains=supplier)

        if quality_control_passed is not None:
            queryset = queryset.filter(quality_control_passed=quality_control_passed)

        if offset:
            queryset = queryset[offset:]

        if limit:
            queryset = queryset[:limit]

        return queryset

    def resolve_batch(self, info, id):
        return ProductBatch.objects.get(id=id)

    def resolve_batch_by_number(self, info, batch_number):
        return ProductBatch.objects.get(batch_number=batch_number)

    def resolve_expired_batches(self, info):
        from django.utils import timezone

        return ProductBatch.objects.filter(expiration_date__lt=timezone.now().date())

    def resolve_expiring_soon_batches(self, info):
        from django.utils import timezone
        from datetime import timedelta

        expiry_threshold = timezone.now().date() + timedelta(days=30)
        return ProductBatch.objects.filter(
            expiration_date__lte=expiry_threshold,
            expiration_date__gte=timezone.now().date(),
        )

    def resolve_quality_control_failed(self, info):
        return ProductBatch.objects.filter(quality_control_passed=False)

    def resolve_batch_stats(self, info):
        from django.utils import timezone
        from datetime import timedelta
        from django.db.models import Count, Sum

        total_batches = ProductBatch.objects.count()
        active_batches = ProductBatch.objects.filter(
            expiration_date__gte=timezone.now().date()
        ).count()

        # Expiring batches
        expiry_threshold = timezone.now().date() + timedelta(days=30)
        expiring_soon = ProductBatch.objects.filter(
            expiration_date__lte=expiry_threshold,
            expiration_date__gte=timezone.now().date(),
        ).count()

        # Quality control
        quality_passed = ProductBatch.objects.filter(
            quality_control_passed=True
        ).count()
        quality_failed = ProductBatch.objects.filter(
            quality_control_passed=False
        ).count()

        # Total value
        total_value = (
            ProductBatch.objects.aggregate(
                total_value=Sum("cost_per_unit" * "remaining_quantity")
            )["total_value"]
            or 0
        )

        # Supplier distribution
        supplier_distribution = (
            ProductBatch.objects.values("supplier")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )

        return {
            "total_batches": total_batches,
            "active_batches": active_batches,
            "expiring_soon": expiring_soon,
            "quality_passed": quality_passed,
            "quality_failed": quality_failed,
            "total_value": float(total_value),
            "supplier_distribution": list(supplier_distribution),
        }
