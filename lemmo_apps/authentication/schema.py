import graphene
from .gql.queries.user import Query as UserQuery
from .gql.mutations.user_mutations import Mutation as UserMutation
from .gql.mutations.session_mutations import Mutation as SessionMutation
from .gql.mutations.activity_mutations import Mutation as ActivityMutation
from .gql.mutations.auth_mutations import AuthMutations


class Query(UserQuery, graphene.ObjectType):
    pass


class Mutation(
    UserMutation, SessionMutation, ActivityMutation, AuthMutations, graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
