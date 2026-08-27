#!/usr/bin/env python3
"""Emits the lookbook as plain static HTML. All copy, names and image paths are
harvested from the existing site — nothing here is invented."""

# --- harvested from the existing site ---------------------------------------

BRAND = "Khyn &amp; Grail"
TAGLINE = "Fancy Skincare for Smart People #StayRich"
SHIP = "Preorder now &ndash; Ships in November"

# name → file, exactly as product.html already labels them
OILS = [
    ("Açaí", "acai.jpg"), ("Alfalfa", "alfalfa.jpg"), ("Avocado", "avocado.jpg"),
    ("Bergamot", "bergamot.jpg"), ("Bitter Orange", "bitter-orange.jpg"),
    ("Calendula", "calendula.jpg"), ("Caprylic", "caprylic.jpg"),
    ("Carrot Seed", "carrot-seed.jpg"), ("Cypress", "cypress.jpg"),
    ("Dandelion Root", "dandelion-root.jpg"), ("Evening Primrose", "evening-primrose.jpg"),
    ("Frankincense", "frankincense.jpg"), ("Galbanum", "galbanum.jpg"),
    ("Grape Seeds", "grapeseed.jpg"), ("Hazelnuts", "hazelnut.jpg"),
    ("Jasmine", "jasmine.jpg"), ("Lavender", "lavendar.jpg"),
    ("Lemon Peel", "lemon-peel.jpg"), ("Pequi", "pequi.jpg"),
    ("Rosehip", "rose-hip---dog-rose.jpg"), ("Rose", "rose.jpg"),
    ("Rosemary", "rosemary.jpg"), ("Safflower", "safflower.jpg"),
    ("Sea Buckthorn", "seabuckthorn.jpg"), ("Sunflower", "sunflower.jpg"),
    ("Turmeric", "tumeric.jpg"), ("White Nettle", "white-nettle.jpg"),
]

# the only lore the site actually writes, kept word for word
LORE = {
    "Grape Seeds": "Light, fast-absorbing, high in linoleic acid.",
    "Rosehip": "Cold-pressed, unrefined, used at real concentrations.",
    "Jasmine": "Cold-pressed, unrefined, used at real concentrations.",
    "Frankincense": "Resin-pressed. A small amount, used for a reason.",
}

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com" />\n'
         '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\n'
         '  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;'
         '0,400;0,500;1,300;1,400&family=Jost:wght@400;500&family=Source+Serif+4:ital,opsz,wght@'
         '0,8..60,200;0,8..60,300;1,8..60,300&display=swap" rel="stylesheet" />\n'
         '  <link rel="stylesheet" href="styles.css" />')


def chrome(dark=False, veil_img=None, veil=True):
    v = ""
    if veil:
        img = veil_img or "assets/img/macro-calendula.jpg"
        v = f"""  <div class="veil" data-veil aria-hidden="true">
    <div class="veil__plate"><img src="{img}" alt="" /></div>
    <p class="veil__word">{BRAND}</p>
  </div>

"""
    return v + f"""  <div class="grain" aria-hidden="true"></div>
  <div class="vignette" aria-hidden="true"></div>
  <div class="ring" data-ring aria-hidden="true"></div>

  <a class="mark" href="index2.html">{BRAND}</a>
  <button class="opener label" type="button" data-open aria-controls="index-overlay">
    <span>Index</span>
  </button>

  <div class="overlay" id="index-overlay" data-overlay>
    <button class="overlay__close label" type="button" data-close>Close</button>
    <nav aria-label="Pages">
      <a href="index2.html">Lookbook</a>
      <a href="garden.html">The <em>Garden</em></a>
      <a href="rituals.html">KG215</a>
      <a href="atelier.html">Atelier</a>
    </nav>
    <div class="overlay__foot label">
      <span>{SHIP}</span>
      <a href="https://skinskool.com" rel="noopener">SKINSKOOL</a>
      <span>{TAGLINE}</span>
    </div>
  </div>

  <figure class="viewer" data-viewer aria-hidden="true">
    <button class="viewer__close label" type="button">Close</button>
    <img src="" alt="" />
    <figcaption class="label"></figcaption>
  </figure>
"""


