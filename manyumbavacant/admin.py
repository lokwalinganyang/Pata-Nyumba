from django.contrib import admin
from .models import Landlord, Property, Report, Advertiser, Advertisement

admin.site.register(Landlord)
admin.site.register(Advertiser)
admin.site.register(Advertisement)
admin.site.register(Property)
admin.site.register(Report)
