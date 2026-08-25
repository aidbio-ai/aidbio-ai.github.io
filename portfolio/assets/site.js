// AidBio Founder Story — progressive-enhancement only.
// The site is fully readable and navigable with this script disabled.
(function () {
  "use strict";

  // Reading-progress hairline under the header, chapter pages only.
  var bar = document.querySelector(".read-progress");
  if (bar) {
    var update = function () {
      var doc = document.documentElement;
      var scrollable = doc.scrollHeight - doc.clientHeight;
      var ratio = scrollable > 0 ? Math.min(1, doc.scrollTop / scrollable) : 0;
      bar.style.transform = "scaleX(" + ratio + ")";
    };
    document.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
  }

  // External links open in a new tab with safe rel, without requiring
  // every author of new markup to remember the attributes by hand.
  document.querySelectorAll('a[href^="http"]').forEach(function (a) {
    if (a.hostname && a.hostname !== window.location.hostname) {
      a.setAttribute("target", "_blank");
      a.setAttribute("rel", "noopener");
    }
  });
})();
