from datetime import datetime
from django.db import connection
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from .models import Performance
import sys

sys.path.append("..")
from vendor_profile_management.models import Vendor
from purchase_order_tracking.models import PurchaseOrder
from purchase_order_tracking.forms import PurchaseOrderCreationForm


# Create your views here.
@api_view(['GET'])
def get_vendor_performance(request, vendor_id):
    try:
        vendor = Vendor.objects.get(vendor_code=vendor_id)
    except Vendor.DoesNotExist:
        return redirect('vendors-list')

    performance = Performance.objects.get(vendor=vendor)
    return render(request, 'VendorPerformance.html', {'performance': performance})


@api_view(['POST', 'GET'])
def po_acknowledgement(request, po_id):
    po = PurchaseOrder.objects.get(po_number=po_id)

    if request.method == 'POST':
        po = PurchaseOrder.objects.get(po_number=po_id)
        vendor_id = Vendor.objects.get(vendor_code=po.vendor.vendor_code)
        po.acknowledgment_date = str(datetime.now())
        po.save()

        # Average Response Time
        with connection.cursor() as c:
            query = f'SELECT avg(acknowledgment_date - issue_date) FROM purchase_order_tracking_purchaseorder where acknowledgment_date is not NULL and vendor_id="{vendor_id}"'
            c.execute(query)
            row = c.fetchone()
            average_response_time = row[0]
            if average_response_time is None:
                average_response_time = 0
            print('vendor acknowledged')
            query = f'update vendor_performance_evaluation_performance set average_response_time={average_response_time} where vendor_id="{vendor_id}"'
            c.execute(query)

        return redirect('home-page')
    else:
        return render(request, 'index.html', {'object': po})


@api_view(['GET'])
def po_acknowledgement_list(request):
    POS = PurchaseOrder.objects.exclude(acknowledgment_date__isnull=False)
    return render(request, 'acknowledgementList.html', {'POS': POS})
