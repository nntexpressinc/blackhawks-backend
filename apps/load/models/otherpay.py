from django.db import models

from .load import Load


class OtherPay(models.Model):

    TYPE_CHOICES = [
        ('DETENTION', 'Detention'),
        ('EQUIPMENT', 'Equipment'),
        ('LAYOVER', 'Layover'),
        ('LUMPER', 'Lumper'),
        ('DRIVERASSIST','Driver Assist'),
        ('TRAILERWASH', 'Trailer Wash'),
        ('ESCORTFEE', 'Escort Fee'),
        ('BONUS', 'Bonus'),
        ('CHARGEBACK', 'Charge Back'),
        ('OTHER', 'Other'),
    ]
    load = models.ForeignKey(Load, on_delete=models.CASCADE, related_name='otherpay_load', blank=True, null=True)
    # pay = models.FloatField(max_length=50, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pay_type = models.CharField(max_length=100, choices=TYPE_CHOICES, blank=True, null=True)
    note = models.CharField(max_length=200, blank=True, null=True)


