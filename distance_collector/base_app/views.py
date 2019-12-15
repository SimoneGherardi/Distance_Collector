from asyncio import wait
from urllib import request
from django.shortcuts import render
from django.forms import models, formset_factory
from geopy.distance import geodesic
import time
from .models import *
from .forms import *
from geopy.geocoders import Nominatim

global passengers
passengers = []

global drivers
drivers = []

global destination
destination = []


def fill_data_place(place, form):
    place.address = form.cleaned_data['address']
    place.city = form.cleaned_data['city']
    place.country_code = form.cleaned_data['country_code']
    place.zip_code = form.cleaned_data['zip_code']
    print(place.address + ' ' + place.city + ' ' + place.zip_code + ' ' + place.country_code)
    return place


def istanciate_new_passenger(form):

    passenger_to_add = Passenger(first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'], starting_point=(form.cleaned_data['address'] + ' , ' + form.cleaned_data['city'] + ' , ' + form.cleaned_data['zip_code'] + ' , ' + form.cleaned_data['country_code']))
    new_starting_place = Place()
    new_starting_place = fill_data_place(new_starting_place, form)
    new_starting_place.set_coordinates()
    passenger_to_add.starting_place = new_starting_place
#    passenger_to_add.starting_place = fill_data_place(passenger_to_add.starting_place, form)
#    passenger_to_add.starting_place.set_coordinates(passenger_to_add.starting_place)
    return passenger_to_add


def istanciate_new_driver(form):
    driver_to_add = Driver(first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'], starting_point=(form.cleaned_data['address'] + ' , ' + form.cleaned_data['city'] + ' , ' + form.cleaned_data['zip_code'] + ' , ' + form.cleaned_data['country_code']))
    new_starting_place = Place()
    new_starting_place = fill_data_place(new_starting_place, form)
    new_starting_place.set_coordinates()
    driver_to_add.starting_place = new_starting_place
#    driver_to_add.starting_place = fill_data_place(driver_to_add.starting_place, form)
#    driver_to_add.starting_place.set_coordinates(driver_to_add.starting_place)
    return driver_to_add


def istanciate_new_destination(form):
    new_destination = Place()
    new_destination = fill_data_place(new_destination, form)
    new_destination.set_coordinates()
    return new_destination


def collecting_data_view(request):

    destination_formset = formset_factory(DestinationForm)
    passenger_formset = formset_factory(PassengerForm)
    driver_formset = formset_factory(DriverForm)

    if 'destination submit' in request.POST:
        form_destination = destination_formset(request.POST)
        for form in form_destination:
            if form.is_valid():
                if destination is not None:
                    if len(destination) == 1:
                        print(destination[0].address)
                        destination.remove(destination[0])
                    destination.append(istanciate_new_destination(form))

    if 'passengers submit' in request.POST:
        form_p = passenger_formset(request.POST)
        for form in form_p:
            if form.is_valid():
                passenger_to_add = istanciate_new_passenger(form)
                if passenger_to_add not in passengers:
                    if passenger_to_add.starting_place is not None:
                        passengers.append(passenger_to_add)

    if 'drivers submit' in request.POST:
        form_d = driver_formset(request.POST)
        for form in form_d:
            if form.is_valid():
                driver_to_add = istanciate_new_driver(form)
                if driver_to_add not in drivers:
                    if driver_to_add.starting_place is not None:
                        drivers.append(driver_to_add)

    form_p = passenger_formset()
    form_d = driver_formset()
    form_destination = destination_formset()

    return render(request, 'base_app/collecting_data_template.html', {'form_p': form_p, 'form_d': form_d, 'form_destination': form_destination, 'passengers': passengers, 'drivers': drivers, 'destination': destination})


def show_result_view(request):

    passenger_distances_matrix = Matrix(matrix_name="passenger_distances_matrix")
    p_rows_number = len(drivers)
    p_cols_number = len(passengers)
    passenger_matrix = [[0 for x in range(p_cols_number)] for y in range(p_rows_number)]
    for i in range(p_rows_number):
        for j in range(p_cols_number):
            passenger_matrix[j][i] = Cell(matrix=passenger_distances_matrix, row=i, col=j, val=geodesic(drivers[i].starting_place.coordinates, passengers[j].starting_place.coordinates).km)
            time.sleep(1)
    print(passenger_matrix)
    for i in range(p_rows_number):
        for j in range(p_cols_number):
            print(passenger_matrix[j][i].val)

    drivers_distances_matrix = Matrix(matrix_name="drivers_distances_matrix")
    d_rows_number = len(drivers)
    d_cols_number = d_rows_number

    return render(request, 'base_app/show_result_template.html', {'passengers': passengers, 'drivers': drivers, 'p_rows_number': p_rows_number, 'p_cols_number': p_cols_number})
