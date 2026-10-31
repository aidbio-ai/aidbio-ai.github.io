/* Homepage-only research cycle and illustrated evidence exchange. No external runtime. */
(function () {
  'use strict';
  var root = document.querySelector('.workflow');
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  function text(node, key) {
    var lang = document.documentElement.lang === 'pt-BR' ? 'pt' : 'en';
    var copy = window.AIDBIO_STRINGS && window.AIDBIO_STRINGS[lang];
    node.setAttribute('data-i18n', key);
    if (copy && copy[key]) node.textContent = copy[key];
  }
  if (root) {
    var controls = Array.from(root.querySelectorAll('[data-flow-stage]'));
    var stageButtons = [1, 2, 3, 4].map(function (stage) {
      return root.querySelector('.workflow-pill[data-flow-stage="' + stage + '"]');
    });
    var details = Array.from(root.querySelectorAll('.workflow-detail'));
    var play = root.querySelector('[data-flow-play]');
    var mode = root.querySelector('[data-flow-mode]');
    var cycle = root.querySelector('[data-flow-cycle]');
    var canvas = root.querySelector('canvas');
    var ctx = canvas.getContext && canvas.getContext('2d');
    var selected = 1, preview = null, playing = !reduced.matches, full = false;
    var visible = false, frame = 0, last = null, elapsed = 0, oneCycle = false;
    var duration = 8000, phase = 0;
    var routes = [1, 2, 3, 4].map(function (i) {
      var path = root.querySelector('#wf-stream-quad-' + i);
      return { path: path, length: path.getTotalLength() };
    });
    var colors = ['#22c55e', '#38bdf8', '#d946ef', '#fb923c'];
    // The stage labels and vector regions share selection and keyboard controls.
    root.querySelectorAll('.infinity-hit-zone').forEach(function (zone) {
      zone.setAttribute('role', 'button'); zone.setAttribute('tabindex', '0');
    });
    controls.forEach(function (control) {
      control.setAttribute('aria-controls', 'workflow-detail-' + control.dataset.flowStage);
    });
    function render() {
      var stage = preview || selected;
      root.dataset.stage = String(stage);
      root.classList.toggle('is-paused', !playing);
      controls.forEach(function (control) {
        var value = Number(control.dataset.flowStage);
        control.classList.toggle('is-active', value === stage);
        if (control.matches('button, [role="button"]')) control.setAttribute('aria-pressed', String(value === selected));
      });
      details.forEach(function (panel, i) { panel.hidden = i + 1 !== stage; });
      for (var i = 1; i <= 4; i++) {
        var quad = root.querySelector('#wf-svg-quad-' + i);
        quad.style.opacity = full || i === stage ? '1' : '.32';
        root.querySelector('#wf-nodes-overlay-' + (i - 1)).style.opacity = full || i === stage ? '1' : '.25';
      }
      root.querySelector('#wf-svg-central-overpass').style.opacity = full || stage !== 2 ? '1' : '.4';
      text(root.querySelector('[data-flow-status]'), 'workflow.' + stage + '.label');
      text(play, reduced.matches ? 'flow.reduced' : playing ? 'flow.play' : 'flow.pause');
      play.setAttribute('aria-pressed', String(playing));
      play.disabled = reduced.matches;
      cycle.disabled = reduced.matches;
      mode.setAttribute('aria-pressed', String(full));
      text(mode, full ? 'flow.full' : 'flow.spotlight');
      draw();
    }
    function select(stage, user) {
      selected = stage; preview = null; elapsed = 0;
      if (user) { playing = false; oneCycle = false; }
      render(); schedule();
    }
    function draw() {
      if (!ctx || reduced.matches || !canvas.width || !canvas.height) return;
      var stage = preview || selected;
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.save(); ctx.scale(canvas.width / 800, canvas.height / 355);
      routes.forEach(function (route, j) {
        for (var k = 0; k < 8; k++) {
          var distance = ((phase / 6500 + k / 8) % 1) * route.length;
          var point = route.path.getPointAtLength(distance);
          ctx.beginPath(); ctx.arc(point.x, point.y, j + 1 === stage ? 3.2 : 2.2, 0, Math.PI * 2);
          ctx.fillStyle = j + 1 === stage || full ? '#ffffff' : colors[j];
          ctx.globalAlpha = j + 1 === stage || full ? .92 : .28; ctx.fill();
        }
      });
      ctx.restore();
    }
    function resize() {
      var box = canvas.getBoundingClientRect(), ratio = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.round(box.width * ratio); canvas.height = Math.round(box.height * ratio);
      draw();
    }
    function schedule() {
      if (!frame && visible && !document.hidden && playing && !reduced.matches) frame = requestAnimationFrame(tick);
    }
    function tick(now) {
      frame = 0;
      if (!visible || document.hidden || !playing || reduced.matches) { last = null; return; }
      var delta = last === null ? 0 : Math.min(now - last, 80); last = now;
      phase += delta;
      // A focused control or hovered stage gets uninterrupted reading time.
      var reading = document.activeElement.closest && document.activeElement.closest('[data-flow-stage], .workflow-detail');
      if (!preview && !(reading && root.contains(reading))) {
        elapsed += delta;
        if (elapsed >= duration) {
          var next = selected % 4 + 1;
          if (oneCycle && next === 1) { oneCycle = false; playing = false; }
          select(next, false);
        }
      }
      draw(); schedule();
    }
    function stopFrames() { if (frame) cancelAnimationFrame(frame); frame = 0; last = null; }
    controls.forEach(function (control) {
      var stage = Number(control.dataset.flowStage);
      control.addEventListener('pointerenter', function (event) {
        if (event.pointerType !== 'touch') { preview = stage; render(); }
      });
      control.addEventListener('pointerleave', function () {
        var focused = document.activeElement.closest && document.activeElement.closest('[data-flow-stage]');
        preview = focused && root.contains(focused) ? Number(focused.dataset.flowStage) : null; render();
      });
      control.addEventListener('focus', function () { preview = stage; render(); });
      control.addEventListener('blur', function () { preview = null; render(); });
      control.addEventListener('click', function () { select(stage, true); });
      control.addEventListener('keydown', function (event) {
        var index = event.key === 'ArrowRight' ? stage % 4 : event.key === 'ArrowLeft' ? (stage + 2) % 4 : event.key === 'Home' ? 0 : event.key === 'End' ? 3 : null;
        if (index !== null) { event.preventDefault(); select(index + 1, true); stageButtons[index].focus(); }
        else if (control.tagName.toLowerCase() !== 'button' && (event.key === 'Enter' || event.key === ' ')) { event.preventDefault(); select(stage, true); }
      });
    });
    play.addEventListener('click', function () { playing = !playing; oneCycle = false; preview = null; last = null; render(); schedule(); });
    mode.addEventListener('click', function () { full = !full; render(); });
    cycle.addEventListener('click', function () { oneCycle = true; playing = true; selected = 1; preview = null; elapsed = 0; last = null; render(); schedule(); });
    root.querySelectorAll('[data-flow-cap]').forEach(function (button) {
      button.addEventListener('click', function () {
        playing = false; oneCycle = false;
        var panel = button.closest('.workflow-detail'), number = panel.id.slice(-1);
        panel.querySelectorAll('[data-flow-cap]').forEach(function (other) { other.setAttribute('aria-pressed', String(other === button)); });
        panel.querySelectorAll('[data-flow-cap-panel]').forEach(function (note) { note.hidden = note.dataset.flowCapPanel !== button.dataset.flowCap; });
        select(Number(number), true);
      });
    });
    var layouts = [['C','T1','T2','T3'],['T2','C','T3','T1'],['T3','T2','C','T1']];
    var processed = false, node = 0;
    root.querySelectorAll('[data-flow-action]').forEach(function (button) {
      button.addEventListener('click', function () {
        var stage = Number(button.dataset.flowAction); select(stage, true);
        if (stage === 1) {
          root.querySelectorAll('.workflow-blocks > div').forEach(function (row, r) {
            var order = layouts[r].slice();
            for (var k = order.length - 1; k > 0; k--) {
              var j = Math.floor(Math.random() * (k + 1)), value = order[k]; order[k] = order[j]; order[j] = value;
            }
            row.querySelectorAll('b').forEach(function (cell, i) {
              cell.dataset.treatment = order[i]; cell.textContent = order[i];
            });
          });
        } else if (stage === 2) {
          processed = !processed; root.querySelector('.workflow-distributions').dataset.processed = String(processed);
          text(root.querySelector('[data-processing-label]'), processed ? 'flow.processed' : 'flow.raw');
        } else if (stage === 3) {
          node = (node + 1) % 3;
          root.querySelectorAll('[data-network-node]').forEach(function (circle) { circle.classList.toggle('is-selected', Number(circle.dataset.networkNode) === node); });
        } else {
          select(1, true); stageButtons[0].focus();
        }
      });
    });
    root.querySelectorAll('.workflow-cap-notes').forEach(function (notes) { notes.querySelectorAll('[data-flow-cap-panel]').forEach(function (note, i) { note.hidden = i !== 0; }); });
    root.querySelector('.workflow-controls').hidden = false;
    root.classList.add('is-interactive', 'is-outside-view');
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        visible = entries[0].isIntersecting; root.classList.toggle('is-outside-view', !visible);
        if (visible) { resize(); last = null; schedule(); } else stopFrames();
      }, { threshold: .08 }).observe(root);
    } else { visible = true; root.classList.remove('is-outside-view'); schedule(); }
    if ('ResizeObserver' in window) new ResizeObserver(resize).observe(canvas);
    else window.addEventListener('resize', resize);
    document.addEventListener('visibilitychange', function () { if (document.hidden) stopFrames(); else { last = null; schedule(); } });
    function motionChange() { if (reduced.matches) { playing = false; oneCycle = false; stopFrames(); } render(); }
    if (reduced.addEventListener) reduced.addEventListener('change', motionChange);
    else reduced.addListener(motionChange);
    document.addEventListener('aidbio:language', render);
    render(); resize();
  }
  // The AidWiki exchange illustrates retrieval and review; it never sends a query.
  document.querySelectorAll('[data-wiki-demo]').forEach(function (demo) {
    var button = demo.querySelector('[data-wiki-replay]'), timeouts = [];
    function reset() {
      timeouts.forEach(clearTimeout); timeouts = []; demo.classList.remove('is-replaying');
      demo.querySelectorAll('[data-evidence-step]').forEach(function (node) { node.classList.remove('is-current'); });
    }
    button.hidden = false;
    button.addEventListener('click', function () {
      reset(); if (reduced.matches) return;
      demo.classList.add('is-replaying');
      demo.querySelectorAll('[data-evidence-step]').forEach(function (node, i) {
        timeouts.push(setTimeout(function () { demo.querySelectorAll('li').forEach(function (li) { li.classList.toggle('is-current', li === node); }); }, i * 1000));
      });
      timeouts.push(setTimeout(reset, 4300));
    });
    function motionChange() { if (reduced.matches) reset(); }
    if (reduced.addEventListener) reduced.addEventListener('change', motionChange);
    document.addEventListener('aidbio:tab', function () { if (document.querySelector('#tab-wiki').getAttribute('aria-selected') !== 'true') reset(); });
  });
})();
