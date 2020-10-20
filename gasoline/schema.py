import graphene
from .models import Prices, Stations
from graphene_django import DjangoObjectType
import django_filters

class PricesType(DjangoObjectType):
    class Meta:
        model = Prices
        filter_fields = ("id","station_id","date", "magna_price","premium_price","diesel_price")

class StationsType(DjangoObjectType):
    class Meta:
        model = Stations
        fields = ("id","name", "latitude", "longitude", "status")
        
class Query(graphene.ObjectType):
    all_stations = graphene.List(StationsType)
    all_prices = graphene.List(PricesType)
   
    def resolve_all_stations(root, info):
        return Stations.objects.all()

    def resolve_all_prices(root, info):
        return Prices.objects.all()

schema = graphene.Schema(query=Query)