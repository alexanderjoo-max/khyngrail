/* ==========================================================================
   Motion
   One observer drives every reveal, so the whole site shares an easing and a
   rhythm. Without JS, or with prefers-reduced-motion, everything is simply
   already visible.
   ========================================================================== */

(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* --- Page curtain ----------------------------------------------------- */

  var curtain = document.querySelector("[data-curtain]");

  function liftCurtain() {
    if (!curtain) return;
    if (reduced) { curtain.remove(); return; }
    curtain.classList.add("is-lifting");
    setTimeout(function () { curtain.style.display = "none"; }, 1000);
  }

  if (curtain && !reduced) {
    var ready = document.fonts ? document.fonts.ready : Promise.resolve();
    var capped = new Promise(function (r) { setTimeout(r, 900); });
    Promise.race([ready, capped]).then(function () { setTimeout(liftCurtain, 100); });
  } else {
    liftCurtain();
  }

  if (curtain && !reduced) {
    document.addEventListener("click", function (e) {
      var a = e.target.closest("a[href]");
      if (!a || a.target || a.hasAttribute("download")) return;
      if (a.hasAttribute("data-open-cart")) return;
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;

      var url = new URL(a.href, location.href);
      if (url.origin !== location.origin) return;
      if (url.pathname === location.pathname) return;   // in-page anchor

      e.preventDefault();
      curtain.style.display = "";
      curtain.classList.remove("is-lifting");
      curtain.classList.add("is-dropping");
      setTimeout(function () { location.href = url.href; }, 540);
    });
  }

  window.addEventListener("pageshow", function (e) {
    if (e.persisted && curtain) {
      curtain.classList.remove("is-dropping");
      curtain.style.display = "none";
    }
  });

  /* --- Reveal ----------------------------------------------------------- */

  document.querySelectorAll("[data-lines]").forEach(function (el) {
    el.classList.add("lines");
    el.querySelectorAll(".ln > span").forEach(function (span, i) {
      span.style.setProperty("--d", i * 95 + "ms");
    });
  });

  var revealables = document.querySelectorAll("[data-anim], [data-lines], [data-plate]");

  if (reduced || !("IntersectionObserver" in window)) {
    revealables.forEach(function (el) { el.classList.add("is-in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-in");
        io.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    revealables.forEach(function (el) { io.observe(el); });

    // Belt and braces: if anything is still hidden while sitting in the
    // viewport a few seconds in, reveal it rather than leave a blank frame.
    setTimeout(function () {
      revealables.forEach(function (el) {
        if (el.classList.contains("is-in")) return;
        var r = el.getBoundingClientRect();
        if (r.top < window.innerHeight && r.bottom > 0) el.classList.add("is-in");
      });
    }, 2500);
  }

  /* --- Counters --------------------------------------------------------- */

  document.querySelectorAll("[data-count]").forEach(function (el) {
    var target = parseFloat(el.dataset.count);
    var decimals = parseInt(el.dataset.decimals || "0", 10);
    var suffix = el.dataset.suffix || "";
    var show = function (v) { el.textContent = v.toFixed(decimals) + suffix; };

    if (reduced || !("IntersectionObserver" in window)) { show(target); return; }

    var ob = new IntersectionObserver(function (entries) {
      if (!entries[0].isIntersecting) return;
      ob.disconnect();
      var start = performance.now();
      (function tick(now) {
        var p = Math.min((now - start) / 1400, 1);
        show(target * (1 - Math.pow(1 - p, 4)));
        if (p < 1) requestAnimationFrame(tick);
      })(start);
    }, { threshold: 0.6 });
    ob.observe(el);
  });

  /* --- Scroll-driven ---------------------------------------------------- */

  var header = document.querySelector("[data-header]");
  var parallaxEls = Array.prototype.slice.call(document.querySelectorAll("[data-parallax]"));
  var oil = document.querySelector("[data-oil]");

  var ticking = false;

  function frame() {
    ticking = false;
    var y = window.scrollY;

    if (header) header.classList.toggle("is-stuck", y > 8);

    if (reduced) return;

    /* Photography drifts a few percent against its frame — never more. */
    parallaxEls.forEach(function (el) {
      var box = el.parentElement.getBoundingClientRect();
      if (box.bottom < -200 || box.top > window.innerHeight + 200) return;
      var mid = (box.top + box.height / 2 - window.innerHeight / 2) / window.innerHeight;
      var amount = parseFloat(el.dataset.parallax) || 0.08;
      el.style.transform = "scale(1.14) translate3d(0," + (mid * amount * 100).toFixed(2) + "%,0)";
    });

    /* The oil macro settles as the band crosses the viewport. */
    if (oil) {
      var r = oil.getBoundingClientRect();
      var span = r.height + window.innerHeight;
      var p = Math.min(Math.max((window.innerHeight - r.top) / span, 0), 1);
      oil.style.setProperty("--oil-scale", (1.24 - p * 0.14).toFixed(3));
    }
  }

  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll, { passive: true });
  frame();
})();
