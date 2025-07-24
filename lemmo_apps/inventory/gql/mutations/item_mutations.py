from core.gql.mutations.core import CoreUnauthenticatedMutation
from core.app_utils import lemmo_message
from lemmo_apps.inventory.services.item import ItemService
import graphene
import logging

logger = logging.getLogger(__name__)

class ItemInput(graphene.InputObjectType):
    label = graphene.String(required=True)
    description = graphene.String(required=True)
    price = graphene.Float(required=True)
    bar_code = graphene.String(required=True)
    product_code = graphene.String(required=True)
    category_code = graphene.String()
    batch_code = graphene.String(required=True)
    expiry_date = graphene.Date()



class CreateItemMutation(CoreUnauthenticatedMutation):

    class Arguments:
        input = ItemInput(required=True)

    @classmethod
    def perform_mutation(cls, root, info, **data):
        input_data = data.get('input')
        if not input_data:
            return lemmo_message(
                success=False,
                message="Invalid input data",
                error_details=["Input data is missing"]
            )

        try:
            return ItemService().create_item(input_data)

        except Exception as e:
            logger.exception("CreateItemMutation failed")
            return lemmo_message(
                success=False,
                message="Failed to create item",
                error_details=[str(e)]
            )
