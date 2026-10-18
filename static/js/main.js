/**
 * Geospatial Portal - Main Application Logic
 * Supports Global Theme Switching (Light/Dark), Project Category Filters,
 * ScrollSpy Active Navigation, and Interactive Copy Helpers
 */

document.addEventListener('DOMContentLoaded', () => {
  initThemeToggle();
  initProjectFilters();
  initScrollSpy();
  initMobileMenu();
   initScrollJumpButton();
});

/**
 * Theme Toggle: Light Background by Default, Click to Switch to Dark Mode,
 * Always Resets to Light Mode on Page Refresh
 */
function initThemeToggle() {
  const themeToggleBtn = document.getElementById('theme-toggle');
  const themeLabel = document.getElementById('theme-label');
  const themeIcon = document.getElementById('theme-icon');

  if (!themeToggleBtn) return;

  // Clear any previously persisted theme preference so refresh always resets to light mode
  try {
    localStorage.removeItem('theme-mode');
  } catch (e) {
    // Ignore environments where localStorage is restricted
  }

  function setLightMode() {
    document.documentElement.classList.remove('dark-theme', 'dark');
    document.documentElement.classList.add('light-theme');
    if (themeLabel) themeLabel.innerText = 'Dark';
    if (themeIcon) themeIcon.innerHTML = '🌙';
    themeToggleBtn.setAttribute('title', 'Switch to Dark Mode');
    themeToggleBtn.setAttribute('aria-label', 'Switch to Dark Mode');
  }

  function setDarkMode() {
    document.documentElement.classList.remove('light-theme');
    document.documentElement.classList.add('dark-theme', 'dark');
    if (themeLabel) themeLabel.innerText = 'Light';
    if (themeIcon) themeIcon.innerHTML = '☀️';
    themeToggleBtn.setAttribute('title', 'Switch to Light Mode');
    themeToggleBtn.setAttribute('aria-label', 'Switch to Light Mode');
  }

  // Always enforce Light Mode on initial load and page refresh
  setLightMode();

  themeToggleBtn.addEventListener('click', () => {
    const isDark = document.documentElement.classList.contains('dark-theme') || 
                   document.documentElement.classList.contains('dark');
    if (isDark) {
      setLightMode();
    } else {
      setDarkMode();
    }
  });
}

/**
 * Filter Projects by Category
 */
function initProjectFilters() {
  const filterButtons = document.querySelectorAll('[data-purpose="filter-tabs"] button');
  const projectCards = document.querySelectorAll('[data-purpose="project-card"]');

  if (!filterButtons.length || !projectCards.length) return;

  filterButtons.forEach(button => {
    button.addEventListener('click', () => {
      // Update active state of buttons
      filterButtons.forEach(btn => {
        btn.classList.remove('theme-btn-primary', 'font-semibold', 'shadow-sm');
        btn.classList.add('theme-card');
      });
      button.classList.remove('theme-card');
      button.classList.add('theme-btn-primary', 'font-semibold', 'shadow-sm');

      const filterCategory = button.getAttribute('data-filter') || 'all';

      projectCards.forEach(card => {
        const cardCategory = card.getAttribute('data-category') || '';
        if (filterCategory === 'all' || cardCategory.includes(filterCategory)) {
          card.style.display = 'flex';
          card.classList.remove('opacity-0', 'scale-95');
          card.classList.add('opacity-100', 'scale-100');
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
}

/**
 * ScrollSpy: Automatically Highlight Active Navigation Links on Scroll
 */
function initScrollSpy() {
  const sections = document.querySelectorAll('section[id], div[id="map-section"]');
  const navLinks = document.querySelectorAll('nav[data-purpose="nav-links"] a');

  if (!sections.length || !navLinks.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        navLinks.forEach(link => {
          if (link.getAttribute('href') === `#${id}`) {
            link.classList.add('text-emerald-400');
            link.classList.remove('opacity-75');
          } else {
            link.classList.remove('text-emerald-400');
          }
        });
      }
    });
  }, {
    rootMargin: '-30% 0px -60% 0px'
  });

  sections.forEach(sec => observer.observe(sec));
}

/**
 * Mobile Navigation Drawer Toggle
 */
function initMobileMenu() {
  const btn = document.getElementById('mobile-menu-btn');
  const menu = document.getElementById('mobile-menu');
  if (!btn || !menu) return;

  btn.addEventListener('click', () => {
    menu.classList.toggle('hidden');
  });

  menu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      menu.classList.add('hidden');
    });
  });
}

/**
 * Scroll Jump Button
 * - Appears after 120px of scroll
 * - Down arrow until the user crosses the midpoint of the page → scrolls to bottom
 * - Up arrow from midpoint onward → scrolls to top
 */
function initScrollJumpButton() {
  const btn      = document.getElementById('scroll-jump-btn');
  const iconDown = document.getElementById('scroll-icon-down');
  const iconUp   = document.getElementById('scroll-icon-up');
  if (!btn) return;

  const SHOW_THRESHOLD = 120; // px scrolled before the button appears

  const updateButton = () => {
    const scrolled   = window.scrollY;
    const docHeight  = document.documentElement.scrollHeight - window.innerHeight;
    const midpoint   = docHeight / 2;

    // Show/hide after threshold
    if (scrolled > SHOW_THRESHOLD) {
      btn.classList.remove('opacity-0', 'pointer-events-none');
    } else {
      btn.classList.add('opacity-0', 'pointer-events-none');
    }

    // Icon direction: down before midpoint, up after
    const goUp = scrolled >= midpoint;

    if (goUp) {
      iconDown?.classList.add('hidden');
      iconUp?.classList.remove('hidden');
      btn.setAttribute('aria-label', 'Scroll to top');
      btn.setAttribute('title', 'Scroll to top');
    } else {
      iconUp?.classList.add('hidden');
      iconDown?.classList.remove('hidden');
      btn.setAttribute('aria-label', 'Scroll to bottom');
      btn.setAttribute('title', 'Scroll to bottom');
    }
  };

  btn.addEventListener('click', () => {
    const scrolled  = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const goUp      = scrolled >= docHeight / 2;

    if (goUp) {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
      window.scrollTo({ top: document.documentElement.scrollHeight, behavior: 'smooth' });
    }
  });

  window.addEventListener('scroll', updateButton, { passive: true });
  window.addEventListener('resize', updateButton);
  updateButton();
}