COLOPHON = f"""  <footer class="colophon">
    <span class="hair" data-lit></span>
    <div class="colophon__grid" style="margin-top: var(--m5)">
      <div>
        <h2>{BRAND}</h2>
        <p>{TAGLINE}</p>
      </div>
      <div>
        <span class="label colophon__head">Elsewhere</span>
        <ul>
          <li><a href="https://skinskool.com" rel="noopener">SKINSKOOL</a></li>
          <li><a href="atelier.html#write">Contact</a></li>
          <li><a href="atelier.html#formulary">Terms &amp; Conditions</a></li>
          <li><a href="atelier.html#formulary">Privacy Policy</a></li>
          <li><a href="atelier.html#formulary">Return Policy</a></li>
        </ul>
      </div>
      <div>
        <span class="label colophon__head">Get it first.</span>
        <form class="subscribe" data-note="You’re on the list." novalidate>
          <label class="sr-only" for="mail">Email</label>
          <input id="mail" type="email" name="email" placeholder="Email" autocomplete="email" required />
          <button class="label" type="submit">Subscribe</button>
        </form>
        <p class="form-note label"></p>
      </div>
    </div>
    <div class="colophon__base label">
      <span>{SHIP}</span>
      <span>© 2026 {BRAND}</span>
    </div>
  </footer>
"""


def page(title, desc, body, body_class="", dark=False, veil_img=None, veil=True):
    cls = (body_class + (" is-dark" if dark else "")).strip()
    return f"""<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="theme-color" content="{'#100e0a' if dark else '#f6f2e7'}" />
  {FONTS}
</head>
<body class="{cls}">
  <a class="sr-only" href="#main">Skip to content</a>
{chrome(dark, veil_img, veil)}
  <main id="main">
{body}
  </main>

{COLOPHON}
  <script src="script.js" defer></script>
</body>
</html>
"""


# ============================================================== LOOKBOOK ====

def hung(name, src, kind="cameo", mods="", ratio=""):
    """One specimen hung on the salon wall."""
    inner = (f'<span class="cameo"><img src="{src}" alt="{name}" loading="lazy" /></span>'
             if kind == "cameo" else
             f'<span class="frame"{ratio}><img src="{src}" alt="{name}" loading="lazy" /></span>')
    return (f'        <figure class="hung {mods}" data-view="{name}" data-r="frame">\n'
            f'          {inner}\n'
            f'          <figcaption class="hung__name label">{name}</figcaption>\n'
            f'        </figure>')


ING = "assets/ingredients/"        # the studio plates, untouched
CUT = "assets/ingredients-cut/"    # the same photographs, cut from their field
IMG = "assets/img/"

WALL = [
    ("wall__row--a", [
        hung("Rose", CUT + "rose.webp", "cameo", "hung--lift"),
        hung("Grape Seed", IMG + "macro-grape.jpg", "frame", "hung--drop hung--wide"),
        hung("Jasmine", CUT + "jasmine.webp", "cameo"),
    ]),
    ("wall__row--b", [
        hung("Calendula, suspended", IMG + "macro-calendula.jpg", "frame", "hung--square"),
        hung("Lavender", CUT + "lavendar.webp", "cameo", "hung--drop"),
    ]),
    ("wall__row--c", [
        hung("Sea Buckthorn", CUT + "seabuckthorn.webp", "cameo"),
        hung("Lemon Peel", CUT + "lemon-peel.webp", "cameo", "hung--drop"),
        hung("Sunflower", IMG + "macro-sunflower.jpg", "frame", "hung--tall hung--lift"),
    ]),
    ("wall__row--d", [
        hung("Cypress", CUT + "cypress.webp", "cameo", "hung--drop"),
        hung("Turmeric", CUT + "tumeric.webp", "cameo"),
        hung("Frankincense", CUT + "frankincense.webp", "cameo", "hung--drop"),
        hung("Rosemary", CUT + "rosemary.webp", "cameo"),
    ]),
]

wall_html = "\n".join(
    f'      <div class="wall__row {cls}">\n' + "\n".join(items) + "\n      </div>"
    for cls, items in WALL
)

