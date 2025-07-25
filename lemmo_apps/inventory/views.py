from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q, F, Count
from django.utils import timezone
from datetime import timedelta

from .models.product import Product, ProductCategory, ProductBatch


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "inventory/product_list.html"
    context_object_name = "products"
    paginate_by = 20

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.GET.get("category_id")
        product_type = self.request.GET.get("product_type")
        is_active = self.request.GET.get("is_active")
        search = self.request.GET.get("search")
        low_stock = self.request.GET.get("low_stock")
        out_of_stock = self.request.GET.get("out_of_stock")

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if product_type:
            queryset = queryset.filter(product_type=product_type)

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active == "true")

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
            if low_stock == "true":
                queryset = queryset.filter(stock_quantity__lte=F("min_stock_level"))
            else:
                queryset = queryset.filter(stock_quantity__gt=F("min_stock_level"))

        if out_of_stock is not None:
            if out_of_stock == "true":
                queryset = queryset.filter(stock_quantity=0)
            else:
                queryset = queryset.filter(stock_quantity__gt=0)

        return queryset


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "inventory/product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    template_name = "inventory/product_form.html"
    fields = [
        "code",
        "name",
        "description",
        "category",
        "product_type",
        "unit_of_measure",
        "price",
        "generic_name",
        "brand_name",
        "manufacturer",
        "ndc_code",
        "rx_required",
        "controlled_substance",
        "storage_type",
        "storage_notes",
        "expiration_date_required",
        "lot_number_required",
        "min_stock_level",
        "max_stock_level",
        "reorder_point",
        "fda_approved",
        "fda_approval_date",
        "requires_prescription",
        "requires_special_handling",
        "hazardous_material",
        "temperature_sensitive",
        "weight_grams",
        "dimensions_cm",
    ]
    success_url = reverse_lazy("inventory:product-list")
    permission_required = "inventory.add_product"


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    template_name = "inventory/product_form.html"
    fields = [
        "code",
        "name",
        "description",
        "category",
        "product_type",
        "unit_of_measure",
        "price",
        "generic_name",
        "brand_name",
        "manufacturer",
        "ndc_code",
        "rx_required",
        "controlled_substance",
        "storage_type",
        "storage_notes",
        "expiration_date_required",
        "lot_number_required",
        "min_stock_level",
        "max_stock_level",
        "reorder_point",
        "fda_approved",
        "fda_approval_date",
        "requires_prescription",
        "requires_special_handling",
        "hazardous_material",
        "temperature_sensitive",
        "weight_grams",
        "dimensions_cm",
    ]
    success_url = reverse_lazy("inventory:product-list")
    permission_required = "inventory.change_product"


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = "inventory/product_confirm_delete.html"
    success_url = reverse_lazy("inventory:product-list")
    permission_required = "inventory.delete_product"


class ProductImageView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "inventory/product_images.html"
    context_object_name = "product"


class CategoryListView(LoginRequiredMixin, ListView):
    model = ProductCategory
    template_name = "inventory/category_list.html"
    context_object_name = "categories"
    paginate_by = 20

    def get_queryset(self):
        queryset = ProductCategory.objects.all()
        is_active = self.request.GET.get("is_active")
        parent_id = self.request.GET.get("parent_id")

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active == "true")

        if parent_id:
            queryset = queryset.filter(parent_id=parent_id)

        return queryset


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = ProductCategory
    template_name = "inventory/category_detail.html"
    context_object_name = "category"


class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ProductCategory
    template_name = "inventory/category_form.html"
    fields = ["name", "description", "parent", "is_active"]
    success_url = reverse_lazy("inventory:category-list")
    permission_required = "inventory.add_productcategory"


class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ProductCategory
    template_name = "inventory/category_form.html"
    fields = ["name", "description", "parent", "is_active"]
    success_url = reverse_lazy("inventory:category-list")
    permission_required = "inventory.change_productcategory"


class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ProductCategory
    template_name = "inventory/category_confirm_delete.html"
    success_url = reverse_lazy("inventory:category-list")
    permission_required = "inventory.delete_productcategory"


class CategoryTreeView(LoginRequiredMixin, ListView):
    model = ProductCategory
    template_name = "inventory/category_tree.html"
    context_object_name = "categories"

    def get_queryset(self):
        return ProductCategory.objects.filter(parent=None)


class BatchListView(LoginRequiredMixin, ListView):
    model = ProductBatch
    template_name = "inventory/batch_list.html"
    context_object_name = "batches"
    paginate_by = 20

    def get_queryset(self):
        queryset = ProductBatch.objects.all()
        product_id = self.request.GET.get("product_id")
        is_expired = self.request.GET.get("is_expired")
        is_expiring_soon = self.request.GET.get("is_expiring_soon")

        if product_id:
            queryset = queryset.filter(product_id=product_id)

        if is_expired is not None:
            if is_expired == "true":
                queryset = queryset.filter(expiration_date__lt=timezone.now().date())
            else:
                queryset = queryset.filter(expiration_date__gte=timezone.now().date())

        if is_expiring_soon is not None:
            expiry_threshold = timezone.now().date() + timedelta(days=30)
            if is_expiring_soon == "true":
                queryset = queryset.filter(
                    expiration_date__lte=expiry_threshold,
                    expiration_date__gte=timezone.now().date(),
                )
            else:
                queryset = queryset.filter(
                    Q(expiration_date__gt=expiry_threshold)
                    | Q(expiration_date__lt=timezone.now().date())
                )

        return queryset


