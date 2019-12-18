import geopy
from django.contrib.gis.db import models
from geopy import Point
from geopy.geocoders import Nominatim


class Car(models.Model):
    # to be changed
    car_name = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=50)
    fuel_consumption = models.FloatField


class Place(models.Model):
    address = models.CharField(max_length=100)
    coordinates = geopy.point.Point
    city = models.CharField(max_length=100, default='')
    country_code = models.CharField(max_length=2, default='')
    zip_code = models.CharField(max_length=20, default='')
    is_valid = models.BooleanField = True

    def set_coordinates(self):
        geo_locator = Nominatim(user_agent="distance_collector")
        nom = Nominatim(domain='localhost:8000', scheme='http')
        my_query = dict({'street': self.address, 'city': self.city, 'postalcode': self.zip_code})
        nominatim_data = geo_locator.geocode(query=my_query, exactly_one=True, timeout=10,
                                             country_codes=self.country_code)
        if nominatim_data is None:
            print("Wrong Address Format")
            self.is_valid = False
            return None
        self.coordinates = nominatim_data.point
        print(self.coordinates)

        return self


class Person(models.Model):
    _id = models.AutoField
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


class Passenger(Person):
    starting_point = models.CharField(max_length=200, default='')
    starting_place = Place
    destination_place = Place
    time_of_appearance = models.TimeField
    endurance_time = models.DurationField


class Driver(Passenger):
    car = Car
    is_driving = models.BooleanField

    #better use Serializer
    def to_json(self):
        return {"last_name": self.last_name, "first_name": self.first_name}


class Trip(models.Model):
    _id = models.AutoField
    passengers = models.ManyToManyField(Passenger, related_name='not_driving_passengers')
    drivers = models.ManyToManyField(Driver, related_name='driving_passengers')
    destination = Place
    date = models.DateField
    arrival_time = models.TimeField

    def add_passenger(self, passenger):
        self.passengers.add(passenger)

    def add_driver(self, driver):
        self.drivers.add(driver)
