"""Port the v3 static pages (index3 / product3 / about3) into the Shopify theme.

Run from this folder:  python3 port_shopify.py
Writes into ../KG Shopify Theme. Re-run after changing the static pages.
"""
import json, re, shutil
from pathlib import Path

SRC = Path(__file__).parent
THEME = SRC.parent / "KG Shopify Theme"
A = THEME / "assets"

# --- Assets: Shopify's assets folder is flat -------------------------------
for f in (SRC / "assets/img").iterdir():
    shutil.copy(f, A / f.name)
for f in (SRC / "assets/icons").iterdir():
    shutil.copy(f, A / f.name)
for f in (SRC / "assets/ingredients").iterdir():
    shutil.copy(f, A / ("ing-" + f.name))

css_order = ["tokens", "reset", "base", "components", "layout", "home", "product", "about", "index3"]
(A / "kg.css").write_text("\n".join((SRC / f"css/{n}.css").read_text() for n in css_order)
    + "\n/* Shopify: keep the footer clear of the fixed sticky buy bar */\n"
    + "body:has(.k3-sticky) .site-footer { padding-bottom: calc(var(--s8) + 6rem); }\n"
    + (SRC / "shopify-overrides.css").read_text())
shutil.copy(SRC / "js/motion.js", A / "kg-motion.js")


def liquidify(html):
    def asset(m):
        folder, name = m.group(1), m.group(2)
        if folder == "ingredients":
            name = "ing-" + name
        return "{{ '%s' | asset_url }}" % name
    html = re.sub(r"assets/(img|icons|ingredients)/([\w.\-]+)", asset, html)
    html = html.replace('href="product3.html"', 'href="{{ kg_url }}"')
    html = html.replace('href="about3.html#contact"', 'href="{{ routes.root_url }}?view=about#contact"')
    html = html.replace('href="about3.html#faq"', 'href="{{ routes.root_url }}?view=about#faq"')
    html = html.replace('href="about3.html"', 'href="{{ routes.root_url }}?view=about"')
    html = html.replace('href="index3.html"', 'href="{{ routes.root_url }}"')
    return html


def main_children(path):
    html = (SRC / path).read_text()
    main = re.search(r"<main id=\"main\">(.*)</main>", html, re.S).group(1)
    # Split on top-level blocks (6-space indent in the source).
    parts = re.split(r"\n(?=      <(?:section|article|div class=\"marquee))", main)
    return [p.strip() for p in parts if p.strip()]


HEAD = "{%- assign kg_url = settings.kg_product.url | default: routes.all_products_collection_url -%}\n"


def write_section(name, label, body):
    schema = {"name": label, "settings": [], "presets": [{"name": label}]}
    (THEME / f"sections/{name}.liquid").write_text(
        (HEAD if "kg_url" in body else "") + body + "\n\n{% schema %}\n" + json.dumps(schema, indent=2) + "\n{% endschema %}\n")


NEWSLETTER = """<section class="newsletter">
  <div class="newsletter__inner">
    <h2 class="h2" data-anim="rise">Newsletter</h2>
    <p data-anim="rise" style="--d: 90ms">Get it first.</p>
    {%- form 'customer', class: 'newsletter__form', data-anim: 'rise' -%}
      <input type="hidden" name="contact[tags]" value="newsletter">
      <div class="newsletter__row">
        <label class="field">
          <span class="sr-only">Email</span>
          <input type="email" name="contact[email]" placeholder="Email" autocomplete="email" required />
        </label>
        <button class="btn" type="submit">Subscribe</button>
      </div>
      <p class="form-status{% if form.posted_successfully? or form.errors %} is-shown{% endif %}" role="status">
        {%- if form.posted_successfully? -%}You&rsquo;re on the list.{%- elsif form.errors -%}That email address doesn&rsquo;t look right.{%- endif -%}
      </p>
    {%- endform -%}
  </div>
</section>"""

