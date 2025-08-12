from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User




class PackageManager(models.Manager):
    def active(self):
        today = timezone.now().date()
        return self.get_queryset().filter(
            is_approved=True
        ).filter(
            Q(expiry_date__isnull=True) | Q(expiry_date__gt=today)
        )


class Package(models.Model):
    img = models.ImageField(upload_to='pic/')
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trip_packages')
    name = models.CharField(max_length=255)
    desc = models.TextField()
    price = models.PositiveIntegerField()
    destination = models.CharField(max_length=100)
    is_top = models.BooleanField(default=False)
    expiry_date = models.DateField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)


    objects = PackageManager()

    def __str__(self):
        return self.name


class Booking(models.Model):
    cus_name = models.CharField(max_length=55)
    cus_ph = models.CharField(max_length=10)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booked_on = models.DateField(auto_now=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cus_name} - {self.package.name}"






class VendorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    # Add other vendor-specific fields here

    def __str__(self):
        return self.user.username



