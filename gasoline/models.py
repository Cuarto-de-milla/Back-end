from django.db import models
from django.contrib.auth.models import User


class Stations(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.FloatField(max_length=9)
    longitude = models.FloatField(max_length=9)

    register = models.CharField(max_length=64)
    active = models.BooleanField(default=True)
    status = models.CharField(max_length=10,default='ghost')

    def __str__(self):
        return self.name

class Prices(models.Model):

    station_id = models.ForeignKey(Stations, on_delete=models.PROTECT)

    date = models.DateField()
    magna_price = models.FloatField(max_length=5)
    premium_price = models.FloatField(max_length=5)
    diesel_price = models.FloatField(max_length=5)

    def __str__(self):
        return f"""{self.magna_price} cuesta la magna en {self.station_id}
                {self.premium_price} cuesta la premium en {self.station_id}
                {self.diesel_price} cuesta el diesel en {self.station_id}
        """



class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)

    def __str__(self):
        return self

class Complaints(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.PROTECT)

    date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=255)
    link_evidence = models.CharField(max_length=255)
    type_complaint = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user_id} en {self.date}'

"""
class GasTypes(models.Model):
    stations = models.ForeignKey(Stations, on_delete=models.PROTECT)
    prices = models.ForeignKey(Prices, on_delete=models.PROTECT)

    gasType = models.CharField(max_length=25)

    def __str__(self):
        return self.gasType
"""     


    