CONTACT_FORM = """{%- form 'contact', class: 'contact__form', data-anim: 'rise' -%}
              <label class="field"><span class="sr-only">Name</span>
                <input type="text" name="contact[name]" placeholder="Name" autocomplete="name" /></label>
              <label class="field"><span class="sr-only">Email</span>
                <input type="email" name="contact[email]" placeholder="Email" autocomplete="email" required /></label>
              <label class="field"><span class="sr-only">Message</span>
                <textarea name="contact[body]" placeholder="Message" rows="3"></textarea></label>
              <p class="form-status{% if form.posted_successfully? or form.errors %} is-shown{% endif %}" role="status">
                {%- if form.posted_successfully? -%}Sent. We&rsquo;ll write back within a day or two.{%- elsif form.errors -%}That email address doesn&rsquo;t look right.{%- endif -%}
              </p>
              <button class="btn btn--white" type="submit">Send</button>
            {%- endform -%}"""

PRICE = "{{ kg_product.price | money_without_trailing_zeros }}"

# --- Home -------------------------------------------------------------------
home_names = ["kg-hero", "kg-creds", "kg-oil", "kg-story", "kg-pile", "kg-marquee", "kg-newsletter"]
home_labels = ["KG Hero", "KG Credentials", "KG Oils", "KG Story", "KG Bottle pile", "KG Marquee", "KG Newsletter"]
for name, label, part in zip(home_names, home_labels, main_children("index3.html")):
    if name == "kg-newsletter":
        part = NEWSLETTER
    write_section(name, label, liquidify(part))

# --- Product ----------------------------------------------------------------
prod = main_children("product3.html")
def swap(html, old, new):
    """Replace exactly one occurrence, so a copy change in the static page can't silently break the port."""
    assert html.count(old) == 1, "port: expected exactly one of %r" % old[:80]
    return html.replace(old, new)

# Pack picker. The store sells the packs as three products (single, 2-pack, 4-pack), each with
# the MLVeda currency app's region variants (ca / na / gb / eu / intl). So each pack is a product:
# the single is the theme's featured product, the packs are the "2-pack product" / "4-pack product"
# theme settings. Each pack uses its "na" variant (else the first available one); every price, the
# per-bottle price and the savings come from the admin. Images are the theme's pack-1/2/4.jpg shots.
PRELUDE = """{%- liquid
  if settings.kg_product != blank
    assign kg_single = settings.kg_product
  else
    assign kg_single = product
  endif
  assign kg_single_v = kg_single.selected_or_first_available_variant
  for v in kg_single.variants
    if v.title == 'na'
      assign kg_single_v = v
    endif
  endfor
  assign kg_page_v = kg_single_v
  if product.id == settings.kg_pack_2.id or product.id == settings.kg_pack_4.id
    assign kg_page_v = product.selected_or_first_available_variant
    for v in product.variants
      if v.title == 'na'
        assign kg_page_v = v
      endif
    endfor
  endif
-%}
"""

PACKS = """<fieldset class="packs" data-packs data-anim="rise" style="--d: 270ms">
              <legend class="label buy__legend">Choose your pack:</legend>
              <div class="packs__list">
                {%- assign kg_counts = '1,2,4' | split: ',' -%}
                {%- for kg_count in kg_counts -%}
                  {%- liquid
                    assign n = kg_count | plus: 0
                    case n
                      when 1
                        assign kg_p = kg_single
                      when 2
                        assign kg_p = settings.kg_pack_2
                      when 4
                        assign kg_p = settings.kg_pack_4
                    endcase
                  -%}
                  {%- if kg_p != blank -%}
                  {%- liquid
                    assign kg_v = kg_p.selected_or_first_available_variant
                    for v in kg_p.variants
                      if v.title == 'na'
                        assign kg_v = v
                      endif
                    endfor
                    assign each = kg_v.price | divided_by: n
                    assign save = kg_single_v.price | times: n | minus: kg_v.price
                    case n
                      when 1
                        assign kg_name = 'Single'
                      else
                        assign kg_name = n | append: '-Pack'
                    endcase
                  -%}
                <label class="pack">
                  <input type="radio" name="pack" value="{{ kg_v.id }}" data-variant-id="{{ kg_v.id }}" data-available="{{ kg_v.available }}" data-price="{{ kg_v.price | money_without_trailing_zeros }}" data-img="{{ 'pack-' | append: n | append: '.jpg' | asset_url }}"{% if kg_v.id == kg_page_v.id %} checked{% endif %} />
                  <span class="pack__name">{{ kg_name }}</span>
                  <span class="pack__meta">{{ n }} bottle{% if n > 1 %}s &middot; {{ each | money_without_trailing_zeros }} each{% endif %}</span>
                  <span class="pack__price">{{ kg_v.price | money_without_trailing_zeros }}</span>
                  {%- if save > 0 %}<span class="pack__save">Save {{ save | money_without_trailing_zeros }}</span>{% endif %}
                </label>
                  {%- endif -%}
                {%- endfor -%}
              </div>
            </fieldset>"""

