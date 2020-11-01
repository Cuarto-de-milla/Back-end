"""Schemas for gasoline app """
# Django
import django_filters

# Models
from gasoline.models import Price, Station

# Graphene
import graphene
from graphene import relay, ObjectType, Connection, Node, ConnectionField
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

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
    """Node of the stations of gasoline"""
    class Meta:
        """Meta class."""
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
    """Node of prices of each station of gasoline"""
    class Meta:
        """Meta class."""
        model = Price
        filter_fields = {
            'id': ['exact'],
            'station__name': ['exact', 'icontains','istartswith'],
            'gas_type': ['exact', 'icontains','istartswith'],
            'price':['exact', 'icontains','istartswith'],
            'date':['exact'],
        }
        interfaces = (relay.Node,Node)


class PriceConnection(Connection):
    """Price Connection"""
    class Meta:
        """Class Meta"""
        node = PriceNode


#---------------SCHEMA---------------
class Query(graphene.ObjectType):
    """Gasoline Query class"""
    all_stations = ConnectionField(StationConnection)
    all_prices = ConnectionField(PriceConnection)

    def resolve_all_stations(root, info,  **kwargs):
        """ Return all the stations """
        return Station.objects.filter(is_active=True)

    def resolve_all_prices(root, info, **kwargs):
        """ Return all prices """
        return Price.objects.filter(station__is_active=True)

    # Node Query class
    station = relay.Node.Field(StationNode)
    node_station = DjangoFilterConnectionField(StationNode)

    price = relay.Node.Field(PriceNode)
    node_price = DjangoFilterConnectionField(PriceNode)

class Mutation(graphene.ObjectType):
    """ Gasoline Mutation class."""
    pass