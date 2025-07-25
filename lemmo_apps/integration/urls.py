from django.urls import path
from . import views

app_name = "integration"

urlpatterns = (
    [
        # Integration URLs
        path("", views.IntegrationView.as_view(), name="integration"),
        path("webhooks/", views.WebhookListView.as_view(), name="webhook-list"),
        path(
            "webhooks/<uuid:pk>/",
            views.WebhookDetailView.as_view(),
            name="webhook-detail",
        ),
        path(
            "webhooks/create/", views.WebhookCreateView.as_view(), name="webhook-create"
        ),
        path(
            "webhooks/<uuid:pk>/update/",
            views.WebhookUpdateView.as_view(),
            name="webhook-update",
        ),
        path(
            "webhooks/<uuid:pk>/delete/",
            views.WebhookDeleteView.as_view(),
            name="webhook-delete",
        ),
        path(
            "webhooks/<uuid:pk>/test/",
            views.WebhookTestView.as_view(),
            name="webhook-test",
        ),
        # API Integration URLs
        path(
            "api-connections/",
            views.APIConnectionListView.as_view(),
            name="api-connection-list",
        ),
        path(
            "api-connections/<uuid:pk>/",
            views.APIConnectionDetailView.as_view(),
            name="api-connection-detail",
        ),
        path(
            "api-connections/create/",
            views.APIConnectionCreateView.as_view(),
            name="api-connection-create",
        ),
        path(
            "api-connections/<uuid:pk>/update/",
            views.APIConnectionUpdateView.as_view(),
            name="api-connection-update",
        ),
        path(
            "api-connections/<uuid:pk>/delete/",
            views.APIConnectionDeleteView.as_view(),
            name="api-connection-delete",
        ),
        path(
            "api-connections/<uuid:pk>/test/",
            views.APIConnectionTestView.as_view(),
            name="api-connection-test",
        ),
        # Data Sync URLs
        path("data-sync/", views.DataSyncListView.as_view(), name="data-sync-list"),
        path(
            "data-sync/<uuid:pk>/",
            views.DataSyncDetailView.as_view(),
            name="data-sync-detail",
        ),
        path(
            "data-sync/create/",
            views.DataSyncCreateView.as_view(),
            name="data-sync-create",
        ),
        path(
            "data-sync/<uuid:pk>/update/",
            views.DataSyncUpdateView.as_view(),
            name="data-sync-update",
        ),
        path(
            "data-sync/<uuid:pk>/delete/",
            views.DataSyncDeleteView.as_view(),
            name="data-sync-delete",
        ),
        path(
            "data-sync/<uuid:pk>/run/",
            views.DataSyncRunView.as_view(),
            name="data-sync-run",
        ),
        # Healthcare specific integration URLs
        path("hl7/", views.HL7IntegrationView.as_view(), name="hl7-integration"),
        path("fhir-sync/", views.FHIRSyncView.as_view(), name="fhir-sync"),
        path(
            "emr-integration/",
            views.EMRIntegrationView.as_view(),
            name="emr-integration",
        ),
        path(
            "pharmacy-system/",
            views.PharmacySystemView.as_view(),
            name="pharmacy-system",
        ),
        # Analytics URLs
        path(
            "integration-stats/",
            views.IntegrationStatsView.as_view(),
            name="integration-stats",
        ),
    ],
)
