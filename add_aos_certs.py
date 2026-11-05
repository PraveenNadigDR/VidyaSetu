with open('dashboard/templates/dashboard/certificates.html', 'r') as f:
    content = f.read()

content = content.replace('<div class="col">', '<div class="col" data-aos="zoom-in" data-aos-anchor-placement="top-bottom">')

with open('dashboard/templates/dashboard/certificates.html', 'w') as f:
    f.write(content)

