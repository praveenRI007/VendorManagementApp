from django import forms
from .models import Vendor


class VendorCreationForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    contact_details = forms.CharField(max_length=300)
    address = forms.CharField(max_length=300)
    vendor_code = forms.CharField(max_length=100)
    on_time_delivery_rate = forms.FloatField(widget=forms.HiddenInput(), initial=0)
    quality_rating_avg = forms.FloatField(widget=forms.HiddenInput(), initial=0)
    average_response_time = forms.FloatField(widget=forms.HiddenInput(), initial=0)
    fulfillment_rate = forms.FloatField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Vendor
        fields = ['name', 'contact_details','address','vendor_code','on_time_delivery_rate','quality_rating_avg','average_response_time','fulfillment_rate']
