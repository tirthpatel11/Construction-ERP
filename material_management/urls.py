from django.urls import path
from . import views

app_name = 'material_management'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/create/', views.supplier_create, name='supplier_create'),
    path('suppliers/<int:supplier_id>/', views.supplier_detail, name='supplier_detail'),
    path('materials/', views.material_list, name='material_list'),
    path('materials/create/', views.material_create, name='material_create'),
    path('materials/<int:material_id>/', views.material_detail, name='material_detail'),
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/<int:project_id>/', views.inventory_detail, name='inventory_detail'),
    path('purchase-orders/', views.purchase_order_list, name='purchase_order_list'),
    path('purchase-orders/create/', views.purchase_order_create, name='purchase_order_create'),
    path('purchase-orders/<int:po_id>/', views.purchase_order_detail, name='purchase_order_detail'),
    path('requisitions/', views.requisition_list, name='requisition_list'),
    path('requisitions/create/', views.requisition_create, name='requisition_create'),
    path('requisitions/<int:req_id>/', views.requisition_detail, name='requisition_detail'),
]
