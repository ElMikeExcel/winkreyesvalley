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

/* Oct 23, 2026 restructure: shared site nav + footer injection, the
   moved-anchor shim, and the Questions page search. The nav and footer
   are injected from this one definition so both pages share the same
   chrome without duplicated markup. */
(function () {
  'use strict';

  var MOVED = ['vanilla-basics', 'vanilla-iron-golem', 'vanilla-copper-golem', 'vanilla-snow-golem', 'vanilla-enchanting', 'vanilla-anvil', 'vanilla-grindstone', 'vanilla-nether-portal', 'vanilla-beacon', 'vanilla-conduit', 'vanilla-villager-trades', 'vanilla-curing', 'vanilla-breeding', 'vanilla-farm-crops', 'vanilla-kelp', 'vanilla-elytra', 'vanilla-shulker-box', 'vanilla-ender-chest', 'vanilla-trident', 'vanilla-crossbow', 'vanilla-netherite', 'vanilla-netherite-template', 'vanilla-ancient-debris', 'vanilla-brewing', 'vanilla-fishing', 'vanilla-composter', 'vanilla-bees', 'vanilla-axolotls', 'vanilla-goats', 'vanilla-frogs', 'vanilla-allays', 'vanilla-leads', 'vanilla-name-tags', 'vanilla-maps', 'vanilla-lodestone', 'vanilla-recovery-compass', 'vanilla-shriekers', 'vanilla-respawn-anchor', 'vanilla-piglin-bartering', 'nightly-maintenance', 'zombie-charge', 'wither-skulls', 'elite-drops', 'dropped-items', 'raid-glow', 'vanilla-raids', 'raid-expiry', 'vanilla-totem', 'vanilla-chest-boat', 'vanilla-silk-fortune'];

  var onQuestions = /(^|\/)questions\.html$/.test(location.pathname);

  // Moved-anchor shim: links shared before the restructure point at
  // index.html#vanilla-... — send them to the Questions page instead.
  if (!onQuestions && location.hash.length > 1) {
    var shimId = null;
    try { shimId = decodeURIComponent(location.hash.slice(1)); } catch (_) { shimId = null; }
    if (shimId && MOVED.indexOf(shimId) !== -1) {
      location.replace('questions.html#' + encodeURIComponent(shimId));
      return;
    }
  }

  // Slim sticky nav, shared by both pages.
  var NAV = [
    ['Home', 'top'],
    ['Join', 'join'],
    ['Seals', 'seals'],
    ['Guide', 'guide'],
    ['Questions', null],
    ['Skill Trees', 'skill-trees'],
    ['Plugins', 'all-plugins'],
    ['Rules', 'rules'],
    ['Changelog', 'changelog']
  ];
  var nav = document.createElement('nav');
  nav.className = 'site-nav';
  nav.setAttribute('aria-label', 'Site');
  var navWrap = document.createElement('div');
  navWrap.className = 'wrap';
  NAV.forEach(function (item) {
    var a = document.createElement('a');
    a.textContent = item[0];
    if (item[0] === 'Questions') {
      a.href = onQuestions ? '#vanilla-basics' : 'questions.html';
      if (onQuestions) a.setAttribute('aria-current', 'page');
    } else if (item[0] === 'Home') {
      a.href = onQuestions ? 'index.html#top' : '#top';
      if (!onQuestions) a.setAttribute('aria-current', 'page');
    } else {
      a.href = (onQuestions ? 'index.html#' : '#') + item[1];
    }
    navWrap.appendChild(a);
  });
  nav.appendChild(navWrap);
  document.body.insertBefore(nav, document.body.firstChild);

  // The Questions page carries no static footer (footer text would land
  // in the knowledge extraction there); inject the main page's footer.
  if (!document.querySelector('footer')) {
    var footer = document.createElement('footer');
    var fwrap = document.createElement('div');
    fwrap.className = 'wrap';
    fwrap.textContent = 'Wink Reyes Valley. A family Minecraft server.';
    footer.appendChild(fwrap);
    document.body.appendChild(footer);
  }

  // Questions page: search filter + open the entry a hash points at.
  var qaSearch = document.getElementById('qa-search');
  if (qaSearch) {
    var qaEntries = Array.from(document.querySelectorAll('.qa-entry'));
    var qaResults = document.getElementById('qa-results');
    function qaFilter() {
      var words = qaSearch.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
      var count = 0;
      qaEntries.forEach(function (entry) {
        var match = words.every(function (w) {
          return entry.textContent.toLowerCase().indexOf(w) !== -1;
        });
        entry.hidden = !match;
        var det = entry.querySelector('details.qa');
        if (det) det.open = match && words.length > 0;
        if (match) count += 1;
      });
      if (qaResults) qaResults.textContent = words.length
        ? count + ' of ' + qaEntries.length + ' questions shown'
        : '';
    }
    qaSearch.addEventListener('input', qaFilter);
    qaSearch.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') { qaSearch.value = ''; qaFilter(); }
    });

    function qaOpenHash() {
      if (!location.hash) return;
      var id;
      try { id = decodeURIComponent(location.hash.slice(1)); } catch (_) { return; }
      var entry = document.getElementById(id);
      if (entry && entry.classList.contains('qa-entry')) {
        var det = entry.querySelector('details.qa');
        if (det) det.open = true;
      }
    }
    window.addEventListener('hashchange', qaOpenHash);
    qaOpenHash();
  }
})();
