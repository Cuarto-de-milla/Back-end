"""Schemas for gasoline app """
# Django
import django_filters
from django.contrib.auth.models import User

# Models
from .models import Price, Station, Profile, Complaint

# Graphene
import graphene
from graphene import relay, ObjectType, Connection, Node, ConnectionField
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

#------------------QUERIES---------------
class StationType(DjangoObjectType):
    """Type for Station Model"""
    class Meta:
        """ Class Meta"""
        model = Station
        fields = (
            'id',
            'name',
            'about',
            'picture',
            'register',
            'latitude', 
            'longitude',
            'town',
            'state',
            'is_active',
            'status',
        )


class PriceType(DjangoObjectType):
    """ Type for price model"""
    class Meta:
        """Class Meta"""
        model = Price
        fields = (
            'id',
            'station',
            'gas_type',
            'price',
            'date',
        )


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


class ComplaintType(DjangoObjectType):
    """ Type for Complaint Model"""
    class Meta:
        """Class Meta"""
        model = Complaint
        fields = (
            'user',
            'station',
            'description',
            'link_evidence',
            'type_complaint',
            'date',
            'actual_price',
            'offered_price'
        )


#-----------NODE-QUERIES----------

class StationNode(DjangoObjectType):
    class Meta:
        model = Station
        filter_fields = {
            'id':['exact'],
            'name':['exact', 'icontains','istartswith'],
            'register':['exact', 'icontains','istartswith'],
            'latitude':['exact', 'icontains','istartswith'], 
            'longitude':['exact', 'icontains','istartswith'],
            'town':['exact', 'icontains','istartswith'],
            'state':['exact', 'icontains','istartswith'],
            'is_active':['exact'],
            'status':['exact'],
        }
        interfaces = (relay.Node, Node)


class StationConnection(Connection):
    """Station Connection"""
    class Meta:
        """Class Meta"""
        node = StationNode

class PriceNode(DjangoObjectType):
    class Meta:
        model = Price
        filter_fields = {
            'id': ['exact'],
            'station__name': ['exact', 'icontains','istartswith'],
            'gas_type': ['exact', 'icontains','istartswith'],
            'price':['exact', 'icontains','istartswith'],
            'date':['exact'],
        }
        interfaces = (relay.Node,)


class ProfileNode(DjangoObjectType):
    class Meta:
        model = Profile
        filter_fields = {
            "user": ['exact'],
            "phone_number": ['exact', 'icontains','istartswith'],
        }
        interfaces = (relay.Node,)


class ComplaintNode(DjangoObjectType):
    class Meta:
        model = Complaint
        filter_fields = {
            'user': ['exact'],
            'station__id': ['exact', 'icontains','istartswith'],
            'description': ['exact', 'icontains','istartswith'],
            'type_complaint': ['exact', 'icontains','istartswith'],
            'date': ['exact', 'icontains','istartswith'],
            'actual_price__price': ['exact', 'icontains','istartswith'],
            'offered_price': ['exact', 'icontains','istartswith'],
        }
        interfaces = (relay.Node,)

#-------------MUTATIONS------------

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

#---------------SCHEMA---------------

class Query(graphene.ObjectType):
    """General Query class"""
    # all_stations = graphene.List(StationType)
    all_stations = ConnectionField(StationConnection)
    all_prices = graphene.List(PriceType)
    all_profiles = graphene.List(ProfileType)
    all_complaints = graphene.List(ComplaintType)

    def resolve_all_stations(root, info,  **kwargs):
        """ Return all the stations """
        return Station.objects.all()

    def resolve_all_prices(root, info):
        """ Return all prices """
        return Price.objects.all()

    def resolve_all_profiles(root, info):
        """ Return all profiles"""
        return Profile.objects.all()
    
    def resolve_all_complaints(root, info):
        """ Return all complaints"""
        return Complaint.objects.all()

    """Node Query class"""
    station = relay.Node.Field(StationNode)
    node_station = DjangoFilterConnectionField(StationNode)

    price = relay.Node.Field(PriceNode)
    node_price = DjangoFilterConnectionField(PriceNode)

    profile = relay.Node.Field(ProfileNode)
    node_profile = DjangoFilterConnectionField(ProfileNode)

    complaint = relay.Node.Field(ComplaintNode)
    node_complaint = DjangoFilterConnectionField(ComplaintNode)


class Mutation(graphene.ObjectType):
    update_user = UpdateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)