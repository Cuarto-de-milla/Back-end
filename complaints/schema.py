""" Complaint schema """

# Models
from complaints.models import Complaint
from django.contrib.auth.models import User
from gasoline.models import Station, Price

# Graphene
import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

# JWT 
from graphql_jwt.decorators import login_required

# Schemas
from gasoline.schema import StationType, PriceType
from users.schema import UserType

#------------------QUERIES---------------
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
            'actual_price',
            'offered_price'
        )


#-----------NODE-QUERIES----------
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

#---------------MUTATION--------------
class CreateComplaint(graphene.Mutation):
    """Create a new complaint

    Based in a price,gasoline station, and specified user
    Needs to be logged.
    """
    complaint = graphene.Field(ComplaintType)
    class Arguments:
        """Arguments necessaries to create a complaint"""
        price_id = graphene.Int(required=True)
        offered_price = graphene.Float(required=True)
        description = graphene.String(required=True)
        link_evidence = graphene.String(required=True)
        type_complaint = graphene.String(required=True)

    @login_required
    def mutate(self,info, **kwargs):
        """Mutation for create a complaint"""
        actual_price = Price.objects.get(pk=kwargs.get('price_id'))
        
        complaint = Complaint(
                            user=info.context.user,
                            station=actual_price.station,
                            actual_price=actual_price,
                            offered_price=kwargs.get('offered_price'),
                            description=kwargs.get('description'),
                            link_evidence=kwargs.get('link_evidence'),
                            type_complaint=kwargs.get('type_complaint'),
                    )
        complaint.save()
        return CreateComplaint(complaint=complaint)

#---------------SCHEMA---------------
class Query(graphene.ObjectType):
    """Complaints Query class."""
    my_complaints = graphene.List(ComplaintType)

    @login_required
    def resolve_my_complaints(root, info):
        """ Return complaints created by the logged user"""
        return Complaint.objects.filter(user=info.context.user)

    # Node Query Class
    complaint = relay.Node.Field(ComplaintNode)
    node_complaint = DjangoFilterConnectionField(ComplaintNode)


class Mutation(graphene.ObjectType):
    """ Complaints Mutation class."""
    create_complaint = CreateComplaint.Field()