from django.contrib import admin
# from apps.load.models.amazon import AmazonRelayPayment
from apps.load.models.driver import Pay, DriverPay, DriverExpense
from apps.load.models.truck import Unit
from apps.load.models.team import Team
from apps.load.models import (
    Load, LoadTags, Driver, DriverTags, Trailer, 
    TrailerTags, TruckTags, Truck, Dispatcher,
    DispatcherTags, EmployeeTags, CustomerBroker, 
    Stops, Employee, OtherPay, Commodities)

# admin.py
from django.contrib import admin
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import messages
from apps.load.models.amazon import (
    AmazonRelayPayment, AmazonRelayProcessedRecord
)
class AmazonRelayPaymentAdmin(admin.ModelAdmin):
    list_display = ['uploaded_at', 'status', 'total_amount', 'loads_updated', 'processed_at']
    list_filter = ['status', 'uploaded_at']
    readonly_fields = ['uploaded_at', 'processed_at', 'total_amount', 'loads_updated', 'error_message']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ['file']
        return self.readonly_fields

class AmazonRelayProcessedRecordAdmin(admin.ModelAdmin):
    list_display = ['payment', 'trip_id', 'load_id', 'gross_pay', 'is_matched', 'matched_load']
    list_filter = ['is_matched', 'payment__status', 'created_at']
    search_fields = ['trip_id', 'load_id', 'matched_load__reference_id']
    raw_id_fields = ['matched_load']

admin.site.register(AmazonRelayPayment, AmazonRelayPaymentAdmin)
admin.site.register(AmazonRelayProcessedRecord, AmazonRelayProcessedRecordAdmin)


# admin.site.register(AmazonRelayPayment)
admin.site.register(DriverExpense)
admin.site.register(Pay)
admin.site.register(DriverPay)
admin.site.register(Load)
admin.site.register(Unit)
admin.site.register(LoadTags)
admin.site.register(Team)
admin.site.register(Driver)

admin.site.register(DriverTags)

admin.site.register(Trailer)

admin.site.register(TrailerTags)

admin.site.register(TruckTags)

admin.site.register(Truck)

admin.site.register(Dispatcher)

admin.site.register(DispatcherTags)

admin.site.register(EmployeeTags)

admin.site.register(CustomerBroker)

admin.site.register(Stops)

admin.site.register(Employee)

admin.site.register(OtherPay)

admin.site.register(Commodities)