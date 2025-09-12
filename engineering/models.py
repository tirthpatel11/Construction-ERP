from django.db import models
from django.contrib.auth.models import User
from projects.models import Project
from decimal import Decimal


class Estimation(models.Model):
    """Project estimation and costing"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='estimations')
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=50, default='1.0')
    description = models.TextField(blank=True)
    total_estimated_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.project.name} - {self.name} v{self.version}"


class EstimationItem(models.Model):
    """Individual items in estimation"""
    estimation = models.ForeignKey(Estimation, on_delete=models.CASCADE, related_name='items')
    item_code = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    unit = models.CharField(max_length=50)
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    unit_rate = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    category = models.CharField(max_length=100, blank=True)
    
    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.unit_rate
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.item_code} - {self.description}"


class ProjectBudget(models.Model):
    """Project budget definition and monitoring"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='budgets')
    name = models.CharField(max_length=255)
    budget_type = models.CharField(max_length=50, choices=[
        ('initial', 'Initial Budget'),
        ('revised', 'Revised Budget'),
        ('final', 'Final Budget')
    ])
    total_budget = models.DecimalField(max_digits=15, decimal_places=2)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approved_budgets')
    approved_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.project.name} - {self.name}"


class BudgetItem(models.Model):
    """Individual budget line items"""
    budget = models.ForeignKey(ProjectBudget, on_delete=models.CASCADE, related_name='items')
    category = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    budget_amount = models.DecimalField(max_digits=15, decimal_places=2)
    actual_spent = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    committed_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    @property
    def variance(self):
        return self.budget_amount - self.actual_spent
    
    @property
    def variance_percentage(self):
        if self.budget_amount > 0:
            return (self.variance / self.budget_amount) * 100
        return 0
    
    def __str__(self):
        return f"{self.category} - {self.description}"


class ProjectSchedule(models.Model):
    """Project scheduling using PERT/CPM"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='schedules')
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.project.name} - {self.name}"


class ScheduleActivity(models.Model):
    """Individual activities in project schedule"""
    schedule = models.ForeignKey(ProjectSchedule, on_delete=models.CASCADE, related_name='activities')
    activity_code = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    planned_start = models.DateField()
    planned_end = models.DateField()
    actual_start = models.DateField(null=True, blank=True)
    actual_end = models.DateField(null=True, blank=True)
    duration_days = models.IntegerField()
    dependencies = models.ManyToManyField('self', blank=True, symmetrical=False)
    is_critical = models.BooleanField(default=False)
    is_milestone = models.BooleanField(default=False)
    completion_percentage = models.IntegerField(default=0)
    
    @property
    def is_delayed(self):
        if self.actual_end and self.planned_end:
            return self.actual_end > self.planned_end
        return False
    
    def __str__(self):
        return f"{self.activity_code} - {self.description}"


class CostControl(models.Model):
    """3-level cost control: Budget, Estimate, Actual"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='cost_controls')
    category = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    
    # 3-level cost control
    budget_amount = models.DecimalField(max_digits=15, decimal_places=2)
    estimate_amount = models.DecimalField(max_digits=15, decimal_places=2)
    actual_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Variances
    @property
    def budget_vs_estimate_variance(self):
        return self.estimate_amount - self.budget_amount
    
    @property
    def estimate_vs_actual_variance(self):
        return self.actual_amount - self.estimate_amount
    
    @property
    def budget_vs_actual_variance(self):
        return self.actual_amount - self.budget_amount
    
    def __str__(self):
        return f"{self.project.name} - {self.category}"