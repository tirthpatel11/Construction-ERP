from django.db import models
from django.contrib.auth.models import User
from projects.models import Project
from decimal import Decimal
from datetime import date


class ChartOfAccounts(models.Model):
    """Chart of accounts for double-entry bookkeeping"""
    ACCOUNT_TYPES = [
        ('asset', 'Asset'),
        ('liability', 'Liability'),
        ('equity', 'Equity'),
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    account_code = models.CharField(max_length=20, unique=True)
    account_name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    parent_account = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['account_code']
    
    def __str__(self):
        return f"{self.account_code} - {self.account_name}"


class JournalEntry(models.Model):
    """Journal entries for double-entry bookkeeping"""
    entry_number = models.CharField(max_length=100, unique=True)
    entry_date = models.DateField()
    reference = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    total_debit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_credit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_posted = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        # Calculate totals from journal entry lines
        if self.pk:
            lines = self.journal_lines.all()
            self.total_debit = sum(line.debit_amount for line in lines)
            self.total_credit = sum(line.credit_amount for line in lines)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"JE-{self.entry_number} - {self.entry_date}"


class JournalEntryLine(models.Model):
    """Individual lines in journal entries"""
    journal_entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name='journal_lines')
    account = models.ForeignKey(ChartOfAccounts, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    debit_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    credit_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.debit_amount > 0 and self.credit_amount > 0:
            raise ValidationError("A line cannot have both debit and credit amounts")
        if self.debit_amount == 0 and self.credit_amount == 0:
            raise ValidationError("A line must have either debit or credit amount")
    
    def __str__(self):
        return f"{self.account.account_name} - Dr: {self.debit_amount}, Cr: {self.credit_amount}"


class Budget(models.Model):
    """Budget monitoring system"""
    BUDGET_TYPES = [
        ('annual', 'Annual Budget'),
        ('project', 'Project Budget'),
        ('department', 'Department Budget'),
        ('monthly', 'Monthly Budget'),
    ]
    
    name = models.CharField(max_length=255)
    budget_type = models.CharField(max_length=20, choices=BUDGET_TYPES)
    financial_year = models.CharField(max_length=10)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    total_budget = models.DecimalField(max_digits=15, decimal_places=2)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE)
    approved_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.financial_year}"


class BudgetItem(models.Model):
    """Individual budget line items"""
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='items')
    account = models.ForeignKey(ChartOfAccounts, on_delete=models.CASCADE)
    budget_amount = models.DecimalField(max_digits=15, decimal_places=2)
    actual_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    committed_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    @property
    def variance(self):
        return self.budget_amount - self.actual_amount
    
    @property
    def variance_percentage(self):
        if self.budget_amount > 0:
            return (self.variance / self.budget_amount) * 100
        return 0
    
    def __str__(self):
        return f"{self.account.account_name} - {self.budget_amount}"


class TrialBalance(models.Model):
    """Trial balance for a specific date"""
    as_on_date = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    total_debit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_credit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Trial Balance - {self.as_on_date}"


class TrialBalanceItem(models.Model):
    """Individual items in trial balance"""
    trial_balance = models.ForeignKey(TrialBalance, on_delete=models.CASCADE, related_name='items')
    account = models.ForeignKey(ChartOfAccounts, on_delete=models.CASCADE)
    debit_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    credit_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.account.account_name} - Dr: {self.debit_balance}, Cr: {self.credit_balance}"


class ProfitLossStatement(models.Model):
    """Profit & Loss statement"""
    period_start = models.DateField()
    period_end = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    total_income = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_expenses = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_profit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        self.net_profit = self.total_income - self.total_expenses
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"P&L - {self.period_start} to {self.period_end}"


class BalanceSheet(models.Model):
    """Balance sheet"""
    as_on_date = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    total_assets = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_liabilities = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_equity = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Balance Sheet - {self.as_on_date}"


class CashFlow(models.Model):
    """Cash flow statement"""
    CASH_FLOW_TYPES = [
        ('operating', 'Operating Activities'),
        ('investing', 'Investing Activities'),
        ('financing', 'Financing Activities'),
    ]
    
    period_start = models.DateField()
    period_end = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    cash_flow_type = models.CharField(max_length=20, choices=CASH_FLOW_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.CharField(max_length=500)
    
    def __str__(self):
        return f"{self.get_cash_flow_type_display()} - {self.amount}"


class Company(models.Model):
    """Company information for multi-company support"""
    name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=100, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    gst_number = models.CharField(max_length=15, blank=True)
    pan_number = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name