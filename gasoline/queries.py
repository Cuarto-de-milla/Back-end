x = Stations(name="Pemex", latitude="18.99",longitude="17.99")
x.save()
y = Prices(station_id=x, date="2020-09-19",magna_price=17.99,premium_price=21.49, diesel_price=14.99)
y.save()

x = Stations(name="PetroGas", latitude=15.753,longitude=-8.397)
x.save()
y = Prices(station_id=x, date="2020-09-19",magna_price=16.99,premium_price=23.59, diesel_price=13.79)
y.save()

x = Stations(name="BritishPetro", latitude=13.77,longitude=-9.897)
x.save()
y = Prices(station_id=x, date="2020-09-19",magna_price=17.99,premium_price=21.19, diesel_price=15.77)
y.save()

x = Stations(name="7Gas", latitude="17.79",longitude="1.79")
x.save()
y = Prices(station_id=x, date="2020-09-19",magna_price=17.99,premium_price=21.49, diesel_price=14.99)
y.save()

x = Stations(name="OxxoGas", latitude=13.473,longitude=-12.3147)
x.save()
y = Prices(station_id=x, date="2020-09-19",magna_price=15.99,premium_price=25.59, diesel_price=15.79)
y.save()

x = Stations(name="WeetPetro", latitude=17.57,longitude=-1.897)
x.save()
y = Prices(station_id=x, date="2020-09-19",magna_price=12.99,premium_price=15.19, diesel_price=21.77)
y.save()