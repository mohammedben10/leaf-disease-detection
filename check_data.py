# check_data.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')
django.setup()

from django.contrib.auth.models import User
from myapp.models import TeamProject, LeafImage, AnalysisResult

def check_database_data():
    print("📊 CHECKING ALL DATA IN POSTGRESQL DATABASE")
    print("=" * 60)
    
    # Check users
    users = User.objects.all().order_by('date_joined')
    print(f"👥 USERS ({users.count()} total):")
    for user in users:
        print(f"   - {user.username} | {user.email} | Joined: {user.date_joined.strftime('%Y-%m-%d %H:%M')}")
    
    print()
    
    # Check projects
    projects = TeamProject.objects.all().order_by('-created_at')
    print(f"📁 PROJECTS ({projects.count()} total):")
    for project in projects:
        team_members = project.team_members.all()
        members_list = ", ".join([member.username for member in team_members])
        print(f"   - '{project.name}'")
        print(f"     Created by: {project.created_by.username}")
        print(f"     Team members: {members_list}")
        print(f"     Created: {project.created_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"     Description: {project.description[:50]}..." if len(project.description) > 50 else f"     Description: {project.description}")
        print()
    
    # Check leaf images
    images = LeafImage.objects.all().order_by('-uploaded_at')
    print(f"🖼️  LEAF IMAGES ({images.count()} total):")
    for image in images:
        status_display = dict(LeafImage.PROJECT_STATUS).get(image.status, image.status)
        print(f"   - {image.original_filename}")
        print(f"     Project: {image.project.name}")
        print(f"     Uploaded by: {image.uploaded_by.username}")
        print(f"     Status: {status_display}")
        print(f"     Uploaded: {image.uploaded_at.strftime('%Y-%m-%d %H:%M')}")
        if image.disease_detected:
            print(f"     Disease: {image.disease_detected} (Confidence: {image.confidence_score})")
        print()
    
    # Check analysis results
    analyses = AnalysisResult.objects.all().order_by('-analyzed_at')
    print(f"🔬 ANALYSIS RESULTS ({analyses.count()} total):")
    for analysis in analyses:
        print(f"   - Image: {analysis.leaf_image.original_filename}")
        print(f"     Predicted: {analysis.predicted_class} (Confidence: {analysis.confidence})")
        print(f"     Analyzed by: {analysis.analyzed_by.username}")
        print(f"     Date: {analysis.analyzed_at.strftime('%Y-%m-%d %H:%M')}")
        print()
    
    # Summary
    print("📈 DATABASE SUMMARY:")
    print(f"   Total Users: {User.objects.count()}")
    print(f"   Total Projects: {TeamProject.objects.count()}")
    print(f"   Total Leaf Images: {LeafImage.objects.count()}")
    print(f"   Total Analyses: {AnalysisResult.objects.count()}")
    
    print("=" * 60)
    print("✅ Database check completed!")

if __name__ == "__main__":
    check_database_data()