from django.contrib import admin
from apps.auth.models import User, UserLocation, Company, Role, Permission
admin.register(UserLocation)

from django.contrib import admin
from apps.auth.models import User, Company
admin.site.register(UserLocation)
admin.site.register(User)
admin.site.register(Company)

admin.site.register(Role)
admin.site.register(Permission)
