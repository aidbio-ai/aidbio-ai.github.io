/*
 * AidBio site chrome behaviour — shared by every page.
 * Theme switcher, language switcher (only when i18n.js is on the page),
 * mobile menu, nav shadow on scroll, scroll-reveal.
 * Requires assets/js/theme.js to have run in <head>.
 */
(function () {
  "use strict";

  var themeApi = window.__aidbioTheme;
  var i18nApi = window.__aidbioI18n;

  function label(key, fallback) {
    return i18nApi && i18nApi.t ? i18nApi.t(key) : fallback;
  }

  // ---- Theme switcher -------------------------------------------------
  if (themeApi) {
    var themeButtons = Array.prototype.slice.call(
      document.querySelectorAll(
        ".theme-switcher:not(.lang-switcher) .theme-option",
      ),
    );

    var getPreference = function () {
      try {
        var stored = localStorage.getItem(themeApi.key);
        if (stored === "system" || stored === "light" || stored === "dark")
          return stored;
      } catch (e) {}
      return themeApi.getStoredPreference();
    };

    var syncThemeButtons = function (preference) {
      themeButtons.forEach(function (button) {
        button.setAttribute(
          "aria-pressed",
          String(button.dataset.themeChoice === preference),
        );
      });
    };

    themeButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        var preference = button.dataset.themeChoice;
        try {
          localStorage.setItem(themeApi.key, preference);
        } catch (e) {}
        themeApi.applyTheme(preference);
        syncThemeButtons(preference);
      });
    });

    themeApi.mediaQuery.addEventListener("change", function () {
      if (getPreference() === "system") {
        themeApi.applyTheme("system");
        syncThemeButtons("system");
      }
    });

    syncThemeButtons(getPreference());
  }

  // ---- Language switcher (only pages that load i18n.js) ----------------
  if (i18nApi) {
    document.querySelectorAll("[data-lang-choice]").forEach(function (button) {
      button.addEventListener("click", function () {
        i18nApi.setLanguage(button.dataset.langChoice);
      });
    });
  }

  // ---- Mobile menu ------------------------------------------------------
  var menuToggle = document.getElementById("menu-toggle");
  var mobileMenu = document.getElementById("mobile-menu");

  if (menuToggle && mobileMenu) {
    var closeMenu = function () {
      mobileMenu.classList.remove("open");
      menuToggle.setAttribute("aria-expanded", "false");
      menuToggle.setAttribute("aria-label", label("nav.openMenu", "Open menu"));
    };

    menuToggle.addEventListener("click", function () {
      var open = mobileMenu.classList.toggle("open");
      menuToggle.setAttribute("aria-expanded", String(open));
      menuToggle.setAttribute(
        "aria-label",
        open
          ? label("nav.closeMenu", "Close menu")
          : label("nav.openMenu", "Open menu"),
      );
    });

    mobileMenu.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", closeMenu);
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && mobileMenu.classList.contains("open")) {
        closeMenu();
        menuToggle.focus();
      }
    });
  }

  // ---- Local sub-nav: keep the current item visible on narrow screens ----
  var current = document.querySelector(".subnav-links a[aria-current]");
  if (current && current.parentElement.scrollWidth > current.parentElement.clientWidth) {
    var strip = current.parentElement;
    strip.scrollLeft = Math.max(
      0,
      current.offsetLeft - (strip.clientWidth - current.offsetWidth) / 2,
    );
  }

  // ---- Nav shadow on scroll ---------------------------------------------
  var nav = document.getElementById("site-nav");
  if (nav) {
    var onScroll = function () {
      nav.classList.toggle("scrolled", window.scrollY > 12);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  // ---- Scroll reveal ----------------------------------------------------
  var revealEls = document.querySelectorAll(".reveal");
  if (revealEls.length) {
    if (!("IntersectionObserver" in window)) {
      revealEls.forEach(function (el) {
        el.classList.add("visible");
      });
    } else {
      var observer = new IntersectionObserver(
        function (entries, obs) {
          entries.forEach(function (entry) {
            if (!entry.isIntersecting) return;
            entry.target.classList.add("visible");
            obs.unobserve(entry.target);
          });
        },
        { threshold: 0.12 },
      );
      revealEls.forEach(function (el) {
        observer.observe(el);
      });
    }
  }
})();
