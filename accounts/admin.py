from django.contrib import admin
from .models import (
    ChartOfAccounts, JournalEntry, JournalEntryLine, Budget, BudgetItem,
    TrialBalance, TrialBalanceItem, ProfitLossStatement, BalanceSheet,
    CashFlow, Company
)


@admin.register(ChartOfAccounts)
class ChartOfAccountsAdmin(admin.ModelAdmin):
    list_display = ['account_code', 'account_name', 'account_type', 'parent_account', 'is_active']
    list_filter = ['account_type', 'is_active']
    search_fields = ['account_code', 'account_name']
    readonly_fields = ['created_at']


class JournalEntryLineInline(admin.TabularInline):
    model = JournalEntryLine
    extra = 2


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ['entry_number', 'entry_date', 'description', 'total_debit', 'total_credit', 'is_posted']
    list_filter = ['entry_date', 'is_posted', 'project']
    search_fields = ['entry_number', 'description']
    inlines = [JournalEntryLineInline]
    readonly_fields = ['created_at']


@admin.register(JournalEntryLine)
class JournalEntryLineAdmin(admin.ModelAdmin):
    list_display = ['journal_entry', 'account', 'description', 'debit_amount', 'credit_amount']
    list_filter = ['account__account_type']


class BudgetItemInline(admin.TabularInline):
    model = BudgetItem
    extra = 1


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['name', 'budget_type', 'financial_year', 'project', 'total_budget', 'approved_by']
    list_filter = ['budget_type', 'financial_year', 'project']
    search_fields = ['name']
    inlines = [BudgetItemInline]
    readonly_fields = ['created_at']


@admin.register(BudgetItem)
class BudgetItemAdmin(admin.ModelAdmin):
    list_display = ['budget', 'account', 'budget_amount', 'actual_amount', 'variance', 'variance_percentage']
    list_filter = ['account__account_type']


class TrialBalanceItemInline(admin.TabularInline):
    model = TrialBalanceItem
    extra = 1


@admin.register(TrialBalance)
class TrialBalanceAdmin(admin.ModelAdmin):
    list_display = ['as_on_date', 'project', 'total_debit', 'total_credit']
    list_filter = ['as_on_date', 'project']
    inlines = [TrialBalanceItemInline]
    readonly_fields = ['created_at']


@admin.register(TrialBalanceItem)
class TrialBalanceItemAdmin(admin.ModelAdmin):
    list_display = ['trial_balance', 'account', 'debit_balance', 'credit_balance']
    list_filter = ['account__account_type']


@admin.register(ProfitLossStatement)
class ProfitLossStatementAdmin(admin.ModelAdmin):
    list_display = ['period_start', 'period_end', 'project', 'total_income', 'total_expenses', 'net_profit']
    list_filter = ['period_start', 'period_end', 'project']
    readonly_fields = ['created_at']


@admin.register(BalanceSheet)
class BalanceSheetAdmin(admin.ModelAdmin):
    list_display = ['as_on_date', 'project', 'total_assets', 'total_liabilities', 'total_equity']
    list_filter = ['as_on_date', 'project']
    readonly_fields = ['created_at']


@admin.register(CashFlow)
class CashFlowAdmin(admin.ModelAdmin):
    list_display = ['period_start', 'period_end', 'project', 'cash_flow_type', 'amount', 'description']
    list_filter = ['cash_flow_type', 'period_start', 'project']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'registration_number', 'city', 'state', 'is_active']
    list_filter = ['is_active', 'state']
    search_fields = ['name', 'registration_number']
    readonly_fields = ['created_at']