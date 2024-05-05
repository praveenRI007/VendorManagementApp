from django.db import models
from django.utils import timezone
from vendor_profile_management.models import Vendor

choices = [
    ('pending', 'pending'),
    ('completed', "completed"),
    ('canceled', "canceled")
]


# Create your models here.
class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True, primary_key=True)
    vendor = models.ForeignKey(Vendor, related_name='vendor_pot', on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=10, choices=choices, default='pending')
    quality_rating = models.FloatField()
    issue_date = models.DateTimeField(default=timezone.now)
    acknowledgment_date = models.DateTimeField(null=True,blank=True)
    completed_date = models.DateTimeField(null=True,blank=True)