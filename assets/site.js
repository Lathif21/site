/* Atelier DIY replica — mobile nav, FAQ accordion, cookie bar. */

/* ---- mobile navigation ---- */
(function () {
  var burger = document.getElementById('burger');
  var nav = document.getElementById('nav');
  if (!burger || !nav) return;

  burger.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    burger.setAttribute('aria-expanded', String(open));
  });

  // close when a link is used, or when the viewport grows past the breakpoint
  nav.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') {
      nav.classList.remove('open');
      burger.setAttribute('aria-expanded', 'false');
    }
  });
  // Safari < 14 has matchMedia but no addEventListener on MediaQueryList, and a
  // throw here would abort the rest of this file — taking the FAQ accordion and
  // the cookie bar down with it. Feature-detect instead.
  var mq = window.matchMedia && window.matchMedia('(min-width: 1024px)');
  if (mq) {
    var closeOnWide = function (m) {
      if (!m.matches) return;
      nav.classList.remove('open');
      burger.setAttribute('aria-expanded', 'false');
    };
    if (mq.addEventListener) mq.addEventListener('change', closeOnWide);
    else if (mq.addListener) mq.addListener(closeOnWide);
  }
})();

/* ---- FAQ accordion ----
   One panel open at a time, matching the live page. */
(function () {
  var qs = document.querySelectorAll('.faq-q');
  if (!qs.length) return;

  qs.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') === 'true';
      qs.forEach(function (o) { o.setAttribute('aria-expanded', 'false'); });
      btn.setAttribute('aria-expanded', String(!open));
    });
  });
})();

/* ---- video CTA ----
   The button reveals the player and starts it, instead of navigating away.
   When the clip ends, or Escape is pressed, the panel returns to its poster
   state so the copy and the button are readable again. */
(function () {
  var cta = document.getElementById('videoCta');
  var btn = document.getElementById('videoCtaPlay');
  var player = document.getElementById('videoCtaPlayer');
  if (!cta || !btn || !player) return;

  function stop() {
    if (!cta.classList.contains('playing')) return;
    player.pause();
    cta.classList.remove('playing');
    btn.setAttribute('aria-expanded', 'false');
    btn.focus();
  }

  btn.addEventListener('click', function () {
    cta.classList.add('playing');
    btn.setAttribute('aria-expanded', 'true');
    player.focus();
    // play() rejects when autoplay policy or a missing file blocks it; the
    // controls are still there, so just leave the player open.
    var p = player.play();
    if (p && p.catch) p.catch(function () {});
  });

  player.addEventListener('ended', stop);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') stop();
  });
})();

/* ---- cookie bar ----
   sessionStorage rather than a real consent cookie: this is a static replica,
   nothing is actually tracked. Swap in the real consent script before use.  */
(function () {
  var bar = document.getElementById('cookie');
  if (!bar) return;

  var stored = null;
  try { stored = sessionStorage.getItem('cookie-choice'); } catch (e) {}
  if (stored) { bar.hidden = true; return; }

  bar.addEventListener('click', function (e) {
    var choice = e.target.getAttribute && e.target.getAttribute('data-cookie');
    if (!choice) return;
    try { sessionStorage.setItem('cookie-choice', choice); } catch (err) {}
    bar.hidden = true;
  });
})();
