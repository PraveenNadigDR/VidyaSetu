import os
import sys
import django
from datetime import date, timedelta
from django.utils import timezone
from PIL import Image, ImageDraw, ImageFont

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyasetu.settings')
django.setup()

from django.contrib.auth.models import User
from dashboard.models import Student, Achievement, Verification

def create_sample_certificate(filename, title, recipient, issuer, category):
    """Generates a clean certificate image using Pillow and saves it in media/certificates/"""
    media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'certificates')
    os.makedirs(media_dir, exist_ok=True)
    filepath = os.path.join(media_dir, filename)

    # 1200x800 elegant certificate background
    width, height = 1200, 800
    img = Image.new('RGB', (width, height), color='#ffffff')
    draw = ImageDraw.Draw(img)

    # Outer and inner border
    draw.rectangle([(25, 25), (width - 25, height - 25)], outline='#1e3a8a', width=8)
    draw.rectangle([(40, 40), (width - 40, height - 40)], outline='#93c5fd', width=2)
    draw.rectangle([(50, 50), (width - 50, height - 50)], outline='#1e3a8a', width=1)

    # Header decorative banner
    draw.rectangle([(60, 60), (width - 60, 140)], fill='#f8fafc')
    draw.text((width // 2, 90), "VIDYA SETU &bull; VERIFIED MERIT CREDENTIAL", fill='#1e3a8a', anchor="mm")
    draw.text((width // 2, 115), "ACADEMIC & MERIT RECOGNITION ARCHIVE", fill='#64748b', anchor="mm")

    # Title
    draw.text((width // 2, 220), "CERTIFICATE OF ACHIEVEMENT", fill='#0f172a', anchor="mm")
    draw.text((width // 2, 260), "THIS IS PROUDLY PRESENTED TO", fill='#64748b', anchor="mm")

    # Student Name
    draw.text((width // 2, 340), recipient.upper(), fill='#1d4ed8', anchor="mm")
    draw.line([(width // 2 - 250, 375), (width // 2 + 250, 375)], fill='#1d4ed8', width=2)

    # Details
    draw.text((width // 2, 430), f"In recognition of successful completion and outstanding performance in:", fill='#334155', anchor="mm")
    draw.text((width // 2, 480), f'"{title}"', fill='#0f172a', anchor="mm")
    draw.text((width // 2, 530), f"Category: {category}  |  Issuing Authority: {issuer}", fill='#475569', anchor="mm")

    # Footer signatures & seals
    draw.rectangle([(120, 640), (360, 710)], fill='#f1f5f9', outline='#cbd5e1')
    draw.text((240, 665), "Digitally Verified", fill='#15803d', anchor="mm")
    draw.text((240, 690), "Vidya Setu Registry", fill='#64748b', anchor="mm")

    draw.rectangle([(width - 360, 640), (width - 120, 710)], fill='#f1f5f9', outline='#cbd5e1')
    draw.text((width - 240, 665), issuer[:25], fill='#0f172a', anchor="mm")
    draw.text((width - 240, 690), "Authorized Signatory", fill='#64748b', anchor="mm")

    img.save(filepath, 'PNG')
    return f"certificates/{filename}"


def seed():
    print("Seeding Vidya Setu Database with realistic student & achievement data...")

    # 1. Superuser / Faculty Coordinator
    admin_user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@vidyasetu.edu'})
    admin_user.set_password('admin123')
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.first_name = 'Dr. Ramesh'
    admin_user.last_name = 'Kulkarni'
    admin_user.save()
    print("Admin user created/updated: admin / admin123")

    # 2. Primary Demo Student: Praveen Kumar
    praveen_user, created = User.objects.get_or_create(username='praveen', defaults={'email': 'praveen.ise@vidyasetu.edu'})
    praveen_user.set_password('student123')
    praveen_user.first_name = 'Praveen'
    praveen_user.last_name = 'Kumar'
    praveen_user.save()

    praveen_student, _ = Student.objects.get_or_create(
        user=praveen_user,
        defaults={
            'student_id': 'VS-2022-045',
            'roll_no': '1IS22IS045',
            'name': 'Praveen Kumar',
            'email': 'praveen.ise@vidyasetu.edu',
            'department': 'Information Science and Engineering',
            'semester': 5,
            'phone': '9876543210'
        }
    )
    # Ensure attributes are updated
    praveen_student.name = 'Praveen Kumar'
    praveen_student.roll_no = '1IS22IS045'
    praveen_student.department = 'Information Science and Engineering'
    praveen_student.semester = 5
    praveen_student.save()

    # Clear old achievements for fresh seed
    praveen_student.achievements.all().delete()

    # Create Sample Certificates
    cert1 = create_sample_certificate('sih_runnerup_praveen.png', 'Smart India Hackathon 2024 - 1st Runner Up', 'Praveen Kumar', 'Ministry of Education Innovation Cell', 'Hackathon')
    cert2 = create_sample_certificate('python_ds_cert_praveen.png', 'Python for Data Science & Machine Learning', 'Praveen Kumar', 'NPTEL / IIT Madras', 'Certification')
    cert3 = create_sample_certificate('basketball_vtu_praveen.png', 'VTU Inter-Collegiate Basketball Championship', 'Praveen Kumar', 'VTU Sports Directorate', 'Sports')
    cert4 = create_sample_certificate('aws_internship_praveen.png', 'Cloud Architecture Virtual Internship', 'Praveen Kumar', 'AWS Academy & AICTE', 'Internship')
    cert5 = create_sample_certificate('coding_olympiad_praveen.png', 'National Coding Olympiad - Regional Round', 'Praveen Kumar', 'GeeksforGeeks', 'Competition')
    cert6 = create_sample_certificate('web_bootcamp_praveen.png', 'Full Stack Web Development BootCamp', 'Praveen Kumar', 'IEEE Student Branch', 'Workshop')

    # Achievements for Praveen
    achievements_data = [
        {
            'title': 'Smart India Hackathon 2024 - 1st Runner Up',
            'category': 'Hackathon',
            'description': 'Secured 1st Runner Up in the Software Edition under the Smart Education theme. Built a localized learning platform for rural students with offline sync and low-bandwidth media streaming.',
            'achievement_date': date(2024, 8, 24),
            'organization': 'Ministry of Education Innovation Cell, Govt. of India',
            'certificate': cert1,
            'status': 'VERIFIED',
            'points': 100,
            'remarks': 'Certificate authenticated via MoE Portal verification QR code. Excellent achievement!',
            'verified_at': timezone.now() - timedelta(days=20),
        },
        {
            'title': 'Python for Data Science & Machine Learning',
            'category': 'Certification',
            'description': '12-week comprehensive certification covering advanced NumPy, Pandas, Scikit-learn, supervised learning algorithms, and real-world predictive modeling.',
            'achievement_date': date(2024, 7, 15),
            'organization': 'NPTEL / IIT Madras',
            'certificate': cert2,
            'status': 'VERIFIED',
            'points': 50,
            'remarks': 'Verified against NPTEL e-certificate registry (Score: 88% - Elite Gold).',
            'verified_at': timezone.now() - timedelta(days=35),
        },
        {
            'title': 'VTU Inter-Collegiate Basketball Championship',
            'category': 'Sports',
            'description': 'Represented the college team and reached semifinals in the VTU Inter-Collegiate Bengaluru Division tournament.',
            'achievement_date': date(2024, 6, 10),
            'organization': 'VTU Sports Directorate',
            'certificate': cert3,
            'status': 'VERIFIED',
            'points': 50,
            'remarks': 'Verified and confirmed by Physical Education Department Director.',
            'verified_at': timezone.now() - timedelta(days=50),
        },
        {
            'title': 'Cloud Architecture Virtual Internship',
            'category': 'Internship',
            'description': 'Completed an 8-week structured internship on AWS Cloud Services, Serverless architecture with Lambda, DynamoDB, API Gateway, and CloudWatch metrics deployment.',
            'achievement_date': date(2024, 9, 5),
            'organization': 'AWS Academy & AICTE',
            'certificate': cert4,
            'status': 'VERIFIED',
            'points': 150,
            'remarks': 'Internship completion badge and project report validated by Department Coordinator.',
            'verified_at': timezone.now() - timedelta(days=10),
        },
        {
            'title': 'National Coding Olympiad - Regional Round',
            'category': 'Competition',
            'description': 'Participated in the regional competitive programming round solving data structures and graph algorithm problems under timed constraints.',
            'achievement_date': date(2024, 9, 28),
            'organization': 'GeeksforGeeks & Coding Ninjas',
            'certificate': cert5,
            'status': 'PENDING',
            'points': 75,
            'remarks': 'Submitted by student. Under review by department verification coordinator.',
            'verified_at': None,
        },
        {
            'title': 'Full Stack Web Development 3-Day BootCamp',
            'category': 'Workshop',
            'description': 'Participated in a 3-day hands-on workshop building microservices, relational database schemas, and REST APIs.',
            'achievement_date': date(2024, 10, 2),
            'organization': 'IEEE Student Branch',
            'certificate': cert6,
            'status': 'PENDING',
            'points': 25,
            'remarks': 'Submitted by student. Under review by department verification coordinator.',
            'verified_at': None,
        },
        {
            'title': 'State Level Engineering Project Symposium',
            'category': 'Competition',
            'description': 'Submitted project abstract and demonstration for the regional tech symposium.',
            'achievement_date': date(2024, 5, 12),
            'organization': 'State Engineering Forum',
            'certificate': None,
            'status': 'REJECTED',
            'points': 75,
            'remarks': 'Proof document was missing participation certificate with official seal. Please re-upload.',
            'verified_at': timezone.now() - timedelta(days=60),
        },
    ]

    for item in achievements_data:
        ach = Achievement.objects.create(
            student=praveen_student,
            title=item['title'],
            category=item['category'],
            description=item['description'],
            achievement_date=item['achievement_date'],
            organization=item['organization'],
            certificate=item['certificate'],
            status=item['status'],
            points=item['points']
        )
        if hasattr(ach, 'verification'):
            ach.verification.status = item['status']
            ach.verification.remarks = item['remarks']
            ach.verification.verified_by = admin_user if item['status'] != 'PENDING' else None
            ach.verification.verified_at = item['verified_at']
            ach.verification.save()

    print(f"Praveen Kumar created with {praveen_student.achievements.count()} achievements. Verified Points: {praveen_student.get_merit_points()} ({praveen_student.get_badge()})")

    # 3. Create Additional Students for Realistic Leaderboard (Section 17)
    leaderboard_students_info = [
        {
            'username': 'ananya',
            'roll_no': '1IS22IS012',
            'name': 'Ananya Rao',
            'email': 'ananya.rao@vidyasetu.edu',
            'department': 'Information Science and Engineering',
            'semester': 5,
            'verified_achievements': [
                ('Winner - Google Solution Challenge 2024', 'Hackathon', 100),
                ('Research Paper Publication in IEEE Xplore', 'Competition', 75),
                ('Summer Research Internship at IISc Bangalore', 'Internship', 150),
                ('TensorFlow Developer Professional Certificate', 'Certification', 50),
                ('ACM-ICPC Asia Regionalist', 'Hackathon', 100),
                ('AI & Machine Learning Internship at Infosys', 'Internship', 150),
                ('College Classical Dance First Prize', 'Cultural', 50),
                ('Advanced Deep Learning Workshop', 'Workshop', 25),
            ] # Total: 700 pts (Merit Champion)
        },
        {
            'username': 'rohan',
            'roll_no': '1CS22CS089',
            'name': 'Rohan Sharma',
            'email': 'rohan.sharma@vidyasetu.edu',
            'department': 'Computer Science and Engineering',
            'semester': 5,
            'verified_achievements': [
                ('Flipkart GRiD 6.0 Robotics Track Finalist', 'Competition', 75),
                ('Full Stack Engineering Internship', 'Internship', 150),
                ('Docker Certified Associate', 'Certification', 50),
                ('DevFest 2024 Hackathon 2nd Place', 'Hackathon', 100),
                ('Cybersecurity Awareness Workshop', 'Workshop', 25),
                ('College Football League Captain', 'Sports', 50),
            ] # Total: 450 pts (Star Performer)
        },
        {
            'username': 'priya',
            'roll_no': '1IS22IS052',
            'name': 'Priya Nair',
            'email': 'priya.nair@vidyasetu.edu',
            'department': 'Information Science and Engineering',
            'semester': 5,
            'verified_achievements': [
                ('AWS Cloud Practitioner Certified', 'Certification', 50),
                ('Web3 Innovation Hackathon Participant', 'Hackathon', 100),
                ('Inter-College Drama & Skit Trophy', 'Cultural', 50),
                ('Kubernetes Fundamentals Workshop', 'Workshop', 25),
            ] # Total: 225 pts (Achiever)
        },
        {
            'username': 'karthik',
            'roll_no': '1EC22EC034',
            'name': 'Karthik V',
            'email': 'karthik.v@vidyasetu.edu',
            'department': 'Electronics and Communication',
            'semester': 5,
            'verified_achievements': [
                ('Embedded Systems & IoT Workshop', 'Workshop', 25),
                ('College Athletic Meet 400m Silver Medal', 'Sports', 50),
            ] # Total: 75 pts (Beginner)
        },
    ]

    for sdata in leaderboard_students_info:
        user, _ = User.objects.get_or_create(username=sdata['username'], defaults={'email': sdata['email']})
        user.set_password('student123')
        user.first_name = sdata['name'].split()[0]
        user.last_name = sdata['name'].split()[-1]
        user.save()

        student, _ = Student.objects.get_or_create(
            user=user,
            defaults={
                'student_id': f"VS-2022-{sdata['roll_no'][-3:]}",
                'roll_no': sdata['roll_no'],
                'name': sdata['name'],
                'email': sdata['email'],
                'department': sdata['department'],
                'semester': sdata['semester'],
            }
        )
        student.name = sdata['name']
        student.roll_no = sdata['roll_no']
        student.department = sdata['department']
        student.semester = sdata['semester']
        student.save()

        # Reset & populate achievements
        student.achievements.all().delete()
        for title, cat, pts in sdata['verified_achievements']:
            ach = Achievement.objects.create(
                student=student,
                title=title,
                category=cat,
                description=f"Verified co-curricular contribution in {cat}.",
                achievement_date=date(2024, 7, 1),
                organization="Accredited Academic / Industry Body",
                status='VERIFIED',
                points=pts
            )
            if hasattr(ach, 'verification'):
                ach.verification.status = 'VERIFIED'
                ach.verification.remarks = 'Verified by Evaluation Panel.'
                ach.verification.verified_by = admin_user
                ach.verification.verified_at = timezone.now() - timedelta(days=15)
                ach.verification.save()

        print(f"Added {student.name} with {student.get_merit_points()} points ({student.get_badge()}).")

    print("\n[OK] Seed completed successfully!")
    print("Demo Student Login: praveen / student123 (or Roll No: 1IS22IS045)")
    print("Admin Portal Login: admin / admin123")

if __name__ == '__main__':
    seed()
