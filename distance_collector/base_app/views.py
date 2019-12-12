from urllib import request
from django.shortcuts import render
from django.forms import models, modelformset_factory, modelform_factory
from .models import *
from .forms import *


def collecting_data_view(request):
    destination_formset = modelform_factory(Place)  # , fields=('address', 'city', 'country', 'zip_code'))
    passenger_formset = modelformset_factory(Passenger,
                                             extra=1)  # , fields=('first_name', 'last_name', 'starting_point'))
    driver_formset = modelformset_factory(Driver, extra=1)  # fields=('first_name', 'last_name', 'starting_point'))

    if 'destination submit' in request.POST:
        form_destination = destination_formset(request.POST)
        for form in form_destination:
            if form.is_valid():
                form.save()

    if 'passengers submit' in request.POST:
        form_p = passenger_formset(request.POST)
        for form in form_p:
            if form.is_valid():
                form.save()

    if 'drivers submit' in request.POST:
        form_d = driver_formset(request.POST)
        for form in form_d:
            if form.is_valid():
                form.save()

    form_p = passenger_formset()
    form_d = driver_formset()
    form_destination = destination_formset()

    return render(request, 'base_app/collecting_data_template.html',
                  {'form_p': form_p, 'form_d': form_d, 'form_destination': form_destination, 'passengers': Passenger.objects,
                   'drivers': Driver.objects, 'destination': Place.objects})


def show_result_view(request):
    return render(request, 'base_app/show_result_template.html')
