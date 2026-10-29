/* Apply the user's preference before styles load; Auto follows the operating system. */
(function () {
  'use strict';
  var root = document.documentElement;
  var key = 'aidbio-theme-preference';
  var media = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  function valid(value) { return ['system', 'light', 'dark'].indexOf(value) !== -1; }
  function stored() {
    try {
      var current = localStorage.getItem(key);
      if (valid(current)) return current;
      var legacy = localStorage.getItem('aidbio-theme');
      if (legacy === 'light' || legacy === 'dark') return legacy;
    } catch (error) { /* Storage is optional. */ }
    return 'system';
  }
  var preference = stored();
  function apply() {
    var theme = preference === 'system' ? (media && media.matches ? 'dark' : 'light') : preference;
    root.setAttribute('data-theme', theme);
    root.setAttribute('data-theme-preference', preference);
    root.style.colorScheme = theme;
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', theme === 'dark' ? '#080B0E' : '#F8FAFC');
    document.dispatchEvent(new CustomEvent('aidbio:theme', { detail: theme }));
  }
  function setPreference(value) {
    if (!valid(value)) return;
    preference = value;
    try { localStorage.setItem(key, value); } catch (error) { /* Keep the in-page choice. */ }
    apply();
  }
  function systemChanged() { if (preference === 'system') apply(); }
  if (media && media.addEventListener) media.addEventListener('change', systemChanged);
  else if (media && media.addListener) media.addListener(systemChanged);
  window.addEventListener('storage', function (event) {
    if (event.key === key || event.key === 'aidbio-theme' || event.key === null) {
      preference = stored();
      apply();
    }
  });
  window.__aidbioTheme = {
    key: key,
    setPreference: setPreference,
    getPreference: function () { return preference; }
  };
  apply();
})();
