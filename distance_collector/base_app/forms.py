from django import forms


class PassengerForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    starting_point = forms.CharField(max_length=200)


class DriverForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    starting_point = forms.CharField(max_length=200)


class DestinationForm(forms.Form):
    address = forms.CharField(max_length=200)
    city = forms.CharField(max_length=100)
    country = forms.CharField(max_length=50)
    zip_code = forms.CharField(max_length=20)