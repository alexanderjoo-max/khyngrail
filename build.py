#!/usr/bin/env python3
"""Compose the three static pages from shared chrome + per-page bodies."""

FONTS = (
    '    <link rel="preconnect" href="https://fonts.googleapis.com" />\n'
    '    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\n'
    '    <link href="https://fonts.googleapis.com/css2?family=Jost:ital,wght@0,400;0,500;0,600;'
    '1,400;1,500;1,600&family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;1,8..60,400'
    '&display=swap" rel="stylesheet" />\n'
    '    <link rel="stylesheet" href="css/site.css" />'
)

STAR = ('<svg viewBox="0 0 28 26" aria-hidden="true"><path d="M14 0l3.11 9.57H27.2l-8.14 5.91 '
        '3.11 9.57L14 19.14l-8.14 5.91 3.11-9.57L.82 9.57h10.06L14 0z"/></svg>')
STARS = '<span class="stars" aria-hidden="true">' + STAR * 5 + '</span>'

# Reveal states are only applied once JS is confirmed, so content can never be
# left hidden by a script that failed to run.
NOJS = ('<script>document.documentElement.className='
        'document.documentElement.className.replace("no-js","js");</script>')

ANNOUNCE = """    <p class="announce">Preorder now &ndash; Ships in November</p>"""


def header(current, mode=""):
    """mode: "" solid cream · "float" over a light hero · "over" over a dark hero."""
    def link(href, label, key):
        cur = ' aria-current="page"' if key == current else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    over_cls = f" site-header--{mode}" if mode else ""
    return f"""    <header class="site-header{over_cls}" data-header>
      <div class="header-inner">
        <div class="header-left">
          <button class="menu-toggle" type="button" data-menu-toggle aria-expanded="false" aria-controls="mobile-nav" aria-label="Menu">
            <span></span><span></span>
          </button>
          <nav class="nav" aria-label="Primary">
            {link("product.html", "Shop", "shop")}
            {link("about.html", "About", "about")}
            {link("about.html#contact", "Contact", "contact")}
          </nav>
        </div>
        <a class="logo" href="index.html" aria-label="Khyn &amp; Grail — home">
          <img class="logo__img" src="assets/img/logo.png" alt="Khyn &amp; Grail" width="500" height="121" />
        </a>
        <div class="header-tools">
          <a class="tool" href="about.html#contact" aria-label="Account">
            <img src="assets/icons/account.svg" alt="" width="22" height="24" />
          </a>
          <button class="tool" type="button" data-open-cart aria-label="Bag">
            <img src="assets/icons/bag.svg" alt="" width="22" height="24" />
            <span class="cart-btn__count" data-cart-count>0</span>
          </button>
        </div>
      </div>
    </header>

    <nav class="mobile-nav" id="mobile-nav" data-mobile-nav aria-label="Mobile">
      <a href="product.html">Shop</a>
      <a href="about.html">About</a>
      <a href="about.html#contact">Contact</a>
      <a href="#bag" data-open-cart>Bag</a>
    </nav>"""


NEWSLETTER = """      <section class="newsletter">
        <div class="newsletter__inner">
          <h2 class="h2" data-anim="rise">Newsletter</h2>
          <p data-anim="rise" style="--d: 90ms">Get it first.</p>
          <form class="newsletter__form" data-newsletter novalidate data-anim="rise" style="--d: 180ms">
            <div class="newsletter__row">
              <label class="field">
                <span class="sr-only">Email</span>
                <input type="email" name="email" placeholder="Email" autocomplete="email" required />
              </label>
              <button class="btn" type="submit">Subscribe</button>
            </div>
            <p class="form-status" data-form-status role="status"></p>
          </form>
        </div>
      </section>"""

FOOTER = """    <footer class="site-footer">
      <div class="footer-inner">
        <div class="footer-brand">
          <a href="index.html" aria-label="Khyn &amp; Grail — home">
            <img class="footer-brand__logo" src="assets/img/logo.png" alt="Khyn &amp; Grail" width="500" height="121" />
          </a>
          <p>Fancy Skincare for Smart People #StayRich</p>
        </div>
        <nav class="footer-nav" aria-label="Footer">
          <a href="https://skinskool.com" rel="noopener">SKINSKOOL</a>
          <a href="about.html#faq">Terms &amp; Conditions</a>
          <a href="about.html#faq">Privacy Policy</a>
          <a href="about.html#faq">Return Policy</a>
          <a href="about.html#contact">Contact</a>
        </nav>
      </div>
    </footer>

    <div class="drawer-scrim" data-scrim></div>
    <aside class="drawer" data-drawer role="dialog" aria-modal="true" aria-label="Your bag">
      <div class="drawer__head">
        <h2 class="label">Your bag</h2>
        <button class="link" type="button" data-close-cart>Close</button>
      </div>
      <div class="drawer__body" data-cart-body></div>
      <div class="drawer__foot">
        <p class="drawer__line"><span>Subtotal</span><span data-cart-total>$0.00</span></p>
        <a class="btn btn--block" href="product.html">Checkout</a>
      </div>
    </aside>

    <script src="js/site.js" defer></script>
    <script src="js/motion.js" defer></script>"""


def marquee(word="Hacking luxury skincare.", variant="", speed="40s", n=8):
    spans = "".join(f"<span>{word}</span>" for _ in range(n))
    return f"""      <div class="marquee {variant}" aria-hidden="true">
        <div class="marquee__track" style="--speed: {speed}">{spans}</div>
      </div>"""


def page(title, desc, body_class, head_extra, chrome, body):
    return f"""<!DOCTYPE html>
<html lang="en" class="no-js">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title}</title>
    <meta name="description" content="{desc}" />
    <meta name="theme-color" content="#f7f2e7" />
    {NOJS}
{FONTS}{head_extra}
  </head>

  <body class="{body_class}">
    <a class="skip-link" href="#main">Skip to content</a>

    <div class="curtain" data-curtain aria-hidden="true">
      <img src="assets/img/logo.png" alt="" width="500" height="121" />
    </div>

{ANNOUNCE}

{chrome}

    <main id="main">
{body}
{NEWSLETTER}
    </main>

{FOOTER}
  </body>
</html>
"""
