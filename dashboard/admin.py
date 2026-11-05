from django.contrib import admin
from .models import Faculty, Student, MeritRule, Achievement

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('faculty_id', 'name', 'department', 'user')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_no', 'name', 'department', 'semester', 'user')

@admin.register(MeritRule)
class MeritRuleAdmin(admin.ModelAdmin):
    list_display = ('category', 'points')

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'rule', 'status', 'points_awarded', 'verified_by')
    list_filter = ('status', 'rule')
