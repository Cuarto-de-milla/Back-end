""" Complaint model"""

# Django
from django.db import models
from django.contrib.auth.models import User

# Models
from gasoline.models import Station, Price
class Complaint(models.Model):
    """Complaint Model

    A complaint is a bad score that an user makes 
    about the prices in a special station.
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE
        )
    description = models.TextField(
        max_length=500,
        null=False,
        )
    link_evidence = models.CharField(max_length=255)
    type_complaint = models.CharField(max_length=255)

    date = models.DateTimeField(
        auto_now_add=True,
        help_text='Datetime when the complaint is created'
        )

    # Prices
    actual_price = models.ForeignKey(
        Price, 
        on_delete=models.CASCADE,
        help_text='Price registered in the system when creating the complaint'
        )
    offered_price = models.FloatField(
        max_length=5,
        help_text='Price published in the station'
        )

    def __str__(self):
        """ Returns user and datetime of the complaint."""
        return '{}: Actual price {}, offered_price {}'.format(
                self.user,
                self.actual_price,
                self.offered_price,
                )


