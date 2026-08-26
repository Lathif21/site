/* Poster-first video.
   ------------------------------------------------------------------
   The webshop hero now runs ambient: video/ov-mortex.* is a real montage cut
   from the client's own photography (kit -> build -> finish -> styled), so it
   carries `autoplay` directly in the markup and never reaches this file — it
   has no trigger button.

   The remaining players are deliberately poster-first: the webshop video band
   and the PDP module both lead with a play button, so the visitor decides.
   Give any of them ambient playback by adding `autoplay` to the element; the
   markup, posters and reduced-motion fallback already assume it.
   ------------------------------------------------------------------ */

(function () {
  function play(video, btn) {
    video.removeAttribute('data-idle');
    if (!video.hasAttribute('controls')) video.setAttribute('controls', '');
    video.removeAttribute('aria-hidden');
    video.removeAttribute('tabindex');
    const r = video.play();
    if (r) r.catch(function () {});
    if (btn) btn.hidden = true;
  }

  document.querySelectorAll('[data-video-trigger]').forEach(function (btn) {
    const target = document.getElementById(btn.getAttribute('data-video-trigger'));
    if (!target) return;
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      play(target, btn);
    });
  });
})();

/* ---- reduced motion ----
   The stylesheet hides ambient clips under prefers-reduced-motion, but a hidden
   <video autoplay> keeps decoding: the preference is honoured visually and
   ignored everywhere else. Stop it for real and let the poster stand in. */
(function () {
  var mq = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)');
  if (!mq || !mq.matches) return;
  document.querySelectorAll('video[autoplay]').forEach(function (v) {
    v.autoplay = false;
    v.pause();
  });
})();
