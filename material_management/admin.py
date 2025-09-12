from django.contrib import admin
from .models import (
    Supplier, MaterialCategory, Material, MaterialStock, MaterialTransaction,
    PurchaseOrder, PurchaseOrderItem, MaterialRequisition, MaterialRequisitionItem
)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'email', 'phone', 'grading', 'rating', 'is_active']
    list_filter = ['grading', 'is_active', 'created_at']
    search_fields = ['name', 'contact_person', 'email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(MaterialCategory)
class MaterialCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_category']
    list_filter = ['parent_category']
    search_fields = ['name']


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'category', 'unit', 'standard_rate', 'reorder_level', 'is_active']
    list_filter = ['category', 'unit', 'is_active']
    search_fields = ['code', 'name']


@admin.register(MaterialStock)
class MaterialStockAdmin(admin.ModelAdmin):
    list_display = ['material', 'project', 'batch_number', 'quantity', 'unit_rate', 'received_date', 'supplier']
    list_filter = ['received_date', 'supplier', 'project']
    search_fields = ['material__name', 'batch_number']


@admin.register(MaterialTransaction)
class MaterialTransactionAdmin(admin.ModelAdmin):
    list_display = ['material', 'project', 'transaction_type', 'quantity', 'unit_rate', 'total_amount', 'transaction_date']
    list_filter = ['transaction_type', 'transaction_date', 'project']
    search_fields = ['material__name', 'reference_number']
    readonly_fields = ['created_at']


class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 1


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['po_number', 'project', 'supplier', 'po_date', 'status', 'total_amount']
    list_filter = ['status', 'po_date', 'project']
    search_fields = ['po_number', 'supplier__name']
    inlines = [PurchaseOrderItemInline]
    readonly_fields = ['created_at']


@admin.register(PurchaseOrderItem)
class PurchaseOrderItemAdmin(admin.ModelAdmin):
    list_display = ['purchase_order', 'material', 'quantity', 'unit_rate', 'total_amount', 'received_quantity']
    list_filter = ['purchase_order__status']


class MaterialRequisitionItemInline(admin.TabularInline):
    model = MaterialRequisitionItem
    extra = 1


@admin.register(MaterialRequisition)
class MaterialRequisitionAdmin(admin.ModelAdmin):
    list_display = ['req_number', 'project', 'requested_by', 'requested_date', 'status']
    list_filter = ['status', 'requested_date', 'project']
    search_fields = ['req_number', 'project__name']
    inlines = [MaterialRequisitionItemInline]


@admin.register(MaterialRequisitionItem)
class MaterialRequisitionItemAdmin(admin.ModelAdmin):
    list_display = ['requisition', 'material', 'quantity', 'purpose']
    list_filter = ['requisition__status']