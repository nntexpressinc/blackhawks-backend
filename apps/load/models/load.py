from django.db import models
import logging

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from .dispatcher import Dispatcher
from apps.auth.models import User
from .customerbroker import CustomerBroker
from .driver import Driver
from .truck import Truck
from .truck import Unit
from .team import Team
# from .stops import Stops
# from apps.load.models.stops import Stops
import requests
class LoadTags(models.Model):
    TAG_CHOICES = [
        ('HAZ', 'Haz'),
        ('DEDICATED LANE', 'Dedicated Lane'),
        ('HOT LOAD', 'Hot Load'),
        ('ISSUE', 'Issue'),
    ]

    tag = models.CharField(max_length=50, choices=TAG_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.tag


class Load(models.Model):
    TAGS_CHOICES = [
        ('HAZ', 'Haz'),
        ('DEDICATED-LINE', 'Dedicated-Line'),

    ]

    EQUIPMENT_TYPE_CHOICES = [
        ('DRYVAN', 'Dryvan'),
        ('REEFER', 'Reefer'),
        ('CARHAUL', 'Carhaul'),
        ('FLATBED', 'Flatbed'),
        ('STEPDECK', 'Stepdeck'),
        ('POWERONLY', 'PowerOnly'),
        ('RGN', 'Rgn'),
        ('TANKERSTYLE', 'TankerStyle'),
    ]

    LOAD_STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('COVERED', 'Covered'),
        ('DISPATCHED', 'Dispatched'),
        ('LOADING', 'Loading'),
        ('ON_ROUTE', 'On Route'),
        ('UNLOADING', 'Unloading'),
        ('IN_YARD', 'In Yard'),
        ('DELIVERED', 'Delivered'),
        ('COMPLETED', 'Completed'),
        )
    company_name = models.CharField(max_length=200, blank=True, null=True)
    reference_id = models.CharField(max_length=200, blank=True, null=True)
    instructions = models.CharField(max_length=200, blank=True, null=True)
    bills = models.IntegerField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='dispatcher', on_delete=models.CASCADE, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    load_id = models.CharField(max_length=200, blank=True, null=True)
    trip_id = models.IntegerField(blank=True, null=True)
    customer_broker = models.ForeignKey(CustomerBroker, related_name='customer_broker', on_delete=models.CASCADE, blank=True, null=True)
    driver = models.ForeignKey(Driver, related_name='driver', on_delete=models.CASCADE, blank=True, null=True)
    co_driver = models.CharField(max_length=100, null=True, blank=True)
    truck = models.ForeignKey(Truck, related_name='truck', on_delete=models.CASCADE, blank=True, null=True)
    dispatcher = models.ForeignKey(Dispatcher, related_name='created_by', on_delete=models.CASCADE, blank=True, null=True)
    load_status = models.CharField(max_length=50, choices=LOAD_STATUS_CHOICES, blank=True, null=True)
    tags = models.ForeignKey(LoadTags, related_name='loadtags', on_delete=models.CASCADE, blank=True, null=True)
    equipment_type = models.CharField(max_length=50, choices=EQUIPMENT_TYPE_CHOICES, blank=True, null=True)
    trip_status = models.CharField(max_length=50, blank=True, null=True)
    invoice_status = models.CharField(max_length=50, blank=True, null=True)
    trip_bil_status = models.CharField(max_length=50, blank=True, null=True)
    load_pay = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    driver_pay = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_pay = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    per_mile = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    mile = models.IntegerField(blank=True, null=True)
    empty_mile = models.IntegerField(blank=True, null=True)
    total_miles = models.IntegerField(blank=True, null=True)
    flagged = models.BooleanField(default=False, blank=True, null=True)
    flagged_reason = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    chat = models.TextField(blank=True, null=True)
    ai = models.BooleanField(blank=True, null=True)
    rate_con = models.FileField(blank=True, null=True)
    bol = models.FileField(blank=True, null=True)
    pod = models.FileField(blank=True, null=True)
    document = models.FileField(blank=True, null=True)
    comercial_invoice = models.FileField(blank=True, null=True)
    message_id = models.CharField(max_length=255, null=True, blank=True)
    pickup_date = models.DateTimeField(blank=True, null=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    pickup_location = models.CharField(max_length=200, blank=True, null=True)
    delivery_location = models.CharField(max_length=200, blank=True, null=True)
    driver_location = models.CharField(max_length=200, blank=True, null=True)
    stop = models.ManyToManyField('Stops', related_name='related_loads', blank=True, null=True)
    group_message_id = models.CharField(max_length=50, null=True, blank=True)
    unit_id = models.ForeignKey(Unit, related_name='unit_load', on_delete=models.CASCADE, blank=True, null=True)
    team_id = models.ForeignKey(Team, related_name='team_load', on_delete=models.CASCADE, blank=True, null=True)
    amazon_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def get_coordinates(self, address):
        """Manzilni koordinatalarga aylantirish (Nominatim API)"""
        try:
            # Manzilni URL-compatible formatga o'tkazish
            formatted_address = requests.utils.quote(address)
            nominatim_url = f"https://nominatim.openstreetmap.org/search?q={formatted_address}&format=json&limit=1"
            headers = {"User-Agent": "TMS_Application/1.0"}
            
            logger.info(f"Koordinatalarni so'rash: {nominatim_url}")
            response = requests.get(nominatim_url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                logger.error(f"Nominatim API xatosi: HTTP {response.status_code}")
                return None, None
            
            data = response.json()
            
            if not data:
                logger.warning(f"Manzil uchun ma'lumot topilmadi: {address}")
                return None, None
                
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            logger.info(f"Manzil '{address}' uchun koordinatalar: {lat}, {lon}")
            return lat, lon
        except Exception as e:
            logger.error(f"Koordinatalarni olishda xatolik: {str(e)}")
            return None, None

    def get_distance(self, start_lat, start_lon, end_lat, end_lon):
        """Masofani milda hisoblash (OSRM API)"""
        try:
            osrm_url = f"http://router.project-osrm.org/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}?overview=false"
            logger.info(f"Masofa so'rovi: {osrm_url}")
            
            response = requests.get(osrm_url, timeout=10)
            
            if response.status_code != 200:
                logger.error(f"OSRM API xatosi: HTTP {response.status_code}")
                return None
                
            data = response.json()
            
            if data.get("code") != "Ok":
                logger.warning(f"OSRM xatoligi: {data.get('code', 'Unknown')}")
                return None
                
            distance_km = data["routes"][0]["distance"] / 1000  # km
            distance_miles = distance_km * 0.621371  # km -> mil
            logger.info(f"Hisoblangan masofa: {distance_miles} mil")
            return distance_miles
        except Exception as e:
            logger.error(f"Masofani hisoblashda xatolik: {str(e)}")
            return None

    def calculate_miles(self):
        """per_mile, empty_mile va total_miles ni hisoblash"""
        logger.info(f"Mile hisoblash boshlandi: Load ID {self.id}, pickup: {self.pickup_location}, delivery: {self.delivery_location}")
        
        if not self.pickup_location or not self.delivery_location:
            logger.warning("Pickup yoki delivery manzili mavjud emas")
            return False
            
        # Manzillarni tozalash
        pickup_location = self.pickup_location.strip()
        delivery_location = self.delivery_location.strip()
        
        # Pickup va delivery koordinatalarini olish
        pickup_lat, pickup_lon = self.get_coordinates(pickup_location)
        if not (pickup_lat and pickup_lon):
            logger.error(f"Pickup koordinatalari topilmadi: {pickup_location}")
            return False
            
        delivery_lat, delivery_lon = self.get_coordinates(delivery_location)
        if not (delivery_lat and delivery_lon):
            logger.error(f"Delivery koordinatalari topilmadi: {delivery_location}")
            return False
            
        logger.info(f"Koordinatalar aniqlandi - Pickup: {pickup_lat},{pickup_lon}, Delivery: {delivery_lat},{delivery_lon}")
        
        # Mile hisoblash (pickup -> delivery)
        per_mile = self.get_distance(pickup_lat, pickup_lon, delivery_lat, delivery_lon)
        if per_mile is None:
            logger.error("Pickup va delivery orasidagi masofani hisoblashda xatolik")
            return False
            
        # Natijalarni saqlash
        self.per_mile = round(per_mile, 2)
        self.mile = int(per_mile)
        
        # Empty mile hisoblash (driver_location -> pickup)
        if self.driver_location and self.driver_location.strip():
            driver_lat, driver_lon = self.get_coordinates(self.driver_location.strip())
            if driver_lat and driver_lon:
                empty_mile = self.get_distance(driver_lat, driver_lon, pickup_lat, pickup_lon)
                if empty_mile is not None:
                    self.empty_mile = int(empty_mile)
                    logger.info(f"Empty mile hisoblandi: {self.empty_mile}")
                else:
                    logger.warning("Empty mile hisoblanmadi")
                    self.empty_mile = 0
            else:
                logger.warning("Driver lokatsiya koordinatalari topilmadi")
                self.empty_mile = 0
        else:
            logger.info("Driver lokatsiyasi ko'rsatilmagan, empty mile = 0")
            self.empty_mile = 0
            
        # Total miles hisoblash
        self.total_miles = int(self.mile) + int(self.empty_mile or 0)
        logger.info(f"Mile hisoblash yakunlandi - Mile: {self.mile}, Empty: {self.empty_mile}, Total: {self.total_miles}")
        
        return True

    def save(self, *args, **kwargs):
        """Saqlashdan oldin masofalarni hisoblash"""
        try:
            # Agar mile hisoblash kerak bo'lsa
            if (self.pickup_location and self.delivery_location and 
                (not self.mile or not self.total_miles or 
                kwargs.get('recalculate_miles', False))):
                
                # kwargs dan recalculate_miles ni o'chirib tashlaymiz agar bo'lsa
                kwargs.pop('recalculate_miles', None)
                
                # Mile hisoblash
                miles_calculated = self.calculate_miles()
                logger.info(f"Mile hisoblash natijasi: {miles_calculated}")
            
            # Asosiy saqlash
            super().save(*args, **kwargs)
            logger.info(f"Load {self.id} saqlandi. Millar: {self.mile}, {self.empty_mile}, {self.total_miles}")
            
        except Exception as e:
            logger.error(f"Load saqlashda xatolik: {str(e)}")
            # Xatolik bo'lsa ham saqlashni davom ettiramiz
            super().save(*args, **kwargs)

