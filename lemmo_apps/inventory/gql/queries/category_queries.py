import graphene
from graphene_django import DjangoObjectType
from lemmo_apps.inventory.models.product import ProductCategory


class ProductCategoryType(DjangoObjectType):
    class Meta:
        model = ProductCategory
        fields = "__all__"


class CategoryQuery(graphene.ObjectType):
    categories = graphene.List(
        ProductCategoryType,
        is_active=graphene.Boolean(),
        parent_id=graphene.UUID(),
        search=graphene.String(),
    )

    category = graphene.Field(ProductCategoryType, id=graphene.UUID(required=True))

    root_categories = graphene.List(ProductCategoryType)
    category_tree = graphene.JSONString()

    def resolve_categories(self, info, is_active=None, parent_id=None, search=None):
        queryset = ProductCategory.objects.all()

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        if parent_id:
            queryset = queryset.filter(parent_id=parent_id)

        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset

    def resolve_category(self, info, id):
        return ProductCategory.objects.get(id=id)

    def resolve_root_categories(self, info):
        return ProductCategory.objects.filter(parent__isnull=True, is_active=True)

    def resolve_category_tree(self, info):
        def build_tree(categories, parent=None):
            tree = []
            for category in categories:
                if category.parent == parent:
                    children = build_tree(categories, category)
                    tree.append(
                        {
                            "id": str(category.id),
                            "name": category.name,
                            "description": category.description,
                            "is_active": category.is_active,
                            "children": children,
                        }
                    )
            return tree

        categories = ProductCategory.objects.all()
        return build_tree(categories)
