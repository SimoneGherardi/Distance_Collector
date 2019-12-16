from asyncio import wait
from urllib import request
from django.shortcuts import render
from django.forms import models, formset_factory
from geopy.distance import geodesic
import time
from .models import *
from .forms import *
import json
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
    passenger_to_add = Passenger(first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'],
                                 starting_point=(
                                         form.cleaned_data['address'] + ' , ' + form.cleaned_data['city'] + ' , ' +
                                         form.cleaned_data['zip_code'] + ' , ' + form.cleaned_data['country_code']))
    new_starting_place = Place()
    new_starting_place = fill_data_place(new_starting_place, form)
    new_starting_place.set_coordinates()
    passenger_to_add.starting_place = new_starting_place
    return passenger_to_add


def istanciate_new_driver(form):
    driver_to_add = Driver(first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'],
                           starting_point=(form.cleaned_data['address'] + ' , ' + form.cleaned_data['city'] + ' , ' +
                                           form.cleaned_data['zip_code'] + ' , ' + form.cleaned_data['country_code']))
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
        new_destination = Place
        for form in form_destination:
            if form.is_valid():
                new_destination = istanciate_new_destination(form)
                if new_destination.is_valid is True:
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
                    if passenger_to_add.starting_place.is_valid is True:
                        passengers.append(passenger_to_add)

    if 'drivers submit' in request.POST:
        form_d = driver_formset(request.POST)
        for form in form_d:
            if form.is_valid():
                driver_to_add = istanciate_new_driver(form)
                if driver_to_add not in drivers:
                    if driver_to_add.starting_place.is_valid is True:
                        drivers.append(driver_to_add)

    form_p = passenger_formset()
    form_d = driver_formset()
    form_destination = destination_formset()

    return render(request, 'base_app/collecting_data_template.html',
                  {'form_p': form_p, 'form_d': form_d, 'form_destination': form_destination, 'passengers': passengers,
                   'drivers': drivers, 'destination': destination})


def show_result_view(request):
    #   building the passengers_distance_matrix aka passenger_matrix
    p_rows_number = len(drivers)
    p_cols_number = len(passengers)
    i = 0;
    j = 0;
    passenger_matrix = [[0 for x in range(p_rows_number)] for y in range(p_cols_number)]
    for i in range(p_rows_number):
        for j in range(p_cols_number):
            passenger_matrix[j][i] = geodesic(drivers[i].starting_place.coordinates,
                                              passengers[j].starting_place.coordinates).km
            time.sleep(1)
    for i in range(p_rows_number):
        for j in range(p_cols_number):
            print(passenger_matrix[j][i])

    # il problema è che passi un oggetto Django al template ed in esso lo metti così com'é. Io l'ho convertito in un
    #   json e poi messo in una stringa. Siccome ce ne sono diversi, li ho messi tutti in una stringa lunga.
    #   Chiaramente questo approccio fa schifo al cazzo.

    # building the destination_distance_matrix aka the distance_matrix
    if len(destination) == 1:
        destination_matrix = [[0 for x in range(p_rows_number)] for y in range(2)]
        for i in range(p_rows_number):
            for j in range(1):
                destination_matrix[j][i] = geodesic(drivers[i].starting_place.coordinates,
                                                    destination[0].coordinates).km
                time.sleep(1)
    else:
        destination_matrix = []

    drivers_json_str = "["
    for driver in drivers:
        drivers_json_str += json.dumps(driver.to_json())
        drivers_json_str += ','
    drivers_json_str = drivers_json_str[:-1]
    drivers_json_str += "]"

    return render(request, 'base_app/show_result_template.html',
                  {'passengers': passengers, 'drivers': str(drivers_json_str), 'p_rows_number': p_rows_number,
                   'p_cols_number': p_cols_number, "destination": destination, 'passenger_matrix': passenger_matrix,
                   'destination_matrix': destination_matrix})
