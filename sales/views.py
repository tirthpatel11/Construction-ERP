from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Count
from projects.models import Project
from .models import (
    Building, Wing, UnitType, SalableUnit, ParkingUnit, PriceList,
    Customer, SaleBooking, PaymentSchedule, Payment, SalesReport
)
from .forms import (
    BuildingForm, SalableUnitForm, CustomerForm, SaleBookingForm,
    PaymentScheduleFormSet, PriceListForm
)


@login_required
def dashboard(request):
    """Sales dashboard"""
    projects = Project.objects.filter(created_by=request.user)
    buildings = Building.objects.filter(project__created_by=request.user)
    units = SalableUnit.objects.filter(project__created_by=request.user)
    customers = Customer.objects.all()
    bookings = SaleBooking.objects.filter(sales_person=request.user)
    
    # Calculate totals
    total_units = units.count()
    sold_units = units.filter(status='sold').count()
    booked_units = units.filter(status='booked').count()
    available_units = units.filter(status='available').count()
    
    total_sales_value = bookings.aggregate(Sum('agreement_value'))['agreement_value__sum'] or 0
    total_collection = Payment.objects.filter(booking__sales_person=request.user, status='paid').aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'projects': projects,
        'buildings': buildings,
        'units': units,
        'customers': customers,
        'bookings': bookings,
        'total_units': total_units,
        'sold_units': sold_units,
        'booked_units': booked_units,
        'available_units': available_units,
        'total_sales_value': total_sales_value,
        'total_collection': total_collection,
    }
    
    return render(request, 'sales/dashboard.html', context)


@login_required
def building_list(request):
    """List all buildings"""
    buildings = Building.objects.filter(project__created_by=request.user).order_by('name')
    
    context = {
        'buildings': buildings,
    }
    
    return render(request, 'sales/building_list.html', context)


@login_required
def building_create(request):
    """Create new building"""
    if request.method == 'POST':
        form = BuildingForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Building created successfully!')
            return redirect('sales:building_list')
    else:
        form = BuildingForm(user=request.user)
    
    context = {
        'form': form,
    }
    
    return render(request, 'sales/building_form.html', context)


@login_required
def building_detail(request, building_id):
    """Building detail view"""
    building = get_object_or_404(Building, id=building_id, project__created_by=request.user)
    units = building.units.all()
    wings = building.wings.all()
    
    context = {
        'building': building,
        'units': units,
        'wings': wings,
    }
    
    return render(request, 'sales/building_detail.html', context)


@login_required
def unit_list(request):
    """List all salable units"""
    units = SalableUnit.objects.filter(project__created_by=request.user).order_by('building__name', 'unit_number')
    
    context = {
        'units': units,
    }
    
    return render(request, 'sales/unit_list.html', context)


@login_required
def unit_create(request):
    """Create new salable unit"""
    if request.method == 'POST':
        form = SalableUnitForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Unit created successfully!')
            return redirect('sales:unit_list')
    else:
        form = SalableUnitForm(user=request.user)
    
    context = {
        'form': form,
    }
    
    return render(request, 'sales/unit_form.html', context)


@login_required
def unit_detail(request, unit_id):
    """Unit detail view"""
    unit = get_object_or_404(SalableUnit, id=unit_id, project__created_by=request.user)
    bookings = unit.bookings.all()
    
    context = {
        'unit': unit,
        'bookings': bookings,
    }
    
    return render(request, 'sales/unit_detail.html', context)


@login_required
def customer_list(request):
    """List all customers"""
    customers = Customer.objects.all().order_by('first_name', 'last_name')
    
    context = {
        'customers': customers,
    }
    
    return render(request, 'sales/customer_list.html', context)


@login_required
def customer_create(request):
    """Create new customer"""
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer created successfully!')
            return redirect('sales:customer_list')
    else:
        form = CustomerForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'sales/customer_form.html', context)


@login_required
def customer_detail(request, customer_id):
    """Customer detail view"""
    customer = get_object_or_404(Customer, id=customer_id)
    bookings = customer.bookings.all()
    
    context = {
        'customer': customer,
        'bookings': bookings,
    }
    
    return render(request, 'sales/customer_detail.html', context)


@login_required
def booking_list(request):
    """List all sale bookings"""
    bookings = SaleBooking.objects.filter(sales_person=request.user).order_by('-created_at')
    
    context = {
        'bookings': bookings,
    }
    
    return render(request, 'sales/booking_list.html', context)


@login_required
def booking_create(request):
    """Create new sale booking"""
    if request.method == 'POST':
        form = SaleBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.sales_person = request.user
            booking.save()
            messages.success(request, 'Sale booking created successfully!')
            return redirect('sales:booking_detail', booking_id=booking.id)
    else:
        form = SaleBookingForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'sales/booking_form.html', context)


@login_required
def booking_detail(request, booking_id):
    """Sale booking detail view"""
    booking = get_object_or_404(SaleBooking, id=booking_id, sales_person=request.user)
    payment_schedule = booking.payment_schedule.all()
    payments = booking.payments.all()
    
    context = {
        'booking': booking,
        'payment_schedule': payment_schedule,
        'payments': payments,
    }
    
    return render(request, 'sales/booking_detail.html', context)


@login_required
def price_list_view(request):
    """List all price lists"""
    price_lists = PriceList.objects.filter(project__created_by=request.user).order_by('-created_at')
    
    context = {
        'price_lists': price_lists,
    }
    
    return render(request, 'sales/price_list.html', context)


@login_required
def price_list_create(request):
    """Create new price list"""
    if request.method == 'POST':
        form = PriceListForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Price list created successfully!')
            return redirect('sales:price_list')
    else:
        form = PriceListForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'sales/price_list_form.html', context)


@login_required
def sales_reports(request):
    """Sales reports and analytics"""
    projects = Project.objects.filter(created_by=request.user)
    
    context = {
        'projects': projects,
    }
    
    return render(request, 'sales/sales_reports.html', context)