HOME = f"""    <section class="overture">
      <div class="overture__plate">
        <img src="{IMG}macro-calendula.jpg" alt="Calendula petals suspended in botanical oil" fetchpriority="high" />
      </div>
      <div class="overture__air">
        <h1 class="display colossus lines" data-lines>
          <span class="ln"><span>You already</span></span>
          <span class="ln"><span><em>know</em></span></span>
        </h1>
        <div class="overture__foot label" data-r="up" style="--d: 700ms">
          <span>{SHIP}</span>
          <span>KG215 &middot; Botanical Oils Facial Serum</span>
        </div>
      </div>
      <span class="scroll-word label" aria-hidden="true">Scroll</span>
    </section>

    <section class="creed">
      <div class="creed__grid">
        <div class="creed__words">
          <p class="label" data-r="up">From SkinSkool</p>
          <h2 class="display huge lines" data-lines>
            <span class="ln"><span>We stopped</span></span>
            <span class="ln"><span><em>comparing</em></span></span>
            <span class="ln"><span>a long time ago</span></span>
          </h2>
          <div class="measure lede" data-r="up" style="--d: 240ms">
            <p>Eight years, sixty thousand formulas, more expensive bottles taken apart and
            understood than we can count.</p>
            <p>One formula. Twenty-seven botanical oils. We take inspiration seriously.
            We don’t take shortcuts.</p>
          </div>
        </div>
        <div class="creed__plate">
          <figure class="frame" data-r="frame" style="--d: 180ms">
            <img src="{IMG}about-hero.jpg" alt="A woman with her arms crossed over her shoulders, lit from the side" loading="lazy" />
          </figure>
          <figcaption class="creed__caption label">Khyn &mdash; pronounced KIN</figcaption>
        </div>
      </div>
    </section>

    <section class="salon">
      <div class="salon__head">
        <p class="label madder" data-r="up">The garden</p>
        <h2 class="display huge" data-r="up" style="--d: 120ms">Twenty-seven oils.<br /><em>Nothing else.</em></h2>
      </div>

      <div class="wall">
{wall_html}
      </div>

      <div class="wall__aside">
        <p class="measure quiet" data-r="up">Grape seed. Rosehip. Jasmine. Frankincense. Hazelnut. Neroli.
        Every oil in this bottle is there because it does something &mdash; not because it sounds
        good on a label.</p>
        <a class="label madder" href="garden.html" data-r="up" style="--d: 160ms">Walk the garden &mdash; all twenty-seven</a>
      </div>
    </section>

    <section class="vessel">
      <div class="vessel__grid">
        <div class="vessel__plate">
          <figure class="frame" data-r="frame">
            <img src="{IMG}product-hero.jpg" alt="The KG215 bottle with orchids and a dish of botanical oil" loading="lazy" />
          </figure>
        </div>
        <div class="vessel__words">
          <p class="label" data-r="up">KG215</p>
          <h2 class="display large" data-r="up" style="--d: 100ms">Botanical Oils<br /><em>Facial Serum</em></h2>
          <p class="measure lede" data-r="up" style="--d: 200ms">27 pressed botanical oils &mdash; grape seed,
          rosehip, jasmine, frankincense among them. Rich without sitting heavy. Sinks in slow and
          finishes like skin, not oil.</p>
          <div class="vessel__price" data-r="up" style="--d: 280ms">
            <b>$69</b>
            <span class="label quiet">Preorder, ships November</span>
            <a class="label madder" href="rituals.html">The ritual &rarr;</a>
          </div>
        </div>
      </div>
    </section>

    <a class="door" href="rituals.html">
      <p class="label quiet" data-r="up">Made to be felt</p>
      <h2 class="display huge" data-r="up" style="--d: 100ms">Formulated without compromise.<br /><em>Priced without ego.</em></h2>
      <p class="door__sub label" data-r="up" style="--d: 220ms">Hacking luxury skincare.</p>
    </a>

    <section class="chorus">
      <div class="chorus__plate"><img src="{IMG}lab-dark2.jpg" alt="" aria-hidden="true" loading="lazy" /></div>
      <div class="chorus__inner">
        <blockquote data-r="up">
          <p>“It has not only evened out my skin tone but my pores are noticeably smaller and my
          skin is brighter and smoother. And the wonderful earthy smell is just an added bonus.”</p>
          <footer class="label">&mdash; D.M.</footer>
        </blockquote>

        <div class="chorus__voices">
          <figure class="voice" data-r="up"><p>“She’s glowing! She’s dewy!”</p><footer class="label">Ali &amp; Kadija</footer></figure>
          <figure class="voice" data-r="up" style="--d: 120ms"><p>“I’m obsessed with it”</p><footer class="label">Nadj &amp; Sophie</footer></figure>
          <figure class="voice" data-r="up" style="--d: 240ms"><p>“It smells SO good!”</p><footer class="label">Mahshid &amp; Camille</footer></figure>
        </div>

        <span class="hash" data-r="up">#stayrich</span>
      </div>
    </section>
"""


