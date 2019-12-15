from django import forms


class PassengerForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=200)
    city = forms.CharField(max_length=100)
    country_code = forms.CharField(max_length=2)
    zip_code = forms.CharField(max_length=20)



class DriverForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=200)
    city = forms.CharField(max_length=100)
    country_code = forms.CharField(max_length=2)
    zip_code = forms.CharField(max_length=20)
    # car's data


class DestinationForm(forms.Form):
    address = forms.CharField(max_length=200)
    city = forms.CharField(max_length=100)
    country_code = forms.CharField(max_length=2)
    zip_code = forms.CharField(max_length=20)