#!/usr/bin/env python3
"""Page bodies. All visible copy is taken verbatim from the KG215 design."""
import os, html
from build import page, header, marquee, STARS

# ---------------------------------------------------------------- HOME -----

CREDS = [
    ("stat-organic.svg",     "svg", "27 Ingredients"),
    ("stat-skintypes.svg",   "svg", "All Skin Types"),
    ("stat-usa.svg",         "svg", "Made in USA"),
    ("stat-single-batch.png", "png", "Single Batch"),
    ("stat-ships.png",        "png", "Ships November"),
]

def cred(i, icon, kind, text):
    return (f'          <div class="cred" data-anim="rise" style="--d: {i*80}ms">\n'
            f'            <img src="assets/icons/{icon}" alt="" />\n'
            f'            <span>{text}</span>\n          </div>')

VCARDS = [
    ("review-1.jpg", "Ali and Kadija talking about the serum on camera",
     "&ldquo;She&rsquo;s glowing! She&rsquo;s dewy!&rdquo;", "- Ali &amp; Kadija"),
    ("review-2.jpg", "Nadj and Sophie holding the KG215 bottle on camera",
     "&ldquo;I&rsquo;m obsessed with it&rdquo;", "- Nadj &amp; Sophie"),
    ("review-3.jpg", "Mahshid and Camille smelling the serum on camera",
     "&ldquo;It smells SO good!&rdquo;", "- Mahshid &amp; Camille"),
]

def vcard(i, img, alt, quote, who):
    return f"""            <figure class="vcard" data-anim="rise" style="--d: {i*120}ms">
              <div class="vcard__media">
                <img src="assets/img/{img}" alt="{alt}" width="520" height="794" />
                <span class="vcard__play" aria-hidden="true"><i></i></span>
                <figcaption class="vcard__cap">
                  <p class="vcard__quote">{quote}</p>
                  <p class="vcard__who">{who}</p>
                </figcaption>
              </div>
            </figure>"""

HOME_BODY = f"""      <section class="hero">
        <figure class="hero__media">
          <img data-parallax="0.07" src="assets/img/hero-portrait.jpg"
               alt="A woman pressing golden botanical oil into her cheek with a glass dropper"
               width="2000" height="1116" fetchpriority="high" />
        </figure>
        <div class="hero__inner">
          <div class="hero__copy">
            <h1 class="display hero__title lines" data-lines>
              <span class="ln"><span>You already</span></span>
              <span class="ln"><span>know</span></span>
            </h1>
            <a class="btn" href="about.html" data-anim="rise" style="--d: 480ms">About Us</a>
          </div>
        </div>
      </section>

      <section class="creds" aria-label="Product credentials">
        <div class="creds__pill">
{chr(10).join(cred(i, *c) for i, c in enumerate(CREDS))}
        </div>
      </section>

      <section class="oil" data-oil>
        <div class="oil__media">
          <img src="assets/img/oil.jpg" alt="Macro photograph of golden botanical oil suspended in water" width="2000" height="1116" />
        </div>
        <div class="oil__inner">
          <article class="oil__card" data-anim="rise">
            <h2 class="h2">Khyn &amp; Grail comes from SkinSkool &mdash;</h2>
            <p>
              Eight years, sixty thousand formulas, more expensive bottles taken apart and
              understood than we can count. We stopped comparing a long time ago.
            </p>
            <a class="btn btn--outlineLight" href="about.html">About Us</a>
          </article>
        </div>
      </section>

      <section class="spot">
        <div class="spot__inner">
          <div class="spot__copy" data-anim="rise">
            <img class="spot__bottle" src="assets/img/bottle.png" alt="Khyn &amp; Grail KG215 white dropper bottle" width="600" height="1316" />
            <p class="spot__sku">KG215</p>
            <h2 class="h2">Botanical Oils Facial Serum</h2>
            {STARS}
            <p class="lede">
              27 pressed botanical oils &mdash; grape seed, rosehip, jasmine, frankincense among
              them. Rich without sitting heavy. Sinks in slow and finishes like skin, not oil.
            </p>
            <a class="btn" href="product.html">Preorder</a>
          </div>
          <figure class="spot__still" data-anim="rise" style="--d: 140ms">
            <img data-parallax="0.05" src="assets/img/lifestyle.jpg" alt="KG215 bottle on a marble stand beside its navy carton" width="1086" height="1448" />
          </figure>
        </div>
      </section>

{marquee(speed="46s")}

      <section class="reviews">
        <div class="reviews__inner">
          <h2 class="h2 reviews__title" data-anim="rise">Product Reviews</h2>

          <div class="reviews__wall">
{chr(10).join(vcard(i, *v) for i, v in enumerate(VCARDS))}
          </div>

          <blockquote class="reviews__quote" data-anim="rise">
            <p>
              &ldquo;I&rsquo;m in my 50&rsquo;s and have been managing rosacea, large pores and
              sensitive skin for my entire life. I&rsquo;ve tried 100&rsquo;s of products. This
              serum is magical! It has not only evened out my skin tone but my pores are noticeably
              smaller and my skin is brighter and smoother. And the wonderful earthy smell is just
              an added bonus! And don&rsquo;t just take my word for it, friends and family have
              taken notice. Love it. Highly recommend.&rdquo;
            </p>
            <footer>&mdash; D.M.</footer>
          </blockquote>

          <p class="hashtag" data-anim="rise">#stayrich</p>
        </div>
      </section>"""

