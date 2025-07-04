from django.contrib import admin
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import messages
from apps.load.models.amazon import AmazonRelayPayment, AmazonRelayProcessedRecord
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

admin.site.register(AmazonRelayPayment, AmazonRelayPaymentAdmin)
admin.site.register(AmazonRelayProcessedRecord, AmazonRelayProcessedRecordAdmin)