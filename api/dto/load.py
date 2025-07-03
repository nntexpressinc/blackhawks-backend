from rest_framework import serializers
from api.dto.auth import CustomUserSerializer
from api.dto.auth import CustomUserSerializer
from apps.load.models.driver import Pay, DriverPay, DriverExpense
from apps.load.models.truck import Unit
from apps.load.models.team import Team

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"
        
from apps.auth.models import User
from apps.load.models import (
    Load, LoadTags, Driver, DriverTags, Trailer, 
    TrailerTags, TruckTags, Truck, Dispatcher,
    DispatcherTags, EmployeeTags, CustomerBroker, 
    Stops, Employee, OtherPay, Commodities)


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"


class DriverExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverExpense
        fields = "__all__"
class DriverPaySerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverPay
        fields = "__all__"


class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay
        fields = "__all__"

class DispatcherLoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispatcher
        fields = ['id', 'nickname']

class CustomerBrokerLoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerBroker
        fields = ['id', 'company_name']

# class DriverLoadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Driver
#         fields = ['id', 'first_name', 'last_name']

class LoadSerializer(serializers.ModelSerializer):
    # ForeignKey maydonlarni faqat ID sifatida qabul qilish uchun
    # created_by = serializers.PrimaryKeyRelatedField(queryset=Dispatcher.objects.all(), required=False, allow_null=True)
    customer_broker = serializers.PrimaryKeyRelatedField(queryset=CustomerBroker.objects.all(), required=False, allow_null=True)
    driver = serializers.PrimaryKeyRelatedField(queryset=Driver.objects.all(), required=False, allow_null=True)
    dispatcher = serializers.PrimaryKeyRelatedField(queryset=Dispatcher.objects.all(), required=False, allow_null=True)
    truck = serializers.PrimaryKeyRelatedField(queryset=Truck.objects.all(), required=False, allow_null=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=LoadTags.objects.all(), required=False, allow_null=True)
    stop = serializers.PrimaryKeyRelatedField(many=True, queryset=Stops.objects.all(), required=False, allow_null=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Load
        fields = "__all__"
        read_only_fields = ['created_by', 'created_date', 'updated_date']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_by'] = CustomUserSerializer(instance.created_by).data if instance.created_by else None
        representation['customer_broker'] = CustomerBrokerSerializer(instance.customer_broker).data if instance.customer_broker else None
        representation['driver'] = DriverSerializer(instance.driver).data if instance.driver else None
        representation['dispatcher'] = DispatcherSerializer(instance.dispatcher).data if instance.dispatcher else None
        representation['truck'] = TruckSerializer(instance.truck).data if instance.truck else None
        representation['tags'] = LoadTagsSerializer(instance.tags).data if instance.tags else None
        representation['stop'] = StopsSerializer(instance.stop.all(), many=True).data if instance.stop.exists() else None
        return representation

class DriverSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    class Meta:
        model = Driver
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = CustomUserSerializer(instance.user).data if instance.user else None
        return representation
class TrailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trailer
        fields = "__all__"

class TrailerTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrailerTags
        fields = "__all__"

class DriverTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverTags
        fields = "__all__"

class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = "__all__"

class TruckTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TruckTags
        fields = "__all__"

class DispatcherSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    class Meta:
        model = Dispatcher
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = CustomUserSerializer(instance.user).data if instance.user else None
        return representation

class DispatcherTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DispatcherTags
        fields = "__all__"

class EmployeeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    class Meta:
        model = Employee
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = CustomUserSerializer(instance.user).data if instance.user else None
        return representation

class EmployeeTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeTags
        fields = "__all__"

class CustomerBrokerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerBroker
        fields = "__all__"
    
class LoadTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadTags
        fields = "__all__"

class StopsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stops
        fields = "__all__"

class OtherPaySerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherPay
        fields = "__all__"

class CommoditiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodities
        fields = "__all__"


        
