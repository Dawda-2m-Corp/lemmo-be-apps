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
from django.db.models import Q, Count
from django.utils import timezone

from .models.requisition import Requisition, RequisitionItem


class RequisitionListView(LoginRequiredMixin, ListView):
    model = Requisition
    template_name = "requisition/requisition_list.html"
    context_object_name = "requisitions"
    paginate_by = 20

    def get_queryset(self):
        queryset = Requisition.objects.all()
        status = self.request.GET.get("status")
        facility_id = self.request.GET.get("facility_id")
        requested_by = self.request.GET.get("requested_by")

        if status:
            queryset = queryset.filter(status=status)

        if facility_id:
            queryset = queryset.filter(facility_id=facility_id)

        if requested_by:
            queryset = queryset.filter(requested_by_id=requested_by)

        return queryset


class RequisitionDetailView(LoginRequiredMixin, DetailView):
    model = Requisition
    template_name = "requisition/requisition_detail.html"
    context_object_name = "requisition"


class RequisitionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Requisition
    template_name = "requisition/requisition_form.html"
    fields = ["facility", "department", "priority", "requested_by", "notes"]
    success_url = reverse_lazy("requisition:requisition-list")
    permission_required = "requisition.add_requisition"


class RequisitionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Requisition
    template_name = "requisition/requisition_form.html"
    fields = ["facility", "department", "priority", "requested_by", "notes"]
    success_url = reverse_lazy("requisition:requisition-list")
    permission_required = "requisition.change_requisition"


class RequisitionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Requisition
    template_name = "requisition/requisition_confirm_delete.html"
    success_url = reverse_lazy("requisition:requisition-list")
    permission_required = "requisition.delete_requisition"


class RequisitionSubmitView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Requisition
    fields = []
    permission_required = "requisition.change_requisition"

    def post(self, request, *args, **kwargs):
        requisition = self.get_object()
        requisition.status = "SUBMITTED"
        requisition.submitted_at = timezone.now()
        requisition.save()
        return JsonResponse({"status": "success"})


class RequisitionApproveView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Requisition
    fields = []
    permission_required = "requisition.change_requisition"

    def post(self, request, *args, **kwargs):
        requisition = self.get_object()
        requisition.status = "APPROVED"
        requisition.approved_at = timezone.now()
        requisition.approved_by = request.user
        requisition.save()
        return JsonResponse({"status": "success"})


class RequisitionRejectView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Requisition
    fields = []
    permission_required = "requisition.change_requisition"

    def post(self, request, *args, **kwargs):
        requisition = self.get_object()
        requisition.status = "REJECTED"
        requisition.rejected_at = timezone.now()
        requisition.rejected_by = request.user
        requisition.save()
        return JsonResponse({"status": "success"})


class RequisitionFulfillView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Requisition
    fields = []
    permission_required = "requisition.change_requisition"

    def post(self, request, *args, **kwargs):
        requisition = self.get_object()
        requisition.status = "FULFILLED"
        requisition.fulfilled_at = timezone.now()
        requisition.fulfilled_by = request.user
        requisition.save()
        return JsonResponse({"status": "success"})


class RequisitionItemListView(LoginRequiredMixin, ListView):
    model = RequisitionItem
    template_name = "requisition/requisition_item_list.html"
    context_object_name = "items"
    paginate_by = 20

    def get_queryset(self):
        requisition_id = self.kwargs.get("requisition_id")
        return RequisitionItem.objects.filter(requisition_id=requisition_id)


class RequisitionItemDetailView(LoginRequiredMixin, DetailView):
    model = RequisitionItem
    template_name = "requisition/requisition_item_detail.html"
    context_object_name = "item"


class RequisitionItemCreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateView
):
    model = RequisitionItem
    template_name = "requisition/requisition_item_form.html"
    fields = ["requisition", "product", "quantity", "notes"]
    success_url = reverse_lazy("requisition:requisition-list")
    permission_required = "requisition.add_requisitionitem"


class RequisitionItemUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateView
):
    model = RequisitionItem
    template_name = "requisition/requisition_item_form.html"
    fields = ["requisition", "product", "quantity", "notes"]
    success_url = reverse_lazy("requisition:requisition-list")
    permission_required = "requisition.change_requisitionitem"


class RequisitionItemDeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteView
):
    model = RequisitionItem
    template_name = "requisition/requisition_item_confirm_delete.html"
    success_url = reverse_lazy("requisition:requisition-list")
    permission_required = "requisition.delete_requisitionitem"
