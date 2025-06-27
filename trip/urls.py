
from django.urls import path
from.import views

urlpatterns=[
 path('',views.index,name="index"),

path('login',views.loginn,name="login"),
path('signup',views.signupp,name="signup"),
path('signup/', views.vendor_register, name='vendor_register'),
path('login/', views.vendor_login, name='vendor_login'),
path('admin_login/', views.admin_login, name='admin_login'),




path('packages/', views.all_packages, name='all_packages'),
path('packages/top/', views.top_packages, name='top_packages'),
path('packages/budget/', views.budget_packages, name='budget_packages'),
path('packages/destination/<str:destination>/', views.packages_by_destination, name='packages_by_destination'),



path('create_package/', views.create_package, name='create_package'),
path('delete-package/<int:package_id>/', views.delete_package, name='delete_package'),
path('edit-package/<int:package_id>/', views.edit_package, name='edit_package'),
path('vendor/bookings/', views.vendor_bookings, name='vendor_bookings'),


path('vendor_dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
path('own/', views.own, name='own'),




path('booking/', views.booking, name='booking'),
path('pay/', views.pay, name='pay'),


]









