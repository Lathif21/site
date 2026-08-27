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
  /* The trigger is a play/pause toggle, because a tutorial is something you
     stop halfway to go and do the thing. The button drives the video, and the
     video's own events drive the button — so the icon and the label stay right
     whether playback changed from the button, from the keyboard, or by the clip
     running out. State lives on the .v-inline host as [data-playing] so CSS can
     swap the glyph and lift the gradient without another class to keep in sync. */
  document.querySelectorAll('[data-video-trigger]').forEach(function (btn) {
    var video = document.getElementById(btn.getAttribute('data-video-trigger'));
    if (!video) return;
    var host = video.closest('.v-inline') || video.parentElement;
    var labelPlay  = btn.getAttribute('data-label-play')  || btn.getAttribute('aria-label');
    var labelPause = btn.getAttribute('data-label-pause') || labelPlay;

    function sync() {
      var playing = !video.paused && !video.ended;
      btn.setAttribute('aria-label', playing ? labelPause : labelPlay);
      if (host) {
        if (playing) host.setAttribute('data-playing', '');
        else host.removeAttribute('data-playing');
      }
    }

    function toggle(e) {
      if (e) e.preventDefault();
      if (video.paused || video.ended) {
        video.removeAttribute('data-idle');
        video.removeAttribute('aria-hidden');
        video.removeAttribute('tabindex');
        var r = video.play();
        if (r && r.catch) r.catch(function () {});
      } else {
        video.pause();
      }
    }

    btn.addEventListener('click', toggle);
    /* the overlay no longer swallows clicks, so the frame itself is a target */
    video.addEventListener('click', toggle);
    ['play', 'pause', 'ended'].forEach(function (ev) {
      video.addEventListener(ev, sync);
    });
    sync();
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
