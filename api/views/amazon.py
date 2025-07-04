from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from apps.load.models.amazon import AmazonRelayPayment
from api.dto.amazon import AmazonRelayPaymentSerializer, AmazonRelayPaymentListSerializer

@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_amazon_relay_file(request):
    """
    Amazon Relay Excel faylini yuklash va qayta ishlash
    
    POST /api/amazon-relay/upload/
    
    Parameters:
    - file: Excel fayl (.xlsx, .xls)
    
    Returns:
    - success: bool
    - message: str
    - data: object (payment ma'lumotlari)
    """
    try:
        if 'file' not in request.FILES:
            return Response({
                'success': False,
                'message': 'Fayl topilmadi',
                'error': 'FILE_NOT_FOUND'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Serializer bilan validation
        serializer = AmazonRelayPaymentSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Fayl validatsiyadan o\'tmadi',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Payment yaratish
        payment = serializer.save()
        
        # Faylni qayta ishlash
        payment.process_excel_file()
        
        # Yangilangan ma'lumotlarni qaytarish
        updated_serializer = AmazonRelayPaymentSerializer(payment)
        
        return Response({
            'success': True,
            'message': 'Fayl muvaffaqiyatli yuklandi va qayta ishlandi',
            'data': updated_serializer.data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Serverda xatolik yuz berdi',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_payment_status(request, payment_id):
    """
    To'lov statusini olish
    
    GET /api/amazon-relay/status/{payment_id}/
    
    Returns:
    - success: bool
    - data: object (payment ma'lumotlari)
    """
    try:
        payment = AmazonRelayPayment.objects.get(id=payment_id)
        serializer = AmazonRelayPaymentSerializer(payment)
        
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except AmazonRelayPayment.DoesNotExist:
        return Response({
            'success': False,
            'message': 'To\'lov ma\'lumotlari topilmadi'
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Serverda xatolik yuz berdi',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_payment_history(request):
    """
    To'lov tarixini olish
    
    GET /api/amazon-relay/history/
    
    Query parameters:
    - limit: int (default: 20)
    - offset: int (default: 0)
    - status: str (pending, processing, completed, failed)
    
    Returns:
    - success: bool
    - data: array
    - total: int
    """
    try:
        # Query parameters
        limit = int(request.GET.get('limit', 20))
        offset = int(request.GET.get('offset', 0))
        status_filter = request.GET.get('status', None)
        
        # Base queryset
        queryset = AmazonRelayPayment.objects.all()
        
        # Status filter
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Total count
        total = queryset.count()
        
        # Pagination
        payments = queryset[offset:offset + limit]
        
        # Serialize
        serializer = AmazonRelayPaymentListSerializer(payments, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data,
            'total': total,
            'limit': limit,
            'offset': offset
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Serverda xatolik yuz berdi',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_payment(request, payment_id):
    """
    To'lov ma'lumotlarini o'chirish
    
    DELETE /api/amazon-relay/delete/{payment_id}/
    
    Returns:
    - success: bool
    - message: str
    """
    try:
        payment = AmazonRelayPayment.objects.get(id=payment_id)
        payment.delete()
        
        return Response({
            'success': True,
            'message': 'To\'lov ma\'lumotlari o\'chirildi'
        }, status=status.HTTP_200_OK)
        
    except AmazonRelayPayment.DoesNotExist:
        return Response({
            'success': False,
            'message': 'To\'lov ma\'lumotlari topilmadi'
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Serverda xatolik yuz berdi',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

