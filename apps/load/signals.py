import requests
import time
import threading
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.forms.models import model_to_dict
from .models import Load
from .models.csv_import import CSVImport
from requests.exceptions import ConnectionError, Timeout, RequestException

# Telegram xabarlarini asinxron ravishda yuborish
@receiver(post_save, sender=Load)
def trigger_telegram_message(sender, instance, created, **kwargs):
    # Xabarni alohida oqimda yuborish
    thread = threading.Thread(target=send_telegram_message, args=(sender, instance, created, kwargs))
    thread.daemon = True
    thread.start()

def send_telegram_message(sender, instance, created, kwargs):
    try:
        # Team modelidan telegram ma'lumotlarini olish
        team = instance.team_id
        
        # Agar team belgilanmagan bo'lsa yoki telegram konfiguratsiyasi bo'lmasa, funksiyadan chiqish
        if not team or not team.telegram_channel_id or not team.telegram_group_id:
            print("Team not assigned or Telegram configuration missing.")
            return
        
        # Team modelidan telegram konfiguratsiyasini olish
        bot_token = team.telegram_token if hasattr(team, 'telegram_token') else "7582469651:AAHBtrGUmdo2tzDPU4RSI61AFN99EQnqbJE"
        
        # Telegram kanal va guruh ID formatini tekshirish va to'g'rilash
        channel_id = process_telegram_id(team.telegram_channel_id)
        group_id = process_telegram_id(team.telegram_group_id)

        # Unit number olish
        unit_number = "Not assigned"
        if instance.unit_id:
            unit_number = instance.unit_id.unit_number

        # Trailer make olish
        trailer_make = "Not assigned"
        if instance.unit_id and instance.unit_id.trailer.exists():
            first_trailer = instance.unit_id.trailer.first()
            if first_trailer and first_trailer.make:
                trailer_make = first_trailer.make

        # Driver name olish
        driver_name = "Not assigned"
        if instance.driver and instance.driver.user:
            first_name = instance.driver.user.first_name or ""
            last_name = instance.driver.user.last_name or ""
            driver_name = f"{first_name} {last_name}".strip()
            if not driver_name:
                driver_name = "Not assigned"

        # Team name va dispatcher nickname olish
        team_info = "Not assigned"
        if instance.team_id:
            team_name = instance.team_id.name or "Unknown Team"
            dispatcher_nickname = ""
            if instance.dispatcher and hasattr(instance.dispatcher, 'nickname'):
                dispatcher_nickname = f"    ({instance.dispatcher.nickname})"
            team_info = f"{team_name}{dispatcher_nickname}"

        # Stops ma'lumotlarini olish va formatda saralash
        stops_text = ""
        delivery_stop = None
        
        if instance.stop.exists():
            for stop in instance.stop.all():
                # Address formatini yaratish
                address_parts = []
                if hasattr(stop, 'address1') and stop.address1:
                    address_parts.append(stop.address1)
                if hasattr(stop, 'address2') and stop.address2:
                    address_parts.append(stop.address2)
                if hasattr(stop, 'city') and stop.city:
                    address_parts.append(stop.city)
                if hasattr(stop, 'state') and stop.state:
                    address_parts.append(stop.state)
                if hasattr(stop, 'zip_code') and stop.zip_code:
                    address_parts.append(str(stop.zip_code))
                
                full_address = ", ".join(address_parts) if address_parts else "Address not specified"
                
                # Arrive time formatini yaratish
                arrive_info = ""
                if hasattr(stop, 'appointmentdate') and stop.appointmentdate:
                    # DateTime formatini o'zgartirish
                    arrive_info = f"Date {stop.appointmentdate.strftime('%m/%d/%Y')} Time {stop.appointmentdate.strftime('%H:%M')}"
                elif hasattr(stop, 'fcfs') and stop.fcfs:
                    arrive_info = f"Date {stop.fcfs.strftime('%m/%d/%Y')} Time {stop.fcfs.strftime('%H:%M')}"
                elif hasattr(stop, 'plus_hour') and stop.plus_hour:
                    arrive_info = f"Date {stop.plus_hour.strftime('%m/%d/%Y')} Time {stop.plus_hour.strftime('%H:%M')}"
                else:
                    arrive_info = "FCFS"
                
                # Reference ID ni olish
                ref_number = ""
                if hasattr(stop, 'reference_id') and stop.reference_id:
                    ref_number = stop.reference_id
                
                # Stop name ni olish
                stop_name = getattr(stop, 'stop_name', 'Stop')
                
                # Delivery stopni alohida saqlash
                if stop_name.upper() == 'DELIVERY':
                    delivery_stop = {
                        'stop_name': stop_name,
                        'company': getattr(stop, 'company_name', 'Unknown Company'),
                        'address': full_address,
                        'arrive_info': arrive_info,
                        'ref_number': ref_number
                    }
                else:
                    # Pickup va boshqa stoplar uchun
                    stops_text += f"""
<b>{stop_name}:</b> 🏭
{getattr(stop, 'company_name', 'Unknown Company')}
{full_address}
Arrive: {arrive_info}
{stop_name} №: {ref_number}
"""

        # Agar stops mavjud bo'lmasa, default pickup ma'lumotini ishlatish
        if not stops_text:
            stops_text = f"""
<b>Pick up:</b> 🏭
{instance.pickup_location or 'Location not specified'}
Arrive: Date {instance.pickup_date.strftime('%m/%d/%Y') if instance.pickup_date else 'TBD'} Time FCFS
Pick up №: 
"""

        # Last Stop (Delivery) formatini yaratish
        last_stop_text = ""
        if delivery_stop:
            last_stop_text = f"""
{delivery_stop['company']}
{delivery_stop['address']}
Arrive: {delivery_stop['arrive_info']}
Delivery №: {delivery_stop['ref_number']}"""
        else:
            last_stop_text = f"""
{instance.delivery_location or 'Location not specified'}
Arrive: Date {instance.delivery_date.strftime('%m/%d/%Y') if instance.delivery_date else 'TBD'} Time TBD
Delivery №: """

        # Xabarni yangi formatda tayyorlash
        message = f"""🚚 {unit_number}
🔖{trailer_make}
👨‍✈️ {driver_name}
<b>Load:</b> {instance.load_id or 'Not specified'}
{stops_text}
<b>Last Stop:</b> 🏭{last_stop_text}

<b>Estimated Payout:</b> ${instance.load_pay or 'TBD'}
  DHM: {instance.empty_mile or 'TBD'}
  LM: {instance.mile or 'TBD'}
<b>$PM:</b> {instance.per_mile or 'TBD'}

<b>Team {team_info}</b>
{instance.company_name or 'Unknown Company'}
---------------------------
⚠️-Traffic/Construction/Weather or other delays (photos or videos) -  should be updated in good time by drivers
⚠️-Please Scale the load after pick up, to avoid axle overweight. Missing scale ticket - 200$ penalty fee.
⚠️-After hooking up the trailer, PTI should be done !!!
🛞<b>Tire pressure:</b>
✍️Drive tire - 105 psi.
✍️Steering tire - 110 psi.
✍️Trailer tire - 100 psi.
🛞🔨if tire has inflation system you need to hit with a hammer to check the pressure.
⚠️📲If you hear air leak sound or detect an oil leak around the rims let us know immediately.
---------------------------
<b>On time PU/DEL:</b>  $150"""

        if created:
            # Send to channel
            channel_data = {
                "chat_id": channel_id,
                "text": message,
                "parse_mode": "HTML"
            }
            
            channel_response = send_telegram_request(f"https://api.telegram.org/bot{bot_token}/sendMessage", channel_data)
            if channel_response and channel_response.get("ok"):
                instance.message_id = channel_response["result"]["message_id"]
                
                # Now also send to group
                group_data = {
                    "chat_id": group_id,
                    "text": message,
                    "parse_mode": "HTML"
                }
                
                group_response = send_telegram_request(f"https://api.telegram.org/bot{bot_token}/sendMessage", group_data)
                if group_response and group_response.get("ok"):
                    instance.group_message_id = group_response["result"]["message_id"]
                    
                # Update both message IDs without triggering the signal again
                Load.objects.filter(pk=instance.pk).update(
                    message_id=instance.message_id,
                    group_message_id=instance.group_message_id
                )
                print(f"Messages sent - Channel ID: {instance.message_id}, Group ID: {instance.group_message_id}")
            else:
                print(f"Error sending to channel: {channel_response}")
                
        else:
            # Update messages in both places if they exist
            if instance.message_id:
                edit_url = f"https://api.telegram.org/bot{bot_token}/editMessageText"
                edit_data = {
                    "chat_id": channel_id,
                    "message_id": instance.message_id,
                    "text": message,
                    "parse_mode": "HTML"
                }
                
                edit_response = send_telegram_request(edit_url, edit_data)
                if edit_response and edit_response.get("ok"):
                    print(f"Message updated in channel, message_id: {instance.message_id}")
                else:
                    print(f"Error updating message in channel: {edit_response}")
                    
            if instance.group_message_id:
                edit_url = f"https://api.telegram.org/bot{bot_token}/editMessageText"
                edit_data = {
                    "chat_id": group_id,
                    "message_id": instance.group_message_id,
                    "text": message,
                    "parse_mode": "HTML"
                }
                
                edit_response = send_telegram_request(edit_url, edit_data)
                if edit_response and edit_response.get("ok"):
                    print(f"Message updated in group, message_id: {instance.group_message_id}")
                else:
                    print(f"Error updating message in group: {edit_response}")
    except Exception as e:
        # Xatolarni ushlash
        print(f"Error in Telegram notification process: {str(e)}")

