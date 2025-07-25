import graphene
from graphene_django import DjangoObjectType
from django.db import transaction
from lemmo_apps.inventory.models.product import Product, ProductCategory, ProductImage


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"


class ProductCategoryType(DjangoObjectType):
    class Meta:
        model = ProductCategory
        fields = "__all__"


class ProductImageType(DjangoObjectType):
    class Meta:
        model = ProductImage
        fields = "__all__"


class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        category_id = graphene.UUID()
        product_type = graphene.String()
        unit_of_measure = graphene.String()
        price = graphene.Decimal(required=True)
        generic_name = graphene.String()
        brand_name = graphene.String()
        manufacturer = graphene.String()
        ndc_code = graphene.String()
        rx_required = graphene.Boolean()
        controlled_substance = graphene.String()
        storage_type = graphene.String()
        storage_notes = graphene.String()
        expiration_date_required = graphene.Boolean()
        lot_number_required = graphene.Boolean()
        min_stock_level = graphene.Int()
        max_stock_level = graphene.Int()
        reorder_point = graphene.Int()
        fda_approved = graphene.Boolean()
        requires_prescription = graphene.Boolean()
        requires_special_handling = graphene.Boolean()
        hazardous_material = graphene.Boolean()
        temperature_sensitive = graphene.Boolean()
        weight_grams = graphene.Decimal()
        dimensions_cm = graphene.String()

    product = graphene.Field(ProductType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, **kwargs):
        try:
            with transaction.atomic():
                # Extract category_id if provided
                category_id = kwargs.pop("category_id", None)
                if category_id:
                    kwargs["category"] = ProductCategory.objects.get(id=category_id)

                product = Product.objects.create(**kwargs)

                return CreateProduct(
                    product=product,
                    success=True,
                    message="Product created successfully",
                )
        except Exception as e:
            return CreateProduct(product=None, success=False, message=str(e))


class UpdateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)
        name = graphene.String()
        description = graphene.String()
        category_id = graphene.UUID()
        product_type = graphene.String()
        unit_of_measure = graphene.String()
        price = graphene.Decimal()
        generic_name = graphene.String()
        brand_name = graphene.String()
        manufacturer = graphene.String()
        ndc_code = graphene.String()
        rx_required = graphene.Boolean()
        controlled_substance = graphene.String()
        storage_type = graphene.String()
        storage_notes = graphene.String()
        expiration_date_required = graphene.Boolean()
        lot_number_required = graphene.Boolean()
        min_stock_level = graphene.Int()
        max_stock_level = graphene.Int()
        reorder_point = graphene.Int()
        fda_approved = graphene.Boolean()
        requires_prescription = graphene.Boolean()
        requires_special_handling = graphene.Boolean()
        hazardous_material = graphene.Boolean()
        temperature_sensitive = graphene.Boolean()
        weight_grams = graphene.Decimal()
        dimensions_cm = graphene.String()
        is_active = graphene.Boolean()

    product = graphene.Field(ProductType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id, **kwargs):
        try:
            product = Product.objects.get(id=id)

            # Handle category update
            category_id = kwargs.pop("category_id", None)
            if category_id:
                kwargs["category"] = ProductCategory.objects.get(id=category_id)

            # Update fields
            for field, value in kwargs.items():
                if value is not None:
                    setattr(product, field, value)

            product.save()

            return UpdateProduct(
                product=product, success=True, message="Product updated successfully"
            )
        except Product.DoesNotExist:
            return UpdateProduct(
                product=None, success=False, message="Product not found"
            )
        except Exception as e:
            return UpdateProduct(product=None, success=False, message=str(e))


class DeleteProduct(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        try:
            product = Product.objects.get(id=id)
            product.delete()

            return DeleteProduct(success=True, message="Product deleted successfully")
        except Product.DoesNotExist:
            return DeleteProduct(success=False, message="Product not found")


class ActivateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)

    product = graphene.Field(ProductType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        try:
            product = Product.objects.get(id=id)
            product.is_active = True
            product.save()

            return ActivateProduct(
                product=product, success=True, message="Product activated successfully"
            )
        except Product.DoesNotExist:
            return ActivateProduct(
                product=None, success=False, message="Product not found"
            )


class DeactivateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)

    product = graphene.Field(ProductType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        try:
            product = Product.objects.get(id=id)
            product.is_active = False
            product.save()

            return DeactivateProduct(
                product=product,
                success=True,
                message="Product deactivated successfully",
            )
        except Product.DoesNotExist:
            return DeactivateProduct(
                product=None, success=False, message="Product not found"
            )


class ProductMutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()
    activate_product = ActivateProduct.Field()
    deactivate_product = DeactivateProduct.Field()
