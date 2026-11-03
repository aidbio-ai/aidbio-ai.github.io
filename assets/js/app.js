/* Shared controls: theme preference, mobile menu, accessible tabs, and copy buttons. */
(function () {
  var themeSelects = document.querySelectorAll('[data-theme-select]');
  function syncTheme() {
    themeSelects.forEach(function (select) {
      select.value = window.__aidbioTheme ? window.__aidbioTheme.getPreference() : 'system';
    });
  }
  themeSelects.forEach(function (select) {
    select.addEventListener('change', function () {
      if (window.__aidbioTheme) window.__aidbioTheme.setPreference(select.value);
    });
  });
  document.addEventListener('aidbio:theme', syncTheme);
  syncTheme();

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

  // Nested scientific examples. Cross-dissolve, with immediate reduced-motion fallback.
  document.querySelectorAll('[role="tablist"]').forEach(function (list) {
    var tabs = Array.prototype.slice.call(list.querySelectorAll('[role="tab"]'));
    var animations = [];
    var timer = 0;
    var family = list.closest('.hero-preview .family-stage > .panel');
    var playback = family && family.querySelector('[data-plot-play]');
    var motion = window.matchMedia('(prefers-reduced-motion: reduce)');
    var playing = !motion.matches;
    var inView = false;
    function schedule() {
      clearTimeout(timer);
      if (!playback || !playing || motion.matches || !inView || document.hidden || family.hidden || family.inert || document.querySelector('dialog[open]') || family.matches(':hover') || family.contains(document.activeElement)) return;
      timer = setTimeout(function () {
        var current = tabs.findIndex(function (tab) { return tab.getAttribute('aria-selected') === 'true'; });
        select(tabs[(current + 1) % tabs.length]);
      }, 6500);
    }
    function syncPlayback() {
      if (!playback) return;
      var lang = document.documentElement.lang === 'pt-BR' ? 'pt' : 'en';
      var key = playing ? 'plot.pause' : 'plot.play';
      var label = playback.querySelector('[data-i18n]');
      label.setAttribute('data-i18n', key);
      label.textContent = window.AIDBIO_STRINGS && window.AIDBIO_STRINGS[lang][key] || (playing ? 'Pause figures' : 'Play figures');
      playback.setAttribute('aria-pressed', String(playing));
      playback.disabled = motion.matches;
      schedule();
    }
    function select(tab) {
      if (tab.getAttribute('aria-selected') === 'true') return;
      animations.forEach(function (animation) { animation.cancel(); });
      animations = [];
      var previous = tabs.find(function (t) { return t.getAttribute('aria-selected') === 'true'; });
      var outgoing = previous && document.getElementById(previous.getAttribute('aria-controls'));
      var incoming = document.getElementById(tab.getAttribute('aria-controls'));
      var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      var dissolve = incoming && outgoing && incoming.animate && !reduced;
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
        var panel = document.getElementById(t.getAttribute('aria-controls'));
        if (panel) {
          panel.hidden = !on && !(dissolve && panel === outgoing);
          panel.inert = !on;
          panel.setAttribute('aria-hidden', String(!on));
        }
      });
      if (dissolve) {
        var fadeOut = outgoing.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 240, easing: 'ease-in-out' });
        var fadeIn = incoming.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 300, easing: 'ease-in-out' });
        animations = [fadeOut, fadeIn];
        fadeOut.onfinish = function () {
          if (previous.getAttribute('aria-selected') !== 'true') outgoing.hidden = true;
        };
      }
      document.dispatchEvent(new CustomEvent('aidbio:tab', { detail: tab.dataset.tab }));
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(t); });
      t.addEventListener('keydown', function (e) {
        var vertical = list.getAttribute('aria-orientation') === 'vertical';
        var n = e.key === 'ArrowRight' || vertical && e.key === 'ArrowDown' ? i + 1 : e.key === 'ArrowLeft' || vertical && e.key === 'ArrowUp' ? i - 1 : e.key === 'Home' ? 0 : e.key === 'End' ? tabs.length - 1 : null;
        if (n === null) return;
        e.preventDefault();
        var target = tabs[(n + tabs.length) % tabs.length];
        select(target); target.focus();
      });
    });
    if (playback) {
      playback.hidden = false;
      playback.addEventListener('click', function () { playing = !playing; syncPlayback(); });
      ['pointerenter', 'pointerleave', 'focusin'].forEach(function (event) { family.addEventListener(event, schedule); });
      family.addEventListener('focusout', function () { setTimeout(schedule, 0); });
      document.addEventListener('aidbio:tab', schedule);
      document.addEventListener('visibilitychange', schedule);
      document.addEventListener('aidbio:language', syncPlayback);
      function motionChange() { if (motion.matches) playing = false; syncPlayback(); }
      if (motion.addEventListener) motion.addEventListener('change', motionChange);
      else motion.addListener(motionChange);
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (entries) { inView = entries[0].isIntersecting; schedule(); }, { threshold: .15 }).observe(family);
      } else { inView = true; }
      syncPlayback();
    }
  });

  // Full-size scientific figures remain readable on narrow screens.
  var plotDialog = document.getElementById('plot-dialog');
  if (plotDialog && plotDialog.showModal) {
    var dialogMedia = plotDialog.querySelector('.plot-dialog-media');
    document.querySelectorAll('[data-expand-plot]').forEach(function (button) {
      button.addEventListener('click', function () {
        var plot = document.getElementById(button.dataset.expandPlot).querySelector('.preview-plot');
        var clone = plot.cloneNode(true);
        // SVG marker IDs must remain unique when the original figure is also present.
        clone.querySelectorAll('[id]').forEach(function (node) {
          var old = node.id;
          node.id = 'expanded-' + old;
          clone.querySelectorAll('[marker-end]').forEach(function (edge) {
            if (edge.getAttribute('marker-end') === 'url(#' + old + ')') edge.setAttribute('marker-end', 'url(#expanded-' + old + ')');
          });
        });
        dialogMedia.replaceChildren(clone);
        plotDialog.showModal();
      });
    });
    plotDialog.querySelector('[data-close-plot]').addEventListener('click', function () { plotDialog.close(); });
  }

  // Pipeline stepper (accordion buttons).
  var steps = document.querySelectorAll('.step-item');
  steps.forEach(function (s) {
    s.addEventListener('click', function () {
      steps.forEach(function (o) { o.setAttribute('aria-expanded', String(o === s)); });
    });
  });

  // Application stories: native details remain readable without JavaScript.
  var applicationCards = Array.prototype.slice.call(document.querySelectorAll('.app-card'));
  function diagramUrl(frame) {
    var language = document.documentElement.lang === 'pt-BR' ? 'pt' : 'en';
    var theme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
    var path = frame.getAttribute('data-diagram-' + language);
    return path ? path + '?embed=1&theme=' + theme : '';
  }
  function updateOpenDiagram(card) {
    var frame = card.querySelector('[data-diagram-en]');
    if (!frame || !card.open) return;
    var url = diagramUrl(frame);
    var full = card.querySelector('[data-diagram-link]');
    if (full) full.setAttribute('href', url.replace('?embed=1&', '?'));
    if (url && frame.getAttribute('src') !== url) frame.setAttribute('src', url);
  }
  applicationCards.forEach(function (card) {
    card.addEventListener('toggle', function () {
      if (card.open) {
        applicationCards.forEach(function (other) { if (other !== card) other.open = false; });
        updateOpenDiagram(card);
      } else {
        var diagram = card.querySelector('[data-diagram-en]');
        if (diagram) diagram.removeAttribute('src');
      }
      if (card.id === 'app-aidweather-report') {
        var report = card.querySelector('[data-report-src]');
        if (report && card.open && !report.getAttribute('src')) report.src = report.dataset.reportSrc;
        if (report && !card.open) report.removeAttribute('src');
      }
    });
  });
  document.addEventListener('aidbio:language', function () { applicationCards.forEach(updateOpenDiagram); });
  document.addEventListener('aidbio:theme', function () { applicationCards.forEach(updateOpenDiagram); });
  function openApplicationHash() {
    var target = document.getElementById(location.hash.slice(1));
    if (target && target.classList.contains('app-card')) target.open = true;
    if (target && target.classList.contains('application-sheet')) {
      var tab = document.getElementById(target.getAttribute('aria-labelledby'));
      if (tab) tab.click();
      // Reveal hidden destinations before positioning an incoming deep link.
      requestAnimationFrame(function () { target.scrollIntoView({ block: 'start', behavior: 'instant' }); });
    }
  }
  window.addEventListener('hashchange', openApplicationHash);
  document.querySelectorAll('a[href^="#app-"]').forEach(function (link) {
    link.addEventListener('click', function () {
      // A repeated link does not emit hashchange after the reader switches panels.
      if (link.hash === location.hash) openApplicationHash();
    });
  });
  openApplicationHash();

  // Copy-to-clipboard buttons: <button class="copy-btn" data-copy="text">.
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var text = btn.getAttribute('data-copy');
      var lang = document.documentElement.lang === 'pt-BR' ? 'pt' : 'en';
      var strings = window.AIDBIO_STRINGS && window.AIDBIO_STRINGS[lang];
      var translated = function (key, fallback) { return strings && strings[key] || fallback; };
      var done = function () {
        var old = btn.textContent; btn.textContent = translated('apps.copied', 'Copied!');
        setTimeout(function () { btn.textContent = old; }, 1800);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, function () { btn.textContent = translated('apps.copyfallback', 'Select and copy'); });
      else btn.textContent = translated('apps.copyfallback', 'Select and copy');
    });
  });
})();
