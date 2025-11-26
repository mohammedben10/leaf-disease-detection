from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.db import models
from .models import TeamProject, LeafImage, AnalysisResult
from .forms import TeamProjectForm, LeafImageForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def home(request):
    """Home page with project overview"""
    if request.user.is_authenticated:
        projects = TeamProject.objects.filter(
            models.Q(created_by=request.user) | 
            models.Q(team_members=request.user)
        ).distinct()[:5]
        total_projects = projects.count()
        recent_images = LeafImage.objects.filter(
            project__in=projects
        ).order_by('-uploaded_at')[:3]
    else:
        projects = []
        total_projects = 0
        recent_images = []
    
    context = {
        'projects': projects,
        'total_projects': total_projects,
        'recent_images': recent_images,
    }
    return render(request, 'myapp/home.html', context)

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            messages.success(request, 'Registration successful!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'myapp/register.html', {'form': form})

@login_required
def project_list(request):
    """List all user's projects"""
    projects = TeamProject.objects.filter(
        models.Q(created_by=request.user) | 
        models.Q(team_members=request.user)
    ).distinct().order_by('-created_at')
    
    return render(request, 'myapp/project_list.html', {'projects': projects})

@login_required
def project_create(request):
    """Create new project"""
    if request.method == 'POST':
        form = TeamProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            project.team_members.add(request.user)  # Add creator as team member
            messages.success(request, 'Project created successfully!')
            return redirect('project-detail', pk=project.pk)
    else:
        form = TeamProjectForm()
    
    return render(request, 'myapp/project_form.html', {'form': form})

@login_required
def project_detail(request, pk):
    """Project detail with images and team management"""
    project = get_object_or_404(TeamProject, pk=pk)
    
    # Check if user has access
    if not (request.user == project.created_by or request.user in project.team_members.all()):
        messages.error(request, 'You do not have access to this project.')
        return redirect('project-list')
    
    leaf_images = project.leaf_images.all().order_by('-uploaded_at')
    
    if request.method == 'POST':
        form = LeafImageForm(request.POST, request.FILES)
        if form.is_valid():
            leaf_image = form.save(commit=False)
            leaf_image.project = project
            leaf_image.uploaded_by = request.user
            leaf_image.original_filename = leaf_image.image.name
            leaf_image.save()
            messages.success(request, 'Image uploaded successfully!')
            return redirect('project-detail', pk=project.pk)
    else:
        form = LeafImageForm()
    
    context = {
        'project': project,
        'leaf_images': leaf_images,
        'form': form,
        'team_members': project.team_members.all(),
    }
    return render(request, 'myapp/project_detail.html', context)

@login_required
def analyze_image(request, image_id):
    """Analyze leaf image (CNN integration ready)"""
    leaf_image = get_object_or_404(LeafImage, pk=image_id)
    
    # Check access
    if not (request.user == leaf_image.project.created_by or 
            request.user in leaf_image.project.team_members.all()):
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    # TODO: Integrate CNN model here
    # For now, simulate analysis
    analysis_data = {
        'predicted_class': 'Healthy',
        'confidence': 0.92,
        'disease_info': 'Leaf appears healthy with no signs of disease.',
        'recommendations': 'Continue current care routine.'
    }
    
    # Save analysis result
    analysis = AnalysisResult.objects.create(
        leaf_image=leaf_image,
        analyzed_by=request.user,
        predicted_class=analysis_data['predicted_class'],
        confidence=analysis_data['confidence'],
        disease_info=analysis_data['disease_info'],
        recommendations=analysis_data['recommendations']
    )
    
    # Update leaf image status
    leaf_image.status = 'analyzed'
    leaf_image.disease_detected = analysis_data['predicted_class']
    leaf_image.confidence_score = analysis_data['confidence']
    leaf_image.save()
    
    messages.success(request, f'Analysis complete: {analysis_data["predicted_class"]}')
    return redirect('project-detail', pk=leaf_image.project.pk)

@login_required
def analysis_history(request, project_id):
    """View analysis history for a project"""
    project = get_object_or_404(TeamProject, pk=project_id)
    
    if not (request.user == project.created_by or request.user in project.team_members.all()):
        messages.error(request, 'Access denied.')
        return redirect('project-list')
    
    analyses = AnalysisResult.objects.filter(
        leaf_image__project=project
    ).select_related('leaf_image', 'analyzed_by').order_by('-analyzed_at')
    
    return render(request, 'myapp/analysis_history.html', {
        'project': project,
        'analyses': analyses
    })

def custom_login(request):
    """Custom login view"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})


@login_required
def custom_logout(request):
    """Custom logout view that accepts GET requests"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')