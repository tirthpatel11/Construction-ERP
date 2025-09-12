from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('chart-of-accounts/', views.chart_of_accounts, name='chart_of_accounts'),
    path('journal-entries/', views.journal_entry_list, name='journal_entry_list'),
    path('journal-entries/create/', views.journal_entry_create, name='journal_entry_create'),
    path('journal-entries/<int:entry_id>/', views.journal_entry_detail, name='journal_entry_detail'),
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/create/', views.budget_create, name='budget_create'),
    path('budgets/<int:budget_id>/', views.budget_detail, name='budget_detail'),
    path('trial-balance/', views.trial_balance, name='trial_balance'),
    path('profit-loss/', views.profit_loss, name='profit_loss'),
    path('balance-sheet/', views.balance_sheet, name='balance_sheet'),
    path('cash-flow/', views.cash_flow, name='cash_flow'),
]
