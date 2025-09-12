from django.contrib import admin
from .models import Project, Partner, ProjectExpense, ProjectPayment, ProjectTimeline

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'company_name', 'status', 'completion_percentage', 'estimated_budget', 'actual_cost', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'company_name']

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'proportion', 'phone_number', 'email']
    list_filter = ['project']
    search_fields = ['name', 'project__name']

@admin.register(ProjectExpense)
class ProjectExpenseAdmin(admin.ModelAdmin):
    list_display = ['project', 'category', 'description', 'amount', 'date']
    list_filter = ['category', 'date', 'project']
    search_fields = ['description', 'project__name']

@admin.register(ProjectPayment)
class ProjectPaymentAdmin(admin.ModelAdmin):
    list_display = ['project', 'description', 'amount', 'due_date', 'status']
    list_filter = ['status', 'due_date', 'project']
    search_fields = ['description', 'project__name']

@admin.register(ProjectTimeline)
class ProjectTimelineAdmin(admin.ModelAdmin):
    list_display = ['project', 'title', 'date', 'is_milestone', 'is_completed']
    list_filter = ['is_milestone', 'is_completed', 'date', 'project']
    search_fields = ['title', 'project__name']