pdp = liquidify(prod[0])
pdp = swap(pdp, '<span data-single-price>$65</span>',
           '<span data-single-price>{{ kg_single_v.price | money_without_trailing_zeros }}</span>')
pdp = swap(pdp, '<span class="buy__amount" data-pack-price>$65</span>',
           '<span class="buy__amount" data-pack-price>{{ kg_page_v.price | money_without_trailing_zeros }}</span>')
pdp = re.sub(r'<fieldset class="packs".*?</fieldset>', lambda m: PACKS, pdp, count=1, flags=re.S)
pdp = swap(pdp, 'data-add data-k3-main-add',
           'data-add data-k3-main-add data-variant-id="{{ kg_page_v.id }}"'
           '{% unless kg_page_v.available %} disabled{% endunless %}')
write_section("kg-product", "KG Product", PRELUDE + pdp)
write_section("kg-how", "KG How to use", liquidify(prod[1]))

# Extra product sections from the full product.html (botanicals, mosaic, reviews).
for part in main_children("product.html"):
    for cls, name, label in [("bots", "kg-bots", "KG Botanicals"), ("mos", "kg-mosaic", "KG Ingredient mosaic"),
                             ("rsum", "kg-reviews", "KG Review summary")]:
        if part.startswith('<section class="%s"' % cls):
            write_section(name, label, liquidify(part))

# --- About ------------------------------------------------------------------
about = main_children("about3.html")
for name, label, part in zip(["kg-about-hero", "kg-manifesto", "kg-faq", None, "kg-contact"],
                             ["KG About hero", "KG Manifesto", "KG FAQ", None, "KG Contact"], about):
    if not name:
        continue
    if name == "kg-contact":
        part = re.sub(r"<form class=\"contact__form\".*?</form>", lambda m: CONTACT_FORM, part, flags=re.S)
    write_section(name, label, liquidify(part))

# Plain store pages (terms, privacy, returns...): our type and margins.
write_section("kg-page", "KG Page", """<article class="kg-page">
  <header class="kg-page__head">
    <p class="label coral" data-anim="rise">Khyn &amp; Grail</p>
    <h1 class="h1" data-anim="rise" style="--d: 60ms">{{ page.title }}</h1>
  </header>
  <div class="kg-page__body rte">{{ page.content }}</div>
</article>""")

# --- Templates --------------------------------------------------------------
def template(path, names):
    # Never clobber a template the theme editor has already saved.
    if (THEME / path).exists() and "kg-" in (THEME / path).read_text():
        return
    data = {"sections": {n: {"type": n, "settings": {}} for n in names}, "order": names}
    (THEME / path).write_text(json.dumps(data, indent=2) + "\n")

template("templates/index.json", home_names)
template("templates/page.json", ["kg-page", "kg-newsletter"])
template("templates/product.json", ["kg-product", "kg-how", "kg-bots", "kg-marquee", "kg-reviews", "kg-newsletter"])
about_sections = ["kg-about-hero", "kg-manifesto", "kg-faq", "kg-marquee", "kg-contact", "kg-newsletter"]
template("templates/index.about.json", about_sections)
template("templates/page.about-us.json", ["kg-about-hero", "kg-manifesto", "kg-faq", "kg-marquee", "kg-contact", "kg-newsletter"])

