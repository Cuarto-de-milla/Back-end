""" Schema OilApp"""

# Graphene
import graphene

# Querys
from users.schema import Query as UserQuery
from complaints.schema import Query as ComplaintQuery
from gasoline.schema import Query as GasolineQuery

# JWT - Graphene
import graphql_jwt

# Mutations
from users.schema import Mutation as UserMutation
from complaints.schema import Mutation as ComplaintMutation
from gasoline.schema import Mutation as GasolineMutation

#---------------SCHEMA---------------
class Query(UserQuery,
            ComplaintQuery,
            GasolineQuery,
            graphene.ObjectType,
            ):
    """ Main query class"""
    pass

class Mutation(UserMutation, 
            ComplaintMutation,
            GasolineMutation,
            graphene.ObjectType,
            ):
    """Main mutation class"""
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)