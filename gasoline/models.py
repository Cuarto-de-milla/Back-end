"""Gasoline models """

# Django
from django.db import models
from django.contrib.auth.models import User

class Stations(models.Model):
    """ Stations Model"""
    name = models.CharField(max_length=200)
    
    # Location
    latitude = models.FloatField(max_length=9)
    longitude = models.FloatField(max_length=9)
    
    # Status
    is_active = models.BooleanField(default=True)
    status = models.CharField(
        max_length=10,
        default='ghost',
        help_text="Station' status based on their activity. It changes when a user verify the station "
        )

    def __str__(self):
        """Return station name"""
        return self.name

class Prices(models.Model):
    """ Prices Model

    Model that holds the prices of each type of gasoline by station.
    """
    station = models.ForeignKey(Stations, on_delete=models.PROTECT)

    date = models.DateTimeField(
        'created at',
        auto_now=True
        help_text='Date Time on wich the prices are registred'
        )
    magna_price = models.FloatField(
        max_length=5,
        null=True
        )
    premium_price = models.FloatField(
        max_length=5,
        null=True
        )
    diesel_price = models.FloatField(
        max_length=5,
        null=True
        )

    def __str__(self):
        """ Returns price of magna."""
        return f'{self.magna_price} cuesta la magna en {self.station}'
"""
class GasTypes(models.Model):
    stations = models.ForeignKey(Stations, on_delete=models.PROTECT)
    prices = models.ForeignKey(Prices, on_delete=models.PROTECT)

    gasType = models.CharField(max_length=25)

    def __str__(self):
        return self.gasType
"""        
class Profile(models.Model):
    """Profile Model 
    
    Model that extends the user model and add extra information of the user.
    """

    user = models.OneToOneField(User, on_delete=models.PROTECT)

    def __str__(self):
        """Returns string representation of user"""
        return self

class Complaints(models.Model):
    """Complaints Model

    A complaint is a bad calification that an user makes 
    about the prices in a special station.
    """
    user = models.ForeignKey(
        Users, 
        on_delete=models.PROTECT
    )
    date = models.DateTimeField(
        auto_now_add=True,
        help_text='Datetime when the complaint is created')
    description = models.TextField(
        max_length=500,
        null=False,
        )
    link_evidence = models.CharField(max_length=255)
    type_complaint = models.CharField(max_length=255)

    def __str__(self):
        """ Returns usern and datetime of the complaint."""
        return f'{self.user} en {self.date}'


