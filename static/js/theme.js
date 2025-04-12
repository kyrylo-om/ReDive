const lightTheme = {
  '--header-bg': '#AE9EC4',
  '--container-bg': 'rgba(255, 255, 255, 0.3)',
  '--text-color': '#2d3436',
  '--accent-color': '#6c5ce7',
  '--search-bg': 'rgba(255, 255, 255, 0.9)',
  '--support-bg': 'rgba(0, 0, 0, 0.1)',
  '--search-text-color': 'black',
  '--header-shadow': '0 0 2rem rgba(0, 0, 0, 0.4)',
  '--btn-hover-bg': 'white',
  '--btn-hover-text': '#6c5ce7',
  '--theme-toggle-hover': 'rgba(0, 0, 0, 0.1)',
  '--filters-btn': 'rgba(0, 0, 0, 0.3)',
  '--filters-btn-hov': 'rgba(0, 0, 0, 0.5)',
};

const darkTheme = {
  '--header-bg': '#2b2735',
  '--container-bg': 'rgba(0, 0, 0, 0.5)',
  '--text-color': 'white',
  '--accent-color': '#a29bfe',
  '--search-bg': 'rgba(255, 255, 255, 0.5)',
  '--search-text-color': 'black',
  '--header-shadow': '0 0 2rem rgba(0, 0, 0, 0.4)',
  '--btn-hover-bg': 'white',
  '--btn-hover-text': '#a29bfe',
  '--theme-toggle-hover': 'rgba(255, 255, 255, 0.1)',
  '--filters-btn': 'rgba(255, 255, 255, 0.1)',
  '--filters-btn-hov': 'rgba(255, 255, 255, 0.4)',
};

function applyTheme(theme) {
  const root = document.documentElement;
  Object.entries(theme).forEach(([varName, value]) => {
    root.style.setProperty(varName, value);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const themeToggle = document.getElementById('theme-toggle');
  const savedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const initialTheme = savedTheme || (prefersDark ? 'dark' : 'light');

  const sunUrl = themeToggle.dataset.sunUrl;
  const moonUrl = themeToggle.dataset.moonUrl;

  function setTheme(themeName) {
    localStorage.setItem('theme', themeName);
    applyTheme(themeName === 'dark' ? darkTheme : lightTheme);
    themeToggle.innerHTML = themeName === 'dark'
      ? `<img class="theme-icon" src="${sunUrl}" alt="Light mode">`
      : `<img class="theme-icon" src="${moonUrl}" alt="Dark mode">`;
  }

  themeToggle.addEventListener('click', () => {
    const newTheme = localStorage.getItem('theme') === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
  });

  setTheme(initialTheme);

  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    if (!localStorage.getItem('theme')) {
      setTheme(e.matches ? 'dark' : 'light');
    }
  });
});
