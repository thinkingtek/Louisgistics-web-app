from django.contrib import admin
from .models import Shipment


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('staff',  'tracking_id', 'sender_name', 'sender_phone',
                    'state_of_origin', 'updated_timestamp', 'status', 'request_refund')
    search_fields = ('sender_name', 'tracking_id', 'state_of_origin__name')
    list_per_page = 35
    prepopulated_fields = {"slug": ['tracking_id']}
