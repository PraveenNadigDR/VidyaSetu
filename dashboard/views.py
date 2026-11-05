from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Student, Faculty, MeritRule, Achievement
from .forms import AchievementForm

# Helper permissions
def is_hod(user):
    return user.is_authenticated and user.is_superuser

def is_faculty(user):
    return user.is_authenticated and hasattr(user, 'faculty_profile')

def is_student(user):
    return user.is_authenticated and hasattr(user, 'student_profile')

def root_redirect(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if is_hod(request.user):
        return redirect('hod_dashboard')
    elif is_faculty(request.user):
        return redirect('faculty_dashboard')
    elif is_student(request.user):
        return redirect('student_dashboard')
    else:
        logout(request)
        return redirect('login')

def login_view(request):
    if request.user.is_authenticated:
        return root_redirect(request)
        
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return root_redirect(request)
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, 'dashboard/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# ----------------- STUDENT VIEWS -----------------
@user_passes_test(is_student, login_url='login')
def student_dashboard(request):
    student = request.user.student_profile
    achievements = student.achievements.all()[:5]
    context = {
        'student': student,
        'badge_info': student.get_badge_info(),
        'merit_points': student.get_merit_points(),
        'recent_achievements': achievements
    }
    return render(request, 'dashboard/student/dashboard.html', context)

@user_passes_test(is_student, login_url='login')
def student_add_achievement(request):
    student = request.user.student_profile
    if request.method == 'POST':
        form = AchievementForm(request.POST, request.FILES)
        if form.is_valid():
            ach = form.save(commit=False)
            ach.student = student
            ach.status = 'PENDING'
            ach.save()
            messages.success(request, "Achievement submitted successfully for verification.")
            return redirect('student_dashboard')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = AchievementForm()
        
    context = {'student': student, 'form': form}
    return render(request, 'dashboard/student/add_achievement.html', context)

@user_passes_test(is_student, login_url='login')
def student_certificates(request):
    student = request.user.student_profile
    achievements = student.achievements.exclude(certificate='')
    
    category = request.GET.get('category')
    if category:
        achievements = achievements.filter(rule__category=category)
        
    categories = MeritRule.objects.all()
    
    context = {
        'student': student, 
        'achievements': achievements,
        'categories': categories,
        'selected_category': category
    }
    return render(request, 'dashboard/student/certificates.html', context)

@user_passes_test(is_student, login_url='login')
def student_leaderboard(request):
    students = sorted(Student.objects.all(), key=lambda s: s.get_merit_points(), reverse=True)
    context = {'student': request.user.student_profile, 'students': students}
    return render(request, 'dashboard/student/leaderboard.html', context)

@user_passes_test(is_student, login_url='login')
def student_rules(request):
    rules = MeritRule.objects.all()
    context = {'student': request.user.student_profile, 'rules': rules}
    return render(request, 'dashboard/student/rules.html', context)

@user_passes_test(is_student, login_url='login')
def student_profile(request):
    context = {'student': request.user.student_profile, 'badge_info': request.user.student_profile.get_badge_info()}
    return render(request, 'dashboard/student/profile.html', context)

# ----------------- FACULTY VIEWS -----------------
@user_passes_test(is_faculty, login_url='login')
def faculty_dashboard(request):
    faculty = request.user.faculty_profile
    students = Student.objects.count()
    pending = Achievement.objects.filter(status='PENDING').count()
    verified = Achievement.objects.filter(status='VERIFIED').count()
    
    context = {
        'faculty': faculty,
        'total_students': students,
        'pending_verifications': pending,
        'verified_achievements': verified,
        'recent_submissions': Achievement.objects.filter(status='PENDING')[:5]
    }
    return render(request, 'dashboard/faculty/dashboard.html', context)

@user_passes_test(is_faculty, login_url='login')
def faculty_students(request):
    students = Student.objects.all()
    context = {'faculty': request.user.faculty_profile, 'students': students}
    return render(request, 'dashboard/faculty/students.html', context)

@user_passes_test(is_faculty, login_url='login')
def faculty_delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.user.delete()
        messages.success(request, f"Student {student.name} deleted successfully.")
    return redirect('faculty_students')

@user_passes_test(is_faculty, login_url='login')
def faculty_add_student(request):
    faculty = request.user.faculty_profile
    if request.method == 'POST':
        name = request.POST.get('name')
        roll_no = request.POST.get('roll_no')
        dept = request.POST.get('department')
        sem = request.POST.get('semester')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=roll_no).exists():
            messages.error(request, "Student with this USN already exists.")
        else:
            user = User.objects.create_user(username=roll_no, email=email, password=password)
            Student.objects.create(user=user, name=name, roll_no=roll_no, department=dept, semester=sem, email=email)
            messages.success(request, f"Student {name} registered successfully.")
            return redirect('faculty_students')
            
    return render(request, 'dashboard/faculty/add_student.html', {'faculty': faculty})