# ------------------------------------------------------------- PRODUCT -----

THUMBS = [
    ("product-hero.jpg", "KG215 bottle with orchids and a dish of botanical oil", 1254, 1254),
    ("lab-light.jpg", "KG215 on a bright apothecary bench of glassware and herbs", 900, 600),
    ("lab-dark.jpg", "KG215 among dark laboratory glassware and dried botanicals", 900, 600),
    ("bottle-render.jpg", "The KG215 bottle, front of pack", 527, 1155),
]

def thumb(i, img, alt, w, h):
    cur = "true" if i == 0 else "false"
    return f"""              <button class="thumb" type="button" data-thumb aria-current="{cur}"
                      data-full="assets/img/{img}" data-alt="{alt}">
                <img src="assets/img/{img}" alt="View {i+1}" width="{w}" height="{h}" />
              </button>"""

BOT_NAMES = {
 "acai": "Açaí", "alfalfa": "Alfalfa", "avocado": "Avocado", "bergamot": "Bergamot",
 "bitter-orange": "Bitter Orange", "calendula": "Calendula", "caprylic": "Caprylic",
 "carrot-seed": "Carrot Seed", "cypress": "Cypress", "dandelion-root": "Dandelion Root",
 "evening-primrose": "Evening Primrose", "frankincense": "Frankincense", "galbanum": "Galbanum",
 "grapeseed": "Grape Seeds", "hazelnut": "Hazelnuts", "jasmine": "Jasmine", "lavendar": "Lavender",
 "lemon-peel": "Lemon Peel", "pequi": "Pequi", "rose-hip---dog-rose": "Rosehip",
 "rose": "Rose", "rosemary": "Rosemary", "safflower": "Safflower", "seabuckthorn": "Sea Buckthorn",
 "sunflower": "Sunflower", "tumeric": "Turmeric", "white-nettle": "White Nettle",
}

def botanical_slides():
    files = sorted(os.listdir("assets/ingredients"))
    out = []
    for f in files:
        slug = f.rsplit(".", 1)[0]
        label = BOT_NAMES.get(slug, slug.replace("-", " ").title())
        out.append(
            f'            <figure class="bot">\n'
            f'              <img src="assets/ingredients/{f}" alt="{html.escape(label)}" width="1000" height="1000" />\n'
            f'              <figcaption>{html.escape(label)}</figcaption>\n'
            f'            </figure>')
    return "\n".join(out)

MOSAIC = [
    ("left",  "macro-grape.jpg", "Extreme macro of dark purple grapes bursting",
     "Grape Seed", "Light, fast-absorbing, high in linoleic acid."),
    ("right", "oil.jpg", "Extreme macro of golden botanical oil",
     "Rosehip &amp; Jasmine", "Cold-pressed, unrefined, used at real concentrations."),
    ("left",  "macro-calendula.jpg", "Extreme macro of calendula petals suspended in clear oil",
     "Frankincense", "Resin-pressed. A small amount, used for a reason."),
    ("right", "macro-sunflower.jpg", "Extreme macro of a sunflower seed head",
     "Tocopherol", "Natural vitamin E, keeps the blend stable."),
]

