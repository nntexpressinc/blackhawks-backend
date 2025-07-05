from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from apps.load.models.amazon import AmazonRelayPayment, AmazonRelayProcessedRecord
from api.dto.amazon import AmazonRelayPaymentSerializer, AmazonRelayProcessedRecordSerializer
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_amazon_relay_file(request):
    """Amazon Relay Excel faylini yuklash"""
    try:
        if 'file' not in request.FILES:
            return Response({
                'error': 'Fayl yuborilmadi'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']
        
        # Fayl kengaytmasini tekshirish
        if not file.name.endswith(('.xlsx', '.xls')):
            return Response({
                'error': 'Fayl formati noto\'g\'ri. Faqat .xlsx yoki .xls fayllar qabul qilinadi'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # AmazonRelayPayment yaratish
        payment = AmazonRelayPayment.objects.create(
            file=file,
            status='pending'
        )
        
        logger.info(f"Amazon Relay fayl yuklandi: {payment.id}")
        
        serializer = AmazonRelayPaymentSerializer(payment)
        return Response({
            'message': 'Fayl muvaffaqiyatli yuklandi va qayta ishlanmoqda',
            'payment': serializer.data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Amazon Relay fayl yuklanishida xatolik: {str(e)}")
        return Response({
            'error': f'Fayl yuklashda xatolik: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_amazon_relay_payments(request):
    """Amazon Relay to'lovlari ro'yxati"""
    try:
        payments = AmazonRelayPayment.objects.all().order_by('-uploaded_at')
        serializer = AmazonRelayPaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Amazon Relay to'lovlari olishda xatolik: {str(e)}")
        return Response({
            'error': 'Ma\'lumotlarni olishda xatolik'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_amazon_relay_payment_detail(request, payment_id):
    """Amazon Relay to'lov tafsilotlari"""
    try:
        payment = AmazonRelayPayment.objects.get(id=payment_id)
        processed_records = AmazonRelayProcessedRecord.objects.filter(payment=payment)
        
        payment_serializer = AmazonRelayPaymentSerializer(payment)
        records_serializer = AmazonRelayProcessedRecordSerializer(processed_records, many=True)
        
        return Response({
            'payment': payment_serializer.data,
            'processed_records': records_serializer.data
        }, status=status.HTTP_200_OK)
        
    except AmazonRelayPayment.DoesNotExist:
        return Response({
            'error': 'To\'lov topilmadi'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Amazon Relay to'lov tafsilotlari olishda xatolik: {str(e)}")
        return Response({
            'error': 'Ma\'lumotlarni olishda xatolik'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)