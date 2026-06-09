(function () {
  'use strict';

  var initialized = false;
  var legacyUnbound = false;

  var HAMBURGER_SVG =
    '<svg class="site-header__hamburger" viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
    '<path class="site-header__bar site-header__bar--top" d="M4 7h16"/>' +
    '<path class="site-header__bar site-header__bar--mid" d="M4 12h16"/>' +
    '<path class="site-header__bar site-header__bar--bot" d="M4 17h16"/>' +
    '</svg>';

  function unbindLegacyHandlers() {
    if (legacyUnbound || !window.jQuery) {
      return;
    }
    window.jQuery('.navbar-toggler').off('click');
    window.jQuery('.lights-off.enabled').off('click');
    legacyUnbound = true;
  }

  function init() {
    if (initialized) {
      unbindLegacyHandlers();
      return;
    }

    var drawer = document.getElementById('mobile-nav');
    var toggler = document.querySelector('header .navbar-toggler');
    var backdrop = document.querySelector('.lights-off');
    var header = document.querySelector('header.site-header, header.header');

    if (!drawer || !toggler) {
      return;
    }

    initialized = true;
    unbindLegacyHandlers();

    var sideFixed = document.querySelector('.side-fixed');
    var searchWrap = document.querySelector('.dgwt-wcas-search-wrapp');
    var spacer = document.querySelector('.spacer');

    var focusableSelector =
      'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';

    function isOpen() {
      return drawer.classList.contains('out');
    }

    function setTogglerState(open) {
      toggler.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggler.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      toggler.classList.toggle('is-active', open);
    }

    function lockBody(open) {
      document.body.classList.toggle('nav-open', open);
      if (!open) {
        document.body.style.overflow = '';
      }
    }

    function updateHeaderHeight() {
      var mobile = window.matchMedia('(max-width: 1199.98px)').matches;
      var tiny = header && header.classList.contains('tiny');
      var height;

      if (mobile) {
        height = tiny ? '64px' : window.matchMedia('(min-width: 768px)').matches ? '84px' : '76px';
      } else {
        height = tiny ? '72px' : '100px';
      }

      document.documentElement.style.setProperty('--site-header-height', height);
    }

    function updateScrollState() {
      var scrolled = window.scrollY >= 1;
      var open = isOpen();
      var tiny = scrolled || open;

      if (header) {
        header.classList.toggle('tiny', tiny);
      }
      if (sideFixed) {
        sideFixed.classList.toggle('tiny', tiny);
      }
      if (searchWrap) {
        searchWrap.classList.toggle('tiny', tiny);
      }
      if (spacer) {
        spacer.classList.toggle('tiny', tiny);
      }
      if (drawer && open) {
        drawer.classList.add('tiny');
      }

      updateHeaderHeight();
    }

    function openMenu() {
      drawer.classList.add('out', 'tiny');
      if (backdrop) {
        backdrop.classList.add('enabled');
      }
      lockBody(true);
      setTogglerState(true);
      updateScrollState();
    }

    function closeMenu() {
      if (!isOpen()) {
        return;
      }

      drawer.classList.remove('out');
      if (backdrop) {
        backdrop.classList.remove('enabled');
      }

      lockBody(false);
      setTogglerState(false);
      updateScrollState();
      toggler.focus();
    }

    function setupMenuIcon() {
      var iconSpan = toggler.querySelector('.site-header__menu-icon');
      if (iconSpan && !iconSpan.querySelector('svg')) {
        iconSpan.innerHTML = HAMBURGER_SVG;
      } else if (!iconSpan && !toggler.querySelector('.site-header__hamburger')) {
        var span = document.createElement('span');
        span.className = 'site-header__menu-icon';
        span.setAttribute('aria-hidden', 'true');
        span.innerHTML = HAMBURGER_SVG;
        toggler.innerHTML = '';
        toggler.appendChild(span);
      }
    }

    function setAriaCurrent() {
      document
        .querySelectorAll(
          '.current-menu-item > a.nav-link, .current_page_item > a.nav-link, li.active > a.nav-link'
        )
        .forEach(function (link) {
          link.setAttribute('aria-current', 'page');
        });
    }

    setupMenuIcon();
    setAriaCurrent();
    setTogglerState(false);
    updateScrollState();

    toggler.addEventListener('click', function (event) {
      event.preventDefault();
      event.stopImmediatePropagation();
      if (isOpen()) {
        closeMenu();
      } else {
        openMenu();
      }
    });

    if (backdrop) {
      backdrop.addEventListener('click', function () {
        if (backdrop.classList.contains('enabled')) {
          closeMenu();
        }
      });
    }

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && isOpen()) {
        event.preventDefault();
        closeMenu();
      }
    });

    document.addEventListener('keydown', function (event) {
      if (event.key !== 'Tab' || !isOpen()) {
        return;
      }

      var focusable = Array.prototype.slice
        .call(drawer.querySelectorAll(focusableSelector))
        .filter(function (el) {
          return el.offsetParent !== null;
        });

      if (!focusable.length) {
        return;
      }

      var first = focusable[0];
      var last = focusable[focusable.length - 1];

      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });

    drawer.addEventListener('click', function (event) {
      var link = event.target.closest('.menu-item-has-children > a.nav-link');
      if (!link || !drawer.contains(link)) {
        return;
      }

      var item = link.parentElement;
      if (!item.classList.contains('menu-item-has-children')) {
        return;
      }

      event.preventDefault();
      var nowOpen = !item.classList.contains('is-open');
      item.classList.toggle('is-open', nowOpen);
      link.setAttribute('aria-expanded', nowOpen ? 'true' : 'false');
    });

    drawer.addEventListener('click', function (event) {
      var link = event.target.closest('a.nav-link');
      if (!link || !drawer.contains(link)) {
        return;
      }

      if (link.parentElement.classList.contains('menu-item-has-children')) {
        return;
      }

      closeMenu();
    });

    var desktopProducts = document.querySelector(
      '#navbar .menu-item-has-children > a.nav-link'
    );
    if (desktopProducts) {
      if (!desktopProducts.hasAttribute('aria-haspopup')) {
        desktopProducts.setAttribute('aria-haspopup', 'true');
      }
      if (!desktopProducts.hasAttribute('aria-expanded')) {
        desktopProducts.setAttribute('aria-expanded', 'false');
      }

      desktopProducts.addEventListener('click', function (event) {
        if (
          window.matchMedia('(min-width: 1200px)').matches &&
          'ontouchstart' in window
        ) {
          var item = desktopProducts.parentElement;
          var open = item.classList.toggle('is-open');
          if (open) {
            event.preventDefault();
          }
          desktopProducts.setAttribute('aria-expanded', open ? 'true' : 'false');
        }
      });

      document.addEventListener('click', function (event) {
        var item = desktopProducts.parentElement;
        if (!item.classList.contains('is-open')) {
          return;
        }
        if (!item.contains(event.target)) {
          item.classList.remove('is-open');
          desktopProducts.setAttribute('aria-expanded', 'false');
        }
      });
    }

    drawer.querySelectorAll('.menu-item-has-children > a.nav-link').forEach(function (link) {
      if (!link.hasAttribute('aria-haspopup')) {
        link.setAttribute('aria-haspopup', 'true');
      }
      if (!link.hasAttribute('aria-expanded')) {
        link.setAttribute('aria-expanded', 'false');
      }
    });

    window.addEventListener('scroll', updateScrollState, { passive: true });
    window.addEventListener('resize', updateHeaderHeight, { passive: true });
  }

  function boot() {
    init();
    unbindLegacyHandlers();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }

  window.addEventListener('load', boot);
  setTimeout(unbindLegacyHandlers, 100);
  setTimeout(unbindLegacyHandlers, 500);
})();
