from rest_framework import serializers
from apps.load.models.amazon import AmazonRelayPayment

class AmazonRelayPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmazonRelayPayment
        fields = ['id', 'file', 'uploaded_at', 'status', 'processed_at', 
                 'total_amount', 'loads_updated', 'error_message']
        read_only_fields = ['id', 'uploaded_at', 'status', 'processed_at', 
                           'total_amount', 'loads_updated', 'error_message']
    
    def validate_file(self, value):
        """Fayl validation"""
        if not value.name.endswith(('.xlsx', '.xls')):
            raise serializers.ValidationError("Faqat Excel fayllari (.xlsx, .xls) qabul qilinadi")
        
        if value.size > 10 * 1024 * 1024:  # 10MB
            raise serializers.ValidationError("Fayl hajmi 10MB dan oshmasligi kerak")
        
        return value


class AmazonRelayPaymentListSerializer(serializers.ModelSerializer):
    """List view uchun serializer"""
    class Meta:
        model = AmazonRelayPayment
        fields = ['id', 'uploaded_at', 'status', 'total_amount', 'loads_updated']