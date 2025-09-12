from django.contrib import admin
from .models import (
    Building, Wing, UnitType, SalableUnit, ParkingUnit, PriceList,
    Customer, SaleBooking, PaymentSchedule, Payment, SalesReport
)


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'total_floors', 'total_units', 'is_active']
    list_filter = ['is_active', 'project']
    search_fields = ['name', 'project__name']
    readonly_fields = ['created_at']


@admin.register(Wing)
class WingAdmin(admin.ModelAdmin):
    list_display = ['name', 'building', 'total_units', 'is_active']
    list_filter = ['is_active', 'building__project']
    search_fields = ['name', 'building__name']


@admin.register(UnitType)
class UnitTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'bedrooms', 'bathrooms', 'carpet_area', 'built_up_area', 'super_built_up_area']
    search_fields = ['name']


@admin.register(SalableUnit)
class SalableUnitAdmin(admin.ModelAdmin):
    list_display = ['unit_number', 'building', 'unit_type', 'floor_number', 'current_price', 'status']
    list_filter = ['status', 'unit_type', 'building__project']
    search_fields = ['unit_number', 'building__name']
    readonly_fields = ['created_at']


@admin.register(ParkingUnit)
class ParkingUnitAdmin(admin.ModelAdmin):
    list_display = ['parking_number', 'building', 'parking_type', 'area', 'current_price', 'status']
    list_filter = ['parking_type', 'status', 'building__project']
    search_fields = ['parking_number', 'building__name']
    readonly_fields = ['created_at']


@admin.register(PriceList)
class PriceListAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'unit_type', 'base_price', 'price_per_sqft', 'valid_from', 'is_active']
    list_filter = ['is_active', 'valid_from', 'project']
    search_fields = ['name', 'project__name']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_id', 'full_name', 'customer_type', 'email', 'phone', 'city']
    list_filter = ['customer_type', 'city', 'state']
    search_fields = ['customer_id', 'first_name', 'last_name', 'company_name', 'email']
    readonly_fields = ['created_at', 'updated_at']


class PaymentScheduleInline(admin.TabularInline):
    model = PaymentSchedule
    extra = 1


@admin.register(SaleBooking)
class SaleBookingAdmin(admin.ModelAdmin):
    list_display = ['booking_number', 'customer', 'unit', 'booking_date', 'agreement_value', 'status']
    list_filter = ['status', 'booking_date', 'unit__building__project']
    search_fields = ['booking_number', 'customer__full_name']
    inlines = [PaymentScheduleInline]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PaymentSchedule)
class PaymentScheduleAdmin(admin.ModelAdmin):
    list_display = ['booking', 'payment_type', 'description', 'due_date', 'amount', 'is_paid']
    list_filter = ['payment_type', 'is_paid', 'due_date']
    search_fields = ['booking__booking_number', 'description']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['booking', 'payment_schedule', 'payment_date', 'amount', 'payment_method', 'status']
    list_filter = ['payment_method', 'status', 'payment_date']
    search_fields = ['booking__booking_number', 'reference_number']
    readonly_fields = ['created_at']


@admin.register(SalesReport)
class SalesReportAdmin(admin.ModelAdmin):
    list_display = ['report_date', 'project', 'total_units', 'sold_units', 'total_sales_value', 'total_collection']
    list_filter = ['report_date', 'project']
    search_fields = ['project__name']