from django import forms
from .models import (
    ChartOfAccounts, JournalEntry, JournalEntryLine, Budget, BudgetItem
)
from projects.models import Project


class ChartOfAccountsForm(forms.ModelForm):
    class Meta:
        model = ChartOfAccounts
        fields = ['account_code', 'account_name', 'account_type', 'parent_account']
        widgets = {
            'account_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account code'}),
            'account_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account name'}),
            'account_type': forms.Select(attrs={'class': 'form-select'}),
            'parent_account': forms.Select(attrs={'class': 'form-select'}),
        }


class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['entry_date', 'reference', 'description', 'project']
        widgets = {
            'entry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reference'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'project': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['project'].queryset = Project.objects.filter(created_by=user)


class JournalEntryLineForm(forms.ModelForm):
    class Meta:
        model = JournalEntryLine
        fields = ['account', 'description', 'debit_amount', 'credit_amount']
        widgets = {
            'account': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'debit_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'credit_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
        }


JournalEntryLineFormSet = forms.inlineformset_factory(
    JournalEntry, JournalEntryLine, form=JournalEntryLineForm, extra=2, can_delete=True
)


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name', 'budget_type', 'financial_year', 'project', 'total_budget', 'approved_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Budget name'}),
            'budget_type': forms.Select(attrs={'class': 'form-select'}),
            'financial_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '2024-25'}),
            'project': forms.Select(attrs={'class': 'form-select'}),
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
        fields = ['account', 'budget_amount']
        widgets = {
            'account': forms.Select(attrs={'class': 'form-select'}),
            'budget_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
        }


BudgetItemFormSet = forms.inlineformset_factory(
    Budget, BudgetItem, form=BudgetItemForm, extra=1, can_delete=True
)
