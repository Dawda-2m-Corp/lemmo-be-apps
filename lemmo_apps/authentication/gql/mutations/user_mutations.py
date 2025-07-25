import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from lemmo_apps.authentication.models import User

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"


class CreateUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        password = graphene.String(required=True)
        role = graphene.String()
        phone_number = graphene.String()
        employee_id = graphene.String()
        department = graphene.String()
        license_number = graphene.String()
        is_active = graphene.Boolean()

    user = graphene.Field(UserType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, email, first_name, last_name, password, **kwargs):
        try:
            # Check if user already exists
            if User.objects.filter(email=email).exists():
                return CreateUser(
                    user=None,
                    success=False,
                    message="User with this email already exists",
                )

            # Create user
            user_data = {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "password": make_password(password),
            }

            # Add optional fields
            for field, value in kwargs.items():
                if value is not None:
                    user_data[field] = value

            user = User.objects.create(**user_data)

            return CreateUser(
                user=user, success=True, message="User created successfully"
            )
        except Exception as e:
            return CreateUser(user=None, success=False, message=str(e))


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)
        email = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        role = graphene.String()
        phone_number = graphene.String()
        employee_id = graphene.String()
        department = graphene.String()
        license_number = graphene.String()
        is_active = graphene.Boolean()

    user = graphene.Field(UserType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id, **kwargs):
        try:
            user = User.objects.get(id=id)

            # Update fields
            for field, value in kwargs.items():
                if value is not None:
                    setattr(user, field, value)

            user.save()

            return UpdateUser(
                user=user, success=True, message="User updated successfully"
            )
        except User.DoesNotExist:
            return UpdateUser(user=None, success=False, message="User not found")
        except Exception as e:
            return UpdateUser(user=None, success=False, message=str(e))


class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        try:
            user = User.objects.get(id=id)
            user.delete()

            return DeleteUser(success=True, message="User deleted successfully")
        except User.DoesNotExist:
            return DeleteUser(success=False, message="User not found")
        except Exception as e:
            return DeleteUser(success=False, message=str(e))


class ActivateUser(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)

    user = graphene.Field(UserType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        try:
            user = User.objects.get(id=id)
            user.is_active = True
            user.save()

            return ActivateUser(
                user=user, success=True, message="User activated successfully"
            )
        except User.DoesNotExist:
            return ActivateUser(user=None, success=False, message="User not found")


class DeactivateUser(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)

    user = graphene.Field(UserType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        try:
            user = User.objects.get(id=id)
            user.is_active = False
            user.save()

            return DeactivateUser(
                user=user, success=True, message="User deactivated successfully"
            )
        except User.DoesNotExist:
            return DeactivateUser(user=None, success=False, message="User not found")


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    activate_user = ActivateUser.Field()
    deactivate_user = DeactivateUser.Field()
