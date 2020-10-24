"""Schemas for gasoline app """
# Django
import django_filters
from django.contrib.auth.models import User

# Models
from .models import Price, Station, Profile, Complaint

# Graphene
import graphene
from graphene_django import DjangoObjectType


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
        filter_fields = (
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


class Complaint(DjangoObjectType):
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


class Query(graphene.ObjectType):
    """Query class"""
    all_stations = graphene.List(StationType)
    all_prices = graphene.List(PriceType)

    def resolve_all_stations(root, info):
        """ Return all the stations """
        return Station.objects.all()

    def resolve_all_prices(root, info):
        """ Return all prices """
        return Price.objects.all()

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


class Mutation(graphene.ObjectType):
    update_user = UpdateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)