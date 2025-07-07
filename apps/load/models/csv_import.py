from django.db import models
import pandas as pd
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class CSVImport(models.Model):
    """Google Sheets CSV import uchun model"""
    
    csv_file = models.FileField(upload_to='csv_imports/')
    start_row = models.IntegerField(default=2, help_text="Qaysi qatordan boshlash (Excel formatida, masalan 2)")
    end_row = models.IntegerField(help_text="Qaysi qatorgacha (Excel formatida, masalan 2200)")
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    success_count = models.IntegerField(default=0)
    error_count = models.IntegerField(default=0)
    error_log = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "CSV Import"
        verbose_name_plural = "CSV Imports"
    
    def __str__(self):
        return f"CSV Import - {self.created_at.strftime('%Y-%m-%d %H:%M')} ({self.start_row}-{self.end_row})"
    
    def process_csv(self):
        """CSV faylni qayta ishlash"""
        from .load import Load
        from .stops import Stops
        
        try:
            # CSV faylni o'qish
            df = pd.read_csv(self.csv_file.path)
            
            # Qatorlarni tanlash (Excel formatidan Python indexiga o'tkazish)
            start_idx = self.start_row - 2  # Excel 1-indexli, pandas 0-indexli, va header bor
            end_idx = self.end_row - 1      # Excel 1-indexli, pandas 0-indexli
            
            if start_idx < 0:
                start_idx = 0
            if end_idx >= len(df):
                end_idx = len(df) - 1
                
            selected_df = df.iloc[start_idx:end_idx + 1]
            
            success_count = 0
            error_count = 0
            error_messages = []
            
            for index, row in selected_df.iterrows():
                try:
                    # Load yaratish
                    load = self.create_load_from_row(row)
                    if load:
                        # Stops yaratish
                        self.create_stops_from_row(row, load)
                        success_count += 1
                        logger.info(f"Load {load.load_id} muvaffaqiyatli yaratildi")
                    else:
                        error_count += 1
                        error_messages.append(f"Qator {index + self.start_row}: Load yaratilmadi")
                        
                except Exception as e:
                    error_count += 1
                    error_msg = f"Qator {index + self.start_row}: {str(e)}"
                    error_messages.append(error_msg)
                    logger.error(error_msg)
            
            # Natijalarni saqlash
            self.success_count = success_count
            self.error_count = error_count
            self.error_log = "\n".join(error_messages)
            self.processed = True
            self.save()
            
            logger.info(f"CSV import yakunlandi: {success_count} muvaffaqiyat, {error_count} xato")
            return True
            
        except Exception as e:
            self.error_log = f"CSV qayta ishlashda umumiy xato: {str(e)}"
            self.processed = True
            self.save()
            logger.error(f"CSV import xatosi: {str(e)}")
            return False
    
    def create_load_from_row(self, row):
        """Bitta qatordan Load yaratish"""
        from .load import Load
        
        try:
            # Dispatcher ID mapping
            dispatcher_mapping = {
                'Uktam': 1,
                'Muhammadali': 2,
                'Alibek': 3,
                'Bayramali': 4,
                'Jasur': 5,
                'Kamron': 6
            }
            
            # Unit ID mapping
            unit_mapping = {
                100: 1,
                103: 2,
                104: 3,
                105: 4
            }
            
            # Driver ID mapping
            driver_mapping = {
                'Omid Barakzai': 1,
                'Jalaluddin Sharifi': 2,
                'Muhibullah Altintash': 3,
                'Muhammad Asif': 4
            }
            
            # Load yaratish
            load = Load()
            
            # Blackhawks load number -> load_id
            if pd.notna(row.get('Blackhawks load number')):
                load.load_id = str(row['Blackhawks load number'])
            
            # Dispatch name -> dispatcher
            dispatch_name = row.get('Dispatch\nname', '').strip()
            if dispatch_name in dispatcher_mapping:
                load.dispatcher_id = dispatcher_mapping[dispatch_name]
            
            # Unit № -> unit_id
            unit_num = row.get('Unit №')
            if pd.notna(unit_num):
                unit_id = unit_mapping.get(int(unit_num))
                if unit_id:
                    load.unit_id_id = unit_id
            
            # Driver -> driver
            driver_name = row.get('Assiged trailer Driver', '').strip()
            if driver_name in driver_mapping:
                load.driver_id = driver_mapping[driver_name]
            
            # Load № -> trip_id
            if pd.notna(row.get('Load №')):
                load.trip_id = int(row['Load №'])
            
            # Rate -> load_pay va total_pay
            if pd.notna(row.get('Rate')):
                rate = float(row['Rate'])
                load.load_pay = rate
                load.total_pay = rate
            
            # DeadHead -> empty_mile
            if pd.notna(row.get('DeadHead')):
                load.empty_mile = int(row['DeadHead'])
            
            # Loaded mile -> mile
            if pd.notna(row.get('Loaded mile')):
                load.mile = int(row['Loaded mile'])
            
            # $ per mile -> per_mile
            if pd.notna(row.get('$ per mile')):
                load.per_mile = float(row['$ per mile'])
            
            # Broker -> customer_broker (har doim 1)
            if pd.notna(row.get('Broker')):
                load.customer_broker_id = 1
            
            # Total miles hisoblash
            load.total_miles = (load.mile or 0) + (load.empty_mile or 0)
            
            # Pick up address -> pickup_location
            if pd.notna(row.get('Pick up\n🏭 Address')):
                load.pickup_location = str(row['Pick up\n🏭 Address'])
            
            # Delivery address -> delivery_location (Last Stop)
            if pd.notna(row.get('Delivery Address\nfor Last Stop')):
                load.delivery_location = str(row['Delivery Address\nfor Last Stop'])
            
            load.save()
            return load
            
        except Exception as e:
            logger.error(f"Load yaratishda xato: {str(e)}")
            return None
    
    def create_stops_from_row(self, row, load):
        """Bitta qatordan barcha Stops yaratish"""
        from .stops import Stops
        
        try:
            # PICKUP stop yaratish
            pickup_address = row.get('Pick up\n🏭 Address')
            pickup_date = row.get('Pick up/Arrive\n🏭 Date')
            pickup_time = row.get('Pick up /Arrive\n🏭 Time')
            
            if pd.notna(pickup_address):
                pickup_stop = Stops()
                pickup_stop.load = load
                pickup_stop.stop_name = 'PICKUP'
                pickup_stop.address1 = str(pickup_address)
                
                # Date va Time ni birlashtirish
                if pd.notna(pickup_date) and pd.notna(pickup_time):
                    try:
                        date_str = str(pickup_date)
                        time_str = str(pickup_time)
                        datetime_str = f"{date_str} {time_str}"
                        pickup_stop.appointmentdate = pd.to_datetime(datetime_str)
                    except:
                        pass
                
                pickup_stop.save()
                load.stop.add(pickup_stop)
            
            # DELIVERY stop yaratish (Last Stop)
            delivery_address = row.get('Delivery Address\nfor Last Stop')
            delivery_date = row.get('Arrive Date\nfor Last Stop')
            delivery_time = row.get('Arrive Time\nfor Last Stop')
            
            if pd.notna(delivery_address):
                delivery_stop = Stops()
                delivery_stop.load = load
                delivery_stop.stop_name = 'DELIVERY'
                delivery_stop.address1 = str(delivery_address)
                
                if pd.notna(delivery_date) and pd.notna(delivery_time):
                    try:
                        date_str = str(delivery_date)
                        time_str = str(delivery_time)
                        datetime_str = f"{date_str} {time_str}"
                        delivery_stop.appointmentdate = pd.to_datetime(datetime_str)
                    except:
                        pass
                
                delivery_stop.save()
                load.stop.add(delivery_stop)
            
            # Stop-2 yaratish
            stop2_address = row.get('Delivery address\nfor Stop2')
            stop2_date = row.get('Delivery Date\nfor Stop2')
            stop2_time = row.get('Delivery Time\nfor Stop2')
            
            if pd.notna(stop2_address):
                stop2 = Stops()
                stop2.load = load
                stop2.stop_name = 'Stop-2'
                stop2.address1 = str(stop2_address)
                
                if pd.notna(stop2_date) and pd.notna(stop2_time):
                    try:
                        date_str = str(stop2_date)
                        time_str = str(stop2_time)
                        datetime_str = f"{date_str} {time_str}"
                        stop2.appointmentdate = pd.to_datetime(datetime_str)
                    except:
                        pass
                
                stop2.save()
                load.stop.add(stop2)
            
            # Stop-3 yaratish
            stop3_address = row.get('Delivery Adress\nfor Stop3')
            stop3_date = row.get('Delivery Date\nfor Stop3')
            stop3_time = row.get('Delivery Time\nfor Stop3')
            
            if pd.notna(stop3_address):
                stop3 = Stops()
                stop3.load = load
                stop3.stop_name = 'Stop-3'
                stop3.address1 = str(stop3_address)
                
                if pd.notna(stop3_date) and pd.notna(stop3_time):
                    try:
                        date_str = str(stop3_date)
                        time_str = str(stop3_time)
                        datetime_str = f"{date_str} {time_str}"
                        stop3.appointmentdate = pd.to_datetime(datetime_str)
                    except:
                        pass
                
                stop3.save()
                load.stop.add(stop3)
                
        except Exception as e:
            logger.error(f"Stops yaratishda xato: {str(e)}")
