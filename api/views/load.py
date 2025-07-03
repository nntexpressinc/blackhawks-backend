from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework import permissions
from datetime import datetime
from django.db.models import Sum
from decimal import Decimal
from rest_framework.pagination import PageNumberPagination


from apps.load.models.driver import Pay, DriverPay, DriverExpense
from apps.load.models.truck import Unit
from apps.load.models.team import Team
from api.dto.load import TeamSerializer

from apps.load.models import (
    Load, LoadTags, Driver, DriverTags, Trailer, 
    TrailerTags, TruckTags, Truck, Dispatcher,
    DispatcherTags, EmployeeTags, CustomerBroker, 
    Stops, Employee, OtherPay, Commodities)

from api.dto.load import (
    LoadSerializer, DriverSerializer, 
    DriverTagsSerializer, TrailerSerializer, 
    TrailerTagsSerializer, TruckSerializer, 
    TruckTagsSerializer, DispatcherSerializer, 
    DispatcherTagsSerializer, EmployeeSerializer, 
    EmployeeTagsSerializer, CustomerBrokerSerializer, 
    LoadTagsSerializer, StopsSerializer, OtherPaySerializer, 
    CommoditiesSerializer, PaySerializer, DriverPaySerializer, 
    DriverExpenseSerializer,  UnitSerializer)


class CustomPagination(PageNumberPagination):
    page_size = 25
    def get_paginated_response(self, data):
        # Create a standard paginated response
        response = Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
        
        # Replace the hostname in the pagination links
        if response.data['next']:
            response.data['next'] = response.data['next'].replace('https://0.0.0.0:8000', 'https://api1.biznes-armiya.uz')
        if response.data['previous']:
            response.data['previous'] = response.data['previous'].replace('https://0.0.0.0:8000', 'https://api1.biznes-armiya.uz')
            
        return response




class TeamListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class UnitListView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        units = Unit.objects.all()
        serializer = UnitSerializer(units, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UnitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UnitDetailView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class DriverExpenseListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        driver_expenses = DriverExpense.objects.all()
        serializer = DriverExpenseSerializer(driver_expenses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DriverExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DriverExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DriverExpense.objects.all()
    serializer_class = DriverExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

class DriverPayListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        driver_pays = DriverPay.objects.all()
        serializer = DriverPaySerializer(driver_pays, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DriverPaySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DriverPayDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DriverPay.objects.all()
    serializer_class = DriverPaySerializer


class PayListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        pays = Pay.objects.all()
        serializer = PaySerializer(pays, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PaySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PayDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Pay.objects.all()
    serializer_class = PaySerializer
    

class LoadListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        loads = Load.objects.all()
        serializer = LoadSerializer(loads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = LoadSerializer(data=request.data, context={'request': request})  # request ni context sifatida uzatamiz
        if serializer.is_valid():
            # created_by ga request.user ni qo‘shamiz
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoadDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Load.objects.all()
    serializer_class = LoadSerializer



class DriverListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # pagination_class = CustomPagination

    # def get(self, request):
    #     drivers = Driver.objects.all()
    #     paginator = self.pagination_class()
    #     page = paginator.paginate_queryset(drivers, request)
    #     serializer = DriverSerializer(page, many=True)
    #     return paginator.get_paginated_response(serializer.data)
    
    # def post(self, request):
    #     serializer = DriverSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = DriverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DriverDetailView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [permissions.IsAuthenticated]
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


class DriverTagsListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        driver_tags = DriverTags.objects.all()
        serializer = DriverTagsSerializer(driver_tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = DriverTagsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DriverTagsDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DriverTags.objects.all()
    serializer_class = DriverTagsSerializer

class TrailerListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        trailers = Trailer.objects.all()
        serializer = TrailerSerializer(trailers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = TrailerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TrailerDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Trailer.objects.all()
    serializer_class = TrailerSerializer

class TrailerTagsListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        trailer_tags = TrailerTags.objects.all()
        serializer = TrailerTagsSerializer(trailer_tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = TrailerTagsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TrailerTagsDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = TrailerTags.objects.all()
    serializer_class = TrailerTagsSerializer

class TruckListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        trucks = Truck.objects.all()
        serializer = TruckSerializer(trucks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = TruckSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TruckDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer

class TruckTagsListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        truck_tags = TruckTags.objects.all()
        serializer = TruckTagsSerializer(truck_tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = TruckTagsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TruckTagsDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = TruckTags.objects.all()
    serializer_class = TruckTagsSerializer

class DispatcherListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        dispatchers = Dispatcher.objects.all()
        serializer = DispatcherSerializer(dispatchers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = DispatcherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DispatcherDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Dispatcher.objects.all()
    serializer_class = DispatcherSerializer

class DispatcherTagsListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        dispatcher_tags = DispatcherTags.objects.all()
        serializer = DispatcherTagsSerializer(dispatcher_tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = DispatcherTagsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DispatcherTagsDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DispatcherTags.objects.all()
    serializer_class = DispatcherTagsSerializer

class EmployeeListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class EmployeeTagsListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        employee_tags = EmployeeTags.objects.all()
        serializer = EmployeeTagsSerializer(employee_tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = EmployeeTagsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EmployeeTagsDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = EmployeeTags.objects.all()
    serializer_class = EmployeeTagsSerializer
    
class CustomerBrokerListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        custom_brokers = CustomerBroker.objects.all()
        serializer = CustomerBrokerSerializer(custom_brokers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CustomerBrokerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomerBrokerDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomerBroker.objects.all()
    serializer_class = CustomerBrokerSerializer

class CommoditiesListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        commodities = Commodities.objects.all()
        serializer = CommoditiesSerializer(commodities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CommoditiesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommoditiesDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Commodities.objects.all()
    serializer_class = CommoditiesSerializer

class OtherPayListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        other_pays = OtherPay.objects.all()
        serializer = OtherPaySerializer(other_pays, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = OtherPaySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OtherPayDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = OtherPay.objects.all()
    serializer_class = OtherPaySerializer

class StopsListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        stops = Stops.objects.all()
        serializer = StopsSerializer(stops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = StopsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class StopsDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Stops.objects.all()
    serializer_class = StopsSerializer

class LoadTagsListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        load_tags = LoadTags.objects.all()
        serializer = LoadTagsSerializer(load_tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = LoadTagsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoadTagsDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = LoadTags.objects.all()
    serializer_class = LoadTagsSerializer



from django.db.models import Q, Min, Max
from datetime import datetime

from django.db.models import Q, Min, Max
from datetime import datetime

class DriverPayCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # POST so'rovdan ma'lumotlarni olish
        pay_from = request.data.get('pay_from')
        pay_to = request.data.get('pay_to')
        driver_id = request.data.get('driver')
        notes = request.data.get('notes', '')

        # Sana formatini tekshirish va konvertatsiya qilish
        try:
            pay_from_date = datetime.strptime(pay_from, '%Y-%m-%d').date()
            pay_to_date = datetime.strptime(pay_to, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        # Driver obyektini olish
        try:
            driver = Driver.objects.get(id=driver_id)
        except Driver.DoesNotExist:
            return Response({"error": "Driver not found."}, status=status.HTTP_404_NOT_FOUND)

        # Driverga bog'langan Pay obyektini olish
        try:
            pay = Pay.objects.filter(driver=driver).latest('id')
        except Pay.DoesNotExist:
            return Response({"error": "No Pay found for this driver."}, status=status.HTTP_404_NOT_FOUND)

        # DriverPay obyektini boshlang'ich saqlash
        driver_pay = DriverPay(
            driver=driver,
            pay=pay,
            pay_from=pay_from_date,
            pay_to=pay_to_date,
            amount=0.0,
            notes=notes,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        driver_pay.save()

        # FIXED: Changed annotation names to avoid conflicts with existing model fields
        loads_with_dates = Load.objects.filter(
            driver=driver,
            stop__appointmentdate__isnull=False
        ).annotate(
            calculated_pickup_date=Min('stop__appointmentdate', filter=Q(stop__stop_name='PICKUP')),
            calculated_delivery_date=Max('stop__appointmentdate', filter=Q(stop__stop_name='DELIVERY'))
        ).filter(
            calculated_pickup_date__isnull=False,
            calculated_delivery_date__isnull=False
        )

        # Filter loads based on overlap with pay period using new annotation names
        filtered_loads = loads_with_dates.filter(
            Q(calculated_pickup_date__date__gte=pay_from_date, calculated_pickup_date__date__lte=pay_to_date) |  # Pickup in period
            Q(calculated_delivery_date__date__gte=pay_from_date, calculated_delivery_date__date__lte=pay_to_date) |  # Delivery in period
            Q(calculated_pickup_date__date__lte=pay_from_date, calculated_delivery_date__date__gte=pay_to_date)  # Period within load span
        ).distinct()

        # Hisoblash va natijani tayyorlash
        total_pay = 0.0
        total_load_pays = 0.0
        total_other_pays = 0.0
        load_details = []
        chargebag_deductions = []
        total_loads_formula = []
        total_other_pays_formula = []
        total_chargebag_amount = 0.0  # FIXED: Track total chargebag separately

        for load in filtered_loads:
            load_payment = 0.0
            load_formula = []
            if load.load_pay and pay.standart:
                load_payment = float(load.load_pay) * (float(pay.standart) / 100)
                total_load_pays += load_payment
                load_formula.append(f"${load.load_pay:.2f} * {pay.standart}%")

            load_total_pay = float(load.total_pay) if load.total_pay else 0.0

            other_pays = OtherPay.objects.filter(load=load)
            load_chargebag_amount = 0.0
            other_pay_details = []

            for other_pay in other_pays:
                if other_pay.amount:
                    amount = float(other_pay.amount)
                    
                    if other_pay.pay_type in ['DETENTION', 'LAYOVER']:
                        # DETENTION va LAYOVER: standart foiz bilan hisoblanadi va qo'shiladi
                        amount_with_percentage = amount * (float(pay.standart) / 100) if pay.standart else amount
                        load_payment += amount_with_percentage
                        total_other_pays += amount_with_percentage
                        total_other_pays_formula.append(f"${amount:.2f} * {pay.standart}%")
                        other_pay_info = {
                            "pay_type": other_pay.pay_type,
                            "formula": f"${amount:.2f} * {pay.standart}%",
                            "result": f"${amount_with_percentage:.2f}",
                            "note": other_pay.note if other_pay.note else ''
                        }
                    elif other_pay.pay_type == 'CHARGEBACK':
                        # CHARGEBACK: ayiriladi (deduction) - FIXED: subtract from load_payment
                        load_chargebag_amount += amount
                        total_chargebag_amount += amount
                        load_payment -= amount  # FIX: Subtract from individual load payment
                        chargebag_deductions.append({
                            "load_id": load.load_id,
                            "amount": f"${amount:.2f}",
                            "note": other_pay.note if other_pay.note else '',
                            "pay_type": other_pay.pay_type
                        })
                        other_pay_info = {
                            "pay_type": other_pay.pay_type,
                            "formula": f"-${amount:.2f}",
                            "result": f"-${amount:.2f}",
                            "note": other_pay.note if other_pay.note else ''
                        }
                    elif other_pay.pay_type in ['EQUIPMENT', 'LUMPER', 'DRIVERASSIST', 'TRAILERWASH', 'ESCORTFEE', 'BONUS', 'OTHER']:
                        # Boshqa barcha payment typelar: to'g'ridan-to'g'ri qo'shiladi
                        load_payment += amount
                        total_other_pays += amount
                        total_other_pays_formula.append(f"${amount:.2f}")
                        other_pay_info = {
                            "pay_type": other_pay.pay_type,
                            "formula": f"${amount:.2f}",
                            "result": f"${amount:.2f}",
                            "note": other_pay.note if other_pay.note else ''
                        }
                    else:
                        # Noma'lum payment typelar uchun default behavior
                        load_payment += amount
                        total_other_pays += amount
                        total_other_pays_formula.append(f"${amount:.2f}")
                        other_pay_info = {
                            "pay_type": other_pay.pay_type,
                            "formula": f"${amount:.2f}",
                            "result": f"${amount:.2f}",
                            "note": other_pay.note if other_pay.note else ''
                        }

                    other_pay_details.append(other_pay_info)

            # Get actual pickup and delivery information from stops
            pickup_stop = None
            delivery_stop = None
            
            # Access stops from the load object
            for stop in load.stop.all():
                if stop.stop_name == 'PICKUP':
                    pickup_stop = stop
                elif stop.stop_name == 'DELIVERY':
                    delivery_stop = stop
            
            pickup_info = "N/A"
            delivery_info = "N/A"
            
            if pickup_stop and pickup_stop.appointmentdate:
                pickup_location = f"{pickup_stop.city}, {pickup_stop.state}" if pickup_stop.city else pickup_stop.address1
                pickup_info = f"{pickup_stop.appointmentdate.strftime('%Y-%m-%d')}, {pickup_location}"
            
            if delivery_stop and delivery_stop.appointmentdate:
                delivery_location = f"{delivery_stop.city}, {delivery_stop.state}" if delivery_stop.city else delivery_stop.address1
                delivery_info = f"{delivery_stop.appointmentdate.strftime('%Y-%m-%d')}, {delivery_location}"

            load_info = {
                "Load #": load.load_id,
                "Pickup": pickup_info,
                "Delivery": delivery_info,
                "Formula": " + ".join(load_formula) if load_formula else "N/A",
                "Result": f"${load_payment:.2f}",
                "Notes": load.note if load.note else '',
                "Chargebag Deduction": f"${load_chargebag_amount:.2f}" if load_chargebag_amount > 0 else None,
                "Other Payments": other_pay_details if other_pay_details else None
            }
            load_details.append(load_info)
            if load_formula:
                total_loads_formula.append(f"({load_info['Formula']} = ${load_payment:.2f})")

        escrow_weekly = driver.escrow_deposit if driver.escrow_deposit else 0

        # Fix 2: Update the driver's cost field by adding the escrow amount
        if escrow_weekly > 0:
            driver.cost = (driver.cost or 0) + escrow_weekly
            driver.save()

        # Expenses calculation
        expenses = DriverExpense.objects.filter(
            driver=driver,
            expense_date__gte=pay_from_date,
            expense_date__lte=pay_to_date
        )

        total_expenses = 0.0
        total_income = 0.0
        expense_details = []
        income_formula = []
        expenses_formula = []

        for expense in expenses:
            amount = float(expense.amount)
            if expense.transaction_type == '+':
                total_income += amount
                income_formula.append(f"${amount:.2f}")
            elif expense.transaction_type == '-':
                total_expenses += amount
                expenses_formula.append(f"${amount:.2f}")

            expense_details.append({
                "Description": expense.description,
                "Formula": f"{'+' if expense.transaction_type == '+' else '-'}${amount:.2f}",
                "Result": f"${amount:.2f}",
                "Type": "Income" if expense.transaction_type == '+' else "Expense",
                "Date": expense.expense_date.strftime('%Y-%m-%d') if expense.expense_date else 'N/A'
            })

        # FIXED: Calculate final total_pay correctly - include all load payments
        print(f"DEBUG: total_load_pays = {total_load_pays}")
        print(f"DEBUG: total_other_pays = {total_other_pays}")
        print(f"DEBUG: total_chargebag_amount = {total_chargebag_amount}")
        print(f"DEBUG: escrow_weekly = {escrow_weekly}")
        print(f"DEBUG: total_expenses = {total_expenses}")
        print(f"DEBUG: total_income = {total_income}")
        
        total_pay = total_load_pays + total_other_pays - escrow_weekly - total_expenses + total_income - total_chargebag_amount

        print(f"DEBUG: calculated total_pay = {total_pay}")
        total_pay = max(total_pay, 0)

        # Prepare total_pay formula
        total_pay_formula = []
        if total_load_pays > 0:
            total_pay_formula.append(f"Load Pays: ${total_load_pays:.2f}")
        if total_other_pays > 0:
            total_pay_formula.append(f"Other Pays: ${total_other_pays:.2f}")
        if total_chargebag_amount > 0:
            total_pay_formula.append(f"Chargeback: -${total_chargebag_amount:.2f}")
        if escrow_weekly > 0:
            total_pay_formula.append(f"Escrow: -${escrow_weekly:.2f}")
        if total_income > 0:
            total_pay_formula.append(f"Income: ${total_income:.2f}")
        if total_expenses > 0:
            total_pay_formula.append(f"Expenses: -${total_expenses:.2f}")

        driver_pay.loads = load_details
        driver_pay.amount = total_pay
        driver_pay.save()

        # Driver ma'lumotlari
        driver_info = {
            "first_name": driver.user.first_name if driver.user else None,
            "last_name": driver.user.last_name if driver.user else None,
            "contact_number": driver.user.telephone if driver.user else None,
            "address1": driver.user.address if driver.user else None,
            "generate_date": driver_pay.created_at.strftime('%Y-%m-%d %H:%M:%S') if driver_pay.created_at else None,
            "report_date": driver_pay.updated_at.strftime('%Y-%m-%d %H:%M:%S') if driver_pay.updated_at else None,
            "search_from": driver_pay.pay_from.strftime('%Y-%m-%d') if driver_pay.pay_from else None,
            "search_to": driver_pay.pay_to.strftime('%Y-%m-%d') if driver_pay.pay_to else None
        }

        # User ma'lumotlari
        user_info = {
            "email": driver.user.email if driver.user else None,
            "company_name": driver.user.company_name if driver.user else None,
            "fax": driver.user.fax if driver.user else None,
            "address": driver.user.address if driver.user else None,
            "country": driver.user.country if driver.user else None,
            "telephone": driver.user.telephone if driver.user else None,
            "state": driver.user.state if driver.user else None,
            "postal_zip": driver.user.postal_zip if driver.user else None
        }

        # Yakuniy javob
        response_data = {
            "driver": driver_info,
            "user_admin": user_info,
            "loads": load_details,
            "total_load_pays": {
                "Formula": " + ".join(total_loads_formula) if total_loads_formula else "N/A",
                "Result": f"${total_load_pays:.2f}"
            },
            "total_other_pays": {
                "Formula": " + ".join(total_other_pays_formula) if total_other_pays_formula else "N/A",
                "Result": f"${total_other_pays:.2f}"
            },
            "escrow_deduction": {
                "Formula": f"-${escrow_weekly:.2f}" if escrow_weekly else "N/A",
                "Result": f"${escrow_weekly:.2f}"
            },
            "chargeback_deductions": chargebag_deductions,
            "expenses": expense_details,
            "total_expenses": {
                "Formula": " + ".join(expenses_formula) if expenses_formula else "N/A",
                "Result": f"${total_expenses:.2f}"
            },
            "total_income": {
                "Formula": " + ".join(income_formula) if income_formula else "N/A",
                "Result": f"${total_income:.2f}"
            },
            "total_pay": {
                "Formula": " + ".join(total_pay_formula) if total_pay_formula else "N/A",
                "Result": f"${total_pay:.2f}"
            }
        }

        return Response(response_data, status=status.HTTP_201_CREATED)