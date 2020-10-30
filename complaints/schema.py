""" Complaint schema """

# Models
from complaints.models import Complaint

# Graphene
import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

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
            'date',
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


#---------------SCHEMA---------------
class Query(graphene.ObjectType):
    """Complaints Query class."""
    all_complaints = graphene.List(ComplaintType)

    def resolve_all_complaints(root, info):
            """ Return all complaints"""
            return Complaint.objects.all()

    # Node Query Class
    complaint = relay.Node.Field(ComplaintNode)
    node_complaint = DjangoFilterConnectionField(ComplaintNode)


class Mutation(graphene.ObjectType):
    """ Complaints Mutation class."""
    pass