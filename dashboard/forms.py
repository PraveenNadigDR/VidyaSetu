from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
import os
from .models import Achievement, MeritRule

class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['title', 'rule', 'description', 'achievement_date', 'organization', 'certificate']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Smart India Hackathon 2024 Winner / Python Certification',
                'required': True,
            }),
            'rule': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your role, key learning outcomes, project details, or rank achieved...',
                'required': True,
            }),
            'achievement_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True,
            }),
            'organization': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Ministry of Education / Coursera / IIT Madras / College Sports Cell',
                'required': True,
            }),
            'certificate': forms.ClearableFileInput(attrs={
                'class': 'form-file-input',
                'accept': '.pdf,.jpg,.jpeg,.png',
                'required': True,
            }),
        }
        labels = {
            'title': 'Achievement Title',
            'rule': 'Category',
            'description': 'Description & Details',
            'achievement_date': 'Achievement Date',
            'organization': 'Organization / Issued By',
            'certificate': 'Certificate / Proof Document (PDF, JPG, PNG)',
        }
        help_texts = {
            'certificate': 'Upload proof in PDF, JPG, JPEG, or PNG format (Max 10 MB).',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rule'].queryset = MeritRule.objects.all().order_by('category')
        self.fields['rule'].empty_label = "Select Category"

    def clean_certificate(self):
        certificate = self.cleaned_data.get('certificate')
        if certificate:
            valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
            ext = os.path.splitext(certificate.name)[1].lower()
            if ext not in valid_extensions:
                raise ValidationError('Unsupported file format. Please upload a PDF, JPG, JPEG, or PNG file.')
            
            max_size = 10 * 1024 * 1024
            if certificate.size > max_size:
                raise ValidationError('File size exceeds the 10 MB limit. Please upload a smaller file.')
        return certificate

    def clean_achievement_date(self):
        achievement_date = self.cleaned_data.get('achievement_date')
        if achievement_date and achievement_date > timezone.now().date():
            raise ValidationError('Achievement date cannot be in the future.')
        return achievement_date
