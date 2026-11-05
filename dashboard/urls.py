from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('', views.root_redirect, name='root_redirect'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Student URLs
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/achievements/add/', views.student_add_achievement, name='student_add_achievement'),
    path('student/certificates/', views.student_certificates, name='student_certificates'),
    path('student/leaderboard/', views.student_leaderboard, name='student_leaderboard'),
    path('student/rules/', views.student_rules, name='student_rules'),
    path('student/profile/', views.student_profile, name='student_profile'),
    
    # Faculty URLs
    path('faculty/dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('faculty/students/', views.faculty_students, name='faculty_students'),
    path('faculty/students/add/', views.faculty_add_student, name='faculty_add_student'),
    path('faculty/students/edit/<int:student_id>/', views.faculty_edit_student, name='faculty_edit_student'),
    path('faculty/students/delete/<int:student_id>/', views.faculty_delete_student, name='faculty_delete_student'),
    path('faculty/verification/', views.faculty_verification, name='faculty_verification'),
    path('faculty/verification/<int:achievement_id>/', views.faculty_verify_action, name='faculty_verify_action'),
    path('faculty/leaderboard/', views.faculty_leaderboard, name='faculty_leaderboard'),
    path('faculty/profile/', views.faculty_profile, name='faculty_profile'),

    # HOD URLs
    path('hod/dashboard/', views.hod_dashboard, name='hod_dashboard'),
    path('hod/faculty/', views.hod_faculty, name='hod_faculty'),
    path('hod/faculty/add/', views.hod_add_faculty, name='hod_add_faculty'),
    path('hod/faculty/edit/<int:faculty_id>/', views.hod_edit_faculty, name='hod_edit_faculty'),
    path('hod/faculty/delete/<int:faculty_id>/', views.hod_delete_faculty, name='hod_delete_faculty'),
    path('hod/leaderboard/', views.hod_leaderboard, name='hod_leaderboard'),
    path('hod/rules/', views.hod_rules, name='hod_rules'),
    path('hod/profile/', views.hod_profile, name='hod_profile'),
]
