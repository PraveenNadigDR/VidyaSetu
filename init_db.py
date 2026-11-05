import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyasetu.settings')
django.setup()

from django.contrib.auth.models import User
from dashboard.models import MeritRule

# Create HOD User
if not User.objects.filter(username='hod').exists():
    User.objects.create_superuser('hod', 'hod@vidyasetu.edu', 'hod123')
    print("HOD user created: hod / hod123")

# Seed Merit Rules
rules = [
    ('Hackathon', 100),
    ('Certification', 50),
    ('Competition', 75),
    ('Sports', 50),
    ('Internship', 150),
    ('Workshop', 25),
    ('Cultural', 50),
]

for category, points in rules:
    MeritRule.objects.get_or_create(category=category, defaults={'points': points})
print("Merit Rules seeded.")

