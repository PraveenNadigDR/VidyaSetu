// Vidya Setu - Student Dashboard Vanilla JavaScript Interactions

document.addEventListener('DOMContentLoaded', function () {
  // 1. Mobile Sidebar Toggle
  const mobileToggle = document.getElementById('mobileMenuToggle');
  const sidebar = document.getElementById('sidebar');
  const sidebarOverlay = document.getElementById('sidebarOverlay');

  if (mobileToggle && sidebar) {
    mobileToggle.addEventListener('click', function () {
      sidebar.classList.toggle('open');
      if (sidebarOverlay) {
        sidebarOverlay.classList.toggle('active');
      }
    });
  }

  if (sidebarOverlay && sidebar) {
    sidebarOverlay.addEventListener('click', function () {
      sidebar.classList.remove('open');
      sidebarOverlay.classList.remove('active');
    });
  }

  // 2. Alert Dismissal
  const alertCloseButtons = document.querySelectorAll('.alert-close');
  alertCloseButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      const alert = this.closest('.alert');
      if (alert) {
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-6px)';
        alert.style.transition = 'all 0.2s ease';
        setTimeout(() => alert.remove(), 200);
      }
    });
  });

  // 3. File Input Name Display Preview
  const fileInput = document.querySelector('.form-file-input');
  const fileLabel = document.getElementById('fileUploadText');

  if (fileInput && fileLabel) {
    fileInput.addEventListener('change', function () {
      if (this.files && this.files.length > 0) {
        const file = this.files[0];
        const fileSizeMB = (file.size / (1024 * 1024)).toFixed(2);
        fileLabel.innerHTML = `<strong>Selected:</strong> ${file.name} (${fileSizeMB} MB)`;
      } else {
        fileLabel.innerHTML = 'Click to select or drag and drop certificate file (PDF, JPG, PNG)';
      }
    });
  }

  // 4. Auto-dismiss alerts after 5 seconds
  const autoDismissAlerts = document.querySelectorAll('.alert-success, .alert-info');
  autoDismissAlerts.forEach(function (alert) {
    setTimeout(function () {
      if (alert && alert.parentElement) {
        alert.style.opacity = '0';
        alert.style.transition = 'opacity 0.4s ease';
        setTimeout(() => alert.remove(), 400);
      }
    }, 5000);
  });
});

