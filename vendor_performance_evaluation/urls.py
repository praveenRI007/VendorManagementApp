from django.urls import path
from .views import get_vendor_performance , po_acknowledgement , po_acknowledgement_list

urlpatterns = [
    path('api/vendors/<str:vendor_id>/performance', get_vendor_performance, name='get_vendor_performance'),
    path('api/purchase_orders/<str:po_id>/acknowledge', po_acknowledgement, name='po_acknowledgement'),
    path('api/purchase_orders_acknowledgementList', po_acknowledgement_list, name='po_acknowledgement_list')
]
