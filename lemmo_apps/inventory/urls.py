from django.urls import path
from . import views

app_name = "inventory"

urlpatterns = [
    # Product URLs
    path("products/", views.ProductListView.as_view(), name="product-list"),
    path(
        "products/<uuid:pk>/", views.ProductDetailView.as_view(), name="product-detail"
    ),
    path("products/create/", views.ProductCreateView.as_view(), name="product-create"),
    path(
        "products/<uuid:pk>/update/",
        views.ProductUpdateView.as_view(),
        name="product-update",
    ),
    path(
        "products/<uuid:pk>/delete/",
        views.ProductDeleteView.as_view(),
        name="product-delete",
    ),
    path(
        "products/<uuid:pk>/images/",
        views.ProductImageView.as_view(),
        name="product-images",
    ),
    # Category URLs
    path("categories/", views.CategoryListView.as_view(), name="category-list"),
    path(
        "categories/<uuid:pk>/",
        views.CategoryDetailView.as_view(),
        name="category-detail",
    ),
    path(
        "categories/create/", views.CategoryCreateView.as_view(), name="category-create"
    ),
    path(
        "categories/<uuid:pk>/update/",
        views.CategoryUpdateView.as_view(),
        name="category-update",
    ),
    path(
        "categories/<uuid:pk>/delete/",
        views.CategoryDeleteView.as_view(),
        name="category-delete",
    ),
    path("categories/tree/", views.CategoryTreeView.as_view(), name="category-tree"),
    # Batch URLs
    path("batches/", views.BatchListView.as_view(), name="batch-list"),
    path("batches/<uuid:pk>/", views.BatchDetailView.as_view(), name="batch-detail"),
    path("batches/create/", views.BatchCreateView.as_view(), name="batch-create"),
    path(
        "batches/<uuid:pk>/update/",
        views.BatchUpdateView.as_view(),
        name="batch-update",
    ),
    path(
        "batches/<uuid:pk>/delete/",
        views.BatchDeleteView.as_view(),
        name="batch-delete",
    ),
    path(
        "batches/expired/", views.ExpiredBatchesView.as_view(), name="expired-batches"
    ),
    path(
        "batches/expiring-soon/",
        views.ExpiringSoonBatchesView.as_view(),
        name="expiring-soon-batches",
    ),
    # Healthcare specific URLs
    path("medications/", views.MedicationsView.as_view(), name="medications"),
    path(
        "medical-supplies/",
        views.MedicalSuppliesView.as_view(),
        name="medical-supplies",
    ),
    path("vaccines/", views.VaccinesView.as_view(), name="vaccines"),
    path(
        "controlled-substances/",
        views.ControlledSubstancesView.as_view(),
        name="controlled-substances",
    ),
    path(
        "refrigerated-products/",
        views.RefrigeratedProductsView.as_view(),
        name="refrigerated-products",
    ),
    path("low-stock/", views.LowStockProductsView.as_view(), name="low-stock"),
    path("out-of-stock/", views.OutOfStockProductsView.as_view(), name="out-of-stock"),
    # Analytics URLs
    path("stats/", views.InventoryStatsView.as_view(), name="inventory-stats"),
    path("alerts/", views.StockAlertsView.as_view(), name="stock-alerts"),
]
