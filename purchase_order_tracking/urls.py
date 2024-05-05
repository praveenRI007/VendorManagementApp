from django.urls import path
from .views import get_po_list, get_po_detail , delete_po , create_po , update_po

urlpatterns = [
    path('api/purchase_orders', get_po_list, name='get_po_list'),
    path('api/purchase_orders/<str:po_number>', get_po_detail, name='get_po_detail'),
    path('api/purchase_orders/delete/<str:po_number>', delete_po, name='delete_po'),
    path('api/create/purchase_orders', create_po, name='create_po'),
    path('api/update/purchase_orders/<str:po_number>', update_po, name='update_po')
]
