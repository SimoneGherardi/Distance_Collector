from django.shortcuts import render
from django.forms import modelformset_factory
from .models import *


def collecting_data_view(request):

    passenger_formset = modelformset_factory(Passenger, fields=('first_name', 'last_name', 'starting_point'))
    driver_formset = modelformset_factory(Driver, fields=('first_name', 'last_name', 'starting_point'))
    #if request.method == 'POST'['passengers submit']:
    if 'passengers submit' in request.POST:
        form_p = passenger_formset(request.POST)

        instances_p = form_p.save()

        #instances = form.save(commit=False)
        #for instance in instances:
        #        instance.save()

    #if request.method == 'POST'['drivers submit']:
    if 'drivers submit' in request.POST:
        form_d = driver_formset(request.POST)
        instances_d = form_d.save()

    form_p = passenger_formset()
    form_d = driver_formset()
    return render(request, 'base_app/collecting_data_template.html', {'form_p': form_p, 'form_d': form_d})
