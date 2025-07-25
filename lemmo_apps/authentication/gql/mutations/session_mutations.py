import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from lemmo_apps.authentication.models import UserSession

User = get_user_model()


class UserSessionType(DjangoObjectType):
    class Meta:
        model = UserSession
        fields = "__all__"


class CreateSession(graphene.Mutation):
    class Arguments:
        user_id = graphene.UUID(required=True)
        ip_address = graphene.String()
        user_agent = graphene.String()

    session = graphene.Field(UserSessionType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, user_id, ip_address=None, user_agent=None):
        try:
            user = User.objects.get(id=user_id)
            session = UserSession.objects.create(
                user=user, ip_address=ip_address, user_agent=user_agent
            )
            return CreateSession(
                session=session, success=True, message="Session created successfully"
            )
        except User.DoesNotExist:
            return CreateSession(session=None, success=False, message="User not found")
        except Exception as e:
            return CreateSession(session=None, success=False, message=str(e))


class EndSession(graphene.Mutation):
    class Arguments:
        session_id = graphene.UUID(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, session_id):
        try:
            session = UserSession.objects.get(id=session_id)
            session.end_session()
            return EndSession(success=True, message="Session ended successfully")
        except UserSession.DoesNotExist:
            return EndSession(success=False, message="Session not found")
        except Exception as e:
            return EndSession(success=False, message=str(e))


class Mutation(graphene.ObjectType):
    create_session = CreateSession.Field()
    end_session = EndSession.Field()
