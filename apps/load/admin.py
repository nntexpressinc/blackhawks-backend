from django.contrib import admin
from apps.load.models.driver import Pay, DriverPay, DriverExpense
from apps.load.models.truck import Unit
from apps.load.models.team import Team
from apps.load.models import (
    Load, LoadTags, Driver, DriverTags, Trailer, 
    TrailerTags, TruckTags, Truck, Dispatcher,
    DispatcherTags, EmployeeTags, CustomerBroker, 
    Stops, Employee, OtherPay, Commodities, CSVImport)

# Register models
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
from django.contrib import admin
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import messages
from apps.load.models.amazon import AmazonRelayPayment, AmazonRelayProcessedRecord


@admin.register(AmazonRelayPayment)
class AmazonRelayPaymentAdmin(admin.ModelAdmin):
    list_display = ['uploaded_at', 'status', 'total_amount', 'loads_updated', 'processed_at', 'work_period_start', 'work_period_end', 'invoice_number', 'weekly_number']
    list_filter = ['status', 'uploaded_at', 'work_period_start', 'work_period_end']
    search_fields = ['invoice_number', 'weekly_number', 'status', 'error_message']
    readonly_fields = ['uploaded_at', 'processed_at', 'total_amount', 'loads_updated', 'error_message']
    fields = ['file', 'status', 'work_period_start', 'work_period_end', 'invoice_number', 'weekly_number', 'uploaded_at', 'processed_at', 'total_amount', 'loads_updated', 'error_message']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ['file']
        return self.readonly_fields

@admin.register(AmazonRelayProcessedRecord)
class AmazonRelayProcessedRecordAdmin(admin.ModelAdmin):
    list_display = ['get_payment_invoice', 'get_payment_weekly', 'get_payment_work_start', 'get_payment_work_end', 'get_payment_status', 'trip_id', 'load_id', 'gross_pay', 'is_matched', 'matched_load']
    list_filter = ['is_matched', 'payment__status', 'created_at', 'payment__work_period_start', 'payment__work_period_end']
    search_fields = ['payment__invoice_number', 'payment__weekly_number', 'payment__work_period_start', 'payment__work_period_end', 'payment__status', 'trip_id', 'load_id', 'matched_load__reference_id', 'route', 'payment__error_message']
    
    def get_queryset(self, request):
        """Optimized queryset"""
        qs = super().get_queryset(request)
        return qs.select_related('payment', 'matched_load')
    
    def get_payment_invoice(self, obj):
        """Payment invoice number"""
        return obj.payment.invoice_number if obj.payment.invoice_number else '-'
    get_payment_invoice.short_description = 'Invoice Number'
    get_payment_invoice.admin_order_field = 'payment__invoice_number'
    
    def get_payment_weekly(self, obj):
        """Payment weekly number"""
        return obj.payment.weekly_number if obj.payment.weekly_number else '-'
    get_payment_weekly.short_description = 'Weekly Number'
    get_payment_weekly.admin_order_field = 'payment__weekly_number'
    
    def get_payment_work_start(self, obj):
        """Payment work period start"""
        return obj.payment.work_period_start if obj.payment.work_period_start else '-'
    get_payment_work_start.short_description = 'Work Start'
    get_payment_work_start.admin_order_field = 'payment__work_period_start'
    
    def get_payment_work_end(self, obj):
        """Payment work period end"""
        return obj.payment.work_period_end if obj.payment.work_period_end else '-'
    get_payment_work_end.short_description = 'Work End'
    get_payment_work_end.admin_order_field = 'payment__work_period_end'
    
    def get_payment_status(self, obj):
        """Payment status"""
        return obj.payment.status
    get_payment_status.short_description = 'Payment Status'
    get_payment_status.admin_order_field = 'payment__status'
    
    def get_load_pay(self, obj):
        """Load modelidan load_pay ni olish"""
        if obj.matched_load and hasattr(obj.matched_load, 'load_pay'):
            return f"${obj.matched_load.load_pay}"
        return "-"
    
    get_load_pay.short_description = 'Load Pay'
    get_load_pay.admin_order_field = 'matched_load__load_pay'

# CSV Import Admin
@admin.register(CSVImport)
class CSVImportAdmin(admin.ModelAdmin):
    list_display = ['id', 'csv_file', 'start_row', 'end_row', 'processed', 'success_count', 'error_count', 'created_at']
    list_filter = ['processed', 'created_at']
    search_fields = ['csv_file']
    readonly_fields = ['processed', 'success_count', 'error_count', 'error_log', 'created_at']
    fields = ['csv_file', 'start_row', 'end_row', 'processed', 'success_count', 'error_count', 'error_log', 'created_at']
    
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.processed:  # Agar qayta ishlangan bo'lsa
            return self.readonly_fields + ['csv_file', 'start_row', 'end_row']
        return self.readonly_fields