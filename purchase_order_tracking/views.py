from datetime import datetime
from django.utils import timezone
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from .models import PurchaseOrder
from .forms import PurchaseOrderCreationForm
from django.db import connection
import sys
from django.db import transaction
sys.path.append("..")

from vendor_profile_management.models import Vendor


# Create your views here.

@api_view(['GET'])
def get_po_list(request):
    PurchaseOrders = PurchaseOrder.objects.filter()
    return render(request, 'purchaseOrders/poList.html', {'PurchaseOrders': PurchaseOrders})


@api_view(['GET'])
def get_po_detail(request, po_number):
    po = PurchaseOrder.objects.get(po_number=po_number)
    return render(request, 'purchaseOrders/podetail.html', {'po': po})


@api_view(['POST', 'GET'])
def delete_po(request, po_number):
    po = PurchaseOrder.objects.get(po_number=po_number)
    if request.method == 'POST':
        po.delete()
        return redirect('get_po_list')
    else:
        return render(request, 'purchaseOrders/confirm_delete.html', {'object': po})


@api_view(['GET', 'POST'])
def create_po(request):
    if request.method == 'POST':
        form = PurchaseOrderCreationForm(request.POST)

        try:
            if form.is_valid():
                form.issue_date = datetime.now()
                form.save()
        except Exception:
            return redirect('get_po_list')

        try:
            if form.data["status"] == "completed" and (form.data["acknowledgment_date"] is None or form.data["acknowledgment_date"] == ''):
                return redirect('get_po_list')

            if form.is_valid() and form.data["status"] == "completed" and form.data["completed_date"] == "":
                form = PurchaseOrderCreationForm(request.POST, instance=form)
                form_u = form.save(commit=False)
                form_u.completed_date = str(datetime.now())
                print('updated completed date')
            try:
                form.save()
            except Exception:
                return redirect('get_po_list')

        except Exception:
            return redirect('get_po_list')

        return redirect('get_po_list')
    else:
        form = PurchaseOrderCreationForm()
        return render(request, 'purchaseOrders/poCreate.html', {'form': form})


@api_view(['GET', 'POST'])
def update_po(request, po_number):
    if request.method == 'POST':
        curr_form = PurchaseOrder.objects.get(po_number=po_number)
        form = PurchaseOrderCreationForm(request.POST, instance=curr_form)

        if form.data["status"] == "completed" and (form.data["acknowledgment_date"] is None or form.data["acknowledgment_date"] == ''):
            return redirect('get_po_list')

        if form.is_valid() and form.data["status"] == "completed" and form.data["completed_date"] == "":
            form = PurchaseOrderCreationForm(request.POST, instance=curr_form)
            form_u = form.save(commit=False)
            form_u.completed_date = str(datetime.now())
            form_u.save()
            print('updated completed date')
        try:
            form.save()
        except Exception:
            return redirect('get_po_list')

        return redirect('get_po_list')
    else:
        curr_form = PurchaseOrder.objects.get(po_number=po_number)
        form = PurchaseOrderCreationForm(instance=curr_form)

    return render(request, 'purchaseOrders/poCreate.html', {'form': form})
