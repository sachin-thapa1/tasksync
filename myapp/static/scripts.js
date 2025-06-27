document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('darkToggle');
  const body = document.body;

  if (!toggle) {
    console.warn("Dark mode toggle not found!");
    return;
  }

  // Load saved theme
  const savedTheme = localStorage.getItem('theme') || 'light';
  body.setAttribute('data-theme', savedTheme);
  toggle.checked = savedTheme === 'dark';

  // Toggle theme on change
  toggle.addEventListener('change', () => {
    const newTheme = toggle.checked ? 'dark' : 'light';
    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
  });

  // Popup functions for notifications
  window.showPopup = function() {
    document.getElementById('popup')?.classList.remove('hidden');
  };

  window.hidePopup = function() {
    document.getElementById('popup')?.classList.add('hidden');
  };
});