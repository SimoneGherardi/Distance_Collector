from django.db import models
from django.contrib.gis.db import models


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
    coordinates = models.PointField
    # to be defined

#   def __init__(self, address, *args, **kwargs):
#       super().__init__(*args, **kwargs)
#       self.address = address

    def set_coordinates(self):
        return

    def calculate_distance(self, place):
        distance = 42
        return distance


class Passenger(Person):
    starting_point = models.CharField(max_length=100, default='')
    destination_point = Place
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