def mosaic():
    rows = []
    for side, img, alt, name, body in MOSAIC:
        flip = " mos__row--flip" if side == "right" else ""
        rows.append(f"""          <div class="mos__row{flip}">
            <figure class="mos__media" data-anim="rise">
              <img src="assets/img/{img}" alt="{alt}" width="1400" height="781" />
            </figure>
            <div class="mos__copy" data-anim="rise" style="--d: 120ms">
              <h3 class="h3 coral">{name}</h3>
              <p>{body}</p>
            </div>
          </div>""")
    return "\n".join(rows)

BARS = [(5, 137), (4, 10), (3, 3), (2, 0), (1, 0)]

def bars():
    total = sum(c for _, c in BARS)
    out = []
    for i, (star, count) in enumerate(BARS):
        pct = round(count / total * 100, 1)
        out.append(f"""            <div class="bar">
              <span class="bar__key">{star} star</span>
              <span class="bar__track"><i style="--pct: {pct}%; --d: {i*90}ms"></i></span>
              <span class="bar__count">{count}</span>
            </div>""")
    return "\n".join(out)

PRODUCT_BODY = f"""      <article class="pdp">
        <div class="pdp__inner">
          <div class="gallery" data-gallery>
            <figure class="gallery__main" data-anim="fade">
              <img data-gallery-main src="assets/img/product-hero.jpg"
                   alt="KG215 bottle with orchids and a dish of botanical oil"
                   width="1254" height="1254" fetchpriority="high" />
            </figure>
            <div class="thumbs">
{chr(10).join(thumb(i, *t) for i, t in enumerate(THUMBS))}
            </div>
          </div>

          <div class="buy">
            <p class="spot__sku" data-anim="rise">KG215</p>
            <h1 class="h1" data-anim="rise" style="--d: 60ms">Botanical Oils Facial Serum</h1>
            <div data-anim="rise" style="--d: 120ms">{STARS}</div>

            <p class="buy__desc" data-anim="rise" style="--d: 160ms">
              27 pressed botanical oils &mdash; grape seed, rosehip, jasmine, frankincense among
              them. Rich without sitting heavy. Sinks in slow and finishes like skin, not oil.
            </p>

            <p class="buy__price" data-anim="rise" style="--d: 200ms">
              <span class="buy__amount">$69</span>
              <span class="buy__ship">&mdash; Preorder, ships November</span>
            </p>

            <div class="buy__block">
              <p class="label buy__legend">Quantity:</p>
              <div class="buy__row">
                <div class="stepper" data-qty>
                  <button type="button" data-step="down" aria-label="Decrease quantity">&minus;</button>
                  <span class="stepper__value" data-qty-value aria-live="polite">1</span>
                  <button type="button" data-step="up" aria-label="Increase quantity">+</button>
                </div>
                <button class="btn" type="button" data-add>
                  <span class="btn__swap"><span>Preorder</span><span>Added to bag</span></span>
                </button>
              </div>
            </div>

            <div class="plate buy__plate" data-plate>
              <p class="plate__line" style="--d: 0ms"><span>Formula</span><span>27 pressed botanical oils</span></p>
              <p class="plate__line" style="--d: 90ms"><span>Skin</span><span>All Skin Types</span></p>
              <p class="plate__line" style="--d: 180ms"><span>Batch</span><span>Single Batch</span></p>
              <p class="plate__line" style="--d: 270ms"><span>Origin</span><span>Made in USA</span></p>
            </div>
          </div>
        </div>
      </article>

      <section class="how" id="how">
        <figure class="how__media" data-anim="fade">
          <img data-parallax="0.06" src="assets/img/howto.jpg" alt="Pressing the serum along the cheekbone with the KG215 dropper" width="1600" height="2143" />
        </figure>
        <div class="how__panel">
          <div class="how__copy">
            <h2 class="h2 coral" data-anim="rise">How To Use</h2>
            <ol class="steps">
              <li class="step" data-anim="rise"><span class="step__n">1</span><p>Place 4 or 5 drops of oil in hand.</p></li>
              <li class="step" data-anim="rise" style="--d: 130ms"><span class="step__n">2</span><p>Rub hands together and press serum onto face and neck.</p></li>
              <li class="step" data-anim="rise" style="--d: 260ms"><span class="step__n">3</span><p>Can be used morning or night.</p></li>
            </ol>
          </div>
        </div>
      </section>

      <section class="bots" id="ingredients">
        <div class="shead">
          <h2 class="h2 coral" data-anim="rise">Twenty-seven oils. Nothing else.</h2>
          <p data-anim="rise" style="--d: 100ms">
            Grape seed. Rosehip. Jasmine. Frankincense. Hazelnut. Neroli. Every oil in this bottle
            is there because it does something &mdash; not because it sounds good on a label.
          </p>
        </div>
        <div class="slider" data-slider>
          <div class="slider__track" data-slider-track tabindex="0" role="group" aria-label="The twenty-seven oils">
{botanical_slides()}
          </div>
          <button class="slider__arrow slider__arrow--prev" type="button" data-slider-prev aria-label="Previous oils">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 4 7 12l8 8" /></svg>
          </button>
          <button class="slider__arrow slider__arrow--next" type="button" data-slider-next aria-label="Next oils">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 4l8 8-8 8" /></svg>
          </button>
          <div class="slider__dots" data-slider-dots role="tablist" aria-label="Choose an oil"></div>
        </div>
      </section>

      <section class="mos">
        <div class="shead shead--dark">
          <h2 class="h2 coral" data-anim="rise">What&rsquo;s actually in it.</h2>
          <p data-anim="rise" style="--d: 100ms">No benefit promises here &mdash; just what each oil brings to the blend.</p>
        </div>
        <div class="mos__rows">
{mosaic()}
        </div>
      </section>

{marquee(speed="46s")}

      <section class="rsum" id="reviews">
        <div class="rsum__inner">
          <div class="shead">
            <h2 class="h2" data-anim="rise">Real People. Real Reviews.</h2>
          </div>
          <div class="rsum__grid">
            <div class="rsum__score" data-anim="rise">
              <p class="rsum__num"><span data-count="4.59" data-decimals="2">4.59</span> out of 5</p>
              {STARS}
              <p class="muted">Based on 150 reviews</p>
            </div>
            <div class="rsum__bars" data-anim="rise" style="--d: 120ms">
{bars()}
            </div>
          </div>
        </div>
      </section>"""

