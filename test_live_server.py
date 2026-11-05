import urllib.request
import urllib.parse
import http.cookiejar
import re

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# 1. GET login page to get CSRF token
resp = opener.open('http://127.0.0.1:8000/login/')
html = resp.read().decode('utf-8')
csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', html)
csrf_token = csrf_match.group(1) if csrf_match else ''

# 2. POST login credentials for demo student
data = urllib.parse.urlencode({
    'username': 'praveen',
    'password': 'student123',
    'csrfmiddlewaretoken': csrf_token
}).encode('utf-8')

req = urllib.request.Request(
    'http://127.0.0.1:8000/login/',
    data=data,
    headers={'Referer': 'http://127.0.0.1:8000/login/'}
)
resp = opener.open(req)
print(f"Login request finished with status: {resp.status}")

# 3. Test all important pages
urls = [
    '/dashboard/',
    '/achievements/',
    '/achievements/add/',
    '/certificates/',
    '/leaderboard/',
    '/profile/',
]

for u in urls:
    r = opener.open('http://127.0.0.1:8000' + u)
    content = r.read().decode('utf-8')
    title_match = re.search(r'<title>(.*?)</title>', content)
    title = title_match.group(1).strip() if title_match else 'No Title'
    print(f"Tested {u:20} -> Status {r.status} | Title: {title}")

# Test individual achievement detail with one of Praveen's achievements
r = opener.open('http://127.0.0.1:8000/achievements/28/')
content = r.read().decode('utf-8')
title_match = re.search(r'<title>(.*?)</title>', content)
title = title_match.group(1).strip() if title_match else 'No Title'
print(f"Tested {'/achievements/28/':20} -> Status {r.status} | Title: {title}")

# 4. Admin Portal Authentication & Management Test
admin_cj = http.cookiejar.CookieJar()
admin_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(admin_cj))

admin_login_page = admin_opener.open('http://127.0.0.1:8000/admin/login/').read().decode('utf-8')
admin_csrf = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', admin_login_page).group(1)

admin_data = urllib.parse.urlencode({
    'username': 'admin',
    'password': 'admin123',
    'csrfmiddlewaretoken': admin_csrf,
    'next': '/admin/'
}).encode('utf-8')

admin_req = urllib.request.Request(
    'http://127.0.0.1:8000/admin/login/',
    data=admin_data,
    headers={'Referer': 'http://127.0.0.1:8000/admin/login/'}
)
admin_resp = admin_opener.open(admin_req)
print(f"\nAdmin login status: {admin_resp.status}")

for path in ['/admin/dashboard/student/', '/admin/dashboard/achievement/', '/admin/dashboard/verification/']:
    r = admin_opener.open('http://127.0.0.1:8000' + path)
    print(f"Admin {path:32} -> Status {r.status}")

print("\nAll live HTTP endpoint checks passed successfully!")

