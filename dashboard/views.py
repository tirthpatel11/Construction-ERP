from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from projects.models import Project, Partner, ProjectExpense, ProjectPayment
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
import json


@login_required
def home(request):
    """Main dashboard view with analytics"""
    user_projects = Project.objects.filter(created_by=request.user)
    
    # Project statistics
    total_projects = user_projects.count()
    active_projects = user_projects.filter(status='active').count()
    completed_projects = user_projects.filter(status='completed').count()
    
    # Budget analytics
    total_budget = user_projects.aggregate(Sum('estimated_budget'))['estimated_budget__sum'] or 0
    total_spent = ProjectExpense.objects.filter(project__in=user_projects).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Recent projects
    recent_projects = user_projects.order_by('-created_at')[:5]
    
    # Upcoming payments
    upcoming_payments = ProjectPayment.objects.filter(
        project__in=user_projects,
        due_date__gte=timezone.now(),
        status='pending'
    ).order_by('due_date')[:5]
    
    # Cash flow data for chart (last 6 months)
    cash_flow_data = []
    for i in range(6):
        month_start = timezone.now().replace(day=1) - timedelta(days=30*i)
        month_end = month_start + timedelta(days=30)
        
        income = ProjectPayment.objects.filter(
            project__in=user_projects,
            payment_date__range=[month_start, month_end],
            status='completed'
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        expenses = ProjectExpense.objects.filter(
            project__in=user_projects,
            date__range=[month_start, month_end]
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        cash_flow_data.append({
            'month': month_start.strftime('%b %Y'),
            'income': float(income),
            'expenses': float(expenses),
            'net': float(income - expenses)
        })
    
    cash_flow_data.reverse()
    
    # Cost breakdown data
    cost_breakdown = ProjectExpense.objects.filter(
        project__in=user_projects
    ).values('category').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    context = {
        'total_projects': total_projects,
        'active_projects': active_projects,
        'completed_projects': completed_projects,
        'total_budget': total_budget,
        'total_spent': total_spent,
        'budget_utilization': (total_spent / total_budget * 100) if total_budget > 0 else 0,
        'recent_projects': recent_projects,
        'upcoming_payments': upcoming_payments,
        'cash_flow_data': json.dumps(cash_flow_data),
        'cost_breakdown': json.dumps(list(cost_breakdown)),
    }
    
    return render(request, 'dashboard/home.html', context)


@login_required
def project_selection(request):
    """Project selection page - create new or work on existing"""
    user_projects = Project.objects.filter(created_by=request.user).order_by('-created_at')
    
    context = {
        'projects': user_projects,
    }
    
    return render(request, 'dashboard/project_selection.html', context)


@login_required
def analytics_data(request):
    """API endpoint for dashboard analytics data"""
    user_projects = Project.objects.filter(created_by=request.user)
    
    # Project completion data
    completion_data = []
    for project in user_projects:
        completion_data.append({
            'name': project.name,
            'completion': project.completion_percentage,
            'status': project.status
        })
    
    # Resource utilization (mock data for heatmap)
    resource_data = []
    resources = ['Labor', 'Materials', 'Equipment', 'Subcontractors']
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    
    for resource in resources:
        for month in months:
            resource_data.append({
                'resource': resource,
                'month': month,
                'utilization': __import__('random').randint(20, 100)
            })
    
    return JsonResponse({
        'completion_data': completion_data,
        'resource_data': resource_data,
    })