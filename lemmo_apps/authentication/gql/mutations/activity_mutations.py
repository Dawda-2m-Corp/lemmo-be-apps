import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from lemmo_apps.authentication.models import UserActivity

User = get_user_model()


class UserActivityType(DjangoObjectType):
    class Meta:
        model = UserActivity
        fields = "__all__"


class LogActivity(graphene.Mutation):
    class Arguments:
        user_id = graphene.UUID(required=True)
        activity_type = graphene.String(required=True)
        description = graphene.String()
        ip_address = graphene.String()
        user_agent = graphene.String()
        metadata = graphene.JSONString()

    activity = graphene.Field(UserActivityType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(
        self,
        info,
        user_id,
        activity_type,
        description=None,
        ip_address=None,
        user_agent=None,
        metadata=None,
    ):
        try:
            user = User.objects.get(id=user_id)
            activity = UserActivity.objects.create(
                user=user,
                activity_type=activity_type,
                description=description,
                ip_address=ip_address,
                user_agent=user_agent,
                metadata=metadata or {},
            )
            return LogActivity(
                activity=activity, success=True, message="Activity logged successfully"
            )
        except User.DoesNotExist:
            return LogActivity(activity=None, success=False, message="User not found")
        except Exception as e:
            return LogActivity(activity=None, success=False, message=str(e))


class Mutation(graphene.ObjectType):
    log_activity = LogActivity.Field()
