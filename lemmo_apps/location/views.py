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

from .models.location import Location, LocationType
from .models.facility import Facility, FacilityType, FacilityDepartment, FacilityContact


class LocationListView(LoginRequiredMixin, ListView):
    model = Location
    template_name = "location/location_list.html"
    context_object_name = "locations"
    paginate_by = 20

    def get_queryset(self):
        queryset = Location.objects.all()
        type_id = self.request.GET.get("type_id")
        is_active = self.request.GET.get("is_active")
        search = self.request.GET.get("search")

        if type_id:
            queryset = queryset.filter(type_id=type_id)

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active == "true")

        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset


class LocationDetailView(LoginRequiredMixin, DetailView):
    model = Location
    template_name = "location/location_detail.html"
    context_object_name = "location"


class LocationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Location
    template_name = "location/location_form.html"
    fields = ["name", "type", "parent"]
    success_url = reverse_lazy("location:location-list")
    permission_required = "location.add_location"


class LocationUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Location
    template_name = "location/location_form.html"
    fields = ["name", "type", "parent"]
    success_url = reverse_lazy("location:location-list")
    permission_required = "location.change_location"


class LocationDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Location
    template_name = "location/location_confirm_delete.html"
    success_url = reverse_lazy("location:location-list")
    permission_required = "location.delete_location"


class LocationTypeListView(LoginRequiredMixin, ListView):
    model = LocationType
    template_name = "location/location_type_list.html"
    context_object_name = "location_types"
    paginate_by = 20


class FacilityListView(LoginRequiredMixin, ListView):
    model = Facility
    template_name = "location/facility_list.html"
    context_object_name = "facilities"
    paginate_by = 20

    def get_queryset(self):
        queryset = Facility.objects.all()
        facility_type_id = self.request.GET.get("facility_type_id")
        category = self.request.GET.get("category")
        operational_status = self.request.GET.get("operational_status")
        is_active = self.request.GET.get("is_active")
        search = self.request.GET.get("search")

        if facility_type_id:
            queryset = queryset.filter(facility_type_id=facility_type_id)

        if category:
            queryset = queryset.filter(category=category)

        if operational_status:
            queryset = queryset.filter(operational_status=operational_status)

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active == "true")

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(address__icontains=search)
                | Q(city__icontains=search)
                | Q(state__icontains=search)
            )

        return queryset


class FacilityDetailView(LoginRequiredMixin, DetailView):
    model = Facility
    template_name = "location/facility_detail.html"
    context_object_name = "facility"


class FacilityCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Facility
    template_name = "location/facility_form.html"
    fields = [
        "name",
        "facility_type",
        "category",
        "operational_status",
        "address",
        "city",
        "state",
        "postal_code",
        "country",
        "phone",
        "email",
        "website",
        "license_number",
        "license_expiry_date",
        "accreditation",
        "bed_count",
    ]
    success_url = reverse_lazy("location:facility-list")
    permission_required = "location.add_facility"


class FacilityUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Facility
    template_name = "location/facility_form.html"
    fields = [
        "name",
        "facility_type",
        "category",
        "operational_status",
        "address",
        "city",
        "state",
        "postal_code",
        "country",
        "phone",
        "email",
        "website",
        "license_number",
        "license_expiry_date",
        "accreditation",
        "bed_count",
    ]
    success_url = reverse_lazy("location:facility-list")
    permission_required = "location.change_facility"


class FacilityDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Facility
    template_name = "location/facility_confirm_delete.html"
    success_url = reverse_lazy("location:facility-list")
    permission_required = "location.delete_facility"


class FacilityTypeListView(LoginRequiredMixin, ListView):
    model = FacilityType
    template_name = "location/facility_type_list.html"
    context_object_name = "facility_types"
    paginate_by = 20


class FacilityDepartmentListView(LoginRequiredMixin, ListView):
    model = FacilityDepartment
    template_name = "location/facility_department_list.html"
    context_object_name = "departments"
    paginate_by = 20

    def get_queryset(self):
        facility_id = self.kwargs.get("facility_id")
        return FacilityDepartment.objects.filter(facility_id=facility_id)


class FacilityDepartmentDetailView(LoginRequiredMixin, DetailView):
    model = FacilityDepartment
    template_name = "location/facility_department_detail.html"
    context_object_name = "department"


class FacilityDepartmentCreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateView
):
    model = FacilityDepartment
    template_name = "location/facility_department_form.html"
    fields = [
        "name",
        "description",
        "facility",
        "department_type",
        "head_of_department",
        "phone",
        "email",
        "is_active",
    ]
    success_url = reverse_lazy("location:facility-list")
    permission_required = "location.add_facilitydepartment"


class FacilityDepartmentUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateView
):
    model = FacilityDepartment
    template_name = "location/facility_department_form.html"
    fields = [
        "name",
        "description",
        "facility",
        "department_type",
        "head_of_department",
        "phone",
        "email",
        "is_active",
    ]
    success_url = reverse_lazy("location:facility-list")
    permission_required = "location.change_facilitydepartment"


class FacilityDepartmentDeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteView
):
    model = FacilityDepartment
    template_name = "location/facility_department_confirm_delete.html"
    success_url = reverse_lazy("location:facility-list")
    permission_required = "location.delete_facilitydepartment"


class FacilityContactListView(LoginRequiredMixin, ListView):
    model = FacilityContact
    template_name = "location/facility_contact_list.html"
    context_object_name = "contacts"
    paginate_by = 20

    def get_queryset(self):
        facility_id = self.kwargs.get("facility_id")
        return FacilityContact.objects.filter(facility_id=facility_id)


class FacilityContactDetailView(LoginRequiredMixin, DetailView):
    model = FacilityContact
    template_name = "location/facility_contact_detail.html"
    context_object_name = "contact"


class FacilityContactCreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateView
):
    model = FacilityContact
    template_name = "location/facility_contact_form.html"
    fields = ["facility", "name", "title", "department", "phone", "email", "is_primary"]
    success_url = reverse_lazy("location:facility-list")
    permission_required = "location.add_facilitycontact"


class FacilityContactUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateView
):
    model = FacilityContact
    template_name = "location/facility_contact_form.html"
    fields = ["facility", "name", "title", "department", "phone", "email", "is_primary"]
    success_url = reverse_lazy("location:facility-list")
    permission_required = "location.change_facilitycontact"


class FacilityContactDeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteView
):
    model = FacilityContact
    template_name = "location/facility_contact_confirm_delete.html"
    success_url = reverse_lazy("location:facility-list")
    permission_required = "location.delete_facilitycontact"


class HospitalsView(LoginRequiredMixin, ListView):
    model = Facility
    template_name = "location/hospitals.html"
    context_object_name = "hospitals"

    def get_queryset(self):
        return Facility.objects.filter(category="HOSPITAL", operational_status="ACTIVE")


class ClinicsView(LoginRequiredMixin, ListView):
    model = Facility
    template_name = "location/clinics.html"
    context_object_name = "clinics"

    def get_queryset(self):
        return Facility.objects.filter(category="CLINIC", operational_status="ACTIVE")


class PharmaciesView(LoginRequiredMixin, ListView):
    model = Facility
    template_name = "location/pharmacies.html"
    context_object_name = "pharmacies"

    def get_queryset(self):
        return Facility.objects.filter(category="PHARMACY", operational_status="ACTIVE")


class LaboratoriesView(LoginRequiredMixin, ListView):
    model = Facility
    template_name = "location/laboratories.html"
    context_object_name = "laboratories"

    def get_queryset(self):
        return Facility.objects.filter(
            category="LABORATORY", operational_status="ACTIVE"
        )


class WarehousesView(LoginRequiredMixin, ListView):
    model = Facility
    template_name = "location/warehouses.html"
    context_object_name = "warehouses"

    def get_queryset(self):
        return Facility.objects.filter(
            category="WAREHOUSE", operational_status="ACTIVE"
        )


class ActiveFacilitiesView(LoginRequiredMixin, ListView):
    model = Facility
    template_name = "location/active_facilities.html"
    context_object_name = "facilities"

    def get_queryset(self):
        return Facility.objects.filter(operational_status="ACTIVE")


class FacilityStatsView(LoginRequiredMixin, ListView):
    model = Facility
    template_name = "location/facility_stats.html"
    context_object_name = "stats"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate statistics
        total_facilities = Facility.objects.count()
        active_facilities = Facility.objects.filter(operational_status="ACTIVE").count()

        # Facility type distribution
        facility_type_stats = Facility.objects.values("facility_type__name").annotate(
            count=Count("facility_type")
        )

        # Category distribution
        category_stats = Facility.objects.values("category").annotate(
            count=Count("category")
        )

        # Operational status distribution
        status_stats = Facility.objects.values("operational_status").annotate(
            count=Count("operational_status")
        )

        # Healthcare specific stats
        hospitals = Facility.objects.filter(category="HOSPITAL").count()
        clinics = Facility.objects.filter(category="CLINIC").count()
        pharmacies = Facility.objects.filter(category="PHARMACY").count()
        laboratories = Facility.objects.filter(category="LABORATORY").count()
        warehouses = Facility.objects.filter(category="WAREHOUSE").count()

        context.update(
            {
                "total_facilities": total_facilities,
                "active_facilities": active_facilities,
                "facility_type_stats": facility_type_stats,
                "category_stats": category_stats,
                "status_stats": status_stats,
                "hospitals": hospitals,
                "clinics": clinics,
                "pharmacies": pharmacies,
                "laboratories": laboratories,
                "warehouses": warehouses,
            }
        )

        return context
