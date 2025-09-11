from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Project, Partner, ProjectExpense, ProjectPayment, ProjectTimeline
from .forms import ProjectForm, PartnerFormSet
from django.db import transaction


@login_required
def create_project(request):
    """Create a new project with partners"""
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        
        if project_form.is_valid():
            try:
                with transaction.atomic():
                    project = project_form.save(commit=False)
                    project.created_by = request.user
                    project.save()
                    
                    partner_formset = PartnerFormSet(request.POST, instance=project)
                    if partner_formset.is_valid():
                        partner_formset.save()
                        messages.success(request, 'Project created successfully!')
                        return redirect('projects:detail', project_id=project.id)
                    else:
                        messages.error(request, 'Please correct the partner information.')
            except Exception as e:
                messages.error(request, f'Error creating project: {str(e)}')
    else:
        project_form = ProjectForm()
        partner_formset = PartnerFormSet()
    
    context = {
        'project_form': project_form,
        'partner_formset': partner_formset,
    }
    
    return render(request, 'projects/create.html', context)


@login_required
def project_list(request):
    """List all user projects"""
    projects = Project.objects.filter(created_by=request.user).order_by('-created_at')
    
    context = {
        'projects': projects,
    }
    
    return render(request, 'projects/list.html', context)


@login_required
def project_detail(request, project_id):
    """Project detail view with analytics"""
    project = get_object_or_404(Project, id=project_id, created_by=request.user)
    
    # Get project analytics
    expenses = ProjectExpense.objects.filter(project=project)
    payments = ProjectPayment.objects.filter(project=project)
    timeline_events = ProjectTimeline.objects.filter(project=project)
    
    # Calculate metrics
    total_expenses = sum(expense.amount for expense in expenses)
    total_payments = sum(payment.amount for payment in payments if payment.status == 'completed')
    pending_payments = payments.filter(status='pending')
    
    # Update actual cost
    project.actual_cost = total_expenses
    project.save()
    
    context = {
        'project': project,
        'partners': project.partners.all(),
        'expenses': expenses,
        'payments': payments,
        'timeline_events': timeline_events,
        'total_expenses': total_expenses,
        'total_payments': total_payments,
        'pending_payments': pending_payments,
        'profit_margin': project.profit_margin,
    }
    
    return render(request, 'projects/detail.html', context)


@login_required
def project_analytics(request, project_id):
    """API endpoint for project-specific analytics"""
    project = get_object_or_404(Project, id=project_id, created_by=request.user)
    
    # Expense breakdown by category
    expenses = ProjectExpense.objects.filter(project=project)
    expense_breakdown = {}
    for expense in expenses:
        category = expense.get_category_display()
        expense_breakdown[category] = expense_breakdown.get(category, 0) + float(expense.amount)
    
    # Timeline data
    timeline_data = []
    for event in project.timeline_events.all():
        timeline_data.append({
            'title': event.title,
            'date': event.date.isoformat(),
            'is_milestone': event.is_milestone,
            'is_completed': event.is_completed,
        })
    
    return JsonResponse({
        'expense_breakdown': expense_breakdown,
        'timeline_data': timeline_data,
        'completion_percentage': project.completion_percentage,
        'budget_utilization': float(project.actual_cost / project.estimated_budget * 100) if project.estimated_budget > 0 else 0,
    })