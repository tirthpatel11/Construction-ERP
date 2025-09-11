from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import UserProfile
from .supabase_client import sync_user_to_supabase
import json


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            # Sync user to Supabase
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_data = {
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user_profile.phone_number,
                'company': user_profile.company,
                'address': user_profile.address,
                'django_user_id': user.id,
            }
            
            supabase_result = sync_user_to_supabase(user_data)
            if supabase_result:
                user_profile.supabase_id = supabase_result.get('id')
                user_profile.save()
            
            messages.success(request, 'Login successful!')
            return redirect('dashboard:home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'authentication/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        phone_number = request.POST.get('phone_number', '')
        company = request.POST.get('company', '')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'authentication/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'authentication/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'authentication/register.html')
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            user_profile = UserProfile.objects.create(
                user=user,
                phone_number=phone_number,
                company=company
            )
            
            # Sync to Supabase
            user_data = {
                'email': email,
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'phone_number': phone_number,
                'company': company,
                'django_user_id': user.id,
            }
            
            supabase_result = sync_user_to_supabase(user_data)
            if supabase_result:
                user_profile.supabase_id = supabase_result.get('id')
                user_profile.save()
            
            messages.success(request, 'Registration successful! Please login.')
            return redirect('authentication:login')
            
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
    
    return render(request, 'authentication/register.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('authentication:login')