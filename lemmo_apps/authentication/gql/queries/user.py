import graphene
from graphene_django import DjangoObjectType
from lemmo_apps.authentication.models import User, UserSession, UserActivity


class UserType(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = (
            {
                "id": ["exact"],
                "email": ["exact", "icontains"],
                "first_name": ["exact", "icontains"],
                "last_name": ["exact", "icontains"],
            },
        )
        interfaces = (graphene.relay.Node,)


class UserSessionType(DjangoObjectType):
    class Meta:
        model = UserSession
        filter_fields = (
            {
                "id": ["exact"],
                "user_id": ["exact"],
                "is_active": ["exact"],
            },
        )
        interfaces = (graphene.relay.Node,)


class UserActivityType(DjangoObjectType):
    class Meta:
        model = UserActivity
        filter_fields = (
            {
                "id": ["exact"],
                "user_id": ["exact"],
                "activity_type": ["exact"],
            },
        )
        interfaces = (graphene.relay.Node,)
