from django.urls import path
from . import views

app_name = "location"

urlpatterns = [
    # Location URLs
    path("locations/", views.LocationListView.as_view(), name="location-list"),
    path(
        "locations/<uuid:pk>/",
        views.LocationDetailView.as_view(),
        name="location-detail",
    ),
    path(
        "locations/create/", views.LocationCreateView.as_view(), name="location-create"
    ),
    path(
        "locations/<uuid:pk>/update/",
        views.LocationUpdateView.as_view(),
        name="location-update",
    ),
    path(
        "locations/<uuid:pk>/delete/",
        views.LocationDeleteView.as_view(),
        name="location-delete",
    ),
    path(
        "location-types/",
        views.LocationTypeListView.as_view(),
        name="location-type-list",
    ),
    # Facility URLs
    path("facilities/", views.FacilityListView.as_view(), name="facility-list"),
    path(
        "facilities/<uuid:pk>/",
        views.FacilityDetailView.as_view(),
        name="facility-detail",
    ),
    path(
        "facilities/create/", views.FacilityCreateView.as_view(), name="facility-create"
    ),
    path(
        "facilities/<uuid:pk>/update/",
        views.FacilityUpdateView.as_view(),
        name="facility-update",
    ),
    path(
        "facilities/<uuid:pk>/delete/",
        views.FacilityDeleteView.as_view(),
        name="facility-delete",
    ),
    path(
        "facility-types/",
        views.FacilityTypeListView.as_view(),
        name="facility-type-list",
    ),
    # Facility Departments
    path(
        "facilities/<uuid:facility_id>/departments/",
        views.FacilityDepartmentListView.as_view(),
        name="facility-departments",
    ),
    path(
        "departments/<uuid:pk>/",
        views.FacilityDepartmentDetailView.as_view(),
        name="department-detail",
    ),
    path(
        "departments/create/",
        views.FacilityDepartmentCreateView.as_view(),
        name="department-create",
    ),
    path(
        "departments/<uuid:pk>/update/",
        views.FacilityDepartmentUpdateView.as_view(),
        name="department-update",
    ),
    path(
        "departments/<uuid:pk>/delete/",
        views.FacilityDepartmentDeleteView.as_view(),
        name="department-delete",
    ),
    # Facility Contacts
    path(
        "facilities/<uuid:facility_id>/contacts/",
        views.FacilityContactListView.as_view(),
        name="facility-contacts",
    ),
    path(
        "contacts/<uuid:pk>/",
        views.FacilityContactDetailView.as_view(),
        name="contact-detail",
    ),
    path(
        "contacts/create/",
        views.FacilityContactCreateView.as_view(),
        name="contact-create",
    ),
    path(
        "contacts/<uuid:pk>/update/",
        views.FacilityContactUpdateView.as_view(),
        name="contact-update",
    ),
    path(
        "contacts/<uuid:pk>/delete/",
        views.FacilityContactDeleteView.as_view(),
        name="contact-delete",
    ),
    # Healthcare specific URLs
    path("hospitals/", views.HospitalsView.as_view(), name="hospitals"),
    path("clinics/", views.ClinicsView.as_view(), name="clinics"),
    path("pharmacies/", views.PharmaciesView.as_view(), name="pharmacies"),
    path("laboratories/", views.LaboratoriesView.as_view(), name="laboratories"),
    path("warehouses/", views.WarehousesView.as_view(), name="warehouses"),
    path(
        "active-facilities/",
        views.ActiveFacilitiesView.as_view(),
        name="active-facilities",
    ),
    # Analytics URLs
    path("stats/", views.FacilityStatsView.as_view(), name="facility-stats"),
]
