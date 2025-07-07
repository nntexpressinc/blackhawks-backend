from django.db import models

from .load import Load

class Stops(models.Model):

    STOP_NAME_CHOICES = [
        ('PICKUP', 'Pickup'),
        ('DELIVERY', 'Delivery'),
        ('Stop-2', 'Stop-2'),
        ('Stop-3', 'Stop-3'),
    ]

    STATE_CHOICES = [
        ('AL', 'Alabama'),
        ('AK', 'Alaska'),
        ('AZ', 'Arizona'),
        ('AR', 'Arkansas'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DE', 'Delaware'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('HI', 'Hawaii'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('IA', 'Iowa'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('ME', 'Maine'),
        ('MD', 'Maryland'),
        ('MA', 'Massachusetts'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MS', 'Mississippi'),
        ('MO', 'Missouri'),
        ('MT', 'Montana'),
        ('NE', 'Nebraska'),
        ('NV', 'Nevada'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NY', 'New York'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VT', 'Vermont'),
        ('VA', 'Virginia'),
        ('WA', 'Washington'),
        ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'),
        ('WY', 'Wyoming'),
    ]
    load = models.ForeignKey(Load, on_delete=models.CASCADE, related_name='stops', blank=True, null=True)
    stop_name = models.CharField(max_length=20, choices=STOP_NAME_CHOICES, blank=True, null=True)
    company_name = models.CharField(max_length=50, blank=True, null=True)
    contact_name = models.CharField(max_length=50, blank=True, null=True)
    reference_id = models.CharField(max_length=50, blank=True, null=True)
    appointmentdate = models.DateTimeField(blank=True, null=True)
    address1 = models.CharField(max_length=100, blank=True, null=True)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=50, default='USA', blank=True, null=True)
    state = models.CharField(max_length=50, choices=STATE_CHOICES, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    zip_code = models.IntegerField(blank=True, null=True)
    note = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    fcfs = models.DateTimeField(blank=True, null=True)
    plus_hour = models.DateTimeField(blank=True, null=True)
