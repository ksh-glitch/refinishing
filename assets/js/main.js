/* Antiques & Furniture Restoration — site behaviors
   No dependencies. Progressive enhancement: everything works without JS. */
(function () {
  'use strict';

  var prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------- Header: solid after scroll ---------------- */
  var header = document.querySelector('.site-header');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-scrolled', window.scrollY > 24);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------------- Mobile nav ---------------- */
  var navToggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.site-nav');
  if (navToggle && nav) {
    navToggle.addEventListener('click', function () {
      var open = document.body.classList.toggle('nav-open');
      navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        document.body.classList.remove('nav-open');
        navToggle.setAttribute('aria-expanded', 'false');
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.body.classList.contains('nav-open')) {
        document.body.classList.remove('nav-open');
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.focus();
      }
    });
  }

  /* ---------------- Reveal on scroll ---------------- */
  var revealEls = document.querySelectorAll('[data-reveal]');
  if (revealEls.length && 'IntersectionObserver' in window && !prefersReduced) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-revealed');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    revealEls.forEach(function (el) { io.observe(el); });
    // Safety net: if the observer never fires (unusual embeds), reveal
    // anything still hidden shortly after load so content is never lost.
    window.addEventListener('load', function () {
      setTimeout(function () {
        revealEls.forEach(function (el) {
          if (!el.classList.contains('is-revealed')) {
            var r = el.getBoundingClientRect();
            if (r.top < window.innerHeight && r.bottom > 0) el.classList.add('is-revealed');
          }
        });
      }, 1500);
    });
  } else {
    revealEls.forEach(function (el) { el.classList.add('is-revealed'); });
  }

  /* ---------------- Animated counters ---------------- */
  var counters = document.querySelectorAll('[data-count]');
  if (counters.length && 'IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        cio.unobserve(entry.target);
        var el = entry.target;
        var target = parseInt(el.getAttribute('data-count'), 10);
        if (prefersReduced) { el.textContent = target.toLocaleString(); return; }
        var start = null;
        var dur = 1400;
        var step = function (ts) {
          if (!start) start = ts;
          var p = Math.min((ts - start) / dur, 1);
          var eased = 1 - Math.pow(1 - p, 3);
          el.textContent = Math.round(target * eased).toLocaleString();
          if (p < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
      });
    }, { threshold: 0.5 });
    counters.forEach(function (el) { cio.observe(el); });
  }

  /* ---------------- Before / After slider ---------------- */
  document.querySelectorAll('.ba-slider').forEach(function (slider) {
    var handle = slider.querySelector('.ba-handle');
    var afterPane = slider.querySelector('.ba-after');
    var input = slider.querySelector('.ba-range');
    if (!handle || !afterPane || !input) return;

    var set = function (pct) {
      pct = Math.max(0, Math.min(100, pct));
      slider.style.setProperty('--ba', pct + '%');
      input.value = pct;
      input.setAttribute('aria-valuenow', Math.round(pct));
    };

    var fromEvent = function (e) {
      var rect = slider.getBoundingClientRect();
      var x = (e.touches ? e.touches[0].clientX : e.clientX) - rect.left;
      set((x / rect.width) * 100);
    };

    var dragging = false;
    var startDrag = function (e) { dragging = true; slider.classList.add('is-dragging'); fromEvent(e); e.preventDefault(); };
    var moveDrag = function (e) { if (dragging) fromEvent(e); };
    var endDrag = function () { dragging = false; slider.classList.remove('is-dragging'); };

    slider.addEventListener('mousedown', startDrag);
    window.addEventListener('mousemove', moveDrag);
    window.addEventListener('mouseup', endDrag);

    // Touch: lock to an axis so vertical swipes scroll the page normally
    // and only deliberate horizontal drags move the seam.
    var startX = 0, startY = 0, touchMode = null;
    slider.addEventListener('touchstart', function (e) {
      startX = e.touches[0].clientX;
      startY = e.touches[0].clientY;
      touchMode = null;
    }, { passive: true });
    slider.addEventListener('touchmove', function (e) {
      if (touchMode === 'scroll') return;
      var dx = Math.abs(e.touches[0].clientX - startX);
      var dy = Math.abs(e.touches[0].clientY - startY);
      if (touchMode === null && (dx > 8 || dy > 8)) {
        touchMode = dx > dy ? 'drag' : 'scroll';
        if (touchMode === 'drag') slider.classList.add('is-dragging');
      }
      if (touchMode === 'drag') { fromEvent(e); e.preventDefault(); }
    }, { passive: false });
    slider.addEventListener('touchend', function () {
      touchMode = null;
      slider.classList.remove('is-dragging');
    });

    input.addEventListener('input', function () { set(parseFloat(input.value)); });
    set(parseFloat(input.value) || 50);
  });

  /* ---------------- FAQ accordion (details/summary is native; smooth open) ---------------- */
  document.querySelectorAll('.faq details').forEach(function (d) {
    d.addEventListener('toggle', function () {
      if (d.open) {
        document.querySelectorAll('.faq details[open]').forEach(function (other) {
          if (other !== d) other.open = false;
        });
      }
    });
  });

  /* ---------------- Gallery filter ---------------- */
  var filterBar = document.querySelector('.filter-bar');
  if (filterBar) {
    var items = document.querySelectorAll('[data-category]');
    filterBar.addEventListener('click', function (e) {
      var btn = e.target.closest('button[data-filter]');
      if (!btn) return;
      filterBar.querySelectorAll('button').forEach(function (b) {
        b.classList.toggle('is-active', b === btn);
        b.setAttribute('aria-pressed', b === btn ? 'true' : 'false');
      });
      var f = btn.getAttribute('data-filter');
      items.forEach(function (item) {
        var show = f === 'all' || item.getAttribute('data-category') === f;
        item.classList.toggle('is-hidden', !show);
      });
    });
  }

  /* ---------------- Lightbox ---------------- */
  var lbLinks = Array.prototype.slice.call(document.querySelectorAll('[data-lightbox]'));
  if (lbLinks.length) {
    var lb = document.createElement('div');
    lb.className = 'lightbox';
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-modal', 'true');
    lb.setAttribute('aria-label', 'Image viewer');
    lb.innerHTML =
      '<button class="lb-close" aria-label="Close">&times;</button>' +
      '<button class="lb-prev" aria-label="Previous image">&#8249;</button>' +
      '<figure><img alt=""><figcaption></figcaption></figure>' +
      '<button class="lb-next" aria-label="Next image">&#8250;</button>';
    document.body.appendChild(lb);

    var lbImg = lb.querySelector('img');
    var lbCap = lb.querySelector('figcaption');
    var idx = 0;
    var visibleLinks = function () {
      return lbLinks.filter(function (a) { return !a.closest('.is-hidden'); });
    };
    var openAt = function (links, i) {
      idx = (i + links.length) % links.length;
      var a = links[idx];
      lbImg.src = a.getAttribute('href');
      lbImg.alt = (a.querySelector('img') && a.querySelector('img').alt) || '';
      lbCap.textContent = a.getAttribute('data-caption') || lbImg.alt;
      lb.classList.add('is-open');
      document.body.style.overflow = 'hidden';
      lb.querySelector('.lb-close').focus();
    };
    var close = function () {
      lb.classList.remove('is-open');
      document.body.style.overflow = '';
      lbImg.src = '';
    };

    lbLinks.forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        var links = visibleLinks();
        openAt(links, links.indexOf(a));
      });
    });
    lb.querySelector('.lb-close').addEventListener('click', close);
    lb.querySelector('.lb-prev').addEventListener('click', function () { openAt(visibleLinks(), idx - 1); });
    lb.querySelector('.lb-next').addEventListener('click', function () { openAt(visibleLinks(), idx + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('is-open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') openAt(visibleLinks(), idx - 1);
      if (e.key === 'ArrowRight') openAt(visibleLinks(), idx + 1);
    });
  }

  /* ---------------- Current year ---------------- */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
