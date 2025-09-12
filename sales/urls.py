from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('buildings/', views.building_list, name='building_list'),
    path('buildings/create/', views.building_create, name='building_create'),
    path('buildings/<int:building_id>/', views.building_detail, name='building_detail'),
    path('units/', views.unit_list, name='unit_list'),
    path('units/create/', views.unit_create, name='unit_create'),
    path('units/<int:unit_id>/', views.unit_detail, name='unit_detail'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/create/', views.booking_create, name='booking_create'),
    path('bookings/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('price-lists/', views.price_list_view, name='price_list'),
    path('price-lists/create/', views.price_list_create, name='price_list_create'),
    path('reports/', views.sales_reports, name='sales_reports'),
]
