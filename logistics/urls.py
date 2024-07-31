from django.urls import path
from .views import *

app_name = 'logistics'

urlpatterns = [
    path('user-shipments/', UserShipments.as_view(), name='shipments'),
    path('all-shipments/', AllShipments.as_view(), name='all-shipments'),
    path('shipment-detail/', trackShipment, name='shipment-detail'),
    path('add-shipment/', AddShipment.as_view(), name='add-shipment'),
    path('contact-us/', ContactView.as_view(), name='contact-us'),
    path('delete-shipment/<slug:slug>/delete/',
         deleteShipment, name='delete-shipment'),
    path('update-shipment/<slug:slug>/',
         UpdateShipment.as_view(), name='update-shipment'),
    path('', IndexView.as_view(), name='home'),

]
