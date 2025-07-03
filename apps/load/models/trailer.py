from django.db import models


class TrailerTags(models.Model):
    tag = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.tag
    

class Trailer(models.Model):
    TYPE_CHOICES = (
        ('REEFER', 'Reefer'),
        ('DRYVAN', 'Dryvan'),
        ('STEPDECK', 'Stepdeck'),
        ('LOWBOY', 'Lowboy'),
        ('CARHAUL', 'Carhaul'),
        ('FLATBED', 'Flatbed'),
    )

    OWNER_CHOICES = (
        ('RYDER', 'Ryder'),
        ('PENSKE', 'Penske'),
        ('ADD VENDOR', 'Add Vendor'),
    )

    OWNERSHIP_CHOICES = (
        ('COMPANY', 'Company'),
        ('OWNER_OPERATOR', 'Owner-operator'),
        ('LEASE', 'Lease'),
        ('RENTAL', 'Rental'),
    )

    INTEGRATION_ELD_CHOICES = (
        ('ELD', 'Eld'),
        ('MOBILE', 'Mobile'),
        ('TELEMATICS', 'Telematics'),
        ('OTHER', 'Other'),
    )

    make = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, blank=True, null=True)
    ownership = models.CharField(max_length=20, choices=OWNERSHIP_CHOICES, blank=True, null=True)

    vin = models.CharField(max_length=20, blank=True, null=True)
    owner = models.CharField(max_length=50, choices=OWNER_CHOICES, blank=True, null=True)
    mc_number = models.CharField(max_length=20, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    unit_number = models.CharField(blank=True, null=True)
    plate_number = models.CharField(max_length=20, blank=True, null=True)
    last_annual_inspection_date = models.DateField(blank=True, null=True)
    registration_expiry_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    integration_eld = models.CharField(max_length=50, choices=INTEGRATION_ELD_CHOICES, blank=True, null=True)
    integration_id = models.CharField(max_length=50, blank=True, null=True)
    integration_api = models.CharField(max_length=50, blank=True, null=True)
    tags = models.ForeignKey(TrailerTags, related_name='trailertags', on_delete=models.CASCADE, blank=True, null=True)
    driver = models.CharField(max_length=50, blank=True, null=True)
    co_driver = models.CharField(max_length=50, blank=True, null=True)
    drop_date = models.DateField(blank=True, null=True)
    pickup_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.unit_number}"
    