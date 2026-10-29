/* AidBio site behaviour: theme, mobile menu, tabs, copy buttons, contact form. */
(function () {
  var root = document.documentElement;

  // Theme toggle (initial theme is set by the inline script in <head>).
  var toggle = document.getElementById('themeToggle');
  if (toggle) toggle.addEventListener('click', function () {
    var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('aidbio-theme', next); } catch (e) {}
    document.dispatchEvent(new CustomEvent('aidbio:theme'));
  });

  // Mobile menu.
  var menuBtn = document.getElementById('menuBtn');
  var menu = document.getElementById('mobileMenu');
  if (menuBtn && menu) {
    menuBtn.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', String(open));
    });
    menu.addEventListener('click', function (e) {
      if (e.target.closest('a')) { menu.classList.remove('open'); menuBtn.setAttribute('aria-expanded', 'false'); }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('open')) { menu.classList.remove('open'); menuBtn.setAttribute('aria-expanded', 'false'); menuBtn.focus(); }
    });
  }

  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  // Tabs (hero preview). Arrow keys move between tabs.
  document.querySelectorAll('[role="tablist"]').forEach(function (list) {
    var tabs = Array.prototype.slice.call(list.querySelectorAll('[role="tab"]'));
    function select(tab) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
        var panel = document.getElementById(t.getAttribute('aria-controls'));
        if (panel) panel.hidden = !on;
      });
      document.dispatchEvent(new CustomEvent('aidbio:tab', { detail: tab.dataset.tab }));
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(t); });
      t.addEventListener('keydown', function (e) {
        var n = e.key === 'ArrowRight' ? i + 1 : e.key === 'ArrowLeft' ? i - 1 : null;
        if (n === null) return;
        e.preventDefault();
        var target = tabs[(n + tabs.length) % tabs.length];
        select(target); target.focus();
      });
    });
  });

  // Pipeline stepper (accordion buttons).
  var steps = document.querySelectorAll('.step-item');
  steps.forEach(function (s) {
    s.addEventListener('click', function () {
      steps.forEach(function (o) { o.setAttribute('aria-expanded', String(o === s)); });
    });
  });

  // Copy-to-clipboard buttons: <button class="copy-btn" data-copy="text">.
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var text = btn.getAttribute('data-copy');
      var done = function () {
        var old = btn.textContent; btn.textContent = 'Copied!';
        setTimeout(function () { btn.textContent = old; }, 1800);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, done);
      else done();
    });
  });
})();
