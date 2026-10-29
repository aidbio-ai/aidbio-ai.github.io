/* Run with node --test scripts/theme.test.cjs. No package install is required. */
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(new URL('../assets/js/theme.js', `file://${__filename}`), 'utf8');

function boot({ dark = false, saved = {}, denied = false, oldMedia = false } = {}) {
  const attrs = {}, meta = {}, listeners = {}, data = { ...saved };
  const root = { style: {}, setAttribute: (name, value) => { attrs[name] = value; } };
  let changed;
  const media = { matches: dark };
  if (oldMedia) media.addListener = callback => { changed = callback; };
  else media.addEventListener = (_, callback) => { changed = callback; };
  const document = {
    documentElement: root,
    querySelector: () => ({ setAttribute: (key, value) => { meta[key] = value; } }),
    dispatchEvent: () => {},
  };
  const window = {
    matchMedia: () => media,
    addEventListener: (name, callback) => { listeners[name] = callback; },
  };
  vm.runInNewContext(source, {
    window, document,
    localStorage: {
      getItem: key => { if (denied) throw Error('blocked'); return data[key] ?? null; },
      setItem: (key, value) => { if (denied) throw Error('blocked'); data[key] = value; },
    },
    CustomEvent: class { constructor(name, details) { this.type = name; this.detail = details.detail; } },
  });
  return {
    attrs, root, meta, data, api: window.__aidbioTheme,
    os(value) { media.matches = value; changed(); },
    storage(key, value) { if (value === null) delete data[key]; else data[key] = value; listeners.storage({ key }); },
  };
}

test('fresh Auto resolves either OS scheme before styles and follows changes', () => {
  for (const dark of [false, true]) {
    const site = boot({ dark });
    assert.equal(site.attrs['data-theme'], dark ? 'dark' : 'light');
    assert.equal(site.attrs['data-theme-preference'], 'system');
    site.os(!dark);
    assert.equal(site.attrs['data-theme'], dark ? 'light' : 'dark');
    assert.equal(site.root.style.colorScheme, site.attrs['data-theme']);
  }
});
test('manual choice survives OS changes and returning to Auto restores following', () => {
  const site = boot({ dark: true });
  site.api.setPreference('light');
  site.os(false); site.os(true);
  assert.equal(site.attrs['data-theme'], 'light');
  assert.equal(site.data['aidbio-theme-preference'], 'light');
  site.api.setPreference('system');
  assert.equal(site.attrs['data-theme'], 'dark');
  assert.equal(site.meta.content, '#080B0E');
});
test('canonical preference wins; legacy and invalid values resolve safely', () => {
  assert.equal(boot({ saved: { 'aidbio-theme': 'dark' } }).attrs['data-theme'], 'dark');
  assert.equal(boot({ dark: true, saved: { 'aidbio-theme': 'dark', 'aidbio-theme-preference': 'light' } }).attrs['data-theme'], 'light');
  assert.equal(boot({ saved: { 'aidbio-theme-preference': 'invalid' } }).attrs['data-theme-preference'], 'system');
});
test('blocked storage still permits Auto and an in-page override', () => {
  const site = boot({ dark: true, denied: true });
  assert.equal(site.attrs['data-theme'], 'dark');
  site.api.setPreference('light');
  assert.equal(site.attrs['data-theme'], 'light');
});
test('storage events synchronize open pages', () => {
  const site = boot();
  site.storage('aidbio-theme-preference', 'dark');
  assert.equal(site.attrs['data-theme'], 'dark');
  site.storage('aidbio-theme-preference', null);
  assert.equal(site.attrs['data-theme-preference'], 'system');
});
test('older matchMedia listeners are supported and invalid choices are ignored', () => {
  const site = boot({ oldMedia: true });
  site.os(true);
  assert.equal(site.attrs['data-theme'], 'dark');
  site.api.setPreference('invalid');
  assert.equal(site.api.getPreference(), 'system');
});
