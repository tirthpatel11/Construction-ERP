from django import forms
from .models import Project, Partner


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name', 'company_name', 'description', 'project_address',
            'start_date', 'end_date', 'estimated_budget', 'status'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project name'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter company name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Project description'}),
            'project_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Project address'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estimated_budget': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = [
            'name', 'date_of_birth', 'proportion', 'address',
            'phone_number', 'email'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Partner name'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'proportion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100', 'placeholder': 'Percentage (0-100)'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Partner address'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
        }


# Formset for multiple partners
PartnerFormSet = forms.inlineformset_factory(
    Project, Partner, form=PartnerForm, extra=1, can_delete=True
)