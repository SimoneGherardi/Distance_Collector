from urllib import request
from django.shortcuts import render
from django.forms import modelformset_factory, models
from .models import *


#def create_new_passenger_object(new_passenger, passengers):
#    for data_set in new_passenger:
#        tmp = data_set.cleaned_data
#        new_passenger = Passenger(first_name=tmp.get('first_name'), last_name=tmp.get('last_name'), starting_point=tmp.get('starting_point'))
#        if new_passenger not in passengers:
#            passengers.add(new_passenger)


#def create_new_driver_object(new_drivers, drivers):
#    for data_set in new_drivers:
#        tmp = data_set.cleaned_data
#        new_driver = Driver(first_name=tmp.get('first_name'), last_name=tmp.get('last_name'), starting_point=tmp.get('starting_point'))
#        if new_driver not in drivers:
#            drivers.add(new_driver)


def collecting_data_view(request):

    destination_formset = modelformset_factory(DestinationForm, fields=('address', 'city', 'country', 'zip_code'))
    passenger_formset = modelformset_factory(PassengerForm, fields=('first_name', 'last_name', 'starting_point'))
    driver_formset = modelformset_factory(DriverForm, fields=('first_name', 'last_name', 'starting_point'))
    passengers = models.ManyToManyField(Passenger, related_name='added_passengers')
    drivers = models.ManyToManyField(Driver, related_name='added_drivers')

    if 'destination submit' in request.POST:
        form_destination = destination_formset(request.POST)
        instances_destination = form_destination.save()


    if 'passengers submit' in request.POST:
        form_p = passenger_formset(request.POST)
        instances_p = form_p.save()
  #      for instance in instances_p:
#           create_new_passenger_object(instances_p, passengers)

    if 'drivers submit' in request.POST:
        form_d = driver_formset(request.POST)
        instances_d = form_d.save()
 #     for instance in instances_d:
    #          create_new_driver_object(instances_d, drivers)

    form_p = passenger_formset()
    form_d = driver_formset()
    return render(request, 'base_app/collecting_data_template.html', {'form_p': form_p, 'form_d': form_d, 'form_destination': form_destination})


def show_result_view(request):

    return render(request, 'base_app/show_result_template.html')
