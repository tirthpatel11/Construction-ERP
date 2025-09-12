from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum
from projects.models import Project
from .models import (
    ChartOfAccounts, JournalEntry, JournalEntryLine, Budget, BudgetItem,
    TrialBalance, TrialBalanceItem, ProfitLossStatement, BalanceSheet, CashFlow
)
from .forms import (
    ChartOfAccountsForm, JournalEntryForm, JournalEntryLineFormSet,
    BudgetForm, BudgetItemFormSet
)


@login_required
def dashboard(request):
    """Accounts dashboard"""
    projects = Project.objects.filter(created_by=request.user)
    recent_entries = JournalEntry.objects.filter(created_by=request.user).order_by('-created_at')[:5]
    budgets = Budget.objects.filter(approved_by=request.user)
    
    # Calculate totals
    total_debit = JournalEntry.objects.filter(created_by=request.user).aggregate(Sum('total_debit'))['total_debit__sum'] or 0
    total_credit = JournalEntry.objects.filter(created_by=request.user).aggregate(Sum('total_credit'))['total_credit__sum'] or 0
    
    context = {
        'projects': projects,
        'recent_entries': recent_entries,
        'budgets': budgets,
        'total_debit': total_debit,
        'total_credit': total_credit,
    }
    
    return render(request, 'accounts/dashboard.html', context)


@login_required
def chart_of_accounts(request):
    """Chart of accounts view"""
    accounts = ChartOfAccounts.objects.filter(is_active=True).order_by('account_code')
    
    context = {
        'accounts': accounts,
    }
    
    return render(request, 'accounts/chart_of_accounts.html', context)


@login_required
def journal_entry_list(request):
    """List all journal entries"""
    entries = JournalEntry.objects.filter(created_by=request.user).order_by('-created_at')
    
    context = {
        'entries': entries,
    }
    
    return render(request, 'accounts/journal_entry_list.html', context)


@login_required
def journal_entry_create(request):
    """Create new journal entry"""
    if request.method == 'POST':
        form = JournalEntryForm(request.POST, user=request.user)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.created_by = request.user
            entry.save()
            messages.success(request, 'Journal entry created successfully!')
            return redirect('accounts:journal_entry_detail', entry_id=entry.id)
    else:
        form = JournalEntryForm(user=request.user)
    
    context = {
        'form': form,
    }
    
    return render(request, 'accounts/journal_entry_form.html', context)


@login_required
def journal_entry_detail(request, entry_id):
    """Journal entry detail view"""
    entry = get_object_or_404(JournalEntry, id=entry_id, created_by=request.user)
    lines = entry.journal_lines.all()
    
    context = {
        'entry': entry,
        'lines': lines,
    }
    
    return render(request, 'accounts/journal_entry_detail.html', context)


@login_required
def budget_list(request):
    """List all budgets"""
    budgets = Budget.objects.filter(approved_by=request.user).order_by('-created_at')
    
    context = {
        'budgets': budgets,
    }
    
    return render(request, 'accounts/budget_list.html', context)


@login_required
def budget_create(request):
    """Create new budget"""
    if request.method == 'POST':
        form = BudgetForm(request.POST, user=request.user)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.approved_by = request.user
            budget.save()
            messages.success(request, 'Budget created successfully!')
            return redirect('accounts:budget_detail', budget_id=budget.id)
    else:
        form = BudgetForm(user=request.user)
    
    context = {
        'form': form,
    }
    
    return render(request, 'accounts/budget_form.html', context)


@login_required
def budget_detail(request, budget_id):
    """Budget detail view"""
    budget = get_object_or_404(Budget, id=budget_id, approved_by=request.user)
    items = budget.items.all()
    
    context = {
        'budget': budget,
        'items': items,
    }
    
    return render(request, 'accounts/budget_detail.html', context)


@login_required
def trial_balance(request):
    """Trial balance view"""
    # This would typically generate trial balance from journal entries
    # For now, showing a placeholder
    accounts = ChartOfAccounts.objects.filter(is_active=True)
    
    context = {
        'accounts': accounts,
    }
    
    return render(request, 'accounts/trial_balance.html', context)


@login_required
def profit_loss(request):
    """Profit & Loss statement view"""
    # This would typically generate P&L from journal entries
    # For now, showing a placeholder
    context = {}
    
    return render(request, 'accounts/profit_loss.html', context)


@login_required
def balance_sheet(request):
    """Balance sheet view"""
    # This would typically generate balance sheet from journal entries
    # For now, showing a placeholder
    context = {}
    
    return render(request, 'accounts/balance_sheet.html', context)


@login_required
def cash_flow(request):
    """Cash flow statement view"""
    # This would typically generate cash flow from journal entries
    # For now, showing a placeholder
    context = {}
    
    return render(request, 'accounts/cash_flow.html', context)