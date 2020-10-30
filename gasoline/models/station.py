"""Station model """

# Django
from django.db import models
from django.contrib.auth.models import User

class Station(models.Model):
    """ Station Model"""
    # Information
    name = models.CharField(
        max_length=200,
    )
    about = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text='Short description of the station'
        ) 
    picture = models.ImageField(
        upload_to=None,
        blank=True,
        null=True
        )
    register = models.CharField(
        max_length=64,
        unique=True,
        blank=True,
        null=True,
        help_text='Unique Register given for the Mexican Govenment')
    
    # Location
    latitude = models.FloatField(max_length=9)
    longitude = models.FloatField(max_length=9)
    town = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        )
    state = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text='Official name of the Mexican state where is located the station'
        )

    # Status
    is_active = models.BooleanField(default=False)
    status = models.CharField(
        max_length=10,
        default='ghost',
        help_text="Station' status based on their activity. It changes when a user verify the station "
        )

    def __str__(self):
        """Return station name"""
        return self.name