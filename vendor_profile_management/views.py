from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from .models import Vendor
from .forms import VendorCreationForm
import sys
sys.path.append("..")
from vendor_performance_evaluation.models import Performance


# Create your views here.

@api_view(['GET'])
def get_vendor(request):
    Vendors = Vendor.objects.filter()
    return render(request, 'vendorProfiles/vendorsList.html', {'Vendors': Vendors})


@api_view(['GET'])
def get_vendor_detail(request, vendor_code):
    vendor = Vendor.objects.get(vendor_code=vendor_code)
    return render(request, 'vendorProfiles/vendordetails.html', {'vendor': vendor})


@api_view(['POST', 'GET'])
def delete_vendor(request, vendor_code):
    vendor = Vendor.objects.get(vendor_code=vendor_code)
    if request.method == 'POST':
        vendor.delete()
        return redirect('vendors-list')
    else:
        return render(request, 'vendorProfiles/confirm_delete.html', {'object': vendor})


@api_view(['GET', 'POST'])
def create_vendor(request):
    if request.method == 'POST':
        form = VendorCreationForm(request.POST)
        form.on_time_delivery_rate = 0
        form.quality_rating_avg = 0
        form.average_response_time = 0
        form.fulfillment_rate = 0
        try:
            form_u = form.save(commit=False)
        except Exception:
            return redirect('vendors-list')

        if form.is_valid():
            form_u.save()

            # create metrics record
            metrics = Performance(vendor=Vendor.objects.get(vendor_code=request.POST["vendor_code"]),on_time_delivery_rate=0,quality_rating_avg=0,average_response_time=0,fulfillment_rate=0)
            metrics.save()

            return redirect('vendors-list')
        else:
            return redirect('vendors-list')
    else:
        form = VendorCreationForm()
    return render(request, 'vendorProfiles/vendorCreate.html', {'form': form})


@api_view(['GET', 'POST'])
def update_vendor(request, vendor_code):
    if request.method == 'POST':
        curr_form = Vendor.objects.get(vendor_code=vendor_code)
        form = VendorCreationForm(request.POST, instance=curr_form)
        try:
            form_u = form.save(commit=False)
        except Exception:
            return redirect('vendors-list')

        if form.is_valid():
            form.save()
            return redirect('vendors-list')
    else:
        curr_form = Vendor.objects.get(vendor_code=vendor_code)
        form = VendorCreationForm(instance=curr_form)

    return render(request, 'vendorProfiles/vendorCreate.html', {'form': form})
