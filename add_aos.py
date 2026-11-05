with open('dashboard/templates/dashboard/dashboard.html', 'r') as f:
    content = f.read()

content = content.replace('<div class="col-sm-6 col-xl-3">', '<div class="col-sm-6 col-xl-3" data-aos="fade-up" data-aos-delay="200">', 1)
content = content.replace('<div class="col-sm-6 col-xl-3">', '<div class="col-sm-6 col-xl-3" data-aos="fade-up" data-aos-delay="300">', 1)
content = content.replace('<div class="col-sm-6 col-xl-3">', '<div class="col-sm-6 col-xl-3" data-aos="fade-up" data-aos-delay="400">', 1)

content = content.replace('<div class="card border-0 shadow-sm mb-4">', '<div class="card border-0 shadow-sm mb-4" data-aos="fade-up" data-aos-delay="100">')
content = content.replace('<!-- Recent Achievements -->\n  <div class="col-lg-8">', '<!-- Recent Achievements -->\n  <div class="col-lg-8" data-aos="fade-up" data-aos-delay="200">')
content = content.replace('<!-- Quick Actions -->\n  <div class="col-lg-4">', '<!-- Quick Actions -->\n  <div class="col-lg-4" data-aos="fade-up" data-aos-delay="300">')

with open('dashboard/templates/dashboard/dashboard.html', 'w') as f:
    f.write(content)

