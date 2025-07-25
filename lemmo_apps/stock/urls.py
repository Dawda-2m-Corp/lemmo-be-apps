from django.urls import path
from . import views

app_name = "stock"

urlpatterns = [
    # Stock URLs
    path("stock/", views.StockListView.as_view(), name="stock-list"),
    path("stock/<uuid:pk>/", views.StockDetailView.as_view(), name="stock-detail"),
    path("stock/create/", views.StockCreateView.as_view(), name="stock-create"),
    path(
        "stock/<uuid:pk>/update/", views.StockUpdateView.as_view(), name="stock-update"
    ),
    path(
        "stock/<uuid:pk>/delete/", views.StockDeleteView.as_view(), name="stock-delete"
    ),
    # Stock Transaction URLs
    path(
        "transactions/",
        views.StockTransactionListView.as_view(),
        name="transaction-list",
    ),
    path(
        "transactions/<uuid:pk>/",
        views.StockTransactionDetailView.as_view(),
        name="transaction-detail",
    ),
    path(
        "transactions/create/",
        views.StockTransactionCreateView.as_view(),
        name="transaction-create",
    ),
    path(
        "transactions/<uuid:pk>/update/",
        views.StockTransactionUpdateView.as_view(),
        name="transaction-update",
    ),
    path(
        "transactions/<uuid:pk>/delete/",
        views.StockTransactionDeleteView.as_view(),
        name="transaction-delete",
    ),
    # Healthcare specific URLs
    path("low-stock/", views.LowStockView.as_view(), name="low-stock"),
    path("out-of-stock/", views.OutOfStockView.as_view(), name="out-of-stock"),
    path("overstocked/", views.OverstockedView.as_view(), name="overstocked"),
    path("expiring-stock/", views.ExpiringStockView.as_view(), name="expiring-stock"),
    path("expired-stock/", views.ExpiredStockView.as_view(), name="expired-stock"),
    # Analytics URLs
    path("stock-stats/", views.StockStatsView.as_view(), name="stock-stats"),
    path(
        "transaction-stats/",
        views.TransactionStatsView.as_view(),
        name="transaction-stats",
    ),
]
