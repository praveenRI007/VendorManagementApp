from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder
import sys
sys.path.append("..")
from vendor_profile_management.models import Vendor
from django.db import connection


@receiver(post_save, sender=PurchaseOrder)
def update_metrics(sender, instance, created, **kwargs):
    if created or not created:
        on_time_delivery_rate = 0
        quality_rating_avg = 0
        fulfillment_rate = 0
        #  On-Time Delivery Rate
        with connection.cursor() as c:
            temp = PurchaseOrder.objects.get(po_number=instance.po_number)

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
            vendor = Vendor.objects.get(vendor_code=instance.vendor)
            vendor.on_time_delivery_rate = 0
            vendor.save()
            on_time_delivery_rate = 0
        else:
            vendor = Vendor.objects.get(vendor_code=instance.vendor.vendor_code)
            vendor.on_time_delivery_rate = (successful_delivery_count / completed_count)
            vendor.save()
            on_time_delivery_rate = (successful_delivery_count / completed_count)

        #  Quality Rating Average:
        vendor = Vendor.objects.get(vendor_code=instance.vendor.vendor_code)
        if avg_quality_rating is None:
            vendor.quality_rating_avg = 0
            avg_quality_rating = 0
        else:
            vendor.quality_rating_avg = avg_quality_rating
        vendor.save()
        quality_rating_avg = avg_quality_rating

        #  Fulfilment Rate
        if completed_count == 0 or total_pos == 0:
            vendor = Vendor.objects.get(vendor_code=instance.vendor.vendor_code)
            vendor.fulfillment_rate = 0
            vendor.save()
            fulfillment_rate = 0
        else:
            vendor = Vendor.objects.get(vendor_code=instance.vendor.vendor_code)
            vendor.fulfillment_rate = completed_count / total_pos
            vendor.save()
            fulfillment_rate = completed_count / total_pos

        with connection.cursor() as c:
            temp = PurchaseOrder.objects.get(po_number=instance.po_number)
            query = f'update vendor_performance_evaluation_performance set on_time_delivery_rate={on_time_delivery_rate},quality_rating_avg={quality_rating_avg},fulfillment_rate={fulfillment_rate} where vendor_id={temp.vendor.vendor_code}'
            c.execute(query)

