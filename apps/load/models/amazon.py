# models.py
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import pandas as pd
from decimal import Decimal
from django.utils import timezone
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

class AmazonRelayPayment(models.Model):
    """Amazon Relay dan keladigan to'lov ma'lumotlarini saqlash uchun model"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    file = models.FileField(upload_to='amazon_relay_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    processed_at = models.DateTimeField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    loads_updated = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    
    def __str__(self):
        return f"Amazon Relay Payment - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        verbose_name = "Amazon Relay Payment"
        verbose_name_plural = "Amazon Relay Payments"
        ordering = ['-uploaded_at']


class AmazonRelayProcessedRecord(models.Model):
    """Excel fayldan qayta ishlangan har bir yozuvni saqlash uchun model"""
    
    payment = models.ForeignKey(AmazonRelayPayment, on_delete=models.CASCADE, related_name='processed_records')
    trip_id = models.CharField(max_length=100, blank=True, null=True)
    load_id = models.CharField(max_length=100, blank=True, null=True)
    route = models.CharField(max_length=200, blank=True)
    gross_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    distance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Load modeli bilan bog'lanish
    matched_load = models.ForeignKey('Load', on_delete=models.SET_NULL, null=True, blank=True)
    is_matched = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Record: {self.trip_id or self.load_id} - ${self.gross_pay}"
    
    class Meta:
        verbose_name = "Amazon Relay Processed Record"
        verbose_name_plural = "Amazon Relay Processed Records"


from apps.load.models.load import Load  # Load modelini import qilish


# signals.py
@receiver(post_save, sender=AmazonRelayPayment)
def process_amazon_relay_file(sender, instance, created, **kwargs):
    """Excel fayl yuklanganda avtomatik qayta ishlash"""
    if created and instance.file:
        try:
            process_excel_file(instance)
        except Exception as e:
            logger.error(f"Excel faylni qayta ishlashda xatolik: {str(e)}")
            instance.status = 'failed'
            instance.error_message = str(e)
            instance.save()


def process_excel_file(payment_instance):
    """Excel faylni qayta ishlash funksiyasi"""
    try:
        payment_instance.status = 'processing'
        payment_instance.save()
        
        # Excel faylni o'qish
        file_path = payment_instance.file.path
        df = pd.read_excel(file_path)
        
        # Kerakli ustunlarni tekshirish
        required_columns = ['Trip ID', 'Load ID', 'Gross Pay', 'Route', 'Start Date', 'End Date', 'Distance (Mi)']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValidationError(f"Excel faylda quyidagi ustunlar topilmadi: {missing_columns}")
        
        # Ma'lumotlarni tozalash
        def clean_gross_pay(value):
            """Gross Pay qiymatini tozalash funksiyasi"""
            if pd.isna(value) or value == '':
                return 0.0
            
            # Agar qiymat string bo'lsa
            if isinstance(value, str):
                # $, virgul va bo'shliqlarni olib tashlash
                cleaned = value.replace('$', '').replace(',', '').strip()
                # Bo'sh string bo'lsa 0 qaytarish
                if cleaned == '':
                    return 0.0
                try:
                    return float(cleaned)
                except ValueError:
                    return 0.0
            
            # Agar qiymat raqam bo'lsa
            try:
                return float(value)
            except (ValueError, TypeError):
                return 0.0
        
        # Gross Pay ustunini tozalash
        df['Gross Pay'] = df['Gross Pay'].apply(clean_gross_pay)
        df['Distance (Mi)'] = pd.to_numeric(df['Distance (Mi)'], errors='coerce').fillna(0)
        
        # Sana ustunlarini to'g'rilash
        df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
        df['End Date'] = pd.to_datetime(df['End Date'], errors='coerce')
        
        # Unique ID yaratish: Trip ID bo'lsa uni, bo'lmasa Load ID ni ishlatish
        def get_unique_id(row):
            """Unique ID yaratish funksiyasi"""
            trip_id = row['Trip ID']
            load_id = row['Load ID']
            
            # Trip ID bor va bo'sh emas bo'lsa
            if pd.notna(trip_id) and str(trip_id).strip():
                return ('trip', str(trip_id).strip())
            # Trip ID bo'lmasa, Load ID ni ishlatish
            elif pd.notna(load_id) and str(load_id).strip():
                return ('load', str(load_id).strip())
            else:
                # Ikkala ID ham bo'lmasa, unique qiymat yaratish
                return ('unknown', f"unknown_{row.name}")
        
        # Har bir qator uchun unique ID qo'shish
        df['unique_id'] = df.apply(get_unique_id, axis=1)
        
        # Unique ID bo'yicha guruhlash
        def group_by_unique_id(group):
            """Guruh bo'yicha ma'lumotlarni agregat qilish"""
            first_row = group.iloc[0]
            unique_id_tuple = first_row['unique_id']
            
            return pd.Series({
                'id_type': unique_id_tuple[0],
                'id_value': unique_id_tuple[1],
                'Trip ID': first_row['Trip ID'] if pd.notna(first_row['Trip ID']) else None,
                'Load ID': first_row['Load ID'] if pd.notna(first_row['Load ID']) else None,
                'Gross Pay': group['Gross Pay'].sum(),
                'Route': first_row['Route'],
                'Start Date': first_row['Start Date'],
                'End Date': first_row['End Date'],
                'Distance (Mi)': group['Distance (Mi)'].sum()
            })
        
        grouped_data = df.groupby('unique_id').apply(group_by_unique_id).reset_index(drop=True)
        
        total_amount = 0
        loads_updated = 0
        
        for _, row in grouped_data.iterrows():
            trip_id = row['Trip ID']
            load_id = row['Load ID']
            gross_pay = Decimal(str(row['Gross Pay']))
            
            # Processed record yaratish
            processed_record = AmazonRelayProcessedRecord.objects.create(
                payment=payment_instance,
                trip_id=trip_id if pd.notna(trip_id) else None,
                load_id=load_id if pd.notna(load_id) else None,
                route=row['Route'] if pd.notna(row['Route']) else '',
                gross_pay=gross_pay,
                start_date=row['Start Date'].date() if pd.notna(row['Start Date']) else None,
                end_date=row['End Date'].date() if pd.notna(row['End Date']) else None,
                distance=Decimal(str(row['Distance (Mi)']))
            )
            
            # Load modelini topish va yangilash
            # Asosiy ID (Trip ID yoki Load ID) bo'yicha qidirish
            main_id = row['id_value']
            matched_load = find_and_update_load(trip_id, load_id, gross_pay, main_id)
            
            if matched_load:
                processed_record.matched_load = matched_load
                processed_record.is_matched = True
                processed_record.save()
                
                loads_updated += 1
                total_amount += gross_pay
        
        # Payment instanceni yangilash
        payment_instance.status = 'completed'
        payment_instance.processed_at = timezone.now()
        payment_instance.total_amount = total_amount
        payment_instance.loads_updated = loads_updated
        payment_instance.save()
        
        logger.info(f"Excel fayl muvaffaqiyatli qayta ishlandi. {loads_updated} ta load yangilandi.")
        
    except Exception as e:
        payment_instance.status = 'failed'
        payment_instance.error_message = str(e)
        payment_instance.save()
        logger.error(f"Excel faylni qayta ishlashda xatolik: {str(e)}")
        raise


def find_and_update_load(trip_id, load_id, gross_pay, main_id=None):
    """Load modelini topish va amazon_amount ni yangilash"""
    try:
        matched_load = None
        
        # Birinchi Trip ID bo'yicha qidirish (agar mavjud bo'lsa)
        if trip_id and pd.notna(trip_id):
            trip_id_str = str(trip_id).strip()
            if trip_id_str:
                try:
                    matched_load = Load.objects.get(reference_id=trip_id_str)
                    logger.info(f"Load topildi Trip ID bo'yicha: {trip_id_str}")
                except Load.DoesNotExist:
                    logger.info(f"Load topilmadi Trip ID bo'yicha: {trip_id_str}")
                except Load.MultipleObjectsReturned:
                    logger.warning(f"Bir nechta Load topildi Trip ID bo'yicha: {trip_id_str}")
                    matched_load = Load.objects.filter(reference_id=trip_id_str).first()
        
        # Agar Trip ID bo'yicha topilmasa, Load ID bo'yicha qidirish
        if not matched_load and load_id and pd.notna(load_id):
            load_id_str = str(load_id).strip()
            if load_id_str:
                try:
                    matched_load = Load.objects.get(reference_id=load_id_str)
                    logger.info(f"Load topildi Load ID bo'yicha: {load_id_str}")
                except Load.DoesNotExist:
                    logger.info(f"Load topilmadi Load ID bo'yicha: {load_id_str}")
                except Load.MultipleObjectsReturned:
                    logger.warning(f"Bir nechta Load topildi Load ID bo'yicha: {load_id_str}")
                    matched_load = Load.objects.filter(reference_id=load_id_str).first()
        
        # Agar main_id berilgan bo'lsa va hali ham topilmagan bo'lsa, uni ham sinab ko'rish
        if not matched_load and main_id:
            main_id_str = str(main_id).strip()
            if main_id_str:
                try:
                    matched_load = Load.objects.get(reference_id=main_id_str)
                    logger.info(f"Load topildi Main ID bo'yicha: {main_id_str}")
                except Load.DoesNotExist:
                    logger.info(f"Load topilmadi Main ID bo'yicha: {main_id_str}")
                except Load.MultipleObjectsReturned:
                    logger.warning(f"Bir nechta Load topildi Main ID bo'yicha: {main_id_str}")
                    matched_load = Load.objects.filter(reference_id=main_id_str).first()
        
        # Load topilsa, amazon_amount ni yangilash
        if matched_load:
            # Agar oldin amazon_amount bo'lsa, qo'shish
            if matched_load.amazon_amount:
                matched_load.amazon_amount += gross_pay
            else:
                matched_load.amazon_amount = gross_pay
            
            matched_load.save()
            logger.info(f"Load {matched_load.reference_id} amazon_amount yangilandi: ${matched_load.amazon_amount}")
            
            return matched_load
        
        else:
            logger.warning(f"Load topilmadi: Trip ID={trip_id}, Load ID={load_id}, Main ID={main_id}")
            return None
            
    except Exception as e:
        logger.error(f"Load ni topish va yangilashda xatolik: {str(e)}")
        return None


# admin.py