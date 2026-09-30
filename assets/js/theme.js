/*
 * AidBio theme bootstrap. Loaded synchronously in <head>, after the
 * <meta name="theme-color"> tag and before any stylesheet, so the right
 * theme is applied before first paint (no flash of the wrong theme).
 *
 * Reads localStorage "aidbio-theme-preference" (legacy: "aidbio-theme"),
 * resolves "system" via prefers-color-scheme, and sets data-theme +
 * color-scheme on <html>. assets/js/chrome.js wires the toggle buttons.
 */
(function () {
  "use strict";

  var STORAGE_KEY = "aidbio-theme-preference";
  var legacyKey = "aidbio-theme";
  var root = document.documentElement;
  var metaTheme = document.querySelector('meta[name="theme-color"]');
  var mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");

  function read(key) {
    try {
      return localStorage.getItem(key);
    } catch (e) {
      return null;
    }
  }

  function getStoredPreference() {
    var current = read(STORAGE_KEY);
    if (current === "system" || current === "light" || current === "dark")
      return current;

    var legacy = read(legacyKey);
    if (legacy === "light" || legacy === "dark") return legacy;

    return "system";
  }

  function getResolvedTheme(preference) {
    if (preference === "light" || preference === "dark") return preference;
    return mediaQuery.matches ? "dark" : "light";
  }

  function applyTheme(preference) {
    var resolved = getResolvedTheme(preference);
    root.setAttribute("data-theme", resolved);
    root.style.colorScheme = resolved;
    root.setAttribute("data-theme-preference", preference);

    if (metaTheme) {
      metaTheme.setAttribute(
        "content",
        resolved === "dark" ? "#0E1219" : "#FBFCFE",
      );
    }
  }

  applyTheme(getStoredPreference());

  window.__aidbioTheme = {
    key: STORAGE_KEY,
    mediaQuery: mediaQuery,
    applyTheme: applyTheme,
    getStoredPreference: getStoredPreference,
    getResolvedTheme: getResolvedTheme,
  };
})();
