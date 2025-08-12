from django import forms
from .models import Package, Booking

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        # Explicitly list the fields you want to include
        fields = ['img', 'name', 'desc', 'price', 'destination', 'is_top', 'expiry_date']  # removed 'is_approved' and 'vendor'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
            'img': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_top': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'name': "Package Name",
            'desc': "Description",
            'destination': "Destination",
            'img': "Image",
            'is_top': "Top Package?",
        }



class BookingForm(forms.ModelForm):
    booking_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Travel Date"
    )

    class Meta:
        model = Booking
        fields = '__all__'
        widgets = {
            'cus_name': forms.TextInput(attrs={'class': 'form-control'}),
            'cus_ph': forms.TextInput(attrs={'class': 'form-control'}),
            'package': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'cus_name': "Customer Name",
            'cus_ph': "Customer Phone",
            'package': "Package",
        }








from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import VendorProfile


class VendorRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20)
    company_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit)
        phone = self.cleaned_data.get('phone')
        company = self.cleaned_data.get('company_name')
        VendorProfile.objects.create(user=user, phone=phone, company_name=company)
        return user













