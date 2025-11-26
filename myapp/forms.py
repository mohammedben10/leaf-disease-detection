from django import forms
from .models import TeamProject, LeafImage

class TeamProjectForm(forms.ModelForm):
    class Meta:
        model = TeamProject
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your project...'
            }),
        }

class LeafImageForm(forms.ModelForm):
    class Meta:
        model = LeafImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }