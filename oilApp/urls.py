"""oilApp URL  """

# Django
from django.contrib import admin
from django.urls import path

# Graphene
from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("graphql", GraphQLView.as_view(graphiql=True))
]
