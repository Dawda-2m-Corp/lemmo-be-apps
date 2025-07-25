import graphene
from graphene_django import DjangoObjectType
from django.db import transaction
from lemmo_apps.inventory.models.product import ProductCategory


class ProductCategoryType(DjangoObjectType):
    class Meta:
        model = ProductCategory
        fields = "__all__"


class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        parent_id = graphene.UUID()
        is_active = graphene.Boolean()

    category = graphene.Field(ProductCategoryType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, **kwargs):
        try:
            with transaction.atomic():
                # Extract parent_id if provided
                parent_id = kwargs.pop("parent_id", None)
                if parent_id:
                    kwargs["parent"] = ProductCategory.objects.get(id=parent_id)

                category = ProductCategory.objects.create(**kwargs)

                return CreateCategory(
                    category=category,
                    success=True,
                    message="Category created successfully",
                )
        except Exception as e:
            return CreateCategory(category=None, success=False, message=str(e))


class UpdateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)
        name = graphene.String()
        description = graphene.String()
        parent_id = graphene.UUID()
        is_active = graphene.Boolean()

    category = graphene.Field(ProductCategoryType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id, **kwargs):
        try:
            category = ProductCategory.objects.get(id=id)

            # Handle parent update
            parent_id = kwargs.pop("parent_id", None)
            if parent_id:
                kwargs["parent"] = ProductCategory.objects.get(id=parent_id)

            # Update fields
            for field, value in kwargs.items():
                if value is not None:
                    setattr(category, field, value)

            category.save()

            return UpdateCategory(
                category=category, success=True, message="Category updated successfully"
            )
        except ProductCategory.DoesNotExist:
            return UpdateCategory(
                category=None, success=False, message="Category not found"
            )
        except Exception as e:
            return UpdateCategory(category=None, success=False, message=str(e))


class DeleteCategory(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        try:
            category = ProductCategory.objects.get(id=id)

            # Check if category has children
            if category.children.exists():
                return DeleteCategory(
                    success=False, message="Cannot delete category with subcategories"
                )

            # Check if category has products
            if category.product_set.exists():
                return DeleteCategory(
                    success=False, message="Cannot delete category with products"
                )

            category.delete()

            return DeleteCategory(success=True, message="Category deleted successfully")
        except ProductCategory.DoesNotExist:
            return DeleteCategory(success=False, message="Category not found")


class ActivateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)

    category = graphene.Field(ProductCategoryType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        try:
            category = ProductCategory.objects.get(id=id)
            category.is_active = True
            category.save()

            return ActivateCategory(
                category=category,
                success=True,
                message="Category activated successfully",
            )
        except ProductCategory.DoesNotExist:
            return ActivateCategory(
                category=None, success=False, message="Category not found"
            )


class DeactivateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)

    category = graphene.Field(ProductCategoryType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        try:
            category = ProductCategory.objects.get(id=id)
            category.is_active = False
            category.save()

            return DeactivateCategory(
                category=category,
                success=True,
                message="Category deactivated successfully",
            )
        except ProductCategory.DoesNotExist:
            return DeactivateCategory(
                category=None, success=False, message="Category not found"
            )


class CategoryMutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()
    activate_category = ActivateCategory.Field()
    deactivate_category = DeactivateCategory.Field()
