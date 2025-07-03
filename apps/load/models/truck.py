from django.db import models
from apps.load.models.trailer import Trailer
from apps.load.models.employee import Employee
from apps.load.models.dispatcher import Dispatcher
from .team import Team

# from apps.load.models.load import Load
from apps.auth.models import User
class TruckTags(models.Model):
    tag = models.CharField(max_length=40, blank=True, null=True)


class Truck(models.Model):
    ASSIGNMENT_STATUS_CHOICES = (
        ('AVAILABLE', 'Company'),
        ('INACTIVE', 'Inactive'),

    )
    OWNERSHIP_CHOICES = (
        ('COMPANY', 'Company'),
        ('OWNER_OPERATOR', 'Owner-operator'),
        ('LEASE', 'Lease'),
        ('RENTAL', 'Rental'),
        ('OTHER', 'Other'),
    )

    OWNER_CHOICES = (
        ('COMPANY', 'Company'),
        ('OWNER_OPERATOR', 'Owner-operator'),
        ('LEASE', 'Lease'),
        ('RENTAL', 'Rental'),
        ('OTHER', 'Other'),
    )
    INTEGRATION_ELD_CHOICES = (
        ('ELD', 'Eld'),
        ('MOBILE', 'Mobile'),
        ('TELEMATICS', 'Telematics'),
        ('OTHER', 'Other'),
    )

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
    make = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    unit_number = models.CharField(blank=True, null=True) #search
    plate_number = models.CharField(max_length=50, blank=True, null=True)
    vin = models.CharField(max_length=20, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, blank=True, null=True)

    weight = models.IntegerField(blank=True, null=True)

    registration_expiry_date = models.DateField(blank=True, null=True)
    last_annual_inspection_date = models.DateField(blank=True, null=True)

    color = models.CharField(max_length=50, blank=True, null=True)
    integration_eld = models.CharField(max_length=50, choices=INTEGRATION_ELD_CHOICES, blank=True, null=True)
    integration_id = models.IntegerField(blank=True, null=True)
    integration_api = models.CharField(max_length=50, blank=True, null=True)

    ownership_type = models.CharField(max_length=20, choices=OWNERSHIP_CHOICES, blank=True, null=True)
    tags = models.ForeignKey(TruckTags, related_name='trucktags', on_delete=models.CASCADE, blank=True, null=True)
    mc_number = models.CharField(max_length=50, blank=True, null=True)
    pickup_odometer = models.CharField(max_length=50, blank=True, null=True)
    owner = models.CharField(max_length=50, choices=OWNER_CHOICES, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    assignment_status = models.CharField(max_length=50, choices=ASSIGNMENT_STATUS_CHOICES, blank=True, null=True)
    driver = models.CharField(max_length=50, blank=True, null=True)
    co_driver = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    pickup_date = models.DateField(blank=True, null=True)
    drop_date = models.DateField(blank=True, null=True)
    mileage_on_pickup = models.IntegerField(blank=True, null=True)
    mileage_on_drop = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)



    def __str__(self):
        return f"Unit number {self.unit_number}, ID {self.id}"
    

class Unit(models.Model):
    unit_number = models.CharField(unique=True)
    truck = models.ManyToManyField(Truck, related_name='unit_trucks', blank=True, null=True)
    driver = models.ManyToManyField('Driver', related_name='unit_drivers', blank=True, null=True)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='unit_team_id', blank=True, null=True)
    trailer = models.ManyToManyField(Trailer, related_name='unit_trailers', blank=True, null=True)
    employee = models.ManyToManyField(Employee, related_name='unit_employees', blank=True, null=True)
    # load = models.ManyToManyField('load.Load', related_name='loads', blank=True, null=True)