# Telegram ID formatini tekshirish va to'g'rilash
def process_telegram_id(telegram_id):
    """
    Telegram ID ni qaysi formatda ekanligini tekshirish va to'g'ri formatga o'zgartirish
    - '@username' formatidan username qilib qaytaradi
    - 'id:123456789' formatidan faqat raqamni qaytaradi
    - '@username extra text' formatidan username qilib qaytaradi
    - Boshqa holatda qiymat o'zgarmaydi
    """
    if not telegram_id:
        return None
        
    # '@username' formatini tekshirish
    if telegram_id.startswith('@'):
        # '@username' formatidagi bo'lsa, qo'shimcha so'zlarni olib tashlash
        username = telegram_id.split()[0]  # Birinchi so'zni olish (@ bilan)
        return username
        
    # 'id:123456789' formatini tekshirish
    if telegram_id.lower().startswith('id:'):
        # Faqat ID raqamini qaytarish
        id_parts = telegram_id.split(':')
        if len(id_parts) > 1:
            return id_parts[1].strip()
    
    # Boshqa formatlar uchun o'zgartirish kerak emas
    return telegram_id

# Telegram so'rovlarini qayta urinish funksiyasi
def send_telegram_request(url, data, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(url, data=data, timeout=10)
            return response.json()
        except (ConnectionError, Timeout) as e:
            wait_time = 2 ** attempt
            print(f"Connection error (attempt {attempt+1}/{max_retries}): {str(e)}")
            print(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        except RequestException as e:
            print(f"Request error: {str(e)}")
            return None
    
    print(f"Failed to connect to Telegram API after {max_retries} attempts")
    return None

# O'zgarishlarni kuzatish
@receiver(pre_save, sender=Load)
def detect_changes(sender, instance, **kwargs):
    if instance.pk:
        try:
            # Ma'lumotlar bazasidan joriy yozuvni olish
            old_instance = Load.objects.get(pk=instance.pk)
            
            # Muhim maydonlardagi o'zgarishlarni tekshirish
            fields_to_check = [
                'load_id', 'reference_id', 'driver', 'company_name', 'instructions',
                'load_status', 'tags', 'equipment_type', 'created_date', 'load_pay',
                'driver_pay', 'total_pay', 'mile', 'empty_mile', 'created_date', 'total_miles',
                'rate_con', 'bol', 'pod', 'comercial_invoice', 'pickup_date', 'delivery_date',
                'pickup_location', 'delivery_location', 'unit_id', 'team_id', 'dispatcher'
            ]
            
            # O'zgargan maydonlarni saqlash
            instance._changed_fields = []
            
            for field in fields_to_check:
                old_value = getattr(old_instance, field)
                new_value = getattr(instance, field)
                if old_value != new_value:
                    instance._changed_fields.append(field)
                    
        except Load.DoesNotExist:
            # Bu yangi obyekt
            pass

# CSV Import signal
@receiver(post_save, sender=CSVImport)
def process_csv_import(sender, instance, created, **kwargs):
    """CSV import yaratilgandan so'ng CSV ni qayta ishlash"""
    if created and not instance.processed:
        # CSV ni asinxron qayta ishlash
        thread = threading.Thread(target=process_csv_async, args=(instance,))
        thread.daemon = True
        thread.start()

def process_csv_async(import_instance):
    """CSV faylni asinxron qayta ishlash"""
    try:
        import_instance.process_csv()
        print(f"CSV import #{import_instance.id} muvaffaqiyatli qayta ishlandi")
    except Exception as e:
        print(f"CSV import #{import_instance.id} xatolik: {str(e)}")


