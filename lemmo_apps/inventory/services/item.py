from typing import Dict

from django.forms.utils import ErrorList
from core.app_utils import lemmo_message
from lemmo_apps.inventory.models.item import Item
from django.forms.models import model_to_dict
import traceback

class ItemService:

    def create_item(self, data: dict) -> Dict[str, bool | str | list[str] | dict]:
        try:
            print(data)
            new_item = Item(**data)
            new_item.save()

            new_item_dict = model_to_dict(new_item)
            return lemmo_message(
                success=True,
                message="Item created successfully",
                data=new_item_dict,
                errors=[]
            )
        except Exception as exc:
            return lemmo_message(
                message="An unexpected error occurred when creating the product item",
                errors=[traceback.format_exc(), str(exc)],
                error_details=[traceback.format_exc(), str(exc)],
                data=data
            )
    def update_item(self, data: dict) -> Dict[str, bool | str | list[str] | dict]:
        try:
            item_id = data.get('id')
            if not item_id:
                return lemmo_message(
                    success=False,
                    message="Item ID is required",
                    errors=["Item ID is required"]
                )

            item = Item.objects.get(id=item_id)

            for key, value in data.items():
                setattr(item, key, value)
            item.save()
            updated_item_dict = model_to_dict(item)
            return lemmo_message(
                success=True,
                message="Item updated successfully",
                data=updated_item_dict,
                errors=[]
            )
        except Item.DoesNotExist:
            return lemmo_message(
                success=False,
                message="Product Item not found",
                errors=["Item not found"]
            )
        except Exception:
            return lemmo_message(
                success=False,
                message="An unexpected error occurred",
                errors=[traceback.format_exc()]
            )

    def verify_data(self, action: str = "create", data: dict = {}) -> Dict[str, bool | str | list[str] | dict]:
        try:
            if not data:
                if action == "create":
                    return lemmo_message(
                        success=False,
                        message="Data is required",
                        errors=["Data is required"]
                    )
                elif action == "update":
                    return lemmo_message(
                        success=False,
                        message="Data is required",
                        errors=["Data is required"]
                    )

        except Exception as exc:
            return lemmo_message(
                message="An unexpected error occurred when verifying the data",
                errors=[traceback.format_exc(), str(exc)],
                error_details=[traceback.format_exc(), str(exc)],
                data=data
            )

    def _verify_create_data(self, data: dict = {}) -> Dict[str, bool | str | list[str] | dict[str, bool | str | list[str] | dict]]:
        errors = []
        if data:
            product_code = data.pop("product_code")
            category_code = data.pop("category_code")

            if not product_code:
                return lemmo_message(
                    success=False,
                    message="Product code is required",
                    errors=["Product code is required"]
                )
            if not category_code:
                return lemmo_message(
                    success=False,
                    message="Category code is required",
                    errors=["Category code is required"]
                )

            return lemmo_message(
                success=True,
                data={
                    "product_code": product_code,
                    "category_code": category_code
                }
            )

        return lemmo_message(
            success=False,
            message="Data is required",
            errors=["Data is required"]
        )
