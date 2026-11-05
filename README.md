# VIDYA SETU (विद्या सेतु)
### Digital Merit Wallet for Student Achievements
**Phase II Mini-Project Intermediate Working Module**  
*Department of Information Science and Engineering*

---

## 📌 Project Overview
**Vidya Setu** is a decentralized, digital achievement and merit management platform for engineering colleges. It enables students to maintain a verified digital portfolio of co-curricular, extracurricular, and academic accomplishments with cryptographically and faculty-validated proof documents.

This intermediate deliverable encompasses the complete **Student-Side Module**, featuring:
- Dynamic Student Merit Dashboard
- Four real-time database summary statistics (Total, Verified, Pending, Merit Points)
- 4-Tier Merit Badge Progression (Beginner, Achiever, Star Performer, Merit Champion)
- Achievement Management (CRUD & Category/Status Filters + Search)
- File Upload Validation (PDF, JPG, PNG stored in `media/certificates/`)
- Student Verification Lifecycle Status Interface (Submitted → Under Review → Verified/Rejected)
- Digital Certificate Repository & Document Viewer
- Institutional Merit Leaderboard with rank honors
- Student Academic Identity & Credentials Profile
- Django Admin interface for evaluation coordinator management

---

## 🛠️ Technology Stack
- **Backend:** Python 3.13, Django 6.1
- **Database:** SQLite (Development) — structured via Django ORM for direct migration to MySQL in production
- **Frontend:** Semantic HTML5, Custom Responsive CSS3 (Zero 3rd-party CSS bloat, CSS variables), Vanilla JavaScript
- **Media Engine:** Pillow 12.3 (Digital certificate generation & rendering)
- **Authentication:** Django Built-in Authentication with dual-lookup (USN / Username)

---

## 🚀 Quickstart Guide

### 1. Activate the Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Run Database Migrations (already applied)
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 3. Re-seed Demo Data (if needed)
```powershell
python seed_demo_data.py
```

### 4. Run the Development Server
```powershell
python manage.py runserver
```
Navigate to: **`http://127.0.0.1:8000/`**

---

## 🔑 Demo Login Credentials

### Student Portal (`/login/` or `/`)
| Parameter | Value |
| :--- | :--- |
| **Username** | `praveen` *(or USN: `1IS22IS045`)* |
| **Password** | `student123` |
| **Student** | Praveen Kumar (5th Sem ISE) |
| **Current Standing**| 350 Verified Merit Points &bull; **Star Performer** |

### Additional Leaderboard Students
| USN | Student Name | Password | Points | Badge |
| :--- | :--- | :--- | :--- | :--- |
| `1IS22IS012` | Ananya Rao | `student123` | 700 pts | Merit Champion |
| `1CS22CS089` | Rohan Sharma | `student123` | 450 pts | Star Performer |
| `1IS22IS052` | Priya Nair | `student123` | 225 pts | Achiever |
| `1EC22EC034` | Karthik V | `student123` | 75 pts | Beginner |

### Faculty / Admin Portal (`/admin/`)
| Parameter | Value |
| :--- | :--- |
| **Username** | `admin` |
| **Password** | `admin123` |
| **Role** | Department Evaluation Coordinator |

---

## 📊 Merit Points & Badge System

### Points Allocation Table
| Category | Default Merit Points |
| :--- | :--- |
| **Internship** | +150 Points |
| **Hackathon** | +100 Points |
| **Competition** | +75 Points |
| **Certification** | +50 Points |
| **Sports** | +50 Points |
| **Cultural** | +50 Points |
| **Workshop** | +25 Points |

> **Rule:** Only achievements with **`VERIFIED`** status contribute to the student's active merit wallet score.

### Badge Progression Hierarchy
- **0 – 99 pts:** `Beginner` (Tier 1)
- **100 – 299 pts:** `Achiever` (Tier 2)
- **300 – 599 pts:** `Star Performer` (Tier 3)
- **600+ pts:** `Merit Champion` (Tier 4)

---

## 📂 Project Architecture

```
Vidya Setu/
│
├── venv/                       # Python virtual environment
├── manage.py                   # Django command-line utility
├── db.sqlite3                  # Local development database
├── seed_demo_data.py           # Demo seeding script
├── test_live_server.py         # Automated HTTP verification script
│
├── vidyasetu/                  # Project configuration
│   ├── __init__.py
│   ├── settings.py             # Settings (Static, Media, Auth, TZ)
│   ├── urls.py                 # Root URL configuration
│   ├── asgi.py
│   └── wsgi.py
│
├── dashboard/                  # Core student application
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── templates/dashboard/
│   │   ├── base.html           # Master layout with sidebar & topbar
│   │   ├── login.html          # Clean dual-mode login
│   │   ├── dashboard.html      # Main student dashboard
│   │   ├── achievements.html   # Searchable achievements list
│   │   ├── add_achievement.html# Achievement submission form
│   │   ├── achievement_detail.html # Detail & verification pipeline
│   │   ├── certificates.html   # Digital certificate wallet gallery
│   │   ├── leaderboard.html    # Institutional merit leaderboard
│   │   └── profile.html        # Student credentials & profile
│   ├── static/dashboard/
│   │   ├── css/style.css       # Academic styling (custom CSS variables)
│   │   └── js/dashboard.js     # Responsive toggle & UI interactions
│   ├── admin.py                # Admin registrations & bulk actions
│   ├── apps.py
│   ├── forms.py                # AchievementForm with file validation
│   ├── models.py               # Student, Achievement, Verification
│   ├── tests.py                # Test suite (9 test cases passed)
│   ├── urls.py                 # App routing
│   └── views.py                # Views & query isolation
│
└── media/                      # Uploaded and sample certificates
    └── certificates/
        ├── aws_internship_praveen.png
        ├── basketball_vtu_praveen.png
        ├── coding_olympiad_praveen.png
        ├── python_ds_cert_praveen.png
        ├── sih_runnerup_praveen.png
        └── web_bootcamp_praveen.png
```

---

## 🔮 Scope for Next Phase (Phase III)
1. **Faculty Reviewer Dashboard:** Dedicated faculty login with pending queue approvals, rejection remarks, and batch verification.
2. **QR Code Verification:** Public QR verification endpoint to validate certificate authenticity without logging in.
3. **Database Migration to MySQL:** Seamless migration by updating `DATABASES` dictionary in `vidyasetu/settings.py` to `django.db.backends.mysql`.