# ================================================================ GARDEN ====

def slug(f):
    return f.rsplit(".", 1)[0]

contents_html = "\n".join(
    f'          <li><a href="#{slug(f)}">{i:02d} &nbsp; {n}</a></li>'
    for i, (n, f) in enumerate(OILS, 1)
)

def plate(i, name, file):
    lore = LORE.get(name)
    lore_html = f'\n          <p class="plate__lore">{lore}</p>' if lore else ""
    return f"""      <article class="plate" id="{slug(file)}" data-lit>
        <div class="plate__cameo" data-view="{name}">
          <span class="cameo"><img src="{CUT}{slug(file)}.webp" alt="{name}" loading="lazy" /></span>
        </div>
        <div class="plate__words">
          <p class="numeral">{i:02d} &mdash; 27</p>
          <h2 class="display large"><em>{name}</em></h2>{lore_html}
        </div>
      </article>"""

plates_html = "\n".join(plate(i, n, f) for i, (n, f) in enumerate(OILS, 1))

GARDEN = f"""    <section class="frontispiece">
      <p class="label label--wide" data-r="up">Herbarium</p>
      <h1 class="display huge lines" data-lines style="margin-top: var(--m3)">
        <span class="ln"><span>Twenty-seven oils.</span></span>
        <span class="ln"><span><em>Nothing else.</em></span></span>
      </h1>
      <p class="measure lede" data-r="up" style="--d: 260ms">Grape seed. Rosehip. Jasmine. Frankincense.
      Hazelnut. Neroli. Every oil in this bottle is there because it does something &mdash; not
      because it sounds good on a label.</p>
    </section>

    <div class="herbarium">
      <nav class="contents" data-contents aria-label="The twenty-seven">
        <ol>
{contents_html}
        </ol>
      </nav>

      <div class="plates">
{plates_html}
      </div>
    </div>
"""


# =============================================================== RITUALS ====

LORE_CHAPTERS = [
    ("Grape Seed", "Light, fast-absorbing, high in linoleic acid.", IMG + "macro-grape.jpg",
     "Extreme macro of dark purple grapes bursting"),
    ("Rosehip &amp; Jasmine", "Cold-pressed, unrefined, used at real concentrations.", IMG + "macro-rosehip.jpg",
     "Extreme macro of a rosehip cut open"),
    ("Frankincense", "Resin-pressed. A small amount, used for a reason.", IMG + "oil.jpg",
     "Extreme macro of golden resinous oil"),
    ("Tocopherol", "Natural vitamin E, keeps the blend stable.", IMG + "macro-sunflower.jpg",
     "Extreme macro of a sunflower seed head"),
]

lore_html = "\n".join(f"""      <section class="lore__chapter">
        <figure class="frame" data-r="frame"><img src="{src}" alt="{alt}" loading="lazy" /></figure>
        <div class="lore__air">
          <h3 class="display large" data-r="up"><em>{name}</em></h3>
          <p data-r="up" style="--d: 140ms">{body}</p>
        </div>
      </section>""" for name, body, src, alt in LORE_CHAPTERS)

STEPS = [
    "Place 4 or 5 drops of oil in hand.",
    "Rub hands together and press serum onto face and neck.",
    "Can be used morning or night.",
]
steps_html = "\n".join(
    f'          <div class="rite__step" data-r="up" style="--d: {i*130}ms">\n'
    f'            <span class="numeral">{i+1:02d}</span>\n'
    f'            <p>{t}</p>\n          </div>' for i, t in enumerate(STEPS))

BARS = [(5, 137), (4, 10), (3, 3), (2, 0), (1, 0)]
bars_html = "\n".join(
    f'        <div class="tally__bar"><span class="label">{s} star</span>'
    f'<i style="--pct: {round(c/150*100,1)}%; --d: {i*110}ms"></i>'
    f'<span class="label">{c}</span></div>' for i, (s, c) in enumerate(BARS))

