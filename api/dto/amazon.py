from rest_framework import serializers
from apps.load.models.amazon import AmazonRelayPayment, AmazonRelayProcessedRecord
from apps.load.models.load import Load

class AmazonRelayPaymentSerializer(serializers.ModelSerializer):
    file_name = serializers.SerializerMethodField()
    
    class Meta:
        model = AmazonRelayPayment
        fields = ['id', 'file', 'file_name', 'uploaded_at', 'status', 'processed_at', 
                 'total_amount', 'loads_updated', 'error_message']
        read_only_fields = ['id', 'uploaded_at', 'status', 'processed_at', 
                           'total_amount', 'loads_updated', 'error_message']
    
    def get_file_name(self, obj):
        if obj.file:
            return obj.file.name.split('/')[-1]
        return None
    
    def validate_file(self, value):
        """Fayl validation"""
        if not value.name.endswith(('.xlsx', '.xls')):
            raise serializers.ValidationError("Faqat Excel fayllari (.xlsx, .xls) qabul qilinadi")
        
        if value.size > 10 * 1024 * 1024:  # 10MB
            raise serializers.ValidationError("Fayl hajmi 10MB dan oshmasligi kerak")
        
        return value


class AmazonRelayPaymentListSerializer(serializers.ModelSerializer):
    """List view uchun serializer"""
    file_name = serializers.SerializerMethodField()
    
    class Meta:
        model = AmazonRelayPayment
        fields = ['id', 'file_name', 'uploaded_at', 'status', 'total_amount', 'loads_updated']
    
    def get_file_name(self, obj):
        if obj.file:
            return obj.file.name.split('/')[-1]
        return None


class LoadSerializer(serializers.ModelSerializer):
    """Load modeli uchun serializer"""
    class Meta:
        model = Load
        fields = ['id', 'reference_id', 'load_pay', 'amazon_amount']


class AmazonRelayProcessedRecordSerializer(serializers.ModelSerializer):
    """Processed records uchun serializer"""
    matched_load = LoadSerializer(read_only=True)
    
    class Meta:
        model = AmazonRelayProcessedRecord
        fields = ['id', 'trip_id', 'load_id', 'route', 'gross_pay', 
                 'start_date', 'end_date', 'distance', 'matched_load', 
                 'is_matched', 'created_at']