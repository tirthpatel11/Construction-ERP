from django import forms
from .models import (
    Estimation, EstimationItem, ProjectBudget, BudgetItem,
    ProjectSchedule, ScheduleActivity, CostControl
)
from projects.models import Project


class EstimationForm(forms.ModelForm):
    class Meta:
        model = Estimation
        fields = ['project', 'name', 'version', 'description']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estimation name'}),
            'version': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Version'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['project'].queryset = Project.objects.filter(created_by=user)


class EstimationItemForm(forms.ModelForm):
    class Meta:
        model = EstimationItem
        fields = ['item_code', 'description', 'unit', 'quantity', 'unit_rate', 'category']
        widgets = {
            'item_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item code'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unit'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001', 'placeholder': '0.000'}),
            'unit_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category'}),
        }


EstimationItemFormSet = forms.inlineformset_factory(
    Estimation, EstimationItem, form=EstimationItemForm, extra=1, can_delete=True
)


class BudgetForm(forms.ModelForm):
    class Meta:
        model = ProjectBudget
        fields = ['project', 'name', 'budget_type', 'total_budget', 'approved_date']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Budget name'}),
            'budget_type': forms.Select(attrs={'class': 'form-select'}),
            'total_budget': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'approved_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['project'].queryset = Project.objects.filter(created_by=user)


class BudgetItemForm(forms.ModelForm):
    class Meta:
        model = BudgetItem
        fields = ['category', 'description', 'budget_amount']
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'budget_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
        }


BudgetItemFormSet = forms.inlineformset_factory(
    ProjectBudget, BudgetItem, form=BudgetItemForm, extra=1, can_delete=True
)


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = ProjectSchedule
        fields = ['project', 'name', 'start_date', 'end_date']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Schedule name'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['project'].queryset = Project.objects.filter(created_by=user)


class CostControlForm(forms.ModelForm):
    class Meta:
        model = CostControl
        fields = ['project', 'category', 'description', 'budget_amount', 'estimate_amount', 'actual_amount']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'budget_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'estimate_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'actual_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['project'].queryset = Project.objects.filter(created_by=user)
