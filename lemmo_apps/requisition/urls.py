from django.urls import path
from . import views

app_name = "requisition"

urlpatterns = [
    # Requisition URLs
    path("requisitions/", views.RequisitionListView.as_view(), name="requisition-list"),
    path(
        "requisitions/<uuid:pk>/",
        views.RequisitionDetailView.as_view(),
        name="requisition-detail",
    ),
    path(
        "requisitions/create/",
        views.RequisitionCreateView.as_view(),
        name="requisition-create",
    ),
    path(
        "requisitions/<uuid:pk>/update/",
        views.RequisitionUpdateView.as_view(),
        name="requisition-update",
    ),
    path(
        "requisitions/<uuid:pk>/delete/",
        views.RequisitionDeleteView.as_view(),
        name="requisition-delete",
    ),
    path(
        "requisitions/<uuid:pk>/submit/",
        views.RequisitionSubmitView.as_view(),
        name="requisition-submit",
    ),
    path(
        "requisitions/<uuid:pk>/approve/",
        views.RequisitionApproveView.as_view(),
        name="requisition-approve",
    ),
    path(
        "requisitions/<uuid:pk>/reject/",
        views.RequisitionRejectView.as_view(),
        name="requisition-reject",
    ),
    path(
        "requisitions/<uuid:pk>/fulfill/",
        views.RequisitionFulfillView.as_view(),
        name="requisition-fulfill",
    ),
    # Requisition Items
    path(
        "requisitions/<uuid:requisition_id>/items/",
        views.RequisitionItemListView.as_view(),
        name="requisition-items",
    ),
    path(
        "requisition-items/<uuid:pk>/",
        views.RequisitionItemDetailView.as_view(),
        name="requisition-item-detail",
    ),
    path(
        "requisition-items/create/",
        views.RequisitionItemCreateView.as_view(),
        name="requisition-item-create",
    ),
    path(
        "requisition-items/<uuid:pk>/update/",
        views.RequisitionItemUpdateView.as_view(),
        name="requisition-item-update",
    ),
    path(
        "requisition-items/<uuid:pk>/delete/",
        views.RequisitionItemDeleteView.as_view(),
        name="requisition-item-delete",
    ),
    # Healthcare specific URLs
    path(
        "pending-requisitions/",
        views.PendingRequisitionsView.as_view(),
        name="pending-requisitions",
    ),
    path(
        "approved-requisitions/",
        views.ApprovedRequisitionsView.as_view(),
        name="approved-requisitions",
    ),
    path(
        "rejected-requisitions/",
        views.RejectedRequisitionsView.as_view(),
        name="rejected-requisitions",
    ),
    path(
        "fulfilled-requisitions/",
        views.FulfilledRequisitionsView.as_view(),
        name="fulfilled-requisitions",
    ),
    # Analytics URLs
    path(
        "requisition-stats/",
        views.RequisitionStatsView.as_view(),
        name="requisition-stats",
    ),
]
