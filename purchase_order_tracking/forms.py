from django import forms
from django.forms import DateInput
import sys
sys.path.append("..")

from vendor_profile_management.models import Vendor
from .models import PurchaseOrder
from django.utils import timezone

choices = [
    ('pending', 'pending'),
    ('completed', "completed"),
    ('canceled', "canceled")
]


class PurchaseOrderCreationForm(forms.ModelForm):
    po_number = forms.CharField(max_length=100)
    order_date = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': 'yyyy-mm-dd'}))
    delivery_date = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': 'yyyy-mm-dd'}))
    items = forms.JSONField()
    quantity = forms.IntegerField()
    status = forms.ChoiceField(choices=choices)
    quality_rating = forms.FloatField()
    issue_date = forms.DateTimeField(widget=forms.HiddenInput(),initial=timezone.now)
    acknowledgment_date = forms.DateTimeField(widget=forms.HiddenInput(),required=False)
    completed_date = forms.DateTimeField(widget=forms.HiddenInput(),required=False)

    class Meta:
        model = PurchaseOrder
        fields = ['po_number', 'vendor', 'order_date', 'delivery_date', 'items', 'quantity', 'status', 'quality_rating',
                  'issue_date', 'acknowledgment_date']

    def clean(self):
        cleaned_data = super().clean()
        order_date = cleaned_data.get("order_date")
        delivery_date = cleaned_data.get("delivery_date")
        if delivery_date < order_date:
            raise forms.ValidationError("End date should be greater than start date.")
