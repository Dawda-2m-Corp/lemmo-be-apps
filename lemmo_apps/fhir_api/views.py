from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Q, Count
from django.utils import timezone

from lemmo_apps.inventory.models.product import Product
from lemmo_apps.location.models.facility import Facility
from lemmo_apps.authentication.models import User


class FHIRAPIView(LoginRequiredMixin, TemplateView):
    template_name = "fhir_api/fhir_api.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get FHIR API statistics
        total_patients = 0  # Would need Patient model
        total_medications = Product.objects.filter(product_type="MEDICATION").count()
        total_organizations = Facility.objects.count()
        total_practitioners = User.objects.filter(
            role__in=["PHARMACIST", "NURSE", "DOCTOR"]
        ).count()

        context.update(
            {
                "total_patients": total_patients,
                "total_medications": total_medications,
                "total_organizations": total_organizations,
                "total_practitioners": total_practitioners,
            }
        )

        return context


class PatientListView(LoginRequiredMixin, ListView):
    model = None  # Would need Patient model
    template_name = "fhir_api/patient_list.html"
    context_object_name = "patients"

    def get_queryset(self):
        # This would need to be implemented with a Patient model
        return []


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = None  # Would need Patient model
    template_name = "fhir_api/patient_detail.html"
    context_object_name = "patient"


class MedicationListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "fhir_api/medication_list.html"
    context_object_name = "medications"

    def get_queryset(self):
        return Product.objects.filter(product_type="MEDICATION")


class MedicationDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "fhir_api/medication_detail.html"
    context_object_name = "medication"


class MedicationRequestListView(LoginRequiredMixin, ListView):
    model = None  # Would need MedicationRequest model
    template_name = "fhir_api/medication_request_list.html"
    context_object_name = "medication_requests"

    def get_queryset(self):
        # This would need to be implemented with a MedicationRequest model
        return []


class MedicationRequestDetailView(LoginRequiredMixin, DetailView):
    model = None  # Would need MedicationRequest model
    template_name = "fhir_api/medication_request_detail.html"
    context_object_name = "medication_request"


class OrganizationListView(LoginRequiredMixin, ListView):
    model = Facility
    template_name = "fhir_api/organization_list.html"
    context_object_name = "organizations"

    def get_queryset(self):
        return Facility.objects.all()


class OrganizationDetailView(LoginRequiredMixin, DetailView):
    model = Facility
    template_name = "fhir_api/organization_detail.html"
    context_object_name = "organization"


class PractitionerListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "fhir_api/practitioner_list.html"
    context_object_name = "practitioners"

    def get_queryset(self):
        return User.objects.filter(role__in=["PHARMACIST", "NURSE", "DOCTOR"])


class PractitionerDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "fhir_api/practitioner_detail.html"
    context_object_name = "practitioner"


class HealthcareFacilityListView(LoginRequiredMixin, ListView):
    model = Facility
    template_name = "fhir_api/healthcare_facility_list.html"
    context_object_name = "healthcare_facilities"

    def get_queryset(self):
        return Facility.objects.filter(
            category__in=["HOSPITAL", "CLINIC", "PHARMACY", "LABORATORY"]
        )


class HealthcareFacilityDetailView(LoginRequiredMixin, DetailView):
    model = Facility
    template_name = "fhir_api/healthcare_facility_detail.html"
    context_object_name = "healthcare_facility"
