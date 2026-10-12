(function () {
  'use strict';

  // Keep every guide readable when JavaScript is unavailable.
  var root = document.getElementById('plugtabs');
  var tabs = root ? Array.from(root.querySelectorAll('[role="tab"]')) : [];
  var cards = Array.from(document.querySelectorAll('.skill-card'));
  var search = document.getElementById('skill-search');
  var category = document.getElementById('skill-category');
  var results = document.getElementById('skill-results');
  var empty = document.getElementById('skill-empty');

  function showTab(tab, focus) {
    tabs.forEach(function (item) {
      var selected = item === tab;
      item.setAttribute('aria-selected', String(selected));
      item.tabIndex = selected ? 0 : -1;
      document.getElementById(item.getAttribute('aria-controls')).hidden = !selected;
    });
    if (focus) {
      tab.focus();
      tab.scrollIntoView({block: 'nearest', inline: 'nearest'});
    }
  }

  function filterSkills() {
    if (!search || !category) return;
    var words = search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    var count = 0;
    cards.forEach(function (card) {
      var text = card.textContent.toLowerCase();
      var match = (category.value === 'all' || card.dataset.category === category.value) &&
        words.every(function (word) { return text.indexOf(word) !== -1; });
      card.hidden = !match;
      if (match) count += 1;
    });
    results.textContent = count + ' of ' + cards.length + ' skills shown';
    empty.hidden = count !== 0;
  }

  function resetFilters() {
    if (!search || !category) return;
    search.value = '';
    category.value = 'all';
    filterSkills();
  }

  function followHash(scroll) {
    var id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch (_) { return; }
    var target = document.getElementById(id);
    if (!target) return;
    var panel = target.closest('[role="tabpanel"]');
    if (panel) {
      var tab = document.getElementById(panel.getAttribute('aria-labelledby'));
      if (tab) showTab(tab, false);
    }
    var card = target.closest('.skill-card');
    if (card) {
      resetFilters();
      card.open = true;
    }
    if (scroll) target.scrollIntoView({block: 'start'});
  }

  if (root && tabs.length) {
    root.classList.add('js');
    tabs.forEach(function (tab, index) {
      tab.addEventListener('click', function () {
        showTab(tab, false);
        var hash = '#' + tab.getAttribute('aria-controls');
        if (location.hash !== hash) history.pushState(null, '', hash);
      });
      tab.addEventListener('keydown', function (event) {
        var next = null;
        if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
        else if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
        else if (event.key === 'Home') next = 0;
        else if (event.key === 'End') next = tabs.length - 1;
        if (next !== null) {
          event.preventDefault();
          showTab(tabs[next], true);
          history.replaceState(null, '', '#' + tabs[next].getAttribute('aria-controls'));
        }
      });
    });
    showTab(tabs[0], false);
  }

  if (search && category) {
    document.getElementById('skill-controls').hidden = false;
    search.addEventListener('input', filterSkills);
    category.addEventListener('change', filterSkills);
    search.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') { resetFilters(); search.focus(); }
    });
    document.getElementById('skill-reset').addEventListener('click', function () {
      resetFilters();
      search.focus();
    });
    document.getElementById('skill-expand').addEventListener('click', function () {
      cards.forEach(function (card) { if (!card.hidden) card.open = true; });
    });
    document.getElementById('skill-collapse').addEventListener('click', function () {
      cards.forEach(function (card) { card.open = false; });
    });
    filterSkills();
  }

  window.addEventListener('hashchange', function () { followHash(true); });
  document.addEventListener('click', function (event) {
    var link = event.target.closest('a[href^="#"]');
    if (link && link.getAttribute('href') === location.hash) followHash(true);
  });
  window.addEventListener('popstate', function () {
    if (!location.hash && tabs.length) showTab(tabs[0], false);
    followHash(true);
  });
  followHash(Boolean(location.hash));

  var copy = document.getElementById('copy');
  if (copy) copy.addEventListener('click', function () {
    var address = document.getElementById('addr');
    var status = document.getElementById('copied');
    function fallback() {
      var range = document.createRange();
      range.selectNodeContents(address);
      var selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      status.textContent = 'Select the address and copy it, or press and hold on a phone.';
    }
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(address.textContent).then(function () {
        status.textContent = 'Address copied!';
      }, fallback);
    } else fallback();
  });
})();
