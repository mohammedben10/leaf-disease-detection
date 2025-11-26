from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class TeamProject(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    team_members = models.ManyToManyField(User, related_name='team_projects', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ['-created_at']

class LeafImage(models.Model):
    PROJECT_STATUS = [
        ('pending', 'Pending Analysis'),
        ('analyzed', 'Analyzed'),
        ('failed', 'Analysis Failed'),
    ]
    
    project = models.ForeignKey(TeamProject, on_delete=models.CASCADE, related_name='leaf_images')
    image = models.ImageField(upload_to='leaf_uploads/')
    original_filename = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(default=timezone.now)
    
    # CNN Analysis Results
    analysis_result = models.JSONField(null=True, blank=True)
    confidence_score = models.FloatField(null=True, blank=True)
    disease_detected = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=PROJECT_STATUS, default='pending')
    
    def __str__(self):
        return f"Leaf Image - {self.original_filename}"
    
    class Meta:
        ordering = ['-uploaded_at']

class AnalysisResult(models.Model):
    leaf_image = models.ForeignKey(LeafImage, on_delete=models.CASCADE, related_name='analysis_results')
    analyzed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    analyzed_at = models.DateTimeField(default=timezone.now)
    
    # CNN Model Results
    predicted_class = models.CharField(max_length=100)
    confidence = models.FloatField()
    disease_info = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    
    def __str__(self):
        return f"Analysis for {self.leaf_image.original_filename}"
    
    class Meta:
        ordering = ['-analyzed_at']