@user_passes_test(is_faculty, login_url='login')
def faculty_edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    faculty = request.user.faculty_profile
    if request.method == 'POST':
        name = request.POST.get('name')
        dept = request.POST.get('department')
        sem = request.POST.get('semester')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        student.name = name
        student.department = dept
        student.semester = sem
        student.email = email
        student.save()
        
        user = student.user
        user.email = email
        if password:
            user.set_password(password)
        user.save()
        
        messages.success(request, f"Student {name} updated successfully.")
        return redirect('faculty_students')
        
    return render(request, 'dashboard/faculty/edit_student.html', {'faculty': faculty, 'student_obj': student})

@user_passes_test(is_faculty, login_url='login')
def faculty_verification(request):
    pending = Achievement.objects.filter(status='PENDING')
    context = {'faculty': request.user.faculty_profile, 'pending': pending}
    return render(request, 'dashboard/faculty/verification.html', context)

@user_passes_test(is_faculty, login_url='login')
def faculty_verify_action(request, achievement_id):
    ach = get_object_or_404(Achievement, pk=achievement_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        note = request.POST.get('note', '')
        
        if action == 'verify':
            ach.status = 'VERIFIED'
            ach.points_awarded = ach.rule.points
        elif action == 'reject':
            ach.status = 'REJECTED'
            ach.points_awarded = 0
            
        ach.verified_by = request.user.faculty_profile
        ach.verified_at = timezone.now()
        ach.verification_note = note
        ach.save()
        messages.success(request, f"Achievement marked as {ach.status}.")
        return redirect('faculty_verification')
        
    context = {'faculty': request.user.faculty_profile, 'achievement': ach}
    return render(request, 'dashboard/faculty/verify_action.html', context)

@user_passes_test(is_faculty, login_url='login')
def faculty_leaderboard(request):
    students = sorted(Student.objects.all(), key=lambda s: s.get_merit_points(), reverse=True)
    context = {'faculty': request.user.faculty_profile, 'students': students}
    return render(request, 'dashboard/faculty/leaderboard.html', context)

@user_passes_test(is_faculty, login_url='login')
def faculty_profile(request):
    return render(request, 'dashboard/faculty/profile.html', {'faculty': request.user.faculty_profile})

# ----------------- HOD VIEWS -----------------
@user_passes_test(is_hod, login_url='login')
def hod_dashboard(request):
    context = {
        'total_faculty': Faculty.objects.count(),
        'total_students': Student.objects.count(),
        'verified_achievements': Achievement.objects.filter(status='VERIFIED').count(),
        'pending_achievements': Achievement.objects.filter(status='PENDING').count(),
        'recent_faculty': Faculty.objects.all()[:5]
    }
    return render(request, 'dashboard/hod/dashboard.html', context)

@user_passes_test(is_hod, login_url='login')
def hod_faculty(request):
    context = {'faculties': Faculty.objects.all()}
    return render(request, 'dashboard/hod/faculty.html', context)

@user_passes_test(is_hod, login_url='login')
def hod_delete_faculty(request, faculty_id):
    faculty = get_object_or_404(Faculty, id=faculty_id)
    if request.method == 'POST':
        faculty.user.delete()
        messages.success(request, f"Faculty {faculty.name} deleted successfully.")
    return redirect('hod_faculty')

@user_passes_test(is_hod, login_url='login')
def hod_add_faculty(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        fid = request.POST.get('faculty_id')
        dept = request.POST.get('department')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=fid).exists():
            messages.error(request, "Faculty ID already exists.")
        else:
            user = User.objects.create_user(username=fid, email=email, password=password)
            Faculty.objects.create(user=user, name=name, faculty_id=fid, department=dept, email=email)
            messages.success(request, f"Faculty {name} registered successfully.")
            return redirect('hod_faculty')
            
    return render(request, 'dashboard/hod/add_faculty.html')

@user_passes_test(is_hod, login_url='login')
def hod_edit_faculty(request, faculty_id):
    faculty = get_object_or_404(Faculty, id=faculty_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        dept = request.POST.get('department')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        faculty.name = name
        faculty.department = dept
        faculty.email = email
        faculty.save()
        
        user = faculty.user
        user.email = email
        if password:
            user.set_password(password)
        user.save()
        
        messages.success(request, f"Faculty {name} updated successfully.")
        return redirect('hod_faculty')
        
    return render(request, 'dashboard/hod/edit_faculty.html', {'faculty_obj': faculty})

@user_passes_test(is_hod, login_url='login')
def hod_rules(request):
    if request.method == 'POST':
        rule_id = request.POST.get('rule_id')
        points = request.POST.get('points')
        if rule_id and points:
            rule = MeritRule.objects.get(id=rule_id)
            rule.points = int(points)
            rule.save()
            messages.success(request, "Rule updated successfully.")
            return redirect('hod_rules')
            
    context = {'rules': MeritRule.objects.all()}
    return render(request, 'dashboard/hod/rules.html', context)

@user_passes_test(is_hod, login_url='login')
def hod_profile(request):
    return render(request, 'dashboard/hod/profile.html')

@user_passes_test(is_hod, login_url='login')
def hod_leaderboard(request):
    students = sorted(Student.objects.all(), key=lambda s: s.get_merit_points(), reverse=True)
    context = {'students': students}
    return render(request, 'dashboard/hod/leaderboard.html', context)
