"""Schemas for gasoline app """
# Django
import django_filters

# Models
from gasoline.models import Price, Station

# Graphene
import graphene
from graphene import relay, ObjectType
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
        interfaces = (relay.Node,)


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


#---------------SCHEMA---------------
class Query(graphene.ObjectType):
    """Gasoline Query class"""
    all_stations = graphene.List(StationType)
    all_prices = graphene.List(PriceType)

    def resolve_all_stations(root, info):
        """ Return all the stations """
        return Station.objects.all()

    def resolve_all_prices(root, info):
        """ Return all prices """
        return Price.objects.all()

    # Node Query class
    station = relay.Node.Field(StationNode)
    node_station = DjangoFilterConnectionField(StationNode)

    price = relay.Node.Field(PriceNode)
    node_price = DjangoFilterConnectionField(PriceNode)

class Mutation(graphene.ObjectType):
    """ Gasoline Mutation class."""