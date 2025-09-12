from django import forms
from .models import (
    Supplier, Material, MaterialCategory, PurchaseOrder, PurchaseOrderItem,
    MaterialRequisition, MaterialRequisitionItem
)
from projects.models import Project


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            'name', 'contact_person', 'email', 'phone', 'address', 'city', 'state',
            'pincode', 'gst_number', 'pan_number', 'grading', 'rating'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Supplier name'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact person'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'}),
            'gst_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GST number'}),
            'pan_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PAN number'}),
            'grading': forms.Select(attrs={'class': 'form-select'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '5'}),
        }


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = [
            'code', 'name', 'description', 'category', 'unit', 'standard_rate',
            'reorder_level', 'reorder_quantity'
        ]
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Material code'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Material name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'standard_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001', 'placeholder': '0.000'}),
            'reorder_quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001', 'placeholder': '0.000'}),
        }


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['project', 'supplier', 'po_date', 'expected_delivery_date']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-select'}),
            'supplier': forms.Select(attrs={'class': 'form-select'}),
            'po_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expected_delivery_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['project'].queryset = Project.objects.filter(created_by=user)


class PurchaseOrderItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderItem
        fields = ['material', 'quantity', 'unit_rate']
        widgets = {
            'material': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001', 'placeholder': '0.000'}),
            'unit_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
        }


PurchaseOrderItemFormSet = forms.inlineformset_factory(
    PurchaseOrder, PurchaseOrderItem, form=PurchaseOrderItemForm, extra=1, can_delete=True
)


class MaterialRequisitionForm(forms.ModelForm):
    class Meta:
        model = MaterialRequisition
        fields = ['project', 'requested_date', 'required_date', 'remarks']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-select'}),
            'requested_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'required_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Remarks'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['project'].queryset = Project.objects.filter(created_by=user)


class MaterialRequisitionItemForm(forms.ModelForm):
    class Meta:
        model = MaterialRequisitionItem
        fields = ['material', 'quantity', 'purpose']
        widgets = {
            'material': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001', 'placeholder': '0.000'}),
            'purpose': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Purpose'}),
        }


MaterialRequisitionItemFormSet = forms.inlineformset_factory(
    MaterialRequisition, MaterialRequisitionItem, form=MaterialRequisitionItemForm, extra=1, can_delete=True
)