class BatchDetailView(LoginRequiredMixin, DetailView):
    model = ProductBatch
    template_name = "inventory/batch_detail.html"
    context_object_name = "batch"


class BatchCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ProductBatch
    template_name = "inventory/batch_form.html"
    fields = [
        "product",
        "batch_number",
        "lot_number",
        "quantity",
        "remaining_quantity",
        "manufacturing_date",
        "expiration_date",
        "cost_per_unit",
        "supplier",
        "supplier_batch_number",
        "quality_control_passed",
        "notes",
    ]
    success_url = reverse_lazy("inventory:batch-list")
    permission_required = "inventory.add_productbatch"


class BatchUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ProductBatch
    template_name = "inventory/batch_form.html"
    fields = [
        "product",
        "batch_number",
        "lot_number",
        "quantity",
        "remaining_quantity",
        "manufacturing_date",
        "expiration_date",
        "cost_per_unit",
        "supplier",
        "supplier_batch_number",
        "quality_control_passed",
        "notes",
    ]
    success_url = reverse_lazy("inventory:batch-list")
    permission_required = "inventory.change_productbatch"


class BatchDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ProductBatch
    template_name = "inventory/batch_confirm_delete.html"
    success_url = reverse_lazy("inventory:batch-list")
    permission_required = "inventory.delete_productbatch"


class ExpiredBatchesView(LoginRequiredMixin, ListView):
    model = ProductBatch
    template_name = "inventory/expired_batches.html"
    context_object_name = "batches"

    def get_queryset(self):
        return ProductBatch.objects.filter(expiration_date__lt=timezone.now().date())


class ExpiringSoonBatchesView(LoginRequiredMixin, ListView):
    model = ProductBatch
    template_name = "inventory/expiring_soon_batches.html"
    context_object_name = "batches"

    def get_queryset(self):
        expiry_threshold = timezone.now().date() + timedelta(days=30)
        return ProductBatch.objects.filter(
            expiration_date__lte=expiry_threshold,
            expiration_date__gte=timezone.now().date(),
        )


class MedicationsView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "inventory/medications.html"
    context_object_name = "medications"

    def get_queryset(self):
        return Product.objects.filter(product_type="MEDICATION", is_active=True)


class MedicalSuppliesView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "inventory/medical_supplies.html"
    context_object_name = "supplies"

    def get_queryset(self):
        return Product.objects.filter(product_type="MEDICAL_SUPPLY", is_active=True)


class VaccinesView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "inventory/vaccines.html"
    context_object_name = "vaccines"

    def get_queryset(self):
        return Product.objects.filter(product_type="VACCINE", is_active=True)


class ControlledSubstancesView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "inventory/controlled_substances.html"
    context_object_name = "substances"

    def get_queryset(self):
        return Product.objects.filter(
            controlled_substance__in=[
                "SCHEDULE_I",
                "SCHEDULE_II",
                "SCHEDULE_III",
                "SCHEDULE_IV",
                "SCHEDULE_V",
            ]
        )


class RefrigeratedProductsView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "inventory/refrigerated_products.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(
            storage_type__in=["REFRIGERATED", "FROZEN", "ULTRA_COLD"]
        )


class LowStockProductsView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "inventory/low_stock_products.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(stock_quantity__lte=F("min_stock_level"))


class OutOfStockProductsView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "inventory/out_of_stock_products.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(stock_quantity=0)


class InventoryStatsView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "inventory/inventory_stats.html"
    context_object_name = "stats"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate statistics
        total_products = Product.objects.count()
        active_products = Product.objects.filter(is_active=True).count()
        low_stock_products = Product.objects.filter(
            stock_quantity__lte=F("min_stock_level")
        ).count()
        out_of_stock_products = Product.objects.filter(stock_quantity=0).count()

        # Product type distribution
        product_type_stats = Product.objects.values("product_type").annotate(
            count=Count("product_type")
        )

        # Expired batches
        expired_batches = ProductBatch.objects.filter(
            expiration_date__lt=timezone.now().date()
        ).count()

        # Expiring soon batches
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
                "product_type_stats": product_type_stats,
                "expired_batches": expired_batches,
                "expiring_soon_batches": expiring_soon_batches,
            }
        )

        return context


class StockAlertsView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "inventory/stock_alerts.html"
    context_object_name = "alerts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get low stock products
        low_stock_products = Product.objects.filter(
            stock_quantity__lte=F("min_stock_level")
        )

        # Get out of stock products
        out_of_stock_products = Product.objects.filter(stock_quantity=0)

        # Get expired batches
        expired_batches = ProductBatch.objects.filter(
            expiration_date__lt=timezone.now().date()
        )

        # Get expiring soon batches
        expiry_threshold = timezone.now().date() + timedelta(days=30)
        expiring_soon_batches = ProductBatch.objects.filter(
            expiration_date__lte=expiry_threshold,
            expiration_date__gte=timezone.now().date(),
        )

        context.update(
            {
                "low_stock_products": low_stock_products,
                "out_of_stock_products": out_of_stock_products,
                "expired_batches": expired_batches,
                "expiring_soon_batches": expiring_soon_batches,
            }
        )

        return context
