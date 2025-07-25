from django.urls import path
from . import views

app_name = "fhir_api"

urlpatterns = (
    [
        # FHIR API URLs
        path("", views.FHIRAPIView.as_view(), name="fhir-api"),
        path("patient/", views.PatientListView.as_view(), name="patient-list"),
        path(
            "patient/<uuid:pk>/",
            views.PatientDetailView.as_view(),
            name="patient-detail",
        ),
        path("medication/", views.MedicationListView.as_view(), name="medication-list"),
        path(
            "medication/<uuid:pk>/",
            views.MedicationDetailView.as_view(),
            name="medication-detail",
        ),
        path(
            "medication-request/",
            views.MedicationRequestListView.as_view(),
            name="medication-request-list",
        ),
        path(
            "medication-request/<uuid:pk>/",
            views.MedicationRequestDetailView.as_view(),
            name="medication-request-detail",
        ),
        path(
            "organization/",
            views.OrganizationListView.as_view(),
            name="organization-list",
        ),
        path(
            "organization/<uuid:pk>/",
            views.OrganizationDetailView.as_view(),
            name="organization-detail",
        ),
        path(
            "practitioner/",
            views.PractitionerListView.as_view(),
            name="practitioner-list",
        ),
        path(
            "practitioner/<uuid:pk>/",
            views.PractitionerDetailView.as_view(),
            name="practitioner-detail",
        ),
        # Healthcare specific FHIR URLs
        path(
            "healthcare-facility/",
            views.HealthcareFacilityListView.as_view(),
            name="healthcare-facility-list",
        ),
        path(
            "healthcare-facility/<uuid:pk>/",
            views.HealthcareFacilityDetailView.as_view(),
            name="healthcare-facility-detail",
        ),
        path(
            "supply-delivery/",
            views.SupplyDeliveryListView.as_view(),
            name="supply-delivery-list",
        ),
        path(
            "supply-delivery/<uuid:pk>/",
            views.SupplyDeliveryDetailView.as_view(),
            name="supply-delivery-detail",
        ),
        path(
            "supply-request/",
            views.SupplyRequestListView.as_view(),
            name="supply-request-list",
        ),
        path(
            "supply-request/<uuid:pk>/",
            views.SupplyRequestDetailView.as_view(),
            name="supply-request-detail",
        ),
    ],
)