# --------------------------------------------------------------- ABOUT -----

FAQ = [
    ("How long will it take to receive my order?",
     "Preorders ship in November, in the order they were placed. After that, most US orders "
     "ship within one to two business days and arrive in three to seven."),
    ("Who should I contact if I have a question?",
     "Write to us below. Terry and Monieka still read the inbox themselves."),
    ("What is SkinSkool?",
     "The comparison platform the founders built — eight years of taking the beauty industry’s "
     "best-known formulas apart and publishing what is actually inside them."),
    ("How can you sell this luxury facial oil for so much less?",
     "We skip the parts you cannot put on your face. No department-store counter, no celebrity "
     "contract, no box inside a box."),
    ("What’s your name all about, Khyn &amp; Grail?",
     "Khyn is pronounced KIN — family. Grail is the bottle you have been hunting."),
    ("Is the KG185 Botanical Oils Facial Serum vegan?",
     "Yes. The blend is vegan, never tested on animals, and suitable for all skin types "
     "including sensitive."),
]

def faq():
    out = []
    for i, (q, a) in enumerate(FAQ, 1):
        out.append(f"""            <div class="acc__item">
              <button class="acc__trigger" type="button" data-acc-trigger aria-expanded="false" aria-controls="faq-{i}">
                {q} <i aria-hidden="true"></i>
              </button>
              <div class="acc__panel" id="faq-{i}"><div><p>{a}</p></div></div>
            </div>""")
    return "\n".join(out)

