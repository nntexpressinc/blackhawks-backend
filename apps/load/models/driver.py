from django.db import models
from apps.auth.models import User
from .truck import Truck
from .trailer import Trailer
from .dispatcher import Dispatcher
from django.conf import settings

class DriverTags(models.Model):
    tag = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.tag
    

class Driver(models.Model):

    EMPLOYMENT_STATUS_CHOICES = [
        ('ACTIVE (DF)', 'ACTIVE (DF)'),
        ('Terminate', 'Terminate'),
        ('Applicant', 'Applicant'),

    ]

    DRIVER_STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Home', 'Home'),
        ('In-Transit', 'In-Transit'),
        ('Inactive', 'Inactive'),
        ('Shop', 'Shop'),
        ('Rest', 'Rest'),
        ('Dispatched', 'Dispatched'),

    ]

    DL_CLASS_STATUS_CHOICES = [
        ('Unknown', 'Unknown'),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('Other', 'Other'),
    ]

    DRIVER_TYPE_CHOICES = [
        ('COMPANY_DRIVER', 'Company_driver'),
        ('OWNER_OPERATOR', 'Owner_operator'),
        ('LEASE', 'Lease'),
        ('RENTAL', 'Rental'),
    ]

    TEAM_DRIVER_CHOICES = [
        ('DRIVER_2', 'Driver_2'),
        ('ASSIGNED_DISPATCHER', 'Assigned_dispatcher'),
        ('PERCENT_SALARY', 'Percent_salary'),
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='driver_profile', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    employment_status = models.CharField(max_length=50, choices=EMPLOYMENT_STATUS_CHOICES, blank=True, null=True)
    telegram_username = models.CharField(max_length=100, blank=True, null=True)
    driver_status = models.CharField(max_length=50, choices=DRIVER_STATUS_CHOICES, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    driver_license_id = models.CharField(max_length=50, blank=True, null=True)
    dl_class = models.CharField(max_length=10, choices=DL_CLASS_STATUS_CHOICES, blank=True, null=True)
    driver_type = models.CharField(max_length=50, blank=True, null=True, choices=DRIVER_TYPE_CHOICES)
    driver_license_state = models.CharField(max_length=50, choices=STATE_CHOICES, blank=True, null=True)
    driver_license_expiration = models.DateField(blank=True, null=True)
    assigned_truck = models.ForeignKey(Truck, related_name='TRUCK_DRIVERS', on_delete=models.CASCADE, blank=True, null=True)
    assigned_trailer = models.ForeignKey(Trailer, related_name='TRailer_DRIVERS', on_delete=models.CASCADE, blank=True, null=True)
    assigned_dispatcher = models.ForeignKey(Dispatcher, related_name='dispatcher_drivers', on_delete=models.CASCADE, blank=True, null=True)
    other_id = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    tariff = models.FloatField(blank=True, null=True)
    mc_number = models.CharField(max_length=50, blank=True, null=True)
    driver_tags = models.ForeignKey(DriverTags, related_name='drivertags', on_delete=models.CASCADE, blank=True, null=True)
    team_driver = models.CharField(max_length=50, choices=TEAM_DRIVER_CHOICES, blank=True, null=True)
    permile = models.FloatField(blank=True, null=True)
    cost = models.FloatField(blank=True, null=True)
    payd = models.FloatField(blank=True, null=True)
    escrow_deposit = models.FloatField(blank=True, null=True)
    motive_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.id}"

class Pay(models.Model):
    PAY_TYPE_CHOICES = [
        ('Percentage', 'Percentage'),
        ('Per Mile', 'Per Mile'),
        ('Hourly', 'Hourly')
    ]

    CURRENCY_CHOICES = [
        ('USD', 'USD'),
        ('CAD', 'CAD')
    ]
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='driver_pay_amount', blank=True, null=True)
    pay_type = models.CharField(max_length=50, choices=PAY_TYPE_CHOICES, blank=True, null=True)
    currency = models.CharField(max_length=50, choices=CURRENCY_CHOICES, blank=True, null=True)
    standart = models.FloatField(blank=True, null=True)
    additional_charges = models.FloatField(blank=True, null=True)
    picks_per = models.IntegerField(blank=True, null=True)
    drops_per = models.IntegerField(blank=True, null=True)
    wait_time = models.IntegerField(blank=True, null=True)
    

class DriverPay(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='driver_pay', blank=True, null=True)
    pay = models.ForeignKey(Pay, on_delete=models.CASCADE, related_name='pay_driver', blank=True, null=True)
    pay_from = models.DateField(blank=True, null=True)
    pay_to = models.DateField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='driver_pay_files/', blank=True, null=True)
    cd_file = models.FileField(upload_to='driver_pay_cd_files/', blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    loads = models.JSONField(blank=True, null=True, default=list)  # Loads JSON sifatida saqlanadi
    invoice_number = models.IntegerField(blank=True, null=True)
    weekly_number = models.IntegerField(blank=True, null=True)
    
    # Company Driver fields
    company_driver_data = models.JSONField(blank=True, null=True, default=dict)  # Company driver hisob-kitoblari
    total_miles = models.IntegerField(blank=True, null=True)  # Jami miles
    miles_rate = models.FloatField(default=0.65, blank=True, null=True)  # Per mile rate (0.65)
    company_driver_pay = models.FloatField(blank=True, null=True)  # Total pay for company driver


    def __str__(self):
        return f"DriverPay {self.id} for {self.driver}"
    

class DriverExpense(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('+', 'Income'),  # Driverga beriladigan pul
        ('-', 'Expense'),  # Driverdan olinadigan pul
    ]
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='expenses')
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPE_CHOICES)  # Yangi field
    description = models.CharField(max_length=255)
    amount = models.FloatField()
    expense_date = models.DateField()
    invoice_number = models.IntegerField(blank=True, null=True)
    weekly_number = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - ${self.amount} ({self.transaction_type})"
