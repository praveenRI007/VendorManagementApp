from django.urls import path
from .views import get_vendor, get_vendor_detail , delete_vendor , create_vendor , update_vendor

urlpatterns = [
    path('api/vendors', get_vendor, name='vendors-list'),
    path('api/vendors/<str:vendor_code>', get_vendor_detail, name='get-vendor-detail'),
    path('api/vendors/delete/<str:vendor_code>', delete_vendor, name='delete-vendor'),
    path('api/create/vendor', create_vendor, name='create-vendor'),
    path('api/update/vendor/<str:vendor_code>', update_vendor, name='update-vendor')
]
