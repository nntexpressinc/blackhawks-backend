from django.db.models.signals import post_save
from django.dispatch import receiver
from .models.csv_import import CSVImport
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=CSVImport)
def process_csv_import(sender, instance, created, **kwargs):
    """CSV import yaratilgan zahoti uni qayta ishlash"""
    if created and not instance.processed:
        logger.info(f"CSV import boshlandi: {instance.id}")
        try:
            success = instance.process_csv()
            if success:
                logger.info(f"CSV import muvaffaqiyatli yakunlandi: {instance.id}")
            else:
                logger.error(f"CSV import xato bilan yakunlandi: {instance.id}")
        except Exception as e:
            logger.error(f"CSV import signalida xato: {str(e)}")
            instance.error_log = f"Signal xatosi: {str(e)}"
            instance.processed = True
            instance.save()
