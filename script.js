/* ==========================================================================
   Small hands only: a veil, a ring, things arriving late, and a way to look
   closer at a specimen. No framework, no state machine, no cart.
   ========================================================================== */

(function () {
  "use strict";

  var root = document.documentElement;
  root.classList.add("js");

  var still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* --- The veil ---------------------------------------------------------- */

  var veil = $("[data-veil]");
  if (veil && !still) {
    requestAnimationFrame(function () { veil.classList.add("is-focusing"); });
    var ready = document.fonts ? document.fonts.ready : Promise.resolve();
    var capped = new Promise(function (r) { setTimeout(r, 1600); });
    Promise.all([ready, capped]).then(function () {
      veil.classList.add("is-lifted");
      setTimeout(function () { veil.remove(); }, 1000);
    });
  } else if (veil) {
    veil.remove();
  }

  /* --- Arriving late ------------------------------------------------------ */

  $$("[data-lines]").forEach(function (el) {
    el.classList.add("lines");
    $$(".ln > span", el).forEach(function (s, i) { s.style.setProperty("--d", i * 110 + "ms"); });
  });

  var lit = $$("[data-r], [data-lines], [data-lit]");

  if (still || !("IntersectionObserver" in window)) {
    lit.forEach(function (el) { el.classList.add("is-lit"); });
  } else {
    var eye = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add("is-lit");
        eye.unobserve(e.target);
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
    lit.forEach(function (el) { eye.observe(el); });

    // never leave a photograph hidden because an observer never fired
    setTimeout(function () {
      lit.forEach(function (el) {
        if (el.classList.contains("is-lit")) return;
        var r = el.getBoundingClientRect();
        if (r.top < window.innerHeight && r.bottom > 0) el.classList.add("is-lit");
      });
    }, 2600);
  }

  /* --- Overlay index ------------------------------------------------------ */

  var overlay = $("[data-overlay]");
  var opener = $("[data-open]");
  function hold(on) { document.body.classList.toggle("is-held", on); }

  if (overlay && opener) {
    opener.addEventListener("click", function () {
      overlay.classList.add("is-open"); hold(true);
      var first = $("a", overlay); if (first) first.focus();
    });
    $$("[data-close]", overlay).forEach(function (b) {
      b.addEventListener("click", function () { overlay.classList.remove("is-open"); hold(false); opener.focus(); });
    });
  }

  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    if (overlay && overlay.classList.contains("is-open")) { overlay.classList.remove("is-open"); hold(false); }
    closeViewer();
  });

  /* --- A thin ring instead of a pointer ----------------------------------- */

  var ring = $("[data-ring]");
  if (ring && window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
    var rx = 0, ry = 0, x = 0, y = 0, spin = null;
    window.addEventListener("mousemove", function (e) {
      rx = e.clientX; ry = e.clientY;
      ring.classList.add("is-awake");
      if (!spin) spin = requestAnimationFrame(follow);
    }, { passive: true });

    function follow() {
      spin = null;
      x += (rx - x) * 0.18; y += (ry - y) * 0.18;
      ring.style.transform = "translate(" + x.toFixed(1) + "px," + y.toFixed(1) + "px)";
      if (Math.abs(rx - x) > 0.4 || Math.abs(ry - y) > 0.4) spin = requestAnimationFrame(follow);
    }

    document.addEventListener("mouseover", function (e) {
      ring.classList.toggle("is-open", !!e.target.closest("a, button, [data-view]"));
    });
    document.addEventListener("mouseleave", function () { ring.classList.remove("is-awake"); });
  }

  /* --- Looking closer ----------------------------------------------------- */

  var viewer = $("[data-viewer]");
  var viewerImg = viewer && $("img", viewer);
  var viewerCap = viewer && $("figcaption", viewer);
  var lastLooked = null;

  function closeViewer() {
    if (!viewer || !viewer.classList.contains("is-open")) return;
    viewer.classList.remove("is-open");
    hold(false);
    if (lastLooked) lastLooked.focus();
  }

  if (viewer) {
    document.addEventListener("click", function (e) {
      var t = e.target.closest("[data-view]");
      if (t) {
        var img = $("img", t) || t;
        viewerImg.src = img.currentSrc || img.src;
        viewerImg.alt = img.alt || "";
        viewerCap.textContent = t.dataset.view || img.alt || "";
        viewer.classList.add("is-open");
        hold(true);
        lastLooked = t;
        return;
      }
      if (e.target.closest("[data-viewer]")) closeViewer();
    });
  }

  /* --- The running index on the garden ------------------------------------ */

  var contents = $("[data-contents]");
  if (contents && "IntersectionObserver" in window) {
    var marks = {};
    $$("a", contents).forEach(function (a) {
      var id = a.getAttribute("href").slice(1);
      marks[id] = a.parentElement;
    });
    var here = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var li = marks[e.target.id];
        if (li) li.classList.toggle("is-here", e.isIntersecting);
      });
    }, { rootMargin: "-45% 0px -45% 0px" });
    $$(".plate").forEach(function (p) { here.observe(p); });
  }

  /* --- The one form ------------------------------------------------------- */

  $$("[data-note]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var mail = $("input[type=email]", form);
      var note = $(".form-note", form);
      if (!mail || !note) return;
      var ok = /^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(mail.value.trim());
      note.textContent = ok ? form.dataset.note || "Thank you." : "That address doesn’t look right.";
      note.classList.add("is-shown");
      if (ok) form.reset();
    });
  });
})();
