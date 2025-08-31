import graphene
from .gql.queries.user import UserType, UserSessionType, UserActivityType
from .gql.mutations.user_mutations import Mutation as UserMutation
from .gql.mutations.session_mutations import Mutation as SessionMutation
from .gql.mutations.activity_mutations import Mutation as ActivityMutation
from .gql.mutations.auth_mutations import AuthMutations
from graphene_django.filter import DjangoFilterConnectionField
from django.db.models import Q
from lemmo_apps.authentication.models import User, UserSession, UserActivity


class Query(graphene.ObjectType):
    # User queries
    users = DjangoFilterConnectionField(
        UserType,
        role=graphene.String(),
        is_active=graphene.Boolean(),
        search=graphene.String(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )

    user = graphene.Field(UserType, id=graphene.UUID(required=True))

    user_by_email = graphene.Field(UserType, email=graphene.String(required=True))

    # User session queries
    user_sessions = DjangoFilterConnectionField(
        UserSessionType, user_id=graphene.UUID(), is_active=graphene.Boolean()
    )

    # User activity queries
    user_activities = DjangoFilterConnectionField(
        UserActivityType,
        user_id=graphene.UUID(),
        activity_type=graphene.String(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )

    # Healthcare specific queries
    healthcare_professionals = DjangoFilterConnectionField(UserType)
    logistics_staff = DjangoFilterConnectionField(UserType)
    active_users = DjangoFilterConnectionField(UserType)

    # Dashboard statistics
    user_stats = graphene.JSONString()

    def resolve_users(
        self, info, role=None, is_active=None, search=None, limit=None, offset=None
    ):
        queryset = User.objects.all()

        if role:
            queryset = queryset.filter(role=role)

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(email__icontains=search)
                | Q(employee_id__icontains=search)
            )

        if offset:
            queryset = queryset[offset:]

        if limit:
            queryset = queryset[:limit]

        return queryset

    def resolve_user(self, info, id):
        return User.objects.get(id=id)

    def resolve_user_by_email(self, info, email):
        return User.objects.get(email=email)

    def resolve_user_sessions(self, info, user_id=None, is_active=None):
        queryset = UserSession.objects.all()

        if user_id:
            queryset = queryset.filter(user_id=user_id)

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        return queryset

    def resolve_user_activities(
        self, info, user_id=None, activity_type=None, limit=None, offset=None
    ):
        queryset = UserActivity.objects.all()

        if user_id:
            queryset = queryset.filter(user_id=user_id)

        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)

        if offset:
            queryset = queryset[offset:]

        if limit:
            queryset = queryset[:limit]

        return queryset

    def resolve_healthcare_professionals(self, info):
        return User.objects.filter(role__in=["PHARMACIST", "NURSE", "DOCTOR"])

    def resolve_logistics_staff(self, info):
        return User.objects.filter(
            role__in=[
                "LOGISTICS_MANAGER",
                "WAREHOUSE_MANAGER",
                "SUPPLY_CHAIN_SPECIALIST",
                "INVENTORY_CLERK",
                "DISPATCHER",
                "DRIVER",
            ]
        )

    def resolve_active_users(self, info):
        return User.objects.filter(is_active=True)

    def resolve_user_stats(self, info):
        from django.db.models import Count
        from django.utils import timezone
        from datetime import timedelta

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

        # Recent activity
        last_30_days = timezone.now() - timedelta(days=30)
        recent_activities = UserActivity.objects.filter(
            created_at__gte=last_30_days
        ).count()

        # Role distribution
        role_distribution = (
            User.objects.values("role").annotate(count=Count("id")).order_by("-count")
        )

        return {
            "total_users": total_users,
            "active_users": active_users,
            "healthcare_professionals": healthcare_professionals,
            "logistics_staff": logistics_staff,
            "recent_activities": recent_activities,
            "role_distribution": list(role_distribution),
        }


class Mutation(
    UserMutation, SessionMutation, ActivityMutation, AuthMutations, graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
