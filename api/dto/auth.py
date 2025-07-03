from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from apps.auth.models import User, UserLocation, Company, Role, Permission

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name', 'permission_id', 'created_at')

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='company', write_only=True, required=False
    )

    class Meta:
        model = User
        fields = (
            'id', 'email', 'company_name', 'first_name', 'last_name',
            'telephone', 'city', 'address', 'country', 'state',
            'postal_zip', 'ext', 'fax', 'role', 'company', 'profile_photo', 'company_id', 'password'
        )
        extra_kwargs = {'email': {'required': False},
            'password': {'required': False, 'write_only': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'telephone': {'required': False},
            'city': {'required': False},
            'address': {'required': False},
            'country': {'required': False},
            'state': {'required': False},
            'postal_zip': {'required': False},
            'ext': {'required': False},
            'fax': {'required': False},
            'role': {'required': False},
            'company': {'required': False},
            'company_id': {'required': False},
            'profile_photo': {'required': False},
            'password': {'write_only': True, 'min_length': 8}}
    def create(self, validated_data):
        company = validated_data.pop('company', None)
        user = User.objects.create_user(**validated_data)
        if company:
            user.company = company
            user.save()
        return user

    def update(self, instance, validated_data):
        # Faqat yuborilgan maydonlarni yangilash
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)  # Parolni xavfsiz yangilash
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
    

class CustomTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid credentials')

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'role': user.role.id if user.role else None,
            # 'company_id': user.company.id if user.company else None,
        }
    
    
class UserLocationSerializer(serializers.ModelSerializer):
    google_maps_url = serializers.SerializerMethodField()

    class Meta:
        model = UserLocation
        fields = ['user', 'latitude', 'longitude', 'created_at', 'google_maps_url', 'device_info', 'page_status']  # Kerakli maydonlar
        read_only_fields = ['created_at', 'google_maps_url']  # Faqat bu maydonlar read-only

    def get_google_maps_url(self, obj):
        return f"https://www.google.com/maps?q={obj.latitude},{obj.longitude}"
