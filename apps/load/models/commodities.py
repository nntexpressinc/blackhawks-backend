from django.db import models

from .load import Load

class Commodities(models.Model):
    DESCRIPTION_CHOICES = [
        ('GENERALFREIGHT', 'GeneralFreight'),
        ('AUTOPARTS', 'AutoParts'),
        ('CHIP', 'Chip'),
        ('WATER', 'Water'),
        ('VEHICLE', 'Vehicle'),
        ('OTHER', 'Other'),
    ]
    load = models.ForeignKey(Load, on_delete=models.CASCADE, related_name='commodities', blank=True, null=True)
    descriptions = models.CharField(max_length=100, choices=DESCRIPTION_CHOICES, blank=True, null=True)
    qty = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    pcs = models.CharField(max_length=50, blank=True, null=True)
    totalwt = models.CharField(max_length=50, blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)
    note = models.CharField(max_length=200, blank=True, null=True)

