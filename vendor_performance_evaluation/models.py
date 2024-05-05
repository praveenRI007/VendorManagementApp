from django.utils import timezone
from django.db import models
from vendor_profile_management.models import Vendor


# Create your models here.
class Performance(models.Model):
    vendor = models.ForeignKey(Vendor,related_name='vendor_po', on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()