RITUALS = f"""    <section class="still">
      <img src="{IMG}product-hero.jpg" alt="The KG215 bottle with orchids and a dish of botanical oil" fetchpriority="high" />
      <div class="still__air">
        <p class="label" data-r="up">KG215</p>
        <h1 class="display huge lines" data-lines>
          <span class="ln"><span>Botanical Oils</span></span>
          <span class="ln"><span><em>Facial Serum</em></span></span>
        </h1>
      </div>
    </section>

    <section class="spec">
      <div>
        <p class="lede measure" data-r="up">27 pressed botanical oils &mdash; grape seed, rosehip,
        jasmine, frankincense among them. Rich without sitting heavy. Sinks in slow and finishes
        like skin, not oil.</p>
        <div class="vessel__price" data-r="up" style="--d: 160ms">
          <b>$69</b>
          <span class="label quiet">Preorder, ships November</span>
        </div>
      </div>
      <dl data-r="up" style="--d: 120ms">
        <div><dt>Formula</dt><dd>27 pressed botanical oils</dd></div>
        <div><dt>Skin</dt><dd>All Skin Types</dd></div>
        <div><dt>Batch</dt><dd>Single Batch</dd></div>
        <div><dt>Origin</dt><dd>Made in USA</dd></div>
      </dl>
    </section>

    <section class="rite">
      <div class="rite__grid">
        <div class="rite__plate">
          <figure class="frame" data-r="frame">
            <img src="{IMG}howto.jpg" alt="Pressing the serum along the cheekbone with the KG215 dropper" loading="lazy" />
          </figure>
        </div>
        <div>
          <div class="rite__steps" style="margin-top: 0">
            <p class="label madder" data-r="up">The ritual</p>
            <h2 class="display large" data-r="up" style="--d: 100ms">How To <em>Use</em></h2>
          </div>
          <div class="rite__steps">
{steps_html}
          </div>
        </div>
      </div>
    </section>

    <section class="lore">
      <div class="salon__head" style="padding-block: var(--chapter) var(--m4)">
        <p class="label madder" data-r="up">What’s actually in it.</p>
        <h2 class="display large" data-r="up" style="--d: 100ms">No benefit promises here &mdash;
        <em>just what each oil brings to the blend.</em></h2>
      </div>
{lore_html}
    </section>

    <section class="tally" data-lit>
      <div>
        <p class="tally__score">4.59 <span class="label quiet">out of 5</span></p>
        <p class="label quiet" style="margin-top: var(--m2)">Based on 150 reviews</p>
      </div>
      <div class="tally__bars">
{bars_html}
      </div>
    </section>

    <section class="chorus">
      <div class="chorus__plate"><img src="{IMG}lab-dark.jpg" alt="" aria-hidden="true" loading="lazy" /></div>
      <div class="chorus__inner">
        <div class="chorus__voices" style="border-top: 0; margin-top: 0; padding-top: 0">
          <figure class="voice" data-r="up"><p>“She’s glowing! She’s dewy!”</p><footer class="label">Ali &amp; Kadija</footer></figure>
          <figure class="voice" data-r="up" style="--d: 120ms"><p>“I’m obsessed with it”</p><footer class="label">Nadj &amp; Sophie</footer></figure>
          <figure class="voice" data-r="up" style="--d: 240ms"><p>“It smells SO good!”</p><footer class="label">Mahshid &amp; Camille</footer></figure>
        </div>
        <span class="hash" data-r="up">#stayrich</span>
      </div>
    </section>
"""


# =============================================================== ATELIER ====

