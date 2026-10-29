/* Only the homepage loads this module. Translation data never replaces HTML markup. */
(function () {
  'use strict';
  var strings = window.AIDBIO_STRINGS;
  if (!strings) return;
  var language = 'en';
  try { if (localStorage.getItem('aidbio-lang') === 'pt') language = 'pt'; } catch (error) {}
  function apply(value) {
    language = value === 'pt' ? 'pt' : 'en';
    var copy = strings[language];
    document.documentElement.lang = language === 'pt' ? 'pt-BR' : 'en';
    document.querySelectorAll('[data-i18n]').forEach(function (element) {
      var translated = copy[element.getAttribute('data-i18n')];
      if (translated !== undefined) element.textContent = translated;
    });
    document.querySelectorAll('[data-i18n-attr]').forEach(function (element) {
      element.getAttribute('data-i18n-attr').split(';').forEach(function (mapping) {
        var parts = mapping.split(':');
        if (copy[parts[1]] !== undefined) element.setAttribute(parts[0], copy[parts[1]]);
      });
    });
    document.title = copy['meta.title'];
    ['description', 'og:description'].forEach(function (name) {
      var meta = document.querySelector('meta[name="' + name + '"],meta[property="' + name + '"]');
      if (meta) meta.content = copy['meta.description'];
    });
    var title = document.querySelector('meta[property="og:title"]');
    if (title) title.content = copy['meta.title'];
    document.querySelectorAll('[data-language-select]').forEach(function (select) { select.value = language; });
    try { localStorage.setItem('aidbio-lang', language); } catch (error) {}
    document.dispatchEvent(new CustomEvent('aidbio:language', { detail: language }));
  }
  document.querySelectorAll('[data-language-select]').forEach(function (select) {
    select.addEventListener('change', function () { apply(select.value); });
  });
  apply(language);
})();
