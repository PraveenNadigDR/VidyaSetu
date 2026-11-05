from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_profile')
    faculty_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.faculty_id})"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    roll_no = models.CharField(max_length=25, unique=True, help_text="University Seat / Roll Number (USN)")
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    semester = models.IntegerField(default=5)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.roll_no})"

    def get_total_achievements(self):
        return self.achievements.count()

    def get_verified_achievements(self):
        return self.achievements.filter(status='VERIFIED').count()

    def get_pending_achievements(self):
        return self.achievements.filter(status='PENDING').count()

    def get_rejected_achievements(self):
        return self.achievements.filter(status='REJECTED').count()

    def get_merit_points(self):
        points = self.achievements.filter(status='VERIFIED').aggregate(total=models.Sum('points_awarded'))['total']
        return points or 0

    def get_badge(self):
        points = self.get_merit_points()
        if points >= 600:
            return 'Merit Champion'
        elif points >= 300:
            return 'Star Performer'
        elif points >= 100:
            return 'Achiever'
        return 'Beginner'

    def get_badge_info(self):
        points = self.get_merit_points()
        if points >= 600:
            return {
                'badge': 'Merit Champion',
                'css_class': 'badge-champion',
                'level': 4,
                'min_points': 600,
                'max_points': 1000,
                'current_points': points,
                'progress': 100,
                'next_badge': 'Max Level',
                'points_needed': 0,
            }
        elif points >= 300:
            progress = int(((points - 300) / (600 - 300)) * 100)
            return {
                'badge': 'Star Performer',
                'css_class': 'badge-star',
                'level': 3,
                'min_points': 300,
                'max_points': 600,
                'current_points': points,
                'progress': max(5, min(progress, 100)),
                'next_badge': 'Merit Champion',
                'points_needed': 600 - points,
            }
        elif points >= 100:
            progress = int(((points - 100) / (300 - 100)) * 100)
            return {
                'badge': 'Achiever',
                'css_class': 'badge-achiever',
                'level': 2,
                'min_points': 100,
                'max_points': 300,
                'current_points': points,
                'progress': max(5, min(progress, 100)),
                'next_badge': 'Star Performer',
                'points_needed': 300 - points,
            }
        else:
            progress = int((points / 100) * 100) if points > 0 else 0
            return {
                'badge': 'Beginner',
                'css_class': 'badge-beginner',
                'level': 1,
                'min_points': 0,
                'max_points': 100,
                'current_points': points,
                'progress': max(0, min(progress, 100)),
                'next_badge': 'Achiever',
                'points_needed': 100 - points,
            }

    def get_initials(self):
        parts = self.name.strip().split()
        if len(parts) >= 2:
            return f"{parts[0][0]}{parts[1][0]}".upper()
        elif parts:
            return parts[0][:2].upper()
        return "ST"

class MeritRule(models.Model):
    category = models.CharField(max_length=50, unique=True)
    points = models.IntegerField(default=50)
    
    class Meta:
        ordering = ['points']
        
    def __str__(self):
        return f"{self.category} ({self.points} pts)"

class Achievement(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('VERIFIED', 'Verified'),
        ('REJECTED', 'Rejected'),
    ]

    achievement_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=200)
    rule = models.ForeignKey(MeritRule, on_delete=models.PROTECT, related_name='achievements')
    description = models.TextField()
    achievement_date = models.DateField()
    organization = models.CharField(max_length=200)
    certificate = models.FileField(upload_to='certificates/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    points_awarded = models.IntegerField(default=0)
    
    verified_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    verification_note = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.achievement_id:
            import uuid
            self.achievement_id = f"ACH-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.achievement_id or self.title} - {self.student.name} ({self.status})"

    @property
    def is_image(self):
        if not self.certificate:
            return False
        ext = os.path.splitext(self.certificate.name)[1].lower()
        return ext in ['.jpg', '.jpeg', '.png', '.webp']

    @property
    def is_pdf(self):
        if not self.certificate:
            return False
        ext = os.path.splitext(self.certificate.name)[1].lower()
        return ext == '.pdf'
