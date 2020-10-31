""" User schema """

# Graphene
import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

# Django
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# JWT 
from graphql_jwt.decorators import login_required

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
class UserInput(graphene.InputObjectType):
    """ Arguments for User"""
    username   = graphene.String(required=False)
    first_name = graphene.String(required=False)
    last_name  = graphene.String(required=False)
    password   = graphene.String(required=False)
    email      = graphene.String(required=False)


class ProfileInput(graphene.InputObjectType):
    """ Arguments for Profile"""
    phone_number = graphene.String(required=False)


class CreateUser(graphene.Mutation):
    """ Create a new user and Profile"""
    user = graphene.Field(UserType)
    profile = graphene.Field(ProfileType)
    class Arguments:
        """ Arguments for CreateUser

        UserData and ProfileData"""
        user_data = UserInput(required=True)
        profile_data = ProfileInput(required=False)

    def mutate(root,info, user_data, **kwargs):
        """Mutation to create a new User an ProfileUser"""
        # Create and save the user
        user = User(
                    username=user_data['username'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    password=user_data['password'],
                    email=user_data['email'],
                )
        user.save()        

        # Create and save the profile of user
        profile_data = kwargs.get('profile_data')
        profile = Profile(user=user)

        if profile_data is not None:
            setattr(profile, 'phone_number' , profile_data.phone_number)

        profile.save()
        return CreateUser(user=user,profile=profile)


class UpdateUser(graphene.Mutation):
    """ Update user and profile User"""
    user = graphene.Field(UserType)
    profile = graphene.Field(ProfileType)
    
    class Arguments:
        """ Arguments for update User

        UserData and ProfileData"""
        user_data = UserInput(required=True)
        profile_data = ProfileInput(required=False)

    @login_required
    def mutate(self, info, user_data, **kwargs):
        """ Mutation to Update user and profile """
        user = User.objects.get(username=user_data['username'])
        profile = user.profile

        #Assign user data        
        for k, v in user_data.items():
            if (k == 'password') and (v is not None):
                user.set_password(user_data.password)
            else:
                setattr(user, k, v)

        # Asign Profile Data
        profile_data = kwargs.get('profile_data')
        
        if profile_data is not None:
            for k, v in profile_data.items():
                setattr(profile, k, v)

        user.save()
        profile.save()
        return UpdateUser(user=user, profile=profile)


class Query(graphene.ObjectType):
    """ User Query """
    my_user = graphene.Field(ProfileType)

    @login_required
    def resolve_my_user(root, info):
        """ Return profile of the logged user"""
        return Profile.objects.get(user=info.context.user)
    
    # Node Query Class
    profile = relay.Node.Field(ProfileNode)
    node_profile = DjangoFilterConnectionField(ProfileNode)


class Mutation(graphene.ObjectType):
    update_user = UpdateUser.Field()
    create_user = CreateUser.Field()