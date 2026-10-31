/* Homepage-only adaptation of the supplied infinity workflow. No external runtime. */
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
    var stageButtons = [1, 2, 3, 4].map(function (i) { return root.querySelector('.workflow-pill[data-flow-stage="' + i + '"]'); });
    var details = Array.from(root.querySelectorAll('.workflow-detail'));
    var play = root.querySelector('[data-flow-play]'), mode = root.querySelector('[data-flow-mode]'), wave = root.querySelector('[data-flow-wave]');
    var canvas = root.querySelector('canvas'), ctx = canvas.getContext && canvas.getContext('2d');
    var selected = 1, preview = null, playing = !reduced.matches, full = false;
    var visible = false, frame = 0, last = null, elapsed = 0, phase = 0;
    var duration = 6500, burstParticles = [], waveAge = -1, waveStage = 0;
    var colors = ['#22c55e', '#0284c7', '#d946ef', '#f97316'];
    var centers = [[225,245], [225,85], [575,155], [545,265]];
    var routes = [1, 2, 3, 4].map(function (i) {
      var path = root.querySelector('#wf-stream-quad-' + i);
      return { path: path, length: path.getTotalLength() };
    });
    var normalized = true, hub = 0;
    var hubs = [['MYB44-Regulator', '0.96', '+0.42'], ['NRT2.1-Transporter', '0.93', '+0.37'], ['HSP70-Chaperone', '0.91', '+0.29']];
    root.querySelectorAll('.infinity-hit-zone').forEach(function (zone) {
      zone.setAttribute('role', 'button'); zone.setAttribute('tabindex', '0');
    });
    controls.forEach(function (control) { control.setAttribute('aria-controls', 'workflow-detail-' + control.dataset.flowStage); });
    var hubControl = root.querySelector('[data-flow-hub]');
    hubControl.setAttribute('role', 'button'); hubControl.setAttribute('tabindex', '0');
    function highlight() {
      var focus = preview || selected;
      root.dataset.focusStage = String(focus);
      for (var i = 1; i <= 4; i++) {
        var quad = root.querySelector('#wf-svg-quad-' + i), active = i === focus;
        quad.style.opacity = full || active ? '1' : '.42';
        quad.style.filter = active ? 'url(#wf-stage-glow)' : full ? 'url(#wf-subtle-shadow)' : 'none';
        root.querySelector('#wf-nodes-overlay-' + (i - 1)).style.opacity = active ? '1' : full ? '.55' : '.2';
      }
      root.querySelector('#wf-svg-central-overpass').style.opacity = full || focus !== 2 ? '1' : '.55';
      draw();
    }
    function render() {
      root.dataset.stage = String(selected);
      root.dataset.fullLoop = String(full);
      controls.forEach(function (control) {
        var active = Number(control.dataset.flowStage) === selected;
        control.classList.toggle('is-active', active);
        if (control.matches('button, [role="button"]')) control.setAttribute('aria-pressed', String(active));
      });
      details.forEach(function (panel, i) { panel.hidden = i + 1 !== selected; });
      text(root.querySelector('[data-flow-status]'), 'flow.' + selected + '.telemetry');
      text(play, reduced.matches ? 'flow.reduced' : playing ? 'flow.play' : 'flow.pause');
      play.setAttribute('aria-pressed', String(playing)); play.disabled = reduced.matches;
      wave.disabled = reduced.matches;
      mode.setAttribute('aria-pressed', String(full)); text(mode, full ? 'flow.full' : 'flow.spotlight');
      highlight();
    }
    function burst(stage) {
      if (reduced.matches || !ctx) return;
      var center = centers[stage - 1];
      for (var i = 0; i < 18; i++) {
        var angle = Math.PI * 2 * i / 18 + Math.random() * .3, speed = 45 + Math.random() * 85;
        burstParticles.push({x:center[0], y:center[1], vx:Math.cos(angle)*speed, vy:Math.sin(angle)*speed, r:2.5+Math.random()*2.5, life:700, color:colors[stage-1]});
      }
      schedule();
    }
    function pulseCycle() {
      if (reduced.matches) return;
      waveAge = 0; waveStage = 1; root.dataset.waveActive = 'true'; burst(1); schedule();
    }
    function select(stage, user) {
      selected = stage; preview = null; elapsed = 0;
      var panel = details[stage - 1];
      panel.querySelectorAll('[data-flow-cap]').forEach(function (button, i) { button.setAttribute('aria-pressed', String(i === 0)); });
      panel.querySelectorAll('[data-flow-cap-panel]').forEach(function (note, i) { note.hidden = i !== 0; });
      // Like the reference, manual selection resets progression without disabling Auto.
      render(); if (user) burst(stage); schedule();
    }
    function draw() {
      if (!ctx || reduced.matches || !canvas.width || !canvas.height) return;
      var focus = preview || selected;
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.save(); ctx.scale(canvas.width / 800, canvas.height / 355);
      routes.forEach(function (route, j) {
        for (var k = 0; k < 11; k++) {
          var distance = ((phase / 6500 + k / 11) % 1) * route.length;
          var point = route.path.getPointAtLength(distance), active = full || j + 1 === focus;
          ctx.beginPath(); ctx.arc(point.x, point.y, active ? 3.4 : 2.2, 0, Math.PI * 2);
          ctx.fillStyle = active ? '#ffffff' : colors[j]; ctx.globalAlpha = active ? .92 : .28;
          ctx.shadowColor = colors[j]; ctx.shadowBlur = active ? 10 : 0; ctx.fill();
        }
      });
      burstParticles.forEach(function (p) {
        ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = p.color; ctx.globalAlpha = Math.max(0, p.life / 700); ctx.shadowColor = p.color; ctx.shadowBlur = 8; ctx.fill();
      });
      ctx.restore();
    }
    function resize() {
      var box = canvas.getBoundingClientRect(), ratio = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.round(box.width * ratio); canvas.height = Math.round(box.height * ratio); draw();
    }
    function schedule() { if (!frame && visible && !document.hidden && !reduced.matches) frame = requestAnimationFrame(tick); }
    function tick(now) {
      frame = 0;
      if (!visible || document.hidden || reduced.matches) { last = null; return; }
      var delta = last === null ? 0 : Math.min(now - last, 80); last = now;
      phase += delta * (waveAge >= 0 ? 3 : 1);
      if (waveAge >= 0) {
        waveAge += delta;
        while (waveStage < 4 && waveAge >= waveStage * 160) { waveStage++; burst(waveStage); }
        if (waveAge > 1200) { waveAge = -1; root.dataset.waveActive = 'false'; }
      }
      burstParticles.forEach(function (p) { p.x += p.vx * delta / 1000; p.y += p.vy * delta / 1000; p.life -= delta; });
      burstParticles = burstParticles.filter(function (p) { return p.life > 0; });
      var focused = document.activeElement.closest && document.activeElement.closest('[data-flow-stage], .workflow-detail');
      var reading = (focused && root.contains(focused)) || root.querySelector('.workflow-detail:hover');
      if (playing && !preview && !reading) {
        elapsed += delta;
        if (elapsed >= duration) select(selected % 4 + 1, false);
      }
      draw(); schedule();
    }
    function stopFrames() { if (frame) cancelAnimationFrame(frame); frame = 0; last = null; }
    controls.forEach(function (control) {
      var stage = Number(control.dataset.flowStage);
      control.addEventListener('pointerenter', function (event) { if (event.pointerType !== 'touch') { preview = stage; highlight(); } });
      control.addEventListener('pointerleave', function () { preview = null; highlight(); });
      control.addEventListener('focus', function () { preview = stage; highlight(); });
      control.addEventListener('blur', function () { preview = null; highlight(); });
      control.addEventListener('click', function () { select(stage, true); });
      control.addEventListener('keydown', function (event) {
        var index = event.key === 'ArrowRight' ? stage % 4 : event.key === 'ArrowLeft' ? (stage + 2) % 4 : event.key === 'Home' ? 0 : event.key === 'End' ? 3 : null;
        if (index !== null) { event.preventDefault(); select(index + 1, true); stageButtons[index].focus(); }
        else if (control.tagName.toLowerCase() !== 'button' && (event.key === 'Enter' || event.key === ' ')) { event.preventDefault(); select(stage, true); }
      });
    });
    play.addEventListener('click', function () { playing = !playing; elapsed = 0; last = null; render(); schedule(); });
    mode.addEventListener('click', function () { full = !full; render(); });
    wave.addEventListener('click', pulseCycle);
    root.querySelectorAll('[data-flow-cap]').forEach(function (button) {
      button.addEventListener('click', function () {
        var panel = button.closest('.workflow-detail');
        panel.querySelectorAll('[data-flow-cap]').forEach(function (other) { other.setAttribute('aria-pressed', String(other === button)); });
        panel.querySelectorAll('[data-flow-cap-panel]').forEach(function (note) { note.hidden = note.dataset.flowCapPanel !== button.dataset.flowCap; });
      });
    });
    function simulate(stage) {
      if (stage === 1) {
        root.querySelectorAll('.workflow-blocks > div > div').forEach(function (row) {
          var buttons = Array.from(row.children), values = ['C','T1','T2','T3'];
          for (var k = values.length - 1; k > 0; k--) { var j = Math.floor(Math.random() * (k + 1)), value = values[k]; values[k] = values[j]; values[j] = value; }
          buttons.forEach(function (cell, i) {
            var key = {'C':'control','T1':'t1','T2':'t2','T3':'t3'}[values[i]];
            cell.dataset.treatment = values[i]; cell.textContent = values[i]; cell.setAttribute('data-i18n-attr', 'title:flow.' + key);
            var lang = document.documentElement.lang === 'pt-BR' ? 'pt' : 'en';
            cell.title = window.AIDBIO_STRINGS[lang]['flow.' + key];
          });
        });
        root.querySelector('[data-flow-power]').textContent = String(91 + Math.floor(Math.random() * 8)) + '%';
      } else if (stage === 2) {
        normalized = !normalized; root.querySelector('.workflow-distributions').dataset.processed = String(normalized);
        text(root.querySelector('[data-processing-label]'), normalized ? 'flow.processed' : 'flow.raw');
        root.querySelector('[data-flow-signal]').textContent = normalized ? '78.4%' : '31.2%';
        text(root.querySelector('[data-flow-drift]'), normalized ? 'flow.removed' : 'flow.confounded');
      } else if (stage === 3) {
        hub = (hub + 1) % 3;
        root.querySelector('[data-hub-label]').textContent = 'HUB_' + (hub + 1);
        root.querySelector('[data-hub-driver]').textContent = hubs[hub][0];
        root.querySelector('[data-hub-auc]').textContent = hubs[hub][1]; root.querySelector('[data-hub-shap]').textContent = hubs[hub][2];
      } else { pulseCycle(); select(1, false); stageButtons[0].focus(); }
      burst(stage);
    }
    root.querySelectorAll('[data-flow-action]').forEach(function (button) {
      button.addEventListener('click', function () { simulate(Number(button.dataset.flowAction)); });
    });
    hubControl.addEventListener('keydown', function (event) {
      if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); simulate(3); }
    });
    root.querySelectorAll('.workflow-cap-notes').forEach(function (notes) { notes.querySelectorAll('[data-flow-cap-panel]').forEach(function (note, i) { note.hidden = i !== 0; }); });
    root.querySelector('.workflow-controls').hidden = false;
    root.querySelectorAll('.workflow-blocks button').forEach(function (button) { button.disabled = false; });
    root.classList.add('is-interactive', 'is-outside-view');
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        visible = entries[0].isIntersecting; root.classList.toggle('is-outside-view', !visible);
        if (visible) { resize(); last = null; schedule(); } else stopFrames();
      }, { threshold: .02 }).observe(root);
    } else { visible = true; root.classList.remove('is-outside-view'); schedule(); }
    if ('ResizeObserver' in window) new ResizeObserver(resize).observe(canvas);
    else window.addEventListener('resize', resize);
    document.addEventListener('visibilitychange', function () { if (document.hidden) stopFrames(); else { last = null; schedule(); } });
    function motionChange() {
      if (reduced.matches) { playing = false; waveAge = -1; burstParticles = []; root.dataset.waveActive = 'false'; stopFrames(); if (ctx) ctx.clearRect(0, 0, canvas.width, canvas.height); }
      render(); schedule();
    }
    if (reduced.addEventListener) reduced.addEventListener('change', motionChange); else reduced.addListener(motionChange);
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
