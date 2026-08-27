/* ==========================================================================
   Site behaviour — navigation, bag, product controls, forms
   ========================================================================== */

(function () {
  "use strict";

  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* --- Mobile navigation ------------------------------------------------ */

  var toggle = $("[data-menu-toggle]");
  var mobileNav = $("[data-mobile-nav]");

  if (toggle && mobileNav) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      mobileNav.classList.toggle("is-open", !open);
      document.body.classList.toggle("is-locked", !open);
    });

    mobileNav.addEventListener("click", function (e) {
      if (!e.target.closest("a")) return;
      toggle.setAttribute("aria-expanded", "false");
      mobileNav.classList.remove("is-open");
      document.body.classList.remove("is-locked");
    });
  }

  /* --- Bag -------------------------------------------------------------- */

  var drawer = $("[data-drawer]");
  var scrim = $("[data-scrim]");
  var cartBody = $("[data-cart-body]");
  var cartTotal = $("[data-cart-total]");
  var cartCount = $("[data-cart-count]");
  var lastFocus = null;

  var PRODUCT = { sku: "KG215", name: "Botanical Oils Facial Serum", price: 69, img: "assets/img/bottle.png" };
  var qty = 0;

  function money(n) { return "$" + n.toFixed(2); }

  function renderCart() {
    if (!cartBody) return;

    if (qty === 0) {
      cartBody.innerHTML = '<p class="cart-empty">Your bag is empty. KG215 is waiting.</p>';
    } else {
      cartBody.innerHTML =
        '<div class="cart-item">' +
        '<img src="' + PRODUCT.img + '" alt="" width="120" height="263" />' +
        "<div><h3>" + PRODUCT.name + "</h3>" +
        "<p>" + PRODUCT.sku + " · Qty " + qty + "</p>" +
        "<p>" + money(PRODUCT.price * qty) + "</p></div></div>";
    }

    if (cartTotal) cartTotal.textContent = money(PRODUCT.price * qty);
    if (cartCount) {
      cartCount.textContent = String(qty);
      cartCount.classList.toggle("is-shown", qty > 0);
    }
  }

  function openCart() {
    if (!drawer) return;
    lastFocus = document.activeElement;
    drawer.classList.add("is-open");
    if (scrim) scrim.classList.add("is-open");
    document.body.classList.add("is-locked");
    var close = $("[data-close-cart]", drawer);
    if (close) close.focus();
  }

  function closeCart() {
    if (!drawer) return;
    drawer.classList.remove("is-open");
    if (scrim) scrim.classList.remove("is-open");
    document.body.classList.remove("is-locked");
    if (lastFocus) lastFocus.focus();
  }

  document.addEventListener("click", function (e) {
    if (e.target.closest("[data-open-cart]")) { e.preventDefault(); openCart(); }
    if (e.target.closest("[data-close-cart]") || e.target === scrim) closeCart();
  });

  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    if (drawer && drawer.classList.contains("is-open")) closeCart();
    if (mobileNav && mobileNav.classList.contains("is-open") && toggle) toggle.click();
  });

  // Keep focus inside the open drawer.
  if (drawer) {
    drawer.addEventListener("keydown", function (e) {
      if (e.key !== "Tab") return;
      var items = $$('a[href], button:not([disabled]), input', drawer);
      if (!items.length) return;
      var first = items[0], last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  }

  /* --- Quantity stepper ------------------------------------------------- */

  var stepper = $("[data-qty]");
  var qtyValue = $("[data-qty-value]");
  var pending = 1;

  if (stepper && qtyValue) {
    stepper.addEventListener("click", function (e) {
      var btn = e.target.closest("button[data-step]");
      if (!btn) return;
      var next = pending + (btn.dataset.step === "up" ? 1 : -1);
      if (next < 1 || next > 9) return;
      pending = next;
      // Roll the numeral in the direction of travel.
      qtyValue.classList.remove("is-up", "is-down");
      void qtyValue.offsetWidth;
      qtyValue.textContent = pending;
      qtyValue.classList.add(btn.dataset.step === "up" ? "is-up" : "is-down");
    });
  }

  /* --- Add to bag ------------------------------------------------------- */

  var addBtn = $("[data-add]");
  if (addBtn) {
    addBtn.addEventListener("click", function () {
      qty += pending;
      renderCart();
      addBtn.classList.add("is-added");
      setTimeout(function () { addBtn.classList.remove("is-added"); }, 1200);
      setTimeout(openCart, 260);
    });
  }

  /* --- Botanical slider --------------------------------------------------
     scrollBy() is unreliable inside a snap container, so the position is
     animated directly. Drag, trackpad and keyboard all still drive it.      */

  var noMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  $$("[data-slider]").forEach(function (slider) {
    var track = $("[data-slider-track]", slider);
    var dotsWrap = $("[data-slider-dots]", slider);
    var prev = $("[data-slider-prev]", slider);
    var next = $("[data-slider-next]", slider);
    if (!track) return;
    var slides = $$(":scope > *", track);
    if (!slides.length) return;

    function maxScroll() { return track.scrollWidth - track.clientWidth; }

    function sync() {
      var mid = track.scrollLeft + track.clientWidth / 2;
      var closest = 0, best = Infinity;
      slides.forEach(function (slide, i) {
        var c = slide.offsetLeft - track.offsetLeft + slide.offsetWidth / 2;
        var d = Math.abs(c - mid);
        if (d < best) { best = d; closest = i; }
      });
      dots.forEach(function (d, i) {
        d.setAttribute("aria-selected", i === closest ? "true" : "false");
      });
      if (prev) prev.disabled = track.scrollLeft < 4;
      if (next) next.disabled = track.scrollLeft > maxScroll() - 4;
    }

    function glideTo(target) {
      target = Math.max(0, Math.min(target, maxScroll()));
      if (noMotion) { track.scrollLeft = target; sync(); return; }
      var from = track.scrollLeft;
      var delta = target - from;
      var t0 = performance.now();
      (function step(now) {
        var p = Math.min((now - t0) / 480, 1);
        track.scrollLeft = from + delta * (1 - Math.pow(1 - p, 3));
        sync();
        if (p < 1) requestAnimationFrame(step);
      })(t0);
    }

    var dots = slides.map(function (slide, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.setAttribute("role", "tab");
      b.setAttribute("aria-selected", i === 0 ? "true" : "false");
      b.setAttribute("aria-label", (slide.textContent || "").trim() || "Oil " + (i + 1));
      b.addEventListener("click", function () {
        var left = slide.offsetLeft - track.offsetLeft;
        glideTo(left - (track.clientWidth - slide.offsetWidth) / 2);
      });
      if (dotsWrap) dotsWrap.appendChild(b);
      return b;
    });

    function page(dir) { glideTo(track.scrollLeft + dir * track.clientWidth * 0.8); }

    if (prev) prev.addEventListener("click", function () { page(-1); });
    if (next) next.addEventListener("click", function () { page(1); });

    track.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); page(1); }
      if (e.key === "ArrowLeft") { e.preventDefault(); page(-1); }
    });

    var raf = null;
    track.addEventListener("scroll", function () {
      if (!raf) raf = requestAnimationFrame(function () { raf = null; sync(); });
    }, { passive: true });
    window.addEventListener("resize", sync);
    sync();
  });

  /* --- Product gallery -------------------------------------------------- */

  var gallery = $("[data-gallery]");
  if (gallery) {
    var main = $("[data-gallery-main]", gallery);
    gallery.addEventListener("click", function (e) {
      var thumb = e.target.closest("[data-thumb]");
      if (!thumb || !main) return;
      $$("[data-thumb]", gallery).forEach(function (t) { t.setAttribute("aria-current", "false"); });
      thumb.setAttribute("aria-current", "true");
      main.classList.add("is-swapping");
      setTimeout(function () {
        main.src = thumb.dataset.full;
        main.alt = thumb.dataset.alt || "";
        main.classList.remove("is-swapping");
      }, 220);
    });
  }

  /* --- Accordion -------------------------------------------------------- */

  $$("[data-accordion]").forEach(function (acc) {
    acc.addEventListener("click", function (e) {
      var btn = e.target.closest("[data-acc-trigger]");
      if (!btn) return;
      var panel = document.getElementById(btn.getAttribute("aria-controls"));
      var open = btn.getAttribute("aria-expanded") === "true";

      $$("[data-acc-trigger]", acc).forEach(function (other) {
        if (other === btn) return;
        other.setAttribute("aria-expanded", "false");
        var p = document.getElementById(other.getAttribute("aria-controls"));
        if (p) p.style.height = "0px";
      });

      btn.setAttribute("aria-expanded", String(!open));
      if (!panel) return;
      panel.style.height = open ? "0px" : panel.scrollHeight + "px";
    });
  });

  /* --- Newsletter ------------------------------------------------------- */

  $$("[data-newsletter]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var input = $("input[type=email]", form);
      var status = $("[data-form-status]", form);
      if (!input || !status) return;

      var ok = /^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(input.value.trim());
      var isContact = form.classList.contains("contact__form");
      status.textContent = ok
        ? (isContact ? "Sent. We’ll write back within a day or two." : "You’re on the list. Check your inbox to confirm.")
        : "That email address doesn’t look right.";
      status.classList.add("is-shown");
      if (ok) { form.reset(); } else { input.focus(); }
    });
  });

  renderCart();
})();
