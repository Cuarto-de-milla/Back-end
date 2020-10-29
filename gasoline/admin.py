""" gasoline admin"""

# Django
from django.contrib import admin

# Models
from gasoline.models import Station, Price

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
