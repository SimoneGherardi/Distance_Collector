from django.shortcuts import render


def collecting_data_view(request):
    return render(request, 'base_app/collecting_data_template.html', {})
