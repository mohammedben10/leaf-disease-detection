from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from myapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', views.custom_logout, name='logout'),  # Use custom logout
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Main App URLs
    path('', views.home, name='home'),  # ADD THIS - Home page
    path('register/', views.register, name='register'),  # ADD THIS - Registration
    
    # Project URLs
    path('projects/', views.project_list, name='project-list'),
    path('projects/create/', views.project_create, name='project-create'),
    path('projects/<int:pk>/', views.project_detail, name='project-detail'),
    path('projects/<int:project_id>/history/', views.analysis_history, name='analysis-history'),
    path('analyze/<int:image_id>/', views.analyze_image, name='analyze-image'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)