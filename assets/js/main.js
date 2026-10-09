(function () {
  'use strict';

  /* Mobile menu */
  var header = document.querySelector('.site-header');
  var menuBtn = document.querySelector('.menu-btn');
  if (header && menuBtn) {
    menuBtn.addEventListener('click', function () {
      var open = header.classList.toggle('nav-open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && header.classList.contains('nav-open')) {
        header.classList.remove('nav-open');
        menuBtn.setAttribute('aria-expanded', 'false');
        menuBtn.focus();
      }
    });
  }

  /* Quote forms (Web3Forms). Falls back to a normal POST if JavaScript is off. */
  var PHONE_TEXT = '(713) 392-8790';
  document.querySelectorAll('form.quote-form').forEach(function (form) {
    var status = form.querySelector('.form-status');
    var btn = form.querySelector('button[type="submit"]');
    var original = btn ? btn.textContent : '';
    var qs = new URLSearchParams(location.search);
    form.querySelectorAll('input[data-qs]').forEach(function (i) { i.value = qs.get(i.getAttribute('data-qs')) || ''; });
    var src = form.querySelector('input[name="source_page"]');
    if (src) { src.value = location.pathname.split('/').pop() || 'index.html'; }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      btn.disabled = true;
      btn.textContent = 'Sending...';
      status.className = 'form-status';
      status.textContent = '';

      fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        headers: { 'Accept': 'application/json' },
        body: new FormData(form)
      })
        .then(function (res) { return res.json().then(function (j) { return { ok: res.ok, json: j }; }); })
        .then(function (r) {
          if (r.ok && r.json && r.json.success) {
            window.location.href = form.getAttribute('data-thanks') || 'thanks.html';
          } else {
            throw new Error((r.json && r.json.message) || 'Request failed');
          }
        })
        .catch(function () {
          status.className = 'form-status error';
          status.textContent = 'Your request did not go through. Please try again or call ' + PHONE_TEXT + '.';
          btn.disabled = false;
          btn.textContent = original;
        });
    });
  });

  /* Gallery filters */
  var filterBar = document.querySelector('.filters');
  if (filterBar) {
    var items = document.querySelectorAll('.masonry figure');
    filterBar.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-filter]');
      if (!b) { return; }
      filterBar.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
      b.setAttribute('aria-pressed', 'true');
      var f = b.getAttribute('data-filter');
      items.forEach(function (fig) {
        fig.hidden = !(f === 'all' || fig.getAttribute('data-cat') === f);
      });
    });
  }

  /* Lightbox */
  var lb = document.querySelector('.lightbox');
  if (lb) {
    var lbImg = lb.querySelector('img');
    var lbCap = lb.querySelector('p');
    var closeBtn = lb.querySelector('.lb-close');
    var lastFocus = null;
    function close() {
      lb.classList.remove('open');
      lbImg.removeAttribute('src');
      if (lastFocus) { lastFocus.focus(); }
    }
    document.querySelectorAll('.masonry button[data-large]').forEach(function (b) {
      b.addEventListener('click', function () {
        lastFocus = b;
        lbImg.src = b.getAttribute('data-large');
        lbImg.alt = b.getAttribute('data-alt') || '';
        lbCap.textContent = b.getAttribute('data-alt') || '';
        lb.classList.add('open');
        closeBtn.focus();
      });
    });
    closeBtn.addEventListener('click', close);
    lb.addEventListener('click', function (e) { if (e.target === lb) { close(); } });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && lb.classList.contains('open')) { close(); } });
  }

  var y = document.getElementById('year');
  if (y) { y.textContent = new Date().getFullYear(); }
})();
