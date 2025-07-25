import graphene
from graphene_django import DjangoObjectType
from django.db import transaction
from lemmo_apps.inventory.models.product import ProductBatch, Product


class ProductBatchType(DjangoObjectType):
    class Meta:
        model = ProductBatch
        fields = "__all__"


class CreateBatch(graphene.Mutation):
    class Arguments:
        product_id = graphene.UUID(required=True)
        batch_number = graphene.String(required=True)
        lot_number = graphene.String()
        quantity = graphene.Int(required=True)
        manufacturing_date = graphene.Date(required=True)
        expiration_date = graphene.Date(required=True)
        cost_per_unit = graphene.Decimal(required=True)
        supplier = graphene.String()
        supplier_batch_number = graphene.String()
        quality_control_passed = graphene.Boolean()
        notes = graphene.String()

    batch = graphene.Field(ProductBatchType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, **kwargs):
        try:
            with transaction.atomic():
                # Extract product_id
                product_id = kwargs.pop("product_id")
                product = Product.objects.get(id=product_id)

                # Set remaining_quantity to initial quantity
                kwargs["remaining_quantity"] = kwargs["quantity"]
                kwargs["product"] = product

                batch = ProductBatch.objects.create(**kwargs)

                # Update product stock quantity
                product.stock_quantity += kwargs["quantity"]
                product.save()

                return CreateBatch(
                    batch=batch, success=True, message="Batch created successfully"
                )
        except Product.DoesNotExist:
            return CreateBatch(batch=None, success=False, message="Product not found")
        except Exception as e:
            return CreateBatch(batch=None, success=False, message=str(e))


class UpdateBatch(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)
        batch_number = graphene.String()
        lot_number = graphene.String()
        quantity = graphene.Int()
        remaining_quantity = graphene.Int()
        manufacturing_date = graphene.Date()
        expiration_date = graphene.Date()
        cost_per_unit = graphene.Decimal()
        supplier = graphene.String()
        supplier_batch_number = graphene.String()
        quality_control_passed = graphene.Boolean()
        notes = graphene.String()

    batch = graphene.Field(ProductBatchType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id, **kwargs):
        try:
            batch = ProductBatch.objects.get(id=id)

            # Handle quantity changes
            if "quantity" in kwargs:
                old_quantity = batch.quantity
                new_quantity = kwargs["quantity"]
                quantity_diff = new_quantity - old_quantity

                # Update product stock
                batch.product.stock_quantity += quantity_diff
                batch.product.save()

            # Update fields
            for field, value in kwargs.items():
                if value is not None:
                    setattr(batch, field, value)

            batch.save()

            return UpdateBatch(
                batch=batch, success=True, message="Batch updated successfully"
            )
        except ProductBatch.DoesNotExist:
            return UpdateBatch(batch=None, success=False, message="Batch not found")
        except Exception as e:
            return UpdateBatch(batch=None, success=False, message=str(e))


class DeleteBatch(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        try:
            batch = ProductBatch.objects.get(id=id)

            # Update product stock quantity
            batch.product.stock_quantity -= batch.remaining_quantity
            batch.product.save()

            batch.delete()

            return DeleteBatch(success=True, message="Batch deleted successfully")
        except ProductBatch.DoesNotExist:
            return DeleteBatch(success=False, message="Batch not found")


class AdjustBatchQuantity(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)
        adjustment_quantity = graphene.Int(required=True)
        adjustment_reason = graphene.String()

    batch = graphene.Field(ProductBatchType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id, adjustment_quantity, adjustment_reason=None):
        try:
            batch = ProductBatch.objects.get(id=id)

            # Calculate new remaining quantity
            new_remaining = batch.remaining_quantity + adjustment_quantity

            if new_remaining < 0:
                return AdjustBatchQuantity(
                    batch=None,
                    success=False,
                    message="Adjustment would result in negative quantity",
                )

            # Update batch
            batch.remaining_quantity = new_remaining
            batch.save()

            # Update product stock
            batch.product.stock_quantity += adjustment_quantity
            batch.product.save()

            return AdjustBatchQuantity(
                batch=batch,
                success=True,
                message=f"Batch quantity adjusted by {adjustment_quantity}",
            )
        except ProductBatch.DoesNotExist:
            return AdjustBatchQuantity(
                batch=None, success=False, message="Batch not found"
            )


class QualityControlCheck(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)
        passed = graphene.Boolean(required=True)
        notes = graphene.String()

    batch = graphene.Field(ProductBatchType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id, passed, notes=None):
        try:
            batch = ProductBatch.objects.get(id=id)
            batch.quality_control_passed = passed
            if notes:
                batch.quality_notes = notes
            batch.save()

            return QualityControlCheck(
                batch=batch,
                success=True,
                message=f"Quality control {'passed' if passed else 'failed'}",
            )
        except ProductBatch.DoesNotExist:
            return QualityControlCheck(
                batch=None, success=False, message="Batch not found"
            )


class BatchMutation(graphene.ObjectType):
    create_batch = CreateBatch.Field()
    update_batch = UpdateBatch.Field()
    delete_batch = DeleteBatch.Field()
    adjust_batch_quantity = AdjustBatchQuantity.Field()
    quality_control_check = QualityControlCheck.Field()
