from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from dashboard.models import Student, Achievement, Verification

class VidyaSetuTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create student 1
        self.user1 = User.objects.create_user(username='praveen', password='student123', first_name='Praveen')
        self.student1 = Student.objects.create(
            user=self.user1,
            student_id='VS-2022-045',
            roll_no='1IS22IS045',
            name='Praveen Kumar',
            email='praveen@vidyasetu.edu',
            department='Information Science and Engineering',
            semester=5,
        )

        # Create student 2
        self.user2 = User.objects.create_user(username='ananya', password='student123', first_name='Ananya')
        self.student2 = Student.objects.create(
            user=self.user2,
            student_id='VS-2022-012',
            roll_no='1IS22IS012',
            name='Ananya Rao',
            email='ananya@vidyasetu.edu',
            department='Information Science and Engineering',
            semester=5,
        )

        # Create achievements for student 1
        self.ach1 = Achievement.objects.create(
            student=self.student1,
            title='Smart India Hackathon 2024 Winner',
            category='Hackathon',
            description='National level hackathon winner in smart education.',
            achievement_date=date(2024, 8, 20),
            organization='Ministry of Education',
            status='VERIFIED',
            points=100
        )

        self.ach2 = Achievement.objects.create(
            student=self.student1,
            title='Python Specialist Certification',
            category='Certification',
            description='Online technical certification.',
            achievement_date=date(2024, 7, 10),
            organization='NPTEL',
            status='PENDING',
            points=50
        )

        # Create achievement for student 2
        self.ach_student2 = Achievement.objects.create(
            student=self.student2,
            title='Google Solution Challenge Global Finalist',
            category='Hackathon',
            description='Finalist team lead.',
            achievement_date=date(2024, 6, 1),
            organization='Google Developer Groups',
            status='VERIFIED',
            points=100
        )

    def test_points_and_badge_calculation(self):
        """Only VERIFIED achievements should count towards merit points."""
        # Student 1 has 1 verified (100 pts) and 1 pending (50 pts)
        self.assertEqual(self.student1.get_total_achievements(), 2)
        self.assertEqual(self.student1.get_verified_achievements(), 1)
        self.assertEqual(self.student1.get_pending_achievements(), 1)
        self.assertEqual(self.student1.get_merit_points(), 100)
        self.assertEqual(self.student1.get_badge(), 'Achiever')

    def test_unauthenticated_redirect(self):
        """Unauthenticated requests to protected pages must redirect to login."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('login')))

    def test_login_with_username(self):
        """Student can log in using their username."""
        response = self.client.post(reverse('login'), {
            'username': 'praveen',
            'password': 'student123'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome back, Praveen')

    def test_login_with_roll_number(self):
        """Student can log in using their Roll Number / USN."""
        response = self.client.post(reverse('login'), {
            'username': '1IS22IS045',
            'password': 'student123'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome back, Praveen')

    def test_dashboard_displays_database_metrics(self):
        """Dashboard page displays verified, pending, and total stats from DB."""
        self.client.login(username='praveen', password='student123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '100')  # Merit points
        self.assertContains(response, 'Smart India Hackathon 2024 Winner')

    def test_add_achievement_post(self):
        """Form submission saves record to DB, sets PENDING status, and creates Verification."""
        self.client.login(username='praveen', password='student123')
        response = self.client.post(reverse('add_achievement'), {
            'title': 'Autonomous Robotics Competition 2nd Place',
            'category': 'Competition',
            'description': 'Designed an obstacle avoidance line follower bot.',
            'achievement_date': '2024-09-15',
            'organization': 'IIT Bombay Techfest',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Achievement.objects.filter(title='Autonomous Robotics Competition 2nd Place').exists())
        new_ach = Achievement.objects.get(title='Autonomous Robotics Competition 2nd Place')
        self.assertEqual(new_ach.status, 'PENDING')
        self.assertEqual(new_ach.points, 75)  # Competition default points
        self.assertTrue(hasattr(new_ach, 'verification'))

    def test_achievement_privacy_isolation(self):
        """Student 1 cannot view Student 2's achievement detail (returns 404)."""
        self.client.login(username='praveen', password='student123')
        # Student 1 attempts to access Student 2's achievement
        response = self.client.get(reverse('achievement_detail', kwargs={'pk': self.ach_student2.pk}))
        self.assertEqual(response.status_code, 404)

    def test_leaderboard_ranking(self):
        """Leaderboard properly lists ranked students."""
        self.client.login(username='praveen', password='student123')
        response = self.client.get(reverse('leaderboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Institutional Merit Leaderboard')
        self.assertContains(response, 'Praveen Kumar')
        self.assertContains(response, 'Ananya Rao')

    def test_profile_page(self):
        """Profile page displays student's USN and academic info."""
        self.client.login(username='praveen', password='student123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1IS22IS045')
        self.assertContains(response, 'Information Science and Engineering')