# --- Header / footer from the shared chrome --------------------------------
index = (SRC / "index3.html").read_text()
header = re.search(r"(<p class=\"announce\">.*?</nav>\n)\n    <main", index, re.S).group(1)
write_section("header", "KG Header", liquidify(header))
footer = re.search(r"(<footer.*?</footer>)", index, re.S).group(1)
footer = liquidify(footer).replace(
    '<a href="{{ routes.root_url }}?view=about#faq">Terms &amp; Conditions</a>',
    '<a href="/pages/terms-of-use">Terms &amp; Conditions</a>').replace(
    '<a href="{{ routes.root_url }}?view=about#faq">Privacy Policy</a>',
    '<a href="/pages/privacy-policy">Privacy Policy</a>').replace(
    '<a href="{{ routes.root_url }}?view=about#faq">Return Policy</a>',
    '<a href="/pages/return-policy">Return Policy</a>')
footer = footer.replace("</nav>\n      </div>", "</nav>\n      </div>\n      <div class=\"footer-legal\">\n        <p>&copy; {{ 'now' | date: '%Y' }} Khyn &amp; Grail</p>\n        <p>Botanical oils, made in USA</p>\n      </div>", 1)
write_section("footer", "KG Footer", footer)

drawer = re.search(r"(<div class=\"drawer-scrim\".*?</aside>)", index, re.S).group(1)
drawer = liquidify(drawer).replace('<a class="btn btn--block" href="{{ kg_url }}">Checkout</a>',
                                   '<a class="btn btn--block" href="{{ routes.cart_url }}/checkout">Checkout</a>')
curtain = liquidify(re.search(r"(<div class=\"curtain\".*?</div>)", index, re.S).group(1))

# Sticky buy bar: link on home, add-to-bag on product.
sticky_script = re.search(r"<div class=\"k3-sticky\".*?</script>", (SRC / "product3.html").read_text(), re.S).group(0)
sticky_script = sticky_script[sticky_script.index("<script>"):]
sticky_script = sticky_script.replace('document.querySelector(".pdp")',
                                      'document.querySelector(".pdp, .k3-hero")')
sticky_script = sticky_script.replace('bar.querySelector("button")', 'bar.querySelector(".btn")')
sticky_script = sticky_script.replace(
    'bar.querySelector(".btn").addEventListener("click", function () { main.click(); });',
    'if (main.matches("[data-add]")) bar.querySelector(".btn").addEventListener("click", function (e) { e.preventDefault(); main.click(); });')
(THEME / "snippets/kg-sticky.liquid").write_text("""{%- if template == 'index' or template.name == 'product' -%}
  {%- liquid
    if template.name == 'product'
      assign kg_product = product
    else
      assign kg_product = settings.kg_product
    endif
  -%}
  {%- if kg_product != blank -%}
<div class="k3-sticky" data-k3-sticky aria-hidden="true">
  <div class="k3-sticky__id">
    <img src="{{ 'bottle.png' | asset_url }}" alt="" width="600" height="1316" />
    <p>Botanical Oils Facial Serum <span>""" + PRICE + """ &middot; Preorder, ships January</span></p>
  </div>
  <a class="btn btn--sm" href="{{ kg_product.url }}" tabindex="-1" data-k3-sticky-add>{% if template.name == 'product' %}Preorder{% else %}Shop now{% endif %}</a>
</div>
""" + sticky_script + """
  {%- endif -%}
{%- endif -%}
""")

(THEME / "layout/theme.liquid").write_text("""<!doctype html>
<html lang="{{ request.locale.iso_code }}" class="no-js">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="theme-color" content="#f7f2e7">
    <script>document.documentElement.className=document.documentElement.className.replace("no-js","js");</script>
    {% render 'meta-tags' %}
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Jost:ital,wght@0,400;0,500;0,600;1,400;1,500;1,600&family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;1,8..60,400&display=swap" rel="stylesheet">
    {{ 'kg.css' | asset_url | stylesheet_tag }}
    {{ content_for_header }}
  </head>
  {%- liquid
    case template.name
      when 'index'
        if template.suffix == 'about'
          assign page_class = 'page--about'
        else
          assign page_class = 'page--home'
        endif
      when 'product'
        assign page_class = 'page--product'
      else
        assign page_class = 'page--about'
    endcase
  -%}
  <body class="page {{ page_class }} page--k3">
    <div class="k3-grain" aria-hidden="true"></div>
    <a class="skip-link" href="#main">Skip to content</a>
    """ + curtain + """

    {% sections 'header-group' %}

    <main id="main">
      {{ content_for_layout }}
    </main>

    {% sections 'footer-group' %}

    """ + drawer + """

    {% render 'kg-sticky' %}

    <script src="{{ 'kg-site.js' | asset_url }}" defer></script>
    <script src="{{ 'kg-motion.js' | asset_url }}" defer></script>
  </body>
</html>
""")

