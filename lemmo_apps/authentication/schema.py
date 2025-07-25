import graphene
from .gql.queries.user import Query as UserQuery
from .gql.mutations.user_mutations import Mutation as UserMutation


class Query(UserQuery, graphene.ObjectType):
    pass


class Mutation(UserMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
