
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.db import models

from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required

from .models import Package
from .forms import PackageForm, BookingForm, VendorRegisterForm

# ================== Home & Authentication ===================

def index(request):
    return render(request, 'index.html')

def loginn(request):
    if request.method == "POST":
        username = request.POST.get('username').strip()
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in.')
            if user.is_staff:
                return redirect('all_packages')
            elif hasattr(user, 'vendorprofile'):
                return redirect('vendor_dashboard')
            else:
                return redirect('all_packages')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')

def signupp(request):
    if request.method == "POST":
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')

    return render(request, 'signup.html')

def vendor_register(request):
    if request.method == 'POST':
        form = VendorRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('vendor_login')
    else:
        form = VendorRegisterForm()
    return render(request, 'register.html', {'form': form})

def vendor_login(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(request, username=uname, password=pwd)
        if user:
            login(request, user)
            return redirect('vendor_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'vendor_login.html')







# ================== Package Views ===================

def all_packages(request):
    today = timezone.now().date()
    packages = Package.objects.filter(
        is_approved=True
    ).filter(
        Q(expiry_date__isnull=True) | Q(expiry_date__gt=today)
    )
    return render(request, 'destination.html', {'pack': packages, 'title': 'All Packages'})

def top_packages(request):
    today = timezone.now().date()
    packages = Package.objects.filter(
        is_approved=True, is_top=True
    ).filter(
        Q(expiry_date__isnull=True) | Q(expiry_date__gt=today)
    )
    return render(request, 'destination.html', {'pack': packages, 'title': 'Top Packages'})

def budget_packages(request):
    today = timezone.now().date()
    packages = Package.objects.filter(
        is_approved=True, price__lte=5000
    ).filter(
        Q(expiry_date__isnull=True) | Q(expiry_date__gt=today)
    )
    return render(request, 'destination.html', {'pack': packages, 'title': 'Budget-Friendly Packages'})

def packages_by_destination(request, destination):
    today = timezone.now().date()
    packages = Package.objects.filter(
        is_approved=True, destination__iexact=destination
    ).filter(
        Q(expiry_date__isnull=True) | Q(expiry_date__gt=today)
    )
    return render(request, 'destination.html', {'pack': packages, 'title': f'{destination} Packages'})

def create_package(request):


    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES)
        if form.is_valid():
            package = form.save(commit=False)
            package.vendor = request.user
            package.save()
            return redirect('vendor_dashboard')
    else:
        form = PackageForm()
    return render(request, 'create_package.html', {'form': form})



def delete_package(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    if package.vendor == request.user:
        package.delete()
        messages.success(request, "Package deleted.")
    else:
        messages.error(request, "Not authorized to delete this package.")

    return redirect('vendor_dashboard')


from django.contrib.auth.decorators import login_required

@login_required
def edit_package(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    # Ensure the logged-in user is the owner
    if package.vendor != request.user:
        messages.error(request, "You are not allowed to edit this package.")
        return redirect('vendor_dashboard')

    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            form.save()
            messages.success(request, "Package updated successfully.")
            return redirect('vendor_dashboard')
    else:
        form = PackageForm(instance=package)

    return render(request, 'edit_package.html', {'form': form})





from django.contrib.auth.decorators import login_required
from .models import Booking

@login_required
def vendor_bookings(request):
    vendor = request.user
    bookings = Booking.objects.filter(package__vendor=vendor)

    return render(request, 'vendor_bookings.html', {'bookings': bookings})

# ================== Booking ===================

def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking successful!")
            return redirect('pay')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = BookingForm()
    return render(request, 'booking.html', {'form': form})

def pay(request):
    return render(request,'pay.html')

# ================== Admin Dashboard ===================

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('own')
        else:
            messages.error(request, 'Invalid admin credentials.')

    return render(request, 'admin_login.html')


@staff_member_required
@staff_member_required
def own(request):
    today = timezone.now().date()

    total_users = User.objects.count()
    total_packages = Package.objects.count()
    total_bookings = Booking.objects.count()
    active_packages = Package.objects.active().count()
    expired_packages = Package.objects.filter(expiry_date__lt=today).count()
    pending_packages = Package.objects.filter(is_approved=False).count()

    context = {
        'total_users': total_users,
        'total_packages': total_packages,
        'total_bookings': total_bookings,
        'active_packages': active_packages,
        'expired_packages': expired_packages,
        'pending_packages': pending_packages,
        'admin_username': request.user.username,
        'admin_email': request.user.email,
        'my_packages':packages_by_destination ,
    }

    return render(request, 'own.html', context)


# ================== Vendor Dashboard ===================

def vendor_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    today = timezone.now().date()
    vendor = request.user

    vendor_packages = Package.objects.filter(vendor=vendor)

    total_packages = vendor_packages.count()
    approved_packages = vendor_packages.filter(is_approved=True).count()
    pending_packages = vendor_packages.filter(is_approved=False).count()
    expired_packages = vendor_packages.filter(expiry_date__lt=today).count()
    total_bookings = Booking.objects.filter(package__vendor=vendor).count()

    context = {
        'total_packages': total_packages,
        'approved_packages': approved_packages,
        'pending_packages': pending_packages,
        'expired_packages': expired_packages,
        'total_bookings': total_bookings,
        'my_packages': vendor_packages  # 🟢 This is what powers the table
    }
    return render(request, 'dashboard.html', context)

# ================== Package Manager ===================

class PackageManager(models.Manager):
    def active(self):
        today = timezone.now().date()
        return self.get_queryset().filter(
            is_approved=True
        ).filter(
            Q(expiry_date__isnull=True) | Q(expiry_date__gt=today)

        )










