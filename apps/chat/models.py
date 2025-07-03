from django.db import models
import requests
from apps.load.models import Load
from apps.auth.models import User
from PIL import Image
from reportlab.pdfgen import canvas
import os
from django.conf import settings

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

class Chat(models.Model):
    load_id = models.ForeignKey(Load, related_name='LoadChat', on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    user = models.ForeignKey(User, related_name='UserChat', on_delete=models.CASCADE)
    file = models.FileField(upload_to='chat_files/', null=True, blank=True)
    group_message_id = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Yangi obyekt yaratilganda
            super().save(*args, **kwargs)

            # Team ma'lumotlarini olish
            team = self.load_id.team_id
            
            # Agar team belgilanmagan bo'lsa yoki telegram ma'lumotlari bo'lmasa, funksiyadan chiqamiz
            if not team or not team.telegram_group_id or not self.load_id.group_message_id:
                print("Team not assigned, Telegram configuration missing, or load has no group_message_id.")
                return
            
            # Team modelidagi telegram ma'lumotlaridan foydalanish
            bot_token = team.telegram_token if hasattr(team, 'telegram_token') else "7582469651:AAHBtrGUmdo2tzDPU4RSI61AFN99EQnqbJE"  # Default token
            
            # Telegram ID formatini tekshirish va to'g'rilash
            group_channel_id = process_telegram_id(team.telegram_group_id)
            
            message = f"{self.user.email}: {self.message}"

            # Agar fayl bo'lmasa, faqat matnli xabar yuboramiz
            if not self.file:
                url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                data = {
                    "chat_id": group_channel_id,
                    "text": message,
                    "parse_mode": "Markdown",
                    "reply_to_message_id": int(self.load_id.group_message_id) + 1  # +1 qo'shiladi
                }

                response = requests.post(url, data=data)
                response_data = response.json()

                if response_data.get("ok"):
                    print("Matnli xabar yuborildi.")
                    self.group_message_id = response_data["result"]["message_id"]
                    super().save(update_fields=['group_message_id'])
                else:
                    print(f"Xatolik (matn): {response_data.get('description')}")
                    print("Javob ma'lumotlari:", response_data)
                    return

            # Agar fayl bo'lsa, uni tekshirish va yuborish (xabar faqat caption'da)
            if self.file:
                file_path = self.file.path
                file_name = self.file.name

                # Fayl turi bo'yicha tekshirish
                if file_name.endswith(('.jpg', '.jpeg', '.png')):  # Rasm bo'lsa
                    # Rasmni PDF ga aylantirish
                    pdf_path = self.convert_image_to_pdf(file_path)
                    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
                    data = {
                        "chat_id": group_channel_id,
                        "caption": message,  # Xabar faqat caption'da
                        "reply_to_message_id": int(self.load_id.group_message_id) + 1  # +1 qo'shiladi
                    }
                    with open(pdf_path, 'rb') as pdf_file:
                        files = {"document": (os.path.basename(pdf_path), pdf_file)}
                        response = requests.post(url, data=data, files=files)

                    # Vaqtinchalik PDF faylni o'chirish
                    if os.path.exists(pdf_path):
                        os.remove(pdf_path)

                else:  # PDF yoki boshqa fayl bo'lsa
                    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
                    data = {
                        "chat_id": group_channel_id,
                        "caption": message,  # Xabar faqat caption'da
                        "reply_to_message_id": int(self.load_id.group_message_id) + 1  # +1 qo'shiladi
                    }
                    with open(file_path, 'rb') as doc_file:
                        files = {"document": (file_name, doc_file)}
                        response = requests.post(url, data=data, files=files)

                response_data = response.json()
                if response_data.get("ok"):
                    print("Fayl muvaffaqiyatli yuborildi.")
                    self.group_message_id = response_data["result"]["message_id"]
                    super().save(update_fields=['group_message_id'])
                else:
                    print(f"Xatolik (fayl): {response_data.get('description')}")
                    print("Javob ma'lumotlari:", response_data)

        else:
            super().save(*args, **kwargs)

    def convert_image_to_pdf(self, image_path):
        """Rasmni PDF ga aylantirish"""
        image = Image.open(image_path)
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Vaqtinchalik PDF fayl yaratish
        pdf_path = os.path.join(settings.MEDIA_ROOT, 'temp', f"{os.path.basename(image_path)}.pdf")
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

        # PDF yaratish
        c = canvas.Canvas(pdf_path)
        img_width, img_height = image.size
        c.setPageSize((img_width, img_height))
        c.drawImage(image_path, 0, 0, img_width, img_height)
        c.showPage()
        c.save()

        return pdf_path