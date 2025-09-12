from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from projects.models import Project
from .models import (
    Estimation, EstimationItem, ProjectBudget, BudgetItem,
    ProjectSchedule, ScheduleActivity, CostControl
)
from .forms import EstimationForm, EstimationItemFormSet, BudgetForm, BudgetItemFormSet, ScheduleForm, CostControlForm


@login_required
def dashboard(request):
    """Engineering dashboard"""
    projects = Project.objects.filter(created_by=request.user)
    estimations = Estimation.objects.filter(project__created_by=request.user, is_active=True)
    budgets = ProjectBudget.objects.filter(project__created_by=request.user)
    schedules = ProjectSchedule.objects.filter(project__created_by=request.user)
    
    context = {
        'projects': projects,
        'estimations': estimations,
        'budgets': budgets,
        'schedules': schedules,
    }
    
    return render(request, 'engineering/dashboard.html', context)


@login_required
def estimation_list(request):
    """List all estimations"""
    estimations = Estimation.objects.filter(project__created_by=request.user).order_by('-created_at')
    
    context = {
        'estimations': estimations,
    }
    
    return render(request, 'engineering/estimation_list.html', context)


@login_required
def estimation_create(request):
    """Create new estimation"""
    if request.method == 'POST':
        form = EstimationForm(request.POST, user=request.user)
        if form.is_valid():
            estimation = form.save(commit=False)
            estimation.created_by = request.user
            estimation.save()
            messages.success(request, 'Estimation created successfully!')
            return redirect('engineering:estimation_detail', estimation_id=estimation.id)
    else:
        form = EstimationForm(user=request.user)
    
    context = {
        'form': form,
    }
    
    return render(request, 'engineering/estimation_form.html', context)


@login_required
def estimation_detail(request, estimation_id):
    """Estimation detail view"""
    estimation = get_object_or_404(Estimation, id=estimation_id, project__created_by=request.user)
    items = estimation.items.all()
    
    context = {
        'estimation': estimation,
        'items': items,
    }
    
    return render(request, 'engineering/estimation_detail.html', context)


@login_required
def budget_list(request):
    """List all budgets"""
    budgets = ProjectBudget.objects.filter(project__created_by=request.user).order_by('-created_at')
    
    context = {
        'budgets': budgets,
    }
    
    return render(request, 'engineering/budget_list.html', context)


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
            return redirect('engineering:budget_detail', budget_id=budget.id)
    else:
        form = BudgetForm(user=request.user)
    
    context = {
        'form': form,
    }
    
    return render(request, 'engineering/budget_form.html', context)


@login_required
def budget_detail(request, budget_id):
    """Budget detail view"""
    budget = get_object_or_404(ProjectBudget, id=budget_id, project__created_by=request.user)
    items = budget.items.all()
    
    context = {
        'budget': budget,
        'items': items,
    }
    
    return render(request, 'engineering/budget_detail.html', context)


@login_required
def schedule_list(request):
    """List all schedules"""
    schedules = ProjectSchedule.objects.filter(project__created_by=request.user).order_by('-created_at')
    
    context = {
        'schedules': schedules,
    }
    
    return render(request, 'engineering/schedule_list.html', context)


@login_required
def schedule_create(request):
    """Create new schedule"""
    if request.method == 'POST':
        form = ScheduleForm(request.POST, user=request.user)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.created_by = request.user
            schedule.save()
            messages.success(request, 'Schedule created successfully!')
            return redirect('engineering:schedule_detail', schedule_id=schedule.id)
    else:
        form = ScheduleForm(user=request.user)
    
    context = {
        'form': form,
    }
    
    return render(request, 'engineering/schedule_form.html', context)


@login_required
def schedule_detail(request, schedule_id):
    """Schedule detail view"""
    schedule = get_object_or_404(ProjectSchedule, id=schedule_id, project__created_by=request.user)
    activities = schedule.activities.all()
    
    context = {
        'schedule': schedule,
        'activities': activities,
    }
    
    return render(request, 'engineering/schedule_detail.html', context)


@login_required
def cost_control_list(request):
    """List cost control for all projects"""
    projects = Project.objects.filter(created_by=request.user)
    
    context = {
        'projects': projects,
    }
    
    return render(request, 'engineering/cost_control_list.html', context)


@login_required
def cost_control_detail(request, project_id):
    """Cost control detail for a project"""
    project = get_object_or_404(Project, id=project_id, created_by=request.user)
    cost_controls = CostControl.objects.filter(project=project)
    
    context = {
        'project': project,
        'cost_controls': cost_controls,
    }
    
    return render(request, 'engineering/cost_control_detail.html', context)