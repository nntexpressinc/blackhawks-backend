from django.urls import path
from api.views.chat import ChatList, ChatDetail

from api.views.auth import (
    RegisterUserView, ListUsersView, 
    UserDetailView, CustomTokenObtainPairView,
    LocationView, MyLocationsView, LoginUserView, 
    LogoutUserView, CompanyListCreateView, 
    SuperAdminDashboardView, RoleListView,
    RoleDetailView, PermissionListView,
    PermissionDetailView)

from api.views.load import (
    TruckTagsDetailView, LoadListView, 
    LoadDetailView, DriverListView, 
    DriverDetailView, DriverTagsListView, 
    DriverTagsDetailView, TruckListView, 
    TrailerTagsDetailView, TruckDetailView, 
    TrailerListView, TrailerDetailView, 
    TrailerTagsListView, TruckTagsListView, 
    TrailerTagsDetailView, DispatcherListView, 
    DispatcherDetailView, DispatcherTagsListView, 
    DispatcherTagsDetailView, DispatcherTagsDetailView, 
    EmployeeListView, EmployeeDetailView, 
    EmployeeTagsDetailView, EmployeeTagsListView, 
    CustomerBrokerListView, CustomerBrokerDetailView, 
    CommoditiesListView, CommoditiesDetailView, OtherPayListView, 
    OtherPayDetailView, StopsListView, StopsDetailView, LoadTagsListView, 
    LoadTagsDetailView, PayListView, PayDetailView, DriverPayListView,
    DriverPayDetailView, DriverPayCreateView, DriverExpenseListView, 
    DriverExpenseDetailView, UnitListView, UnitDetailView, TeamListView,
    TeamDetailView)

urlpatterns = [
    path('auth/register/', RegisterUserView.as_view(), name='register-user'),
    path('auth/users/', ListUsersView.as_view(), name='list-users'),
    path('auth/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('auth/login/', LoginUserView.as_view(), name='token-obtain-pair'),
    path('auth/location/', LocationView.as_view(), name='location'),
    path('auth/my-locations/', MyLocationsView.as_view(), name='user-locations'),
    path('auth/logout/', LogoutUserView.as_view(), name='logout'),
    path('auth/company/', CompanyListCreateView.as_view(), name='company-list-create'),
    path('auth/login/1/', LoginUserView.as_view(), name='login'),
    path('auth/super-admin/dashboard/', SuperAdminDashboardView.as_view(), name='super-admin-dashboard'),
    path('auth/role/', RoleListView.as_view(), name='role-list'),
    path('auth/role/<int:pk>/', RoleDetailView.as_view(), name='role-detail'),
    path('auth/permission/', PermissionListView.as_view(), name='permission-list'),
    path('auth/permission/<int:pk>/', PermissionDetailView.as_view(), name='permission-detail'),
    


    path('load/', LoadListView.as_view(), name='load-list'),
    path('load/<int:pk>/', LoadDetailView.as_view(), name='load-detail'),
    path('load/tags/', LoadTagsListView.as_view(), name='load-tags-list'),
    path('load/tags/<int:pk>/', LoadTagsDetailView.as_view(), name='load-tags-detail'),

    path('team/', TeamListView.as_view(), name='team-list'),
    path('team/<int:pk>/', TeamDetailView.as_view(), name='team-detail'),

    path('unit/', UnitListView.as_view(), name='unit-list'),
    path('unit/<int:pk>/', UnitDetailView.as_view(), name='unit-detail'),

    path('driver/', DriverListView.as_view(), name='driver-list'),
    path('driver/<int:pk>/', DriverDetailView.as_view(), name='driver-detail'),
    path('driver/tags/', DriverTagsListView.as_view(), name='driver-tags-list'),
    path('driver/tags/<int:pk>/', DriverTagsDetailView.as_view(), name='driver-tags-detail'),
    path('driver/pay/', PayListView.as_view(), name='pay-list'),
    path('driver/pay/<int:pk>/', PayDetailView.as_view(), name='pay-detail'),
    path('driver/pay/driver/', DriverPayListView.as_view(), name='driver-pay-list'),
    path('driver/pay/driver/<int:pk>/', DriverPayDetailView.as_view(), name='driver-pay-detail'),
    path('driver/pay/create/', DriverPayCreateView.as_view(), name='driver-pay-create'),
    path('driver/expense/', DriverExpenseListView.as_view(), name='driver-expense-list'),
    path('driver/expense/<int:pk>/', DriverExpenseDetailView.as_view(), name='driver-expense-detail'),

    path('truck/', TruckListView.as_view(), name='truck-list'),
    path('truck/<int:pk>/', TruckDetailView.as_view(), name='truck-detail'),
    path('truck/tags/', TruckTagsListView.as_view(), name='truck-tags-list'),
    path('truck/tags/<int:pk>/', TruckTagsDetailView.as_view(), name='truck-tags-detail'),

    path('trailer/', TrailerListView.as_view(), name='trailer-list'),
    path('trailer/<int:pk>/', TrailerDetailView.as_view(), name='trailer-detail'),
    path('trailer/tags/', TrailerTagsListView.as_view(), name='trailer-tags-list'),
    path('trailer/tags/<int:pk>/', TrailerTagsDetailView.as_view(), name='trailer-tags-detail'),

    path('dispatcher/', DispatcherListView.as_view(), name='dispatcher-list'),
    path('dispatcher/<int:pk>/', DispatcherDetailView.as_view(), name='dispatcher-detail'),
    path('dispatcher/tags/', DispatcherTagsListView.as_view(), name='dispatcher-tags-list'),
    path('dispatcher/tags/<int:pk>/', DispatcherTagsDetailView.as_view(), name='dispatcher-tags-detail'),

    path('employee/', EmployeeListView.as_view(), name='employee-list'),
    path('employee/<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('employee/tags/', EmployeeTagsListView.as_view(), name='employee-tags-list'),
    path('employee/tags/<int:pk>/', EmployeeTagsDetailView.as_view(), name='employee-tags-detail'),
    
    path('customer_broker/', CustomerBrokerListView.as_view(), name='customer-broker-list'),
    path('customer_broker/<int:pk>/', CustomerBrokerDetailView.as_view(), name='customer-broker-detail'),

    path('commodities/', CommoditiesListView.as_view(), name='commodities-list'),
    path('commodities/<int:pk>/', CommoditiesDetailView.as_view(), name='commodities-detail'),
    
    path('otherpay/', OtherPayListView.as_view(), name='other-pay-list'),
    path('otherpay/<int:pk>/', OtherPayDetailView.as_view(), name='other-pay-detail'),

    path('stops/', StopsListView.as_view(), name='stops-list'),
    path('stops/<int:pk>/', StopsDetailView.as_view(), name='stops-detail'),

    path('load/tags/', LoadTagsListView.as_view(), name='load-tags-list'),
    path('load/tags/<int:pk>/', LoadTagsDetailView.as_view(), name='load-tags-detail'),

    path('chat/', ChatList.as_view()),
    path('chat/<int:pk>/', ChatDetail.as_view()),

]
