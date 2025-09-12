from django.db import models
from django.contrib.auth.models import User
from projects.models import Project
from decimal import Decimal
from datetime import date


class Supplier(models.Model):
    """Supplier registration and grading"""
    GRADING_CHOICES = [
        ('A', 'Grade A - Excellent'),
        ('B', 'Grade B - Good'),
        ('C', 'Grade C - Average'),
        ('D', 'Grade D - Poor'),
    ]
    
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    gst_number = models.CharField(max_length=15, blank=True)
    pan_number = models.CharField(max_length=10, blank=True)
    grading = models.CharField(max_length=1, choices=GRADING_CHOICES, default='C')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_grading_display()})"


class MaterialCategory(models.Model):
    """Material categories for inventory management"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name


class Material(models.Model):
    """Material master data"""
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('ton', 'Ton'),
        ('m', 'Meter'),
        ('sqm', 'Square Meter'),
        ('cum', 'Cubic Meter'),
        ('nos', 'Numbers'),
        ('ltr', 'Liter'),
        ('box', 'Box'),
        ('bag', 'Bag'),
    ]
    
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(MaterialCategory, on_delete=models.CASCADE)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    standard_rate = models.DecimalField(max_digits=10, decimal_places=2)
    reorder_level = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    reorder_quantity = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class MaterialStock(models.Model):
    """Material stock tracking with FIFO, LIFO, FEFO support"""
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='stock')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='material_stock')
    batch_number = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    unit_rate = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField(null=True, blank=True)
    received_date = models.DateField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, blank=True)
    
    # FIFO/LIFO/FEFO tracking
    fifo_sequence = models.IntegerField(default=0)
    lifo_sequence = models.IntegerField(default=0)
    fefo_sequence = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.fifo_sequence:
            # Set FIFO sequence (oldest first)
            last_fifo = MaterialStock.objects.filter(material=self.material, project=self.project).order_by('-fifo_sequence').first()
            self.fifo_sequence = (last_fifo.fifo_sequence + 1) if last_fifo else 1
        
        if not self.lifo_sequence:
            # Set LIFO sequence (newest first)
            last_lifo = MaterialStock.objects.filter(material=self.material, project=self.project).order_by('-lifo_sequence').first()
            self.lifo_sequence = (last_lifo.lifo_sequence + 1) if last_lifo else 1
        
        if not self.fefo_sequence:
            # Set FEFO sequence (expiry date based)
            if self.expiry_date:
                last_fefo = MaterialStock.objects.filter(
                    material=self.material, 
                    project=self.project,
                    expiry_date__isnull=False
                ).order_by('expiry_date', '-fefo_sequence').first()
                self.fefo_sequence = (last_fefo.fefo_sequence + 1) if last_fefo else 1
            else:
                # No expiry date, treat as FIFO
                last_fefo = MaterialStock.objects.filter(material=self.material, project=self.project).order_by('-fefo_sequence').first()
                self.fefo_sequence = (last_fefo.fefo_sequence + 1) if last_fefo else 1
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.material.name} - Batch: {self.batch_number}"


class MaterialTransaction(models.Model):
    """Material transaction history"""
    TRANSACTION_TYPES = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('transfer', 'Transfer'),
        ('adjustment', 'Adjustment'),
    ]
    
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    unit_rate = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    reference_number = models.CharField(max_length=100, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    transaction_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)
    
    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.unit_rate
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.material.name} - {self.get_transaction_type_display()} - {self.quantity}"


class PurchaseOrder(models.Model):
    """Purchase orders for materials"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('acknowledged', 'Acknowledged'),
        ('partial', 'Partially Received'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    po_number = models.CharField(max_length=100, unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='purchase_orders')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    po_date = models.DateField()
    expected_delivery_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"PO-{self.po_number} - {self.supplier.name}"


class PurchaseOrderItem(models.Model):
    """Items in purchase order"""
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    unit_rate = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    received_quantity = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    
    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.unit_rate
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.material.name} - {self.quantity} {self.material.unit}"


class MaterialRequisition(models.Model):
    """Material requisition from site"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('fulfilled', 'Fulfilled'),
    ]
    
    req_number = models.CharField(max_length=100, unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='material_requisitions')
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='material_requisitions')
    requested_date = models.DateField()
    required_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approved_requisitions', null=True, blank=True)
    approved_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    
    def __str__(self):
        return f"REQ-{self.req_number} - {self.project.name}"


class MaterialRequisitionItem(models.Model):
    """Items in material requisition"""
    requisition = models.ForeignKey(MaterialRequisition, on_delete=models.CASCADE, related_name='items')
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    purpose = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return f"{self.material.name} - {self.quantity} {self.material.unit}"