from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from projects.models import Project
from .models import (
    Supplier, Material, MaterialStock, MaterialTransaction,
    PurchaseOrder, MaterialRequisition
)
from .forms import (
    SupplierForm, MaterialForm, PurchaseOrderForm, PurchaseOrderItemFormSet,
    MaterialRequisitionForm, MaterialRequisitionItemFormSet
)


@login_required
def dashboard(request):
    """Material Management dashboard"""
    projects = Project.objects.filter(created_by=request.user)
    suppliers = Supplier.objects.filter(is_active=True)
    materials = Material.objects.filter(is_active=True)
    purchase_orders = PurchaseOrder.objects.filter(project__created_by=request.user)
    requisitions = MaterialRequisition.objects.filter(project__created_by=request.user)
    
    context = {
        'projects': projects,
        'suppliers': suppliers,
        'materials': materials,
        'purchase_orders': purchase_orders,
        'requisitions': requisitions,
    }
    
    return render(request, 'material_management/dashboard.html', context)


@login_required
def supplier_list(request):
    """List all suppliers"""
    suppliers = Supplier.objects.all().order_by('name')
    
    context = {
        'suppliers': suppliers,
    }
    
    return render(request, 'material_management/supplier_list.html', context)


@login_required
def supplier_create(request):
    """Create new supplier"""
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier created successfully!')
            return redirect('material_management:supplier_list')
    else:
        form = SupplierForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'material_management/supplier_form.html', context)


@login_required
def supplier_detail(request, supplier_id):
    """Supplier detail view"""
    supplier = get_object_or_404(Supplier, id=supplier_id)
    purchase_orders = PurchaseOrder.objects.filter(supplier=supplier)
    
    context = {
        'supplier': supplier,
        'purchase_orders': purchase_orders,
    }
    
    return render(request, 'material_management/supplier_detail.html', context)


@login_required
def material_list(request):
    """List all materials"""
    materials = Material.objects.all().order_by('name')
    
    context = {
        'materials': materials,
    }
    
    return render(request, 'material_management/material_list.html', context)


@login_required
def material_create(request):
    """Create new material"""
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Material created successfully!')
            return redirect('material_management:material_list')
    else:
        form = MaterialForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'material_management/material_form.html', context)


@login_required
def material_detail(request, material_id):
    """Material detail view"""
    material = get_object_or_404(Material, id=material_id)
    stock = MaterialStock.objects.filter(material=material)
    transactions = MaterialTransaction.objects.filter(material=material)
    
    context = {
        'material': material,
        'stock': stock,
        'transactions': transactions,
    }
    
    return render(request, 'material_management/material_detail.html', context)


@login_required
def inventory_list(request):
    """List inventory for all projects"""
    projects = Project.objects.filter(created_by=request.user)
    
    context = {
        'projects': projects,
    }
    
    return render(request, 'material_management/inventory_list.html', context)


@login_required
def inventory_detail(request, project_id):
    """Inventory detail for a project"""
    project = get_object_or_404(Project, id=project_id, created_by=request.user)
    stock = MaterialStock.objects.filter(project=project)
    
    context = {
        'project': project,
        'stock': stock,
    }
    
    return render(request, 'material_management/inventory_detail.html', context)


@login_required
def purchase_order_list(request):
    """List all purchase orders"""
    purchase_orders = PurchaseOrder.objects.filter(project__created_by=request.user).order_by('-created_at')
    
    context = {
        'purchase_orders': purchase_orders,
    }
    
    return render(request, 'material_management/purchase_order_list.html', context)


@login_required
def purchase_order_create(request):
    """Create new purchase order"""
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST, user=request.user)
        if form.is_valid():
            po = form.save(commit=False)
            po.created_by = request.user
            po.save()
            messages.success(request, 'Purchase order created successfully!')
            return redirect('material_management:purchase_order_detail', po_id=po.id)
    else:
        form = PurchaseOrderForm(user=request.user)
    
    context = {
        'form': form,
    }
    
    return render(request, 'material_management/purchase_order_form.html', context)


@login_required
def purchase_order_detail(request, po_id):
    """Purchase order detail view"""
    po = get_object_or_404(PurchaseOrder, id=po_id, project__created_by=request.user)
    items = po.items.all()
    
    context = {
        'purchase_order': po,
        'items': items,
    }
    
    return render(request, 'material_management/purchase_order_detail.html', context)


@login_required
def requisition_list(request):
    """List all material requisitions"""
    requisitions = MaterialRequisition.objects.filter(project__created_by=request.user).order_by('-requested_date')
    
    context = {
        'requisitions': requisitions,
    }
    
    return render(request, 'material_management/requisition_list.html', context)


@login_required
def requisition_create(request):
    """Create new material requisition"""
    if request.method == 'POST':
        form = MaterialRequisitionForm(request.POST, user=request.user)
        if form.is_valid():
            req = form.save(commit=False)
            req.requested_by = request.user
            req.save()
            messages.success(request, 'Material requisition created successfully!')
            return redirect('material_management:requisition_detail', req_id=req.id)
    else:
        form = MaterialRequisitionForm(user=request.user)
    
    context = {
        'form': form,
    }
    
    return render(request, 'material_management/requisition_form.html', context)


@login_required
def requisition_detail(request, req_id):
    """Material requisition detail view"""
    req = get_object_or_404(MaterialRequisition, id=req_id, project__created_by=request.user)
    items = req.items.all()
    
    context = {
        'requisition': req,
        'items': items,
    }
    
    return render(request, 'material_management/requisition_detail.html', context)