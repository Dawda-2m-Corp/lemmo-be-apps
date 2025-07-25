from django.urls import path
from . import views

app_name = "authentication"

urlpatterns = [
    path("users/", views.UserListView.as_view(), name="user-list"),
    path("users/<uuid:pk>/", views.UserDetailView.as_view(), name="user-detail"),
    path("users/create/", views.UserCreateView.as_view(), name="user-create"),
    path("users/<uuid:pk>/update/", views.UserUpdateView.as_view(), name="user-update"),
    path("users/<uuid:pk>/delete/", views.UserDeleteView.as_view(), name="user-delete"),
    path(
        "users/<uuid:pk>/activate/",
        views.UserActivateView.as_view(),
        name="user-activate",
    ),
    path(
        "users/<uuid:pk>/deactivate/",
        views.UserDeactivateView.as_view(),
        name="user-deactivate",
    ),
    path("sessions/", views.UserSessionListView.as_view(), name="session-list"),
    path("activities/", views.UserActivityListView.as_view(), name="activity-list"),
    path(
        "healthcare-professionals/",
        views.HealthcareProfessionalsView.as_view(),
        name="healthcare-professionals",
    ),
    path(
        "logistics-staff/", views.LogisticsStaffView.as_view(), name="logistics-staff"
    ),
    path("stats/", views.UserStatsView.as_view(), name="user-stats"),
]
