import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q, Sum, Count, F
from lemmo_apps.inventory.models.product import (
    Product,
    ProductCategory,
    ProductBatch,
    ProductImage,
)


class ProductCategoryType(DjangoObjectType):
    class Meta:
        model = ProductCategory
        fields = "__all__"


class ProductImageType(DjangoObjectType):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductBatchType(DjangoObjectType):
    class Meta:
        model = ProductBatch
        fields = "__all__"


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"


class ProductQuery(graphene.ObjectType):
    # Product queries
    products = graphene.List(
        ProductType,
        category_id=graphene.UUID(),
        product_type=graphene.String(),
        is_active=graphene.Boolean(),
        search=graphene.String(),
        low_stock=graphene.Boolean(),
        out_of_stock=graphene.Boolean(),
        requires_refrigeration=graphene.Boolean(),
        controlled_substance=graphene.String(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )

    product = graphene.Field(ProductType, id=graphene.UUID(required=True))

    product_by_code = graphene.Field(ProductType, code=graphene.String(required=True))

    # Category queries
    product_categories = graphene.List(
        ProductCategoryType, is_active=graphene.Boolean(), parent_id=graphene.UUID()
    )

    product_category = graphene.Field(
        ProductCategoryType, id=graphene.UUID(required=True)
    )

    # Batch queries
    product_batches = graphene.List(
        ProductBatchType,
        product_id=graphene.UUID(),
        is_expired=graphene.Boolean(),
        is_expiring_soon=graphene.Boolean(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )

    product_batch = graphene.Field(ProductBatchType, id=graphene.UUID(required=True))

    # Healthcare specific queries
    medications = graphene.List(ProductType)
    medical_supplies = graphene.List(ProductType)
    vaccines = graphene.List(ProductType)
    controlled_substances = graphene.List(ProductType)
    refrigerated_products = graphene.List(ProductType)
    expired_products = graphene.List(ProductType)
    low_stock_products = graphene.List(ProductType)

    # Dashboard statistics
    inventory_stats = graphene.JSONString()
    stock_alerts = graphene.JSONString()

    def resolve_products(
        self,
        info,
        category_id=None,
        product_type=None,
        is_active=None,
        search=None,
        low_stock=None,
        out_of_stock=None,
        requires_refrigeration=None,
        controlled_substance=None,
        limit=None,
        offset=None,
    ):
        queryset = Product.objects.all()

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if product_type:
            queryset = queryset.filter(product_type=product_type)

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(description__icontains=search)
                | Q(generic_name__icontains=search)
                | Q(brand_name__icontains=search)
                | Q(manufacturer__icontains=search)
                | Q(ndc_code__icontains=search)
            )

        if low_stock is not None:
            if low_stock:
                queryset = queryset.filter(stock_quantity__lte=F("reorder_point"))
            else:
                queryset = queryset.filter(stock_quantity__gt=F("reorder_point"))

        if out_of_stock is not None:
            if out_of_stock:
                queryset = queryset.filter(stock_quantity=0)
            else:
                queryset = queryset.filter(stock_quantity__gt=0)

        if requires_refrigeration is not None:
            queryset = queryset.filter(
                storage_type__in=["REFRIGERATED", "FROZEN", "ULTRA_COLD"]
            )

        if controlled_substance:
            queryset = queryset.filter(controlled_substance=controlled_substance)

        if offset:
            queryset = queryset[offset:]

        if limit:
            queryset = queryset[:limit]

        return queryset

    def resolve_product(self, info, id):
        return Product.objects.get(id=id)

    def resolve_product_by_code(self, info, code):
        return Product.objects.get(code=code)

    def resolve_product_categories(self, info, is_active=None, parent_id=None):
        queryset = ProductCategory.objects.all()

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        if parent_id:
            queryset = queryset.filter(parent_id=parent_id)

        return queryset

    def resolve_product_category(self, info, id):
        return ProductCategory.objects.get(id=id)

    def resolve_product_batches(
        self,
        info,
        product_id=None,
        is_expired=None,
        is_expiring_soon=None,
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

        if offset:
            queryset = queryset[offset:]

        if limit:
            queryset = queryset[:limit]

        return queryset

    def resolve_product_batch(self, info, id):
        return ProductBatch.objects.get(id=id)

    def resolve_medications(self, info):
        return Product.objects.filter(product_type="MEDICATION", is_active=True)

    def resolve_medical_supplies(self, info):
        return Product.objects.filter(product_type="MEDICAL_SUPPLY", is_active=True)

    def resolve_vaccines(self, info):
        return Product.objects.filter(product_type="VACCINE", is_active=True)

    def resolve_controlled_substances(self, info):
        return Product.objects.filter(
            controlled_substance__in=[
                "SCHEDULE_I",
                "SCHEDULE_II",
                "SCHEDULE_III",
                "SCHEDULE_IV",
                "SCHEDULE_V",
            ]
        )

    def resolve_refrigerated_products(self, info):
        return Product.objects.filter(
            storage_type__in=["REFRIGERATED", "FROZEN", "ULTRA_COLD"]
        )

    def resolve_expired_products(self, info):
        from django.utils import timezone

        return (
            ProductBatch.objects.filter(expiration_date__lt=timezone.now().date())
            .values_list("product", flat=True)
            .distinct()
        )

    def resolve_low_stock_products(self, info):
        return Product.objects.filter(stock_quantity__lte=F("reorder_point"))

    def resolve_inventory_stats(self, info):
        from django.utils import timezone
        from datetime import timedelta

        total_products = Product.objects.count()
        active_products = Product.objects.filter(is_active=True).count()
        total_stock_value = (
            Product.objects.aggregate(
                total_value=Sum(F("stock_quantity") * F("price"))
            )["total_value"]
            or 0
        )

        # Stock levels
        out_of_stock = Product.objects.filter(stock_quantity=0).count()
        low_stock = Product.objects.filter(
            stock_quantity__lte=F("reorder_point")
        ).count()

        # Expiring batches
        expiry_threshold = timezone.now().date() + timedelta(days=30)
        expiring_batches = ProductBatch.objects.filter(
            expiration_date__lte=expiry_threshold,
            expiration_date__gte=timezone.now().date(),
        ).count()

        # Product types distribution
        product_types = (
            Product.objects.values("product_type")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        return {
            "total_products": total_products,
            "active_products": active_products,
            "total_stock_value": float(total_stock_value),
            "out_of_stock": out_of_stock,
            "low_stock": low_stock,
            "expiring_batches": expiring_batches,
            "product_types": list(product_types),
        }

    def resolve_stock_alerts(self, info):
        from django.utils import timezone
        from datetime import timedelta

        # Low stock alerts
        low_stock_products = Product.objects.filter(
            stock_quantity__lte=F("reorder_point")
        ).values("id", "name", "stock_quantity", "reorder_point")

        # Out of stock alerts
        out_of_stock_products = Product.objects.filter(stock_quantity=0).values(
            "id", "name", "stock_quantity"
        )

        # Expiring batches alerts
        expiry_threshold = timezone.now().date() + timedelta(days=30)
        expiring_batches = ProductBatch.objects.filter(
            expiration_date__lte=expiry_threshold,
            expiration_date__gte=timezone.now().date(),
        ).values(
            "id",
            "product__name",
            "batch_number",
            "expiration_date",
            "remaining_quantity",
        )

        return {
            "low_stock_alerts": list(low_stock_products),
            "out_of_stock_alerts": list(out_of_stock_products),
            "expiring_batch_alerts": list(expiring_batches),
        }
