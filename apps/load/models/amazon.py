from django.db import models
from django.utils import timezone
import pandas as pd
from decimal import Decimal
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
    
    class Meta:
        db_table = 'amazon_relay_payments'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"Payment {self.id} - {self.status}"
    
    def process_excel_file(self):
        """Excel faylni qayta ishlash"""
        try:
            self.status = 'processing'
            self.save()
            
            # Excel faylni o'qish
            df = pd.read_excel(self.file.path)
            
            # Ma'lumotlarni qayta ishlash
            result = self._process_payment_data(df)
            
            self.total_amount = result['total_amount']
            self.loads_updated = result['loads_updated']
            self.status = 'completed'
            self.processed_at = timezone.now()
            
            logger.info(f"Successfully processed file {self.id}: {self.loads_updated} loads updated")
            
        except Exception as e:
            self.status = 'failed'
            self.error_message = str(e)
            logger.error(f"Error processing file {self.id}: {str(e)}")
        
        finally:
            self.save()
    
    def _process_payment_data(self, df):
        """To'lov ma'lumotlarini qayta ishlash"""
        from apps.load.models import Load  # Load modelingizni import qiling
        
        # Faqat LOAD - COMPLETED statusdagi ma'lumotlarni olish
        load_data = df[df['Item Type'] == 'LOAD - COMPLETED'].copy()
        
        if load_data.empty:
            return {'total_amount': 0, 'loads_updated': 0}
        
        # Trip ID bo'yicha guruhlash va Gross Pay summalarini hisoblash
        trip_groups = self._group_by_trip_id(load_data)
        
        total_amount = 0
        loads_updated = 0
        
        for group_data in trip_groups:
            trip_id = group_data['trip_id']
            load_id = group_data['load_id']
            gross_pay = group_data['total_gross_pay']
            
            # Load ni topish
            load = self._find_load(trip_id, load_id)
            
            if load:
                # Amazon amount ni yangilash
                load.amazon_amount = gross_pay
                load.save()
                
                total_amount += gross_pay
                loads_updated += 1
                
                logger.info(f"Updated load {load.id} with amount {gross_pay}")
            else:
                logger.warning(f"Load not found for Trip ID: {trip_id}, Load ID: {load_id}")
        
        return {
            'total_amount': total_amount,
            'loads_updated': loads_updated
        }
    
    def _group_by_trip_id(self, df):
        """Trip ID bo'yicha guruhlash"""
        groups = []
        
        # Trip ID bo'yicha guruhlash
        for trip_id, group in df.groupby('Trip ID'):
            if pd.notna(trip_id) and str(trip_id).strip():  # Trip ID mavjud bo'lsa
                total_gross_pay = self._calculate_gross_pay(group)
                load_id = group['Load ID'].iloc[0] if not group['Load ID'].empty else None
                
                groups.append({
                    'trip_id': str(trip_id).strip(),
                    'load_id': str(load_id) if load_id else None,
                    'total_gross_pay': total_gross_pay
                })
        
        # Trip ID bo'lmagan ma'lumotlarni Load ID bo'yicha guruhlash
        no_trip_data = df[df['Trip ID'].isna() | (df['Trip ID'] == '')]
        
        if not no_trip_data.empty:
            for load_id, group in no_trip_data.groupby('Load ID'):
                if pd.notna(load_id) and str(load_id).strip():
                    total_gross_pay = self._calculate_gross_pay(group)
                    
                    groups.append({
                        'trip_id': None,
                        'load_id': str(load_id).strip(),
                        'total_gross_pay': total_gross_pay
                    })
        
        return groups
    
    def _calculate_gross_pay(self, group):
        """Gross Pay summalarini hisoblash"""
        total = 0
        for _, row in group.iterrows():
            gross_pay_str = str(row['Gross Pay']).replace('$', '').replace(',', '').strip()
            try:
                amount = Decimal(gross_pay_str)
                total += amount
            except (ValueError, TypeError):
                logger.warning(f"Invalid Gross Pay value: {gross_pay_str}")
        
        return total
    
    def _find_load(self, trip_id, load_id):
        """Load ni topish"""
        from apps.load.models import Load  # Load modelingizni import qiling
        
        # Birinchi Trip ID bo'yicha qidirish
        if trip_id:
            load = Load.objects.filter(reference_id=trip_id).first()
            if load:
                return load
        
        # Trip ID bo'lmasa yoki topilmasa Load ID bo'yicha qidirish
        if load_id:
            load = Load.objects.filter(reference_id=load_id).first()
            if load:
                return load
        
        return None