ABOUT_BODY = f"""      <section class="ahero">
        <figure class="ahero__media">
          <img data-parallax="0.08" src="assets/img/about-hero.jpg"
               alt="A woman with her arms crossed over her shoulders, skin lit from the side"
               width="2000" height="1116" fetchpriority="high" />
        </figure>
        <div class="ahero__copy">
          <h1 class="display lines" data-lines>
            <span class="ln"><span>You already</span></span>
            <span class="ln"><span>know.</span></span>
          </h1>
        </div>
      </section>

      <section class="manifesto">
        <img class="manifesto__bottle" src="assets/img/bottle.png" alt="" width="600" height="1316" data-anim="rise" style="--d: 300ms" aria-hidden="true" />
        <div class="manifesto__inner">
          <p class="manifesto__lead" data-anim="rise">
            Khyn &amp; Grail comes from SkinSkool &mdash; eight years spent inside the beauty
            industry&rsquo;s best-known formulas, understanding exactly what&rsquo;s in them.
            Sixty thousand products. A hundred thousand people a month, searching for the same
            thing: what&rsquo;s actually in this bottle, and is it worth what they&rsquo;re charging.
          </p>

          <p class="manifesto__mid" data-anim="rise" style="--d: 120ms">
            We started asking a different question. Not what a serum should cost &mdash; what it
            should be.
          </p>

          <p class="manifesto__mid manifesto__mid--end" data-anim="rise" style="--d: 200ms">
            Khyn &amp; Grail is the answer. One formula. Twenty-seven botanical oils. We take
            inspiration seriously. We don&rsquo;t take shortcuts.
          </p>

          <p class="manifesto__kicker lines" data-lines>
            <span class="ln"><span>We stopped comparing</span></span>
            <span class="ln"><span>a long time ago</span></span>
          </p>

          <p data-anim="rise" style="--d: 260ms">
            <a class="btn btn--outlineLight" href="https://skinskool.com" rel="noopener">SKINSKOOL</a>
          </p>
        </div>
      </section>

      <section class="vce">
        <div class="vce__media">
          <img data-parallax="0.06" src="assets/img/pomegranate.jpg" alt="Macro photograph of pomegranate seeds suspended in clear gel" width="2000" height="1116" />
        </div>
        <div class="vce__inner">
          <article class="vce__card" data-anim="rise">
            <h2 class="h2">Formulated without compromise.</h2>
            <p class="vce__sub">Priced without ego.<br />Made to be felt, not explained.</p>
            <figure class="vce__figure" data-anim="fade" style="--d: 200ms">
              <img src="assets/img/vce.jpg" alt="Value, Curation and Experience overlapping at superior skincare outcomes, supported by market insight, customer first, selective standards and trust and transparency" width="1400" height="824" />
            </figure>
          </article>
        </div>
      </section>

{marquee(speed="46s")}

      <section class="faq" id="faq">
        <div class="faq__inner">
          <div class="faq__head">
            <h2 class="h2" data-anim="rise">FAQ</h2>
            <p class="muted" data-anim="rise" style="--d: 90ms">Frequently Asked Questions</p>
          </div>
          <div class="accordion" data-accordion data-anim="rise">
{faq()}
          </div>
        </div>
      </section>

      <section class="contact" id="contact">
        <div class="contact__inner">
          <div class="contact__copy">
            <h2 class="h2" data-anim="rise">Contact</h2>
            <form class="contact__form" data-newsletter novalidate data-anim="rise" style="--d: 120ms">
              <label class="field"><span class="sr-only">Name</span>
                <input type="text" name="name" placeholder="Name" autocomplete="name" /></label>
              <label class="field"><span class="sr-only">Email</span>
                <input type="email" name="email" placeholder="Email" autocomplete="email" required /></label>
              <label class="field"><span class="sr-only">Message</span>
                <textarea name="message" placeholder="Message" rows="3"></textarea></label>
              <p class="form-status" data-form-status role="status"></p>
              <button class="btn btn--white" type="submit">Send</button>
            </form>
          </div>
          <figure class="contact__media" data-anim="rise">
            <img src="assets/img/lifestyle.jpg" alt="KG215 bottle on a marble stand beside its navy carton" width="1086" height="1448" />
          </figure>
        </div>
      </section>"""

# --------------------------------------------------------------- WRITE -----

PRELOAD = '\n    <link rel="preload" as="image" href="assets/img/%s" />'

open("index.html", "w").write(page(
    "Khyn &amp; Grail — Fancy Skincare for Smart People",
    "KG215 Botanical Oils Facial Serum. 27 pressed botanical oils. Preorder now, ships November.",
    "page page--home", PRELOAD % "hero-portrait.jpg", header("home", mode="float"), HOME_BODY))

open("product.html", "w").write(page(
    "KG215 Botanical Oils Facial Serum — Khyn &amp; Grail",
    "27 pressed botanical oils. Rich without sitting heavy. Preorder now, ships November.",
    "page page--product", PRELOAD % "product-hero.jpg", header("shop"), PRODUCT_BODY))

open("about.html", "w").write(page(
    "About — Khyn &amp; Grail",
    "Khyn &amp; Grail comes from SkinSkool. We stopped comparing a long time ago.",
    "page page--about", PRELOAD % "about-hero.jpg", header("about", mode="over"), ABOUT_BODY))

print("built index.html, product.html, about.html")
