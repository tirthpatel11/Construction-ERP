from django.contrib import admin
from .models import (
    Estimation, EstimationItem, ProjectBudget, BudgetItem,
    ProjectSchedule, ScheduleActivity, CostControl
)


@admin.register(Estimation)
class EstimationAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'version', 'total_estimated_cost', 'created_by', 'created_at']
    list_filter = ['created_at', 'is_active']
    search_fields = ['name', 'project__name']
    readonly_fields = ['created_at', 'updated_at']


class EstimationItemInline(admin.TabularInline):
    model = EstimationItem
    extra = 1


@admin.register(EstimationItem)
class EstimationItemAdmin(admin.ModelAdmin):
    list_display = ['item_code', 'description', 'quantity', 'unit_rate', 'total_amount', 'estimation']
    list_filter = ['category']
    search_fields = ['item_code', 'description']


@admin.register(ProjectBudget)
class ProjectBudgetAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'budget_type', 'total_budget', 'approved_by', 'approved_date']
    list_filter = ['budget_type', 'approved_date']
    search_fields = ['name', 'project__name']


class BudgetItemInline(admin.TabularInline):
    model = BudgetItem
    extra = 1


@admin.register(BudgetItem)
class BudgetItemAdmin(admin.ModelAdmin):
    list_display = ['category', 'description', 'budget_amount', 'actual_spent', 'variance', 'budget']
    list_filter = ['category']


@admin.register(ProjectSchedule)
class ProjectScheduleAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'start_date', 'end_date', 'created_by']
    list_filter = ['start_date', 'end_date']
    search_fields = ['name', 'project__name']


@admin.register(ScheduleActivity)
class ScheduleActivityAdmin(admin.ModelAdmin):
    list_display = ['activity_code', 'description', 'planned_start', 'planned_end', 'completion_percentage', 'is_critical']
    list_filter = ['is_critical', 'is_milestone', 'completion_percentage']
    search_fields = ['activity_code', 'description']


@admin.register(CostControl)
class CostControlAdmin(admin.ModelAdmin):
    list_display = ['project', 'category', 'budget_amount', 'estimate_amount', 'actual_amount', 'budget_vs_actual_variance']
    list_filter = ['category']
    search_fields = ['project__name', 'category']