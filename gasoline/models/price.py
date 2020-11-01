"""Price models """

# Django
from django.db import models
from django.contrib.auth.models import User

# Models 
from gasoline.models.station import Station

class Price(models.Model):
    """ Price Model

    Model that holds the prices of one type of gasoline by station.
    """
    station = models.ForeignKey(Station, on_delete=models.CASCADE)

    GAS_CHOICES = [
        ('premium','premium'),
        ('regular','regular'),
        ('diesel','diesel')
    ]

    gas_type = models.CharField(
        max_length=20,
        choices=GAS_CHOICES,
        help_text='Type of gasoline between the GAS_CHOICES',
        )
    price = models.FloatField(
        max_length=5,
        )
    date = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Date Time on wich the prices are registred'
        )
    def __str__(self):
        """ Returns price."""
        return f'{self.gas_type} cuesta {self.price} en {self.station}'