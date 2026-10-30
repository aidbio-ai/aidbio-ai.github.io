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

  // Service lifecycle: hover/focus preview a stage; activation saves the selection.
  // All descriptions stay in the DOM so i18n and the no-script fallback share copy.
  document.querySelectorAll('.workflow').forEach(function (workflow) {
    var buttons = Array.prototype.slice.call(workflow.querySelectorAll('[data-workflow-step]'));
    var panels = Array.prototype.slice.call(workflow.querySelectorAll('.workflow-detail'));
    if (!buttons.length || buttons.length !== panels.length) return;
    var selected = buttons[0];
    function show(button) {
      buttons.forEach(function (item) {
        var active = item === button;
        item.classList.toggle('is-active', active);
        item.setAttribute('aria-pressed', String(item === selected));
        document.getElementById(item.getAttribute('aria-controls')).hidden = !active;
      });
    }
    function restore() {
      var focused = buttons.find(function (button) { return button === document.activeElement; });
      show(focused || selected);
    }
    buttons.forEach(function (button) {
      button.disabled = false;
      button.addEventListener('pointerenter', function (event) {
        if (event.pointerType !== 'touch') show(button);
      });
      button.addEventListener('focus', function () { show(button); });
      button.addEventListener('click', function () { selected = button; show(button); });
    });
    workflow.querySelector('.workflow-steps').addEventListener('pointerleave', restore);
    workflow.addEventListener('focusout', function (event) {
      if (buttons.indexOf(event.relatedTarget) === -1) show(selected);
    });
    show(selected);
    workflow.classList.add('is-interactive');
  });

  // Nested scientific examples. Cross-dissolve, with immediate reduced-motion fallback.
  document.querySelectorAll('[role="tablist"]').forEach(function (list) {
    var tabs = Array.prototype.slice.call(list.querySelectorAll('[role="tab"]'));
    var animations = [];
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
        var n = e.key === 'ArrowRight' ? i + 1 : e.key === 'ArrowLeft' ? i - 1 : e.key === 'Home' ? 0 : e.key === 'End' ? tabs.length - 1 : null;
        if (n === null) return;
        e.preventDefault();
        var target = tabs[(n + tabs.length) % tabs.length];
        select(target); target.focus();
      });
    });
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
  }
  window.addEventListener('hashchange', openApplicationHash);
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
