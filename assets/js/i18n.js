/*
 * AidBio client-side i18n: swaps [data-i18n] text content and [data-i18n-attr]
 * attributes from assets/i18n/<lang>.json. Both supported languages, including
 * English, go through the same fetch+apply path — switching away and back to
 * English has to restore the DOM from en.json rather than assume the original
 * hard-coded text is still there, since a prior switch may have overwritten it.
 */
(function () {
  "use strict";

  var LANG_KEY = "aidbio-lang-preference";
  var SUPPORTED = ["en", "pt"];
  var DEFAULT_LANG = "en";

  // Small set of strings that have no DOM default to fall back to, because
  // they're only ever set dynamically by other scripts (e.g. a toggled aria-label).
  var DYNAMIC_FALLBACK = {
    "nav.openMenu": "Open menu",
    "nav.closeMenu": "Close menu",
  };

  var dictCache = {};
  var currentLang = DEFAULT_LANG;
  var currentDict = null;

  function detectLanguage() {
    var stored = localStorage.getItem(LANG_KEY);
    if (SUPPORTED.indexOf(stored) !== -1) return stored;

    var browserLangs =
      navigator.languages && navigator.languages.length
        ? navigator.languages
        : [navigator.language || DEFAULT_LANG];

    for (var i = 0; i < browserLangs.length; i++) {
      var short = String(browserLangs[i]).toLowerCase().slice(0, 2);
      if (SUPPORTED.indexOf(short) !== -1) return short;
    }
    return DEFAULT_LANG;
  }

  function getValue(dict, key) {
    return key.split(".").reduce(function (obj, part) {
      return obj && typeof obj === "object" ? obj[part] : undefined;
    }, dict);
  }

  function applyDictionary(dict) {
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var value = getValue(dict, el.getAttribute("data-i18n"));
      if (typeof value === "string") el.textContent = value;
    });

    document.querySelectorAll("[data-i18n-attr]").forEach(function (el) {
      el.getAttribute("data-i18n-attr")
        .split(";")
        .forEach(function (pair) {
          var parts = pair.split(":");
          var attr = parts[0] && parts[0].trim();
          var key = parts[1] && parts[1].trim();
          if (!attr || !key) return;
          var value = getValue(dict, key);
          if (typeof value === "string") el.setAttribute(attr, value);
        });
    });
  }

  function syncSwitchers(lang) {
    document.querySelectorAll("[data-lang-choice]").forEach(function (btn) {
      btn.setAttribute("aria-pressed", String(btn.dataset.langChoice === lang));
    });
  }

  function loadDictionary(lang) {
    if (dictCache[lang]) return Promise.resolve(dictCache[lang]);
    return fetch("assets/i18n/" + lang + ".json").then(function (res) {
      if (!res.ok) throw new Error("Failed to load " + lang + ".json (" + res.status + ")");
      return res.json();
    }).then(function (dict) {
      dictCache[lang] = dict;
      return dict;
    });
  }

  function setLanguage(lang) {
    if (SUPPORTED.indexOf(lang) === -1) lang = DEFAULT_LANG;

    return loadDictionary(lang)
      .then(function (dict) {
        currentLang = lang;
        currentDict = dict;
        document.documentElement.setAttribute("lang", lang);
        applyDictionary(dict);
        syncSwitchers(lang);
        localStorage.setItem(LANG_KEY, lang);
      })
      .catch(function (err) {
        console.error("[i18n]", err);
      });
  }

  function t(key) {
    if (currentDict) {
      var value = getValue(currentDict, key);
      if (typeof value === "string") return value;
    }
    return DYNAMIC_FALLBACK[key] || key;
  }

  window.__aidbioI18n = {
    key: LANG_KEY,
    supported: SUPPORTED,
    detectLanguage: detectLanguage,
    setLanguage: setLanguage,
    t: t,
    getLang: function () {
      return currentLang;
    },
  };

  setLanguage(detectLanguage());
})();
