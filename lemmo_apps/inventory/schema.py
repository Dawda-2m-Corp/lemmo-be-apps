from lemmo_apps.inventory.gql import mutations
import graphene


class Query(graphene.ObjectType):
    pass

class Mutation(graphene.ObjectType):
    create_product_item = mutations.CreateItemMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
