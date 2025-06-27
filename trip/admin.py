from django.contrib import admin
from .models import Booking, Package

# Register your models here.

from django.contrib import admin
from .models import VendorProfile

admin.site.register(VendorProfile)



from django.contrib import admin
from .models import Package, Booking


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'price', 'is_top', 'is_approved', 'expiry_date')
    list_filter = ('is_approved', 'is_top', 'destination')
    search_fields = ('name', 'destination')
    list_editable = ('is_approved',)
    ordering = ('-id',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('cus_name', 'package', 'booking_date', 'booked_on')
    search_fields = ('cus_name',)
