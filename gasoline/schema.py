import graphene
from .models import Prices, Stations, Profile, Complaints
from graphene_django import DjangoObjectType
import django_filters

#------------------QUERIES---------------
class PricesType(DjangoObjectType):
    class Meta:
        model = Prices
        filter_fields = ("id","station","gas_type","price","date")

class StationsType(DjangoObjectType):
    class Meta:
        model = Stations
        fields = ("id","name","about","picture","register","latitude", "longitude","state","is_active","status")

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = ('username','password','email','first_name','last_name')

class Complaints(DjangoObjectType):
    class Meta:
        model = Complaints
        fields = ('user','station','description','link_evidence','type_complaint','date','actual_price','offered_price')

class Query(graphene.ObjectType):
    all_stations = graphene.List(StationsType)
    all_prices = graphene.List(PricesType)
   
    def resolve_all_stations(root, info):
        return Stations.objects.all()

    def resolve_all_prices(root, info):
        return Prices.objects.all()

#-------------MUTATIONS------------

class UpdateProfile(graphene.Mutation):
    class Arguments:
        user = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String()

    profile = graphene.Field(ProfileType)

    def mutate(self, info, user, password,email,first_name,last_name):
        profile = Profile(user=user,password=password,
        email=email,first_name=first_name,last_name=last_name)
        profile.save()
        return UpdateProfile(profile=profile)


class Mutation(graphene.ObjectType):
    update_user = UpdateProfile.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)