FAQ = [
    ("How long will it take to receive my order?",
     "Preorders ship in November, in the order they were placed. After that, most US orders ship "
     "within one to two business days and arrive in three to seven."),
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

faq_html = "\n".join(f"""        <div class="formulary__item" data-r="up">
          <h3 class="formulary__q">{q}</h3>
          <p class="formulary__a">{a}</p>
        </div>""" for q, a in FAQ)

ATELIER = f"""    <section class="still">
      <img src="{IMG}about-hero.jpg" alt="A woman with her arms crossed over her shoulders, lit from the side" fetchpriority="high" />
      <div class="still__air">
        <p class="label" data-r="up">Atelier</p>
        <h1 class="display huge lines" data-lines>
          <span class="ln"><span>You already</span></span>
          <span class="ln"><span><em>know.</em></span></span>
        </h1>
      </div>
    </section>

    <section class="testament">
      <div class="testament__inner">
        <p data-r="up">{BRAND} comes from SkinSkool &mdash; eight years spent inside the beauty
        industry’s best-known formulas, understanding exactly what’s in them. Sixty thousand
        products. A hundred thousand people a month, searching for the same thing: what’s
        actually in this bottle, and is it worth what they’re charging.</p>

        <p class="turn" data-r="up" style="--d: 120ms">We started asking a different question.
        Not what a serum should cost &mdash; what it should be.</p>

        <p class="turn turn--end" data-r="up" style="--d: 200ms">{BRAND} is the answer. One formula.
        Twenty-seven botanical oils. We take inspiration seriously. We don’t take shortcuts.</p>

        <h2 class="display huge lines" data-lines style="margin-top: var(--m6)">
          <span class="ln"><span>We stopped comparing</span></span>
          <span class="ln"><span><em>a long time ago</em></span></span>
        </h2>

        <p style="margin-top: var(--m4)" data-r="up" style="--d: 300ms">
          <a class="label madder" href="https://skinskool.com" rel="noopener">SKINSKOOL &rarr;</a>
        </p>
      </div>
    </section>

    <section class="creedo">
      <p class="creedo__lines" data-r="up">
        Formulated without compromise.<br />
        Priced without ego.<br />
        <em>Made to be felt, not explained.</em>
      </p>
      <figure data-r="frame" style="--d: 200ms">
        <img src="{IMG}vce.jpg" alt="Value, Curation and Experience overlapping at superior skincare outcomes" loading="lazy" />
      </figure>
    </section>

    <section class="formulary" id="formulary">
      <div class="salon__head" style="padding-inline: 0; text-align: center">
        <p class="label madder" data-r="up">Frequently Asked Questions</p>
      </div>
      <div class="formulary__list">
{faq_html}
      </div>
    </section>

    <section class="write" id="write">
      <div class="write__grid">
        <div>
          <p class="label madder" data-r="up">Contact</p>
          <h2 class="display large" data-r="up" style="--d: 100ms">Write to <em>us</em></h2>
          <form data-note="Sent. We’ll write back." novalidate data-r="up" style="--d: 200ms">
            <label><span class="label quiet">Name</span><input type="text" name="name" autocomplete="name" /></label>
            <label><span class="label quiet">Email</span><input type="email" name="email" autocomplete="email" required /></label>
            <label><span class="label quiet">Message</span><textarea name="message" rows="3"></textarea></label>
            <p class="form-note label"></p>
            <button class="label" type="submit">Send &rarr;</button>
          </form>
        </div>
        <div class="write__plate">
          <figure class="frame" data-r="frame">
            <img src="{IMG}lifestyle.jpg" alt="The KG215 bottle on a marble stand beside its navy carton" loading="lazy" />
          </figure>
        </div>
      </div>
    </section>
"""


# ================================================================= WRITE ====

open("index2.html", "w").write(page(
    "Khyn &amp; Grail — You already know",
    "KG215 Botanical Oils Facial Serum. Twenty-seven pressed botanical oils. Preorder now, ships November.",
    HOME, veil_img=IMG + "macro-calendula.jpg"))

open("garden.html", "w").write(page(
    "The Garden — Khyn &amp; Grail",
    "All twenty-seven pressed botanical oils in the KG215 formula.",
    GARDEN, dark=True, veil_img=IMG + "macro-rosehip.jpg"))

open("rituals.html", "w").write(page(
    "KG215 — Khyn &amp; Grail",
    "KG215 Botanical Oils Facial Serum. $69, preorder, ships November.",
    RITUALS, veil_img=IMG + "product-hero.jpg"))

open("atelier.html", "w").write(page(
    "Atelier — Khyn &amp; Grail",
    "Khyn & Grail comes from SkinSkool. We stopped comparing a long time ago.",
    ATELIER, veil_img=IMG + "about-hero.jpg"))

print("wrote index2.html, garden.html, rituals.html, atelier.html")
