import graphene
import graphql_jwt


class Query(graphene.ObjectType):
    user = graphene.String(
        default_value="Anonymous User",
        description="A simple query to return a user name.",
    )


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
