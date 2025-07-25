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
from datetime import timedelta

from .models import User, UserSession, UserActivity


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "authentication/user_list.html"
    context_object_name = "users"
    paginate_by = 20

    def get_queryset(self):
        queryset = User.objects.all()
        search = self.request.GET.get("search")
        role = self.request.GET.get("role")
        is_active = self.request.GET.get("is_active")

        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(email__icontains=search)
                | Q(employee_id__icontains=search)
            )

        if role:
            queryset = queryset.filter(role=role)

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active == "true")

        return queryset


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "authentication/user_detail.html"
    context_object_name = "user"


class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = User
    template_name = "authentication/user_form.html"
    fields = [
        "email",
        "first_name",
        "last_name",
        "role",
        "phone_number",
        "employee_id",
        "department",
        "license_number",
        "is_active",
        "is_staff",
    ]
    success_url = reverse_lazy("authentication:user-list")
    permission_required = "authentication.add_user"


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    template_name = "authentication/user_form.html"
    fields = [
        "email",
        "first_name",
        "last_name",
        "role",
        "phone_number",
        "employee_id",
        "department",
        "license_number",
        "is_active",
        "is_staff",
    ]
    success_url = reverse_lazy("authentication:user-list")
    permission_required = "authentication.change_user"


class UserDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = User
    template_name = "authentication/user_confirm_delete.html"
    success_url = reverse_lazy("authentication:user-list")
    permission_required = "authentication.delete_user"


class UserActivateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    fields = []
    permission_required = "authentication.change_user"

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = True
        user.save()
        return JsonResponse({"status": "success"})


class UserDeactivateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    fields = []
    permission_required = "authentication.change_user"

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        return JsonResponse({"status": "success"})


class UserSessionListView(LoginRequiredMixin, ListView):
    model = UserSession
    template_name = "authentication/session_list.html"
    context_object_name = "sessions"
    paginate_by = 20

    def get_queryset(self):
        queryset = UserSession.objects.all()
        user_id = self.request.GET.get("user_id")
        is_active = self.request.GET.get("is_active")

        if user_id:
            queryset = queryset.filter(user_id=user_id)

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active == "true")

        return queryset


class UserActivityListView(LoginRequiredMixin, ListView):
    model = UserActivity
    template_name = "authentication/activity_list.html"
    context_object_name = "activities"
    paginate_by = 20

    def get_queryset(self):
        queryset = UserActivity.objects.all()
        user_id = self.request.GET.get("user_id")
        activity_type = self.request.GET.get("activity_type")

        if user_id:
            queryset = queryset.filter(user_id=user_id)

        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)

        return queryset


class HealthcareProfessionalsView(LoginRequiredMixin, ListView):
    model = User
    template_name = "authentication/healthcare_professionals.html"
    context_object_name = "professionals"

    def get_queryset(self):
        return User.objects.filter(role__in=["PHARMACIST", "NURSE", "DOCTOR"]).filter(
            is_active=True
        )


class LogisticsStaffView(LoginRequiredMixin, ListView):
    model = User
    template_name = "authentication/logistics_staff.html"
    context_object_name = "staff"

    def get_queryset(self):
        return User.objects.filter(
            role__in=[
                "LOGISTICS_MANAGER",
                "WAREHOUSE_MANAGER",
                "SUPPLY_CHAIN_SPECIALIST",
                "INVENTORY_CLERK",
                "DISPATCHER",
                "DRIVER",
            ]
        ).filter(is_active=True)


class UserStatsView(LoginRequiredMixin, ListView):
    model = User
    template_name = "authentication/user_stats.html"
    context_object_name = "stats"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate statistics
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        healthcare_professionals = User.objects.filter(
            role__in=["PHARMACIST", "NURSE", "DOCTOR"]
        ).count()
        logistics_staff = User.objects.filter(
            role__in=[
                "LOGISTICS_MANAGER",
                "WAREHOUSE_MANAGER",
                "SUPPLY_CHAIN_SPECIALIST",
                "INVENTORY_CLERK",
                "DISPATCHER",
                "DRIVER",
            ]
        ).count()

        # Role distribution
        role_stats = User.objects.values("role").annotate(count=Count("role"))

        # Recent activity
        recent_activities = UserActivity.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).count()

        context.update(
            {
                "total_users": total_users,
                "active_users": active_users,
                "healthcare_professionals": healthcare_professionals,
                "logistics_staff": logistics_staff,
                "role_stats": role_stats,
                "recent_activities": recent_activities,
            }
        )

        return context
