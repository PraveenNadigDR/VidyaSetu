with open('dashboard/templates/dashboard/leaderboard.html', 'r') as f:
    content = f.read()

content = content.replace('<div class="position-relative overflow-hidden bg-primary bg-gradient text-white p-4 p-md-5 rounded-4 mb-4 d-flex justify-content-between align-items-center shadow">', '<div class="position-relative overflow-hidden bg-primary bg-gradient text-white p-4 p-md-5 rounded-4 mb-4 d-flex justify-content-between align-items-center shadow" data-aos="fade-down">')
content = content.replace('<div class="card shadow-sm border-0 mb-4 rounded-4">', '<div class="card shadow-sm border-0 mb-4 rounded-4" data-aos="fade-up" data-aos-delay="100">')

with open('dashboard/templates/dashboard/leaderboard.html', 'w') as f:
    f.write(content)

