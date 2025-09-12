from django.urls import path
from . import views

app_name = 'engineering'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('estimations/', views.estimation_list, name='estimation_list'),
    path('estimations/create/', views.estimation_create, name='estimation_create'),
    path('estimations/<int:estimation_id>/', views.estimation_detail, name='estimation_detail'),
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/create/', views.budget_create, name='budget_create'),
    path('budgets/<int:budget_id>/', views.budget_detail, name='budget_detail'),
    path('schedules/', views.schedule_list, name='schedule_list'),
    path('schedules/create/', views.schedule_create, name='schedule_create'),
    path('schedules/<int:schedule_id>/', views.schedule_detail, name='schedule_detail'),
    path('cost-control/', views.cost_control_list, name='cost_control_list'),
    path('cost-control/<int:project_id>/', views.cost_control_detail, name='cost_control_detail'),
]
