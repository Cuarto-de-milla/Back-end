"""Gasoline models """

# Django
from django.db import models
from django.contrib.auth.models import User

class Stations(models.Model):
    """ Stations Model"""
    # Information
    name = models.CharField(max_length=200)
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

    # Location
    latitude = models.FloatField(max_length=9)
    longitude = models.FloatField(max_length=9)
    city = models.CharField(max_length=50)
    state = models.CharField(
        max_length=50
        help_text='Oficial name of the Mexican state where is located the station'
        )

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

    Model that holds the prices of one type of gasoline by station.
    """
    station = models.ForeignKey(Stations, on_delete=models.PROTECT)

    GAS_CHOICES = [
        ('PR':'Premium'),
        ('MG':'Magna'),
        ('DS':'Diesel')
    ]
    gas_type = models.CharField(
        GasTypes, 
        on_delete=models.PROTECT,
        choices=GAS_CHOISES,
        help_text='Type of gasoline beetwetn the GAS_CHOICES',
        )
    price = models.FloatField(
        max_length=5,
        )
    date = models.DateTimeField(
        'created at',
        auto_now=True
        help_text='Date Time on wich the prices are registred'
        )
    def __str__(self):
        """ Returns price."""
        return f'{self.gas_type} cuesta {self.price} en {self.station}'


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
    station = models.ForeignKey(
        Stations,
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
        Prices, 
        on_delete=models.PROTECT,
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


