from django.contrib import admin
from apps.load.models.driver import Pay, DriverPay, DriverExpense
from apps.load.models.truck import Unit
from apps.load.models.team import Team
from apps.load.models import (
    Load, LoadTags, Driver, DriverTags, Trailer, 
    TrailerTags, TruckTags, Truck, Dispatcher,
    DispatcherTags, EmployeeTags, CustomerBroker, 
    Stops, Employee, OtherPay, Commodities)

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
    list_filter = ['status', 'uploaded_at']
    search_fields = ['work_period_start', 'work_period_end', 'invoice_number', 'weekly_number']
    readonly_fields = ['uploaded_at', 'processed_at', 'total_amount', 'loads_updated', 'error_message', 'work_period_start', 'work_period_end', 'invoice_number', 'weekly_number']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ['file']
        return self.readonly_fields

@admin.register(AmazonRelayProcessedRecord)
class AmazonRelayProcessedRecordAdmin(admin.ModelAdmin):
    list_display = ['payment', 'is_matched', 'matched_load', 'created_at']
    list_filter = ['is_matched', 'payment__status', 'created_at']
    search_fields = ['payment__invoice_number', 'payment__weekly_number', 'payment__work_period_start', 'payment__work_period_end', 'trip_id', 'load_id', 'matched_load__reference_id']
    
    def get_queryset(self, request):
        """Faqat payment ma'lumotlari ko'rsatilsin"""
        qs = super().get_queryset(request)
        return qs.select_related('payment', 'matched_load')
    
    def has_change_permission(self, request, obj=None):
        """O'zgartirish ruxsatini berish"""
        return True
    
    def has_delete_permission(self, request, obj=None):
        """O'chirish ruxsatini berish"""
        return True
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('payment',)
        }),
        ('Record Details', {
            'fields': ('trip_id', 'load_id', 'route', 'gross_pay', 'start_date', 'end_date', 'distance'),
            'classes': ('collapse',),
        }),
        ('Matching Information', {
            'fields': ('matched_load', 'is_matched'),
            'classes': ('collapse',),
        }),
    )
    
    def get_load_pay(self, obj):
        """Load modelidan load_pay ni olish"""
        if obj.matched_load and hasattr(obj.matched_load, 'load_pay'):
            return f"${obj.matched_load.load_pay}"
        return "-"
    
    get_load_pay.short_description = 'Load Pay'
    get_load_pay.admin_order_field = 'matched_load__load_pay'