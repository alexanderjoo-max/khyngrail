# Khyn & Grail — website redesign (3 pages)

A static redesign of the KG215 build: same imagery, same typefaces, same coral /
cream / slate palette, rebuilt with a tighter type system and motion throughout.

## Pages

| File | What it is |
| --- | --- |
| `index.html` | Home — hero, credential bar, SkinSkool oil band, product spotlight, reviews |
| `product.html` | KG215 PDP — gallery, buy panel, how to use, the 27 botanicals, ingredient mosaic, review summary |
| `about.html` | About — hero, manifesto, VCE system, FAQ, contact |

Nav is Shop → `product.html`, About → `about.html`, Contact → `about.html#contact`.

## Structure

```
css/
  site.css        @imports everything below, in order
  tokens.css      colour, type scale, spacing, motion easings
  reset.css       
  base.css        page ground, type primitives, reveal utilities
  components.css  buttons, spec plate, stars, fields, accordion
  layout.css      announcement, header, marquee, newsletter, footer, bag drawer, curtain
  home.css  product.css  about.css
js/
  site.js         navigation, bag, purchase options, gallery, accordion, forms
  motion.js       one IntersectionObserver for every reveal, plus scroll-driven work
assets/
  img/            page imagery (web-sized from Renderings/ and the Figma export)
  ingredients/    the 27 botanical cut-outs, pre-blended onto the cream ground
  icons/          
```

### Editing the pages

The three pages share their announcement bar, header, newsletter, footer and bag
drawer. Those live once in `build.py`; the page bodies live in `pages.py`.

```bash
python3 pages.py     # rewrites index.html, product.html, about.html
```

Edit the HTML directly if you prefer — nothing depends on the generators at
runtime. If you do, apply chrome changes to all three files.

### Previewing

```bash
python3 serve.py
```

Then open http://localhost:4321.

## Motion

Every reveal runs through a single observer in `motion.js` so the whole site
shares one easing and rhythm. Scroll-driven work (header retreat, parallax, the
oil macro settling) runs in one rAF-throttled handler.

`prefers-reduced-motion: reduce` collapses all of it — reveals resolve
instantly, marquees stop, the page curtain is removed.

## Copy

All visible copy is taken verbatim from the KG215 design. Price is `$69 —
Preorder, ships November`; there is no size selector and no subscribe option. Two places have no
source copy behind them:

- **FAQ answers.** The design lists the six questions with no answers. The
  answers on `about.html` are placeholder — replace them with the real ones.
- **Contact.** The design has no contact section, but the nav and footer both
  point at one, so `about.html#contact` carries a minimal form.

## Known inconsistencies in the source design

Left exactly as the design has them. Say the word and I will align them.

- **Review score.** `4.59 out of 5` sits beside a distribution (137/10/3/0/0
  across 150 reviews) that averages 4.89.
- **Product code.** The last FAQ says `KG185`; everything else says `KG215`.
- **Origin.** The credential bar says *Made in USA*; the carton in the
  photography reads *Made in France*.
- **Review posters** are cropped from a screenshot of the old review widget, so
  they are lower resolution than the rest and carry a play chip baked into the
  image (the coral button sits on top of it). Swap in real video posters when
  they exist.
