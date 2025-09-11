from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('create/', views.create_project, name='create'),
    path('list/', views.project_list, name='list'),
    path('<int:project_id>/', views.project_detail, name='detail'),
    path('<int:project_id>/analytics/', views.project_analytics, name='analytics'),
]