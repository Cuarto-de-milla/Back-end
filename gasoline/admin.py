""" gasoline model admin"""

# Django
from django.contrib import admin

# Models
from .models import Station, Price, Profile, Complaint

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    """Station model admin"""

    list_display = (
        'name',
        'about',
        'picture',
        'register',
        'latitude',
        'longitude',
        'state',
        'is_active',
        'status',
    )
    list_filter =(
        'state',
        'is_active',
        'status',
    )


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    """Price model admin"""

    list_display = (
        'id',
        'station',
        'gas_type',
        'price',
        'date',
    )

    list_filter = (
        'station',
        'gas_type',
        'date',
    )

@admin.register(Complaint)
class  ComplaintAdmin(admin.ModelAdmin):
    """ Complaint model Admin"""

    list_display = (
        'user',
        'station',
        'description',
        'link_evidence',
        'type_complaint',
        'date',
        'actual_price',
        'offered_price',
    )

    list_filter = (
        'user',
        'station',
        'type_complaint',
        'date',
    )