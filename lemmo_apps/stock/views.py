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

from .models.stock import Stock
from .models.transaction import StockTransaction


class StockListView(LoginRequiredMixin, ListView):
    model = Stock
    template_name = "stock/stock_list.html"
    context_object_name = "stock_levels"
    paginate_by = 20

    def get_queryset(self):
        queryset = Stock.objects.all()
        facility_id = self.request.GET.get("facility_id")
        item_id = self.request.GET.get("item_id")
        low_stock = self.request.GET.get("low_stock")

        if facility_id:
            queryset = queryset.filter(facility_id=facility_id)

        if item_id:
            queryset = queryset.filter(item_id=item_id)

        if low_stock is not None:
            if low_stock == "true":
                queryset = queryset.filter(quantity__lte=F("minimum_stock_level"))
            else:
                queryset = queryset.filter(quantity__gt=F("minimum_stock_level"))

        return queryset


class StockDetailView(LoginRequiredMixin, DetailView):
    model = Stock
    template_name = "stock/stock_detail.html"
    context_object_name = "stock"


class StockCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Stock
    template_name = "stock/stock_form.html"
    fields = [
        "item",
        "facility",
        "quantity",
        "minimum_stock_level",
        "maximum_stock_level",
    ]
    success_url = reverse_lazy("stock:stock-list")
    permission_required = "stock.add_stock"


class StockUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Stock
    template_name = "stock/stock_form.html"
    fields = [
        "item",
        "facility",
        "quantity",
        "minimum_stock_level",
        "maximum_stock_level",
    ]
    success_url = reverse_lazy("stock:stock-list")
    permission_required = "stock.change_stock"


class StockDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Stock
    template_name = "stock/stock_confirm_delete.html"
    success_url = reverse_lazy("stock:stock-list")
    permission_required = "stock.delete_stock"


class StockTransactionListView(LoginRequiredMixin, ListView):
    model = StockTransaction
    template_name = "stock/transaction_list.html"
    context_object_name = "transactions"
    paginate_by = 20

    def get_queryset(self):
        queryset = StockTransaction.objects.all()
        facility_id = self.request.GET.get("facility_id")
        item_id = self.request.GET.get("item_id")
        transaction_type = self.request.GET.get("transaction_type")

        if facility_id:
            queryset = queryset.filter(facility_id=facility_id)

        if item_id:
            queryset = queryset.filter(item_id=item_id)

        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)

        return queryset


class StockTransactionDetailView(LoginRequiredMixin, DetailView):
    model = StockTransaction
    template_name = "stock/transaction_detail.html"
    context_object_name = "transaction"


class StockTransactionCreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateView
):
    model = StockTransaction
    template_name = "stock/transaction_form.html"
    fields = [
        "item",
        "facility",
        "transaction_type",
        "quantity",
        "reference_number",
        "notes",
        "transaction_date",
    ]
    success_url = reverse_lazy("stock:transaction-list")
    permission_required = "stock.add_stocktransaction"


class StockTransactionUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateView
):
    model = StockTransaction
    template_name = "stock/transaction_form.html"
    fields = [
        "item",
        "facility",
        "transaction_type",
        "quantity",
        "reference_number",
        "notes",
        "transaction_date",
    ]
    success_url = reverse_lazy("stock:transaction-list")
    permission_required = "stock.change_stocktransaction"


class StockTransactionDeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteView
):
    model = StockTransaction
    template_name = "stock/transaction_confirm_delete.html"
    success_url = reverse_lazy("stock:transaction-list")
    permission_required = "stock.delete_stocktransaction"


class LowStockView(LoginRequiredMixin, ListView):
    model = Stock
    template_name = "stock/low_stock.html"
    context_object_name = "low_stock_items"

    def get_queryset(self):
        return Stock.objects.filter(quantity__lte=F("minimum_stock_level"))


class OutOfStockView(LoginRequiredMixin, ListView):
    model = Stock
    template_name = "stock/out_of_stock.html"
    context_object_name = "out_of_stock_items"

    def get_queryset(self):
        return Stock.objects.filter(quantity=0)


class OverstockedView(LoginRequiredMixin, ListView):
    model = Stock
    template_name = "stock/overstocked.html"
    context_object_name = "overstocked_items"

    def get_queryset(self):
        return Stock.objects.filter(quantity__gt=F("maximum_stock_level"))


class ExpiringStockView(LoginRequiredMixin, ListView):
    model = Stock
    template_name = "stock/expiring_stock.html"
    context_object_name = "expiring_items"

    def get_queryset(self):
        # This would need to be implemented based on your item model structure
        # For now, returning empty queryset
        return Stock.objects.none()


class ExpiredStockView(LoginRequiredMixin, ListView):
    model = Stock
    template_name = "stock/expired_stock.html"
    context_object_name = "expired_items"

    def get_queryset(self):
        # This would need to be implemented based on your item model structure
        # For now, returning empty queryset
        return Stock.objects.none()


class StockStatsView(LoginRequiredMixin, ListView):
    model = Stock
    template_name = "stock/stock_stats.html"
    context_object_name = "stats"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate statistics
        total_stock_items = Stock.objects.count()
        low_stock_items = Stock.objects.filter(
            quantity__lte=F("minimum_stock_level")
        ).count()
        out_of_stock_items = Stock.objects.filter(quantity=0).count()
        overstocked_items = Stock.objects.filter(
            quantity__gt=F("maximum_stock_level")
        ).count()

        # Transaction statistics
        total_transactions = StockTransaction.objects.count()
        recent_transactions = StockTransaction.objects.filter(
            transaction_date__gte=timezone.now() - timedelta(days=7)
        ).count()

        # Transaction type distribution
        transaction_type_stats = StockTransaction.objects.values(
            "transaction_type"
        ).annotate(count=Count("transaction_type"))

        context.update(
            {
                "total_stock_items": total_stock_items,
                "low_stock_items": low_stock_items,
                "out_of_stock_items": out_of_stock_items,
                "overstocked_items": overstocked_items,
                "total_transactions": total_transactions,
                "recent_transactions": recent_transactions,
                "transaction_type_stats": transaction_type_stats,
            }
        )

        return context


class TransactionStatsView(LoginRequiredMixin, ListView):
    model = StockTransaction
    template_name = "stock/transaction_stats.html"
    context_object_name = "stats"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate transaction statistics
        total_transactions = StockTransaction.objects.count()

        # Recent transactions
        today_transactions = StockTransaction.objects.filter(
            transaction_date__date=timezone.now().date()
        ).count()

        week_transactions = StockTransaction.objects.filter(
            transaction_date__gte=timezone.now() - timedelta(days=7)
        ).count()

        month_transactions = StockTransaction.objects.filter(
            transaction_date__gte=timezone.now() - timedelta(days=30)
        ).count()

        # Transaction type distribution
        transaction_type_stats = StockTransaction.objects.values(
            "transaction_type"
        ).annotate(count=Count("transaction_type"))

        # Facility distribution
        facility_stats = StockTransaction.objects.values("facility__name").annotate(
            count=Count("facility")
        )

        context.update(
            {
                "total_transactions": total_transactions,
                "today_transactions": today_transactions,
                "week_transactions": week_transactions,
                "month_transactions": month_transactions,
                "transaction_type_stats": transaction_type_stats,
                "facility_stats": facility_stats,
            }
        )

        return context
