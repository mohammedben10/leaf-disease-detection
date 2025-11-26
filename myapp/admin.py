from django.contrib import admin
from .models import TeamProject, LeafImage, AnalysisResult

@admin.register(TeamProject)
class TeamProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['team_members']

@admin.register(LeafImage)
class LeafImageAdmin(admin.ModelAdmin):
    list_display = ['original_filename', 'project', 'uploaded_by', 'uploaded_at', 'status']
    list_filter = ['status', 'uploaded_at', 'project']
    search_fields = ['original_filename', 'project__name']
    readonly_fields = ['uploaded_at']

@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ['leaf_image', 'analyzed_by', 'analyzed_at', 'predicted_class', 'confidence']
    list_filter = ['analyzed_at', 'predicted_class']
    search_fields = ['leaf_image__original_filename', 'analyzed_by__username']
    readonly_fields = ['analyzed_at']