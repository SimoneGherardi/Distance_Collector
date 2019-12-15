import geopy
from django.db import models
from django.contrib.gis.db import models
from geopy import Point
from geopy.geocoders import Nominatim
from geopy.distance import lonlat, distance


class Person(models.Model):
    _id = models.AutoField
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

#    def __init__(self, first_name, last_name, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.first_name = first_name
#        self.last_name = last_name


class Car(models.Model):
    # to be changed
    car_name = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=50)
    fuel_consumption = models.FloatField

#   def __init__(self, car_name, fuel_type, fuel_consumption, *args, **kwargs):
#       super().__init__(*args, **kwargs)
#       self.car_name = car_name
#       self.fuel_type = fuel_type
#       self.fuel_consumption = fuel_consumption


class Place(models.Model):
    address = models.CharField(max_length=100)
    coordinates = geopy.point.Point
    city = models.CharField(max_length=100, default='')
    country_code = models.CharField(max_length=2, default='')
    zip_code = models.CharField(max_length=20, default='')

    def set_coordinates(self):

        geo_locator = Nominatim(user_agent="distance_collector")
        nom = Nominatim(domain='localhost:8000', scheme='http')
        my_query = dict({'street': self.address, 'city': self.city, 'postalcode': self.zip_code})
        nominatim_data = geo_locator.geocode(query=my_query, exactly_one=True, timeout=10, country_codes=self.country_code)
        if nominatim_data is None:
            print("Wrong Address Format")
            return None
        self.coordinates = nominatim_data.point
        print(self.coordinates)
#self.coordinates = Point(latitude=nominatim_data.latitude, longitude=nominatim_data.longitude, altitude=nominatim_data.altitude) # latitude and longitude are in degrees, while altitude is in kilometers

        return self

    def calculate_distance(self, place):
        return geopy.distance.distance(self.coordinates, place.coordinates).km


class Passenger(Person):
    starting_point = models.CharField(max_length=200, default='')
    starting_place = Place
    destination_place = Place
    time_of_appearance = models.TimeField
    endurance_time = models.DurationField

#   def __init__(self, first_name, last_name, starting_point=None, destination_point=None, *args, **kwargs):
#       super().__init__(first_name, last_name, *args, **kwargs)
#       self.starting_point = starting_point
#       self.destination_point = destination_point


class Driver(Passenger):
    car = Car
    is_driving = models.BooleanField

#   def __init__(self, first_name, last_name, starting_point=None, destination_point=None, *args, **kwargs):
#       super().__init__(first_name, last_name, starting_point, destination_point, *args, **kwargs)
        # create new Car


class Matrix(models.Model):
    matrix_name = models.CharField(max_length=100)


class Cell(models.Model):
    matrix = models.ForeignKey(Matrix, on_delete=models.CASCADE)
    row = models.IntegerField()
    col = models.IntegerField()
    val = models.FloatField()


class Trip(models.Model):
    _id = models.AutoField
    passengers = models.ManyToManyField(Passenger, related_name='not_driving_passengers')
    drivers = models.ManyToManyField(Driver, related_name='driving_passengers')
    destination = Place
    date = models.DateField
    arrival_time = models.TimeField

#   def __init__(self, destination, date, arrival_time,  *args, **kwargs):
#       super().__init__(*args, **kwargs)
#       self.destination = destination
#       self.date = date
#       self.arrival_time = arrival_time

    def add_passenger(self, passenger):
        self.passengers.add(passenger)

    def add_driver(self, driver):
        self.drivers.add(driver)

