/* Illustrative hero visuals: weather chart and protein-network graph. Data are made up for demonstration. */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var dpr = function () { return window.devicePixelRatio || 1; };

  function fit(canvas) {
    var r = canvas.parentElement.getBoundingClientRect();
    canvas.width = Math.round(r.width * dpr()); canvas.height = Math.round(r.height * dpr());
    var ctx = canvas.getContext('2d');
    ctx.setTransform(dpr(), 0, 0, dpr(), 0, 0);
    return { ctx: ctx, w: r.width, h: r.height };
  }
  function dark() { return document.documentElement.getAttribute('data-theme') === 'dark'; }

  // ----- Weather chart (deterministic pseudo data, no Math.random) -----
  var wc = document.getElementById('weatherCanvas');
  var tip = document.getElementById('weatherTip');
  var N = 30, pts = [];
  for (var i = 0; i < N; i++) pts.push({ day: i + 1,
    solar: +(18 + Math.sin(i / 3.5) * 6 + Math.sin(i * 1.5) * 2).toFixed(1),
    gdd: +(12 + Math.cos(i / 4.2) * 5 + Math.sin(i * 2.3) * 0.8).toFixed(1) });
  var pad = { l: 24, r: 24, t: 20, b: 25 };

  function drawWeather(hover) {
    if (!wc || wc.offsetParent === null) return;
    var s = fit(wc), ctx = s.ctx, W = s.w - pad.l - pad.r, H = s.h - pad.t - pad.b;
    ctx.clearRect(0, 0, s.w, s.h);
    ctx.strokeStyle = 'rgba(255,255,255,.07)'; ctx.lineWidth = 1;
    for (var g = 0; g <= 3; g++) { var y = pad.t + H / 3 * g; ctx.beginPath(); ctx.moveTo(pad.l, y); ctx.lineTo(s.w - pad.r, y); ctx.stroke(); }
    function line(key, lo, span, color, width, dash) {
      ctx.beginPath();
      pts.forEach(function (p, k) { var x = pad.l + k / (N - 1) * W, y = pad.t + H - (p[key] - lo) / span * H; k ? ctx.lineTo(x, y) : ctx.moveTo(x, y); });
      ctx.strokeStyle = color; ctx.lineWidth = width; ctx.setLineDash(dash || []); ctx.stroke(); ctx.setLineDash([]);
    }
    line('solar', 10, 20, '#F59E0B', 2.5); line('gdd', 5, 18, '#10B981', 1.8, [3, 3]);
    if (hover >= 0) {
      var hx = pad.l + hover / (N - 1) * W;
      ctx.strokeStyle = 'rgba(255,255,255,.4)'; ctx.beginPath(); ctx.moveTo(hx, pad.t); ctx.lineTo(hx, pad.t + H); ctx.stroke();
      ctx.fillStyle = '#F59E0B'; ctx.beginPath(); ctx.arc(hx, pad.t + H - (pts[hover].solar - 10) / 20 * H, 4, 0, 6.283); ctx.fill();
    }
  }
  if (wc) {
    wc.addEventListener('mousemove', function (e) {
      var r = wc.getBoundingClientRect(), mx = e.clientX - r.left;
      var idx = Math.min(Math.max(Math.round((mx - pad.l) / (r.width - pad.l - pad.r) * (N - 1)), 0), N - 1);
      drawWeather(idx);
      var p = pts[idx];
      tip.hidden = false; tip.textContent = 'Day ' + p.day + ' · Solar ' + p.solar + ' MJ/m² · GDD ' + p.gdd;
      tip.style.left = Math.min(Math.max(mx - 70, 8), r.width - 190) + 'px'; tip.style.top = '8px';
    });
    wc.addEventListener('mouseleave', function () { drawWeather(-1); tip.hidden = true; });
  }

  // ----- Protein network -----
  var gc = document.getElementById('gnnCanvas');
  var nodes = [], edges = [], hovered = null, raf = 0, size = { w: 0, h: 0 };
  var C = { t: '#10B981', p: '#8B5CF6', a: '#F59E0B', c: '#06B6D4' };
  function seed(w, h) {
    nodes = [
      ['Target protein', .45, .48, 16, C.t], ['Protein A', .25, .32, 10, C.p], ['Protein B', .32, .72, 9, C.p],
      ['Protein C', .65, .35, 11, C.p], ['Protein D', .72, .65, 10, C.p],
      ['Function 1', .18, .82, 7, C.a], ['Function 2', .82, .22, 7, C.a], ['Function 3', .55, .82, 8, C.c]
    ].map(function (n) { return { label: n[0], x: w * n[1], y: h * n[2], r: n[3], color: n[4] }; });
    edges = [[0,1,.92],[0,2,.88],[0,3,.95],[0,4,.79],[1,2,.65],[3,4,.71],[2,5,.94],[3,6,.89],[0,7,.98]];
  }
  function frame(t) {
    if (gc.offsetParent === null) { raf = 0; return; }
    var s = fit(gc), ctx = s.ctx;
    if (s.w !== size.w || s.h !== size.h) { size = { w: s.w, h: s.h }; seed(s.w, s.h); }
    var time = t * 0.0015;
    ctx.clearRect(0, 0, s.w, s.h);
    edges.forEach(function (e) {
      var a = nodes[e[0]], b = nodes[e[1]], hot = hovered === a || hovered === b;
      ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y);
      ctx.strokeStyle = hot ? 'rgba(139,92,246,.9)' : 'rgba(255,255,255,.14)'; ctx.lineWidth = hot ? 2.5 : 1.2; ctx.stroke();
      var f = reduce ? .5 : (time * .8 + e[2]) % 1;
      ctx.fillStyle = hot ? '#10B981' : 'rgba(139,92,246,.6)';
      ctx.beginPath(); ctx.arc(a.x + (b.x - a.x) * f, a.y + (b.y - a.y) * f, hot ? 3 : 1.8, 0, 6.283); ctx.fill();
    });
    nodes.forEach(function (n) {
      var y = n.y + (reduce ? 0 : Math.sin(time + n.x) * 1.5);
      if (n === nodes[0] || n === hovered) { ctx.beginPath(); ctx.arc(n.x, y, n.r + 6, 0, 6.283); ctx.fillStyle = n.color + '26'; ctx.fill(); }
      ctx.beginPath(); ctx.arc(n.x, y, n.r, 0, 6.283); ctx.fillStyle = n.color; ctx.fill();
      ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.5; ctx.stroke();
      ctx.fillStyle = '#fff'; ctx.font = '9px "JetBrains Mono", monospace'; ctx.textAlign = 'center'; ctx.fillText(n.label, n.x, y + n.r + 12);
    });
    raf = reduce ? 0 : requestAnimationFrame(frame);
  }
  function startGnn() { if (gc && !raf) raf = requestAnimationFrame(frame); }
  if (gc) gc.addEventListener('mousemove', function (e) {
    var r = gc.getBoundingClientRect(), mx = e.clientX - r.left, my = e.clientY - r.top;
    hovered = nodes.filter(function (n) { return Math.hypot(mx - n.x, my - n.y) < n.r + 6; })[0] || null;
    if (reduce) { raf = 0; startGnn(); }
  });
  if (gc) gc.addEventListener('mouseleave', function () { hovered = null; });

  document.addEventListener('aidbio:tab', function (e) {
    if (e.detail === 'weather') drawWeather(-1);
    if (e.detail === 'gnn') { size = { w: 0, h: 0 }; startGnn(); }
  });
  window.addEventListener('resize', function () { drawWeather(-1); size = { w: 0, h: 0 }; });
  window.addEventListener('DOMContentLoaded', function () { drawWeather(-1); });
})();
