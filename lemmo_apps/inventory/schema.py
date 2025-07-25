import graphene
from .gql.queries.product_queries import ProductQuery
from .gql.queries.category_queries import CategoryQuery
from .gql.queries.batch_queries import BatchQuery
from .gql.mutations.product_mutations import ProductMutation
from .gql.mutations.category_mutations import CategoryMutation
from .gql.mutations.batch_mutations import BatchMutation


class Query(ProductQuery, CategoryQuery, BatchQuery, graphene.ObjectType):
    pass


class Mutation(ProductMutation, CategoryMutation, BatchMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
