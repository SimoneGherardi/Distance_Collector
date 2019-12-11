from urllib import request
from django.shortcuts import render
from django.forms import models, formset_factory
from .models import *
from .forms import *

global passengers
passengers = []

global drivers
drivers = []

global destination
destination = []

def collecting_data_view(request):

    destination_formset = formset_factory(DestinationForm) #, fields=('address', 'city', 'country', 'zip_code'))
    passenger_formset = formset_factory(PassengerForm) #, fields=('first_name', 'last_name', 'starting_point'))
    driver_formset = formset_factory(DriverForm)# fields=('first_name', 'last_name', 'starting_point'))

    if 'destination submit' in request.POST:
        form_destination = destination_formset(request.POST)
        for form in form_destination:
            if form.is_valid():
                if len(destination) == 1:
                    destination.remove(destination[0])
                destination.append(form)

    if 'passengers submit' in request.POST:
        form_p = passenger_formset(request.POST)
        for form in form_p:
            if form.is_valid():
                passenger_to_add = Passenger(first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'], starting_point=form.cleaned_data['starting_point'])
                if passenger_to_add not in passengers:
                    passengers.append(passenger_to_add)

    if 'drivers submit' in request.POST:
        form_d = driver_formset(request.POST)
        for form in form_d:
            if form.is_valid():
                driver_to_add = Driver(first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'], starting_point=form.cleaned_data['starting_point'])
                if driver_to_add not in drivers:
                    drivers.append(driver_to_add)

    form_p = passenger_formset()
    form_d = driver_formset()
    form_destination = destination_formset()

    return render(request, 'base_app/collecting_data_template.html', {'form_p': form_p, 'form_d': form_d, 'form_destination': form_destination, 'passengers': passengers, 'drivers': drivers, 'destination': destination})


def show_result_view(request):

    return render(request, 'base_app/show_result_template.html')
