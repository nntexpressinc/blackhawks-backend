from rest_framework import generics, permissions, status
from rest_framework.response import Response
from api.views.token import get_tokens_for_user
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import PermissionDenied
from django.db.models import Count

from apps.auth.models import User, Company, UserLocation, Role, Permission
from api.dto.auth import CustomUserSerializer, CustomTokenObtainPairSerializer, CompanySerializer, UserLocationSerializer, RoleSerializer, PermissionSerializer
from django.contrib.auth import logout


class RoleListView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]

class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]

class PermissionListView(generics.ListCreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]

class PermissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]


class LogoutUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_200_OK)

class LoginUserView(generics.GenericAPIView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class RegisterUserView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response(tokens, status=status.HTTP_201_CREATED)


class ListUsersView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    queryset = User.objects.all()
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
class CustomTokenObtainPairView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class CompanyListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'super_admin':
            return Company.objects.all()
        return Company.objects.filter(admin=user)

    def perform_create(self, serializer):
        user = self.request.user
        if user.role not in ['super_admin', 'admin']:
            raise permissions.PermissionDenied("Only admins can create companies")
        company = serializer.save(admin=user)
        user.company = company
        user.save()

class LocationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        user_id = request.data.get('user')
        device_info = request.data.get('device_info')
        page_status = request.data.get('page_status')
        print(f"Received data: latitude={latitude}, longitude={longitude}, user={user_id}, device_info={device_info}, page_status={page_status}")  # Debugging

        if latitude is not None and longitude is not None and user_id is not None:
            try:
                user = User.objects.get(id=user_id)
                location = UserLocation(
                    user=user,
                    latitude=float(latitude),
                    longitude=float(longitude),
                    ip_address=request.META.get('REMOTE_ADDR', 'Unknown'),
                    device_info=device_info,
                    page_status=page_status,
                )
                location.save()
                print(f"Location saved: {location}")
                serializer = UserLocationSerializer(location)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                print(f"User with id={user_id} not found")
                return Response({"error": "Foydalanuvchi topilmadi"}, status=status.HTTP_404_NOT_FOUND)
            except ValueError as e:
                print(f"ValueError: {str(e)}")
                return Response({"error": f"Noto‘g‘ri ma'lumot formati: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(f"Error saving to DB: {str(e)}")
                return Response({"error": f"Saqlashda xatolik: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"error": "Latitude, longitude yoki user topilmadi"}, status=status.HTTP_400_BAD_REQUEST)
class MyLocationsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            locations = UserLocation.objects.all()
            if not locations.exists():
                return Response({"message": "Joylashuvlar topilmadi"}, status=status.HTTP_404_NOT_FOUND)
            serializer = UserLocationSerializer(locations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SuperAdminDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.role != 'super_admin':
            raise PermissionDenied("Only super admins can access this")

        companies = Company.objects.annotate(
            user_count=Count('users'),
            driver_count=Count('users__driver_profile'),
            dispatcher_count=Count('users__dispatcher_profile')
        ).values('id', 'name', 'user_count', 'driver_count', 'dispatcher_count')

        return Response({
            'companies': companies,
            'total_users': User.objects.count(),
            'total_companies': Company.objects.count(),
        })
