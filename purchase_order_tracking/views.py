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

            on_time_delivery_rate = 0
            quality_rating_avg = 0
            fulfillment_rate = 0

            #  On-Time Delivery Rate
            with connection.cursor() as c:
                temp = PurchaseOrder.objects.get(po_number=form.data["po_number"])

                query = f'SELECT count(*) FROM purchase_order_tracking_purchaseorder where status=="completed" and completed_date<delivery_date and vendor_id={temp.vendor.vendor_code}'
                c.execute(query)
                row = c.fetchone()
                successful_delivery_count = row[0]

                query = f'SELECT count(*) FROM purchase_order_tracking_purchaseorder where status=="completed" and vendor_id={temp.vendor.vendor_code}'
                c.execute(query)
                row = c.fetchone()
                completed_count = row[0]

                query = f'SELECT avg(quality_rating) FROM purchase_order_tracking_purchaseorder where status=="completed" and vendor_id={temp.vendor.vendor_code}'
                c.execute(query)
                row = c.fetchone()
                avg_quality_rating = row[0]

                query = f'SELECT count(*) FROM purchase_order_tracking_purchaseorder where vendor_id={temp.vendor.vendor_code}'
                c.execute(query)
                row = c.fetchone()
                total_pos = row[0]

            vendor1 = Vendor.objects.get(vendor_code=form.data["vendor"])
            if successful_delivery_count == 0 or completed_count == 0:
                vendor1.on_time_delivery_rate = 0
                vendor1.save()
                on_time_delivery_rate = 0
            else:
                vendor1.on_time_delivery_rate = (successful_delivery_count / completed_count)
                vendor1.save()
                on_time_delivery_rate = (successful_delivery_count / completed_count)

            #  Quality Rating Average:
            vendor2 = Vendor.objects.get(vendor_code=form.data["vendor"])
            vendor2.quality_rating_avg = avg_quality_rating
            vendor2.save()
            quality_rating_avg = avg_quality_rating

            #  Average Response Time

            #  Fulfilment Rate
            vendor3 = Vendor.objects.get(vendor_code=form.data["vendor"])
            if completed_count == 0 or total_pos == 0:
                vendor3.fulfillment_rate = 0
                vendor3.save()
                fulfillment_rate = 0
            else:
                vendor3.fulfillment_rate = completed_count / total_pos
                vendor3.save()
                fulfillment_rate = completed_count / total_pos

            with connection.cursor() as c:
                temp = PurchaseOrder.objects.get(po_number=form.data["po_number"])
                query = f'update vendor_performance_evaluation_performance set on_time_delivery_rate={on_time_delivery_rate},quality_rating_avg={quality_rating_avg},fulfillment_rate={fulfillment_rate} where vendor_id={temp.vendor.vendor_code}'
                c.execute(query)
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

        on_time_delivery_rate = 0
        quality_rating_avg = 0
        fulfillment_rate = 0

        #  On-Time Delivery Rate
        with connection.cursor() as c:
            temp = PurchaseOrder.objects.get(po_number=po_number)

            query = f'SELECT count(*) FROM purchase_order_tracking_purchaseorder where status=="completed" and completed_date<delivery_date and vendor_id={temp.vendor.vendor_code}'
            c.execute(query)
            row = c.fetchone()
            successful_delivery_count = row[0]

            query = f'SELECT count(*) FROM purchase_order_tracking_purchaseorder where status=="completed" and vendor_id={temp.vendor.vendor_code}'
            c.execute(query)
            row = c.fetchone()
            completed_count = row[0]

            query = f'SELECT avg(quality_rating) FROM purchase_order_tracking_purchaseorder where status=="completed" and vendor_id={temp.vendor.vendor_code}'
            c.execute(query)
            row = c.fetchone()
            avg_quality_rating = row[0]

            query = f'SELECT count(*) FROM purchase_order_tracking_purchaseorder where vendor_id={temp.vendor.vendor_code}'
            c.execute(query)
            row = c.fetchone()
            total_pos = row[0]

        if successful_delivery_count == 0 or completed_count == 0:
            vendor = Vendor.objects.get(vendor_code=form.data["vendor"])
            vendor.on_time_delivery_rate = 0
            vendor.save()
            on_time_delivery_rate = 0
        else:
            vendor = Vendor.objects.get(vendor_code=form.data["vendor"])
            vendor.on_time_delivery_rate = (successful_delivery_count / completed_count)
            vendor.save()
            on_time_delivery_rate = (successful_delivery_count / completed_count)

        #  Quality Rating Average:
        vendor = Vendor.objects.get(vendor_code=form.data["vendor"])
        if avg_quality_rating is None:
            vendor.quality_rating_avg = 0
            avg_quality_rating = 0
        else:
            vendor.quality_rating_avg = avg_quality_rating
        vendor.save()
        quality_rating_avg = avg_quality_rating


        #  Fulfilment Rate
        if completed_count == 0 or total_pos == 0:
            vendor = Vendor.objects.get(vendor_code=form.data["vendor"])
            vendor.fulfillment_rate = 0
            vendor.save()
            fulfillment_rate = 0
        else:
            vendor = Vendor.objects.get(vendor_code=form.data["vendor"])
            vendor.fulfillment_rate = completed_count / total_pos
            vendor.save()
            fulfillment_rate = completed_count / total_pos

        with connection.cursor() as c:
            temp = PurchaseOrder.objects.get(po_number=po_number)
            query = f'update vendor_performance_evaluation_performance set on_time_delivery_rate={on_time_delivery_rate},quality_rating_avg={quality_rating_avg},fulfillment_rate={fulfillment_rate} where vendor_id={temp.vendor.vendor_code}'
            c.execute(query)

        return redirect('get_po_list')
    else:
        curr_form = PurchaseOrder.objects.get(po_number=po_number)
        form = PurchaseOrderCreationForm(instance=curr_form)

    return render(request, 'purchaseOrders/poCreate.html', {'form': form})