# --- Theme setting: which product the home page sells -----------------------
schema_path = THEME / "config/settings_schema.json"
schema_text = schema_path.read_text()
if "kg_product" not in schema_text:
    schema_text = schema_text.rstrip().rstrip("]").rstrip().rstrip(",") + """,
  {
    "name": "Khyn & Grail",
    "settings": [
      { "type": "product", "id": "kg_product", "label": "Featured product (home page links and sticky bar)" }
    ]
  }
]
"""
if "kg_pack_2" not in schema_text:
    schema_text = schema_text.replace(
        '{ "type": "product", "id": "kg_product", "label": "Featured product (home page links and sticky bar)" }',
        '{ "type": "product", "id": "kg_product", "label": "Featured product (home page links and sticky bar)" },\n'
        '      { "type": "product", "id": "kg_pack_2", "label": "2-pack product" },\n'
        '      { "type": "product", "id": "kg_pack_4", "label": "4-pack product" }')
schema_path.write_text(schema_text)

print("Ported into", THEME)

# --- Site JS: the bag talks to Shopify's AJAX cart ---------------------------
js = (SRC / "js/site.js").read_text()
start, end = js.index("  var PRODUCT ="), js.index("  function openCart()")
js = js[:start] + r'''  function money(cents) { return "$" + (cents / 100).toFixed(2); }

  function renderCart(cart) {
    if (!cartBody) return;
    if (!cart.item_count) {
      cartBody.innerHTML = '<p class="cart-empty">Your bag is empty. KG215 is waiting.</p>';
    } else {
      cartBody.innerHTML = cart.items.map(function (item) {
        return '<div class="cart-item">' +
          (item.image ? '<img src="' + item.image + '" alt="" width="120" />' : "") +
          "<div><h3>" + item.product_title.replace(/KG185/g, "KG215") + "</h3>" +
          // The MLVeda region variants (ca, na...) are not worth showing.
          (item.variant_title && !(item.options_with_values || []).some(function (o) { return /mlveda/i.test(o.name); })
            ? "<p>" + item.variant_title + "</p>" : "") +
          "<p>Qty " + item.quantity + "</p>" +
          "<p>" + money(item.final_line_price) + "</p></div></div>";
      }).join("");
    }
    if (cartTotal) cartTotal.textContent = money(cart.total_price);
    if (cartCount) {
      cartCount.textContent = String(cart.item_count);
      cartCount.classList.toggle("is-shown", cart.item_count > 0);
    }
  }

  function refreshCart() {
    return fetch("/cart.js", { headers: { Accept: "application/json" } })
      .then(function (r) { return r.json(); })
      .then(renderCart);
  }

''' + js[end:]

start, end = js.index("  var addBtn ="), js.index("  /* --- Botanical slider")
js = js[:start] + r'''  var addBtn = $("[data-add]");
  if (addBtn) {
    addBtn.addEventListener("click", function () {
      addBtn.disabled = true;
      fetch("/cart/add.js", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ items: [{ id: Number(addBtn.dataset.variantId), quantity: pending }] })
      })
        .then(function (r) { if (!r.ok) throw r; return refreshCart(); })
        .then(function () {
          addBtn.classList.add("is-added");
          setTimeout(function () { addBtn.classList.remove("is-added"); }, 1200);
          setTimeout(openCart, 260);
        })
        .catch(function () { alert("Sorry, that couldn't be added to your bag."); })
        .then(function () { addBtn.disabled = false; });
    });
  }

''' + js[end:]
js = js.replace("  renderCart();\n})();", "  refreshCart();\n})();")
# Real Shopify forms submit normally; only keep the old handler for any leftover demo forms.
(A / "kg-site.js").write_text(js)
print("Wrote kg-site.js")
