from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    permission_id = models.ForeignKey('Permission', on_delete=models.CASCADE, related_name='roles')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('dispatcher', 'Dispatcher'),
        ('driver', 'Driver'),
        ('fleet_manager', 'Fleet Manager'),
        ('accounting', 'Accounting'),
        ('super_admin', 'Super Admin'),
    )
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='users', blank=True, null=True)
    username = None
    email = models.EmailField(unique=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    postal_zip = models.IntegerField(blank=True, null=True)
    ext = models.IntegerField(blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')    
    profile_photo = models.FileField(upload_to='media/profile', default='media/profile/profile_avatar.jpg', blank=True, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_role(self) -> str:
        return self.role

    def get_user_id(self):
        return self.id

    def __str__(self):
        return self.email


class UserLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='locations')
    latitude = models.FloatField()
    longitude = models.FloatField()
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    device_info = models.TextField(blank=True, null=True)  # Uzunroq matn uchun TextField
    page_status = models.CharField(max_length=10, choices=[('open', 'Open'), ('hidden', 'Hidden')], default='open')  # String uchun CharField

    def get_google_maps_url(self):
        return f"https://www.google.com/maps?q={self.latitude},{self.longitude}"

    def __str__(self):
        return f"{self.user.username} - ({self.latitude}, {self.longitude})"


class Company(models.Model):
    company_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    company_logo = models.FileField(upload_to='company-logo', blank=True, null=True)

    def __str__(self):
        return self.company_name
    

class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    load_create = models.BooleanField(default=False)
    load_update = models.BooleanField(default=False)
    load_delete = models.BooleanField(default=False)
    load_view = models.BooleanField(default=False)

    driver_create = models.BooleanField(default=False)
    driver_update = models.BooleanField(default=False)
    driver_delete = models.BooleanField(default=False)
    driver_view = models.BooleanField(default=False)

    truck_create = models.BooleanField(default=False)
    truck_update = models.BooleanField(default=False)
    truck_delete = models.BooleanField(default=False)
    truck_view = models.BooleanField(default=False)

    trailer_create = models.BooleanField(default=False)
    trailer_update = models.BooleanField(default=False)
    trailer_delete = models.BooleanField(default=False)
    trailer_view = models.BooleanField(default=False)

    user_create = models.BooleanField(default=False)
    user_update = models.BooleanField(default=False)
    user_delete = models.BooleanField(default=False)
    user_view = models.BooleanField(default=False)

    accounting_create = models.BooleanField(default=False)
    accounting_update = models.BooleanField(default=False)
    accounting_delete = models.BooleanField(default=False)
    accounting_view = models.BooleanField(default=False)

    dispatcher_create = models.BooleanField(default=False)
    dispatcher_update = models.BooleanField(default=False)
    dispatcher_delete = models.BooleanField(default=False)
    dispatcher_view = models.BooleanField(default=False)

    stop_create = models.BooleanField(default=False)
    stop_update = models.BooleanField(default=False)
    stop_delete = models.BooleanField(default=False)
    stop_view = models.BooleanField(default=False)
    
    otherpay_create = models.BooleanField(default=False)
    otherpay_update = models.BooleanField(default=False)
    otherpay_delete = models.BooleanField(default=False)
    otherpay_view = models.BooleanField(default=False)

    employee_create = models.BooleanField(default=False)
    employee_update = models.BooleanField(default=False)
    employee_delete = models.BooleanField(default=False)
    employee_view = models.BooleanField(default=False)

    commodity_create = models.BooleanField(default=False)
    commodity_update = models.BooleanField(default=False)
    commodity_delete = models.BooleanField(default=False)
    commodity_view = models.BooleanField(default=False)

    customerbroker_create = models.BooleanField(default=False)
    customerbroker_update = models.BooleanField(default=False)
    customerbroker_delete = models.BooleanField(default=False)
    customerbroker_view = models.BooleanField(default=False)

    chat_create = models.BooleanField(default=False)
    chat_update = models.BooleanField(default=False)
    chat_delete = models.BooleanField(default=False)
    chat_view = models.BooleanField(default=False)

    userlocation_create = models.BooleanField(default=False)
    userlocation_update = models.BooleanField(default=False)
    userlocation_delete = models.BooleanField(default=False)
    userlocation_view = models.BooleanField(default=False)

    

    def __str__(self):
        return self.name
