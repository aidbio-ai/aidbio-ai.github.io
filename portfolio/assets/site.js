
(() => {
  document.querySelectorAll('img[data-fallback]').forEach(img => {
    img.addEventListener('error', () => {
      img.style.display='none';
      const fb=img.parentElement.querySelector('.paper-fallback');
      if(fb) fb.style.display='grid';
    });
    img.addEventListener('load', () => {
      const fb=img.parentElement.querySelector('.paper-fallback');
      if(fb) fb.style.display='none';
    });
  });
})();

(() => {
  const themeApi = window.__aidbioTheme;
  if (!themeApi) return;
  const buttons = Array.from(document.querySelectorAll('.theme-option'));
  const STORAGE_KEY = themeApi.key;
  const mediaQuery = themeApi.mediaQuery;

  function getPreference() {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored === 'system' || stored === 'light' || stored === 'dark') return stored;
    return themeApi.getStoredPreference();
  }
  function syncThemeButtons(preference) {
    buttons.forEach((button) => {
      button.setAttribute('aria-pressed', String(button.dataset.themeChoice === preference));
    });
  }
  function setPreference(preference) {
    localStorage.setItem(STORAGE_KEY, preference);
    themeApi.applyTheme(preference);
    syncThemeButtons(preference);
  }
  buttons.forEach((button) => {
    button.addEventListener('click', () => setPreference(button.dataset.themeChoice));
  });
  mediaQuery.addEventListener('change', () => {
    const preference = getPreference();
    if (preference === 'system') {
      themeApi.applyTheme('system');
      syncThemeButtons('system');
    }
  });
  syncThemeButtons(getPreference());
})();

(() => {
  const menuToggle = document.getElementById('menu-toggle');
  const mobileMenu = document.getElementById('mobile-menu');
  if (!menuToggle || !mobileMenu) return;

  function closeMenu() {
    mobileMenu.classList.remove('open');
    menuToggle.setAttribute('aria-expanded', 'false');
    menuToggle.setAttribute('aria-label', 'Open menu');
  }
  menuToggle.addEventListener('click', () => {
    const open = mobileMenu.classList.toggle('open');
    menuToggle.setAttribute('aria-expanded', String(open));
    menuToggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  });
  mobileMenu.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));
})();
