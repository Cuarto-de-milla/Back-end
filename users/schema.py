""" User schema """

# Graphene
import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

# Django
from django.contrib.auth.models import User

# Models
from users.models import Profile

#------------------QUERIES---------------
class UserType(DjangoObjectType):
    """Type for user model"""
    class Meta:
        """Class Meta"""
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )


class ProfileType(DjangoObjectType):
    """ Type for Profile model"""
    class Meta:
        """Class Meta"""
        model = Profile
        fields = (
            "user",
            "phone_number"
        )

#-----------NODE-QUERIES----------

class ProfileNode(DjangoObjectType):
    class Meta:
        model = Profile
        filter_fields = {
            "user": ['exact'],
            "phone_number": ['exact', 'icontains','istartswith'],
        }
        interfaces = (relay.Node,)


#-----------MUTATIONS----------
class UpdateUser(graphene.Mutation):
    class Arguments:
        user = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String()

    user = graphene.Field(UserType)

    def mutate(self, info, user, password,email,first_name,last_name):
        user = User(
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
        user.save()
        return UpdateUser(user=user)


class Query(graphene.ObjectType):
    """ User Query """
    all_profiles = graphene.List(ProfileType)

    def resolve_all_profiles(root, info):
        """ Return all profiles"""
        return Profile.objects.all()
    
    # Node Query Class
    profile = relay.Node.Field(ProfileNode)
    node_profile = DjangoFilterConnectionField(ProfileNode)

class Mutation(graphene.ObjectType):
    update_user = UpdateUser.Field()