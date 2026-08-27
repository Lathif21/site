#!/usr/bin/env python3
"""
Generates the four replica pages from shared partials so the header, footer and
cookie bar stay identical across them. Run `python3 build.py` after editing
anything here; the .html files it writes are the deliverable.

Writes ONLY: index.html, hoe-werkt-het.html, realisaties.html, tutorials.html.
webshop.html and product.html are the hand-authored catalogue pages on the other
stylesheet (assets/app.css) — this script must never write over them. Their nav
markup is duplicated by hand, so a change to NAV below has to be mirrored there.
"""
import pathlib

OUT = pathlib.Path(__file__).parent

NAV = [("index.html", "Overzicht"), ("hoe-werkt-het.html", "Hoe werkt het?"),
       ("realisaties.html", "Realisaties"), ("webshop.html", "Webshop"),
       ("tutorials.html", "Tutorials")]

# ---------------------------------------------------------------------------
# The chrome is shared, and every page is the brandbook build now: all six load
# assets/brand.css and take the branded header. (index / hoe-werkt-het /
# realisaties / tutorials were the staging replica and ran without it; that
# split is gone, and header(brand=False) is kept only so the replica can be
# reproduced from this script if it is ever needed for comparison.)
#
# header() takes brand=. With it, the wordmark is the palette version --
# #c75433 / #000000 on transparent (img/logo-brand.png). Without it the header
# is exactly what it was before the brand layer existed: the replica's #fd8b11
# wordmark (img/logo.png).
#
# The lockup does NOT set the logo-icoon beside the wordmark. 01.03 allows it
# ("in combinatie met tekst") and this script used to emit it, but it was taken
# back out of every page by hand: the bean is SETT's mark, and this is Atelier
# DIY's site. The brandbook is the design system here, not the brand.
#
# Both branches emit the same links in the same order with the same aria, so the
# navigation itself cannot drift between the two halves. Only the wordmark file
# differs.
# ---------------------------------------------------------------------------

ARROW = ('<svg width="20" height="14" viewBox="0 0 22 14" fill="none" stroke="currentColor" '
         'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M1 7h19M14.5 1.5 20.5 7l-6 5.5"/></svg>')

PLAY = ('<svg width="16" height="18" viewBox="0 0 16 18" fill="currentColor" aria-hidden="true">'
        '<path d="M2 1.6a1 1 0 0 1 1.5-.87l11 7.4a1 1 0 0 1 0 1.74l-11 7.4A1 1 0 0 1 2 16.4z"/></svg>')

GAUGE = ('<svg viewBox="0 0 40 34" fill="none" aria-hidden="true">'
         '<path d="M4 28a16 16 0 1 1 32 0" stroke="#fd8b11" stroke-width="3.4" stroke-linecap="round"/>'
         '<path d="M20 28 30 15" stroke="#212838" stroke-width="3.2" stroke-linecap="round"/>'
         '<circle cx="20" cy="28" r="2.6" fill="#212838"/></svg>')

CLOCK = ('<svg viewBox="0 0 34 34" fill="none" aria-hidden="true">'
         '<circle cx="17" cy="18" r="12.5" stroke="#fd8b11" stroke-width="3"/>'
         '<path d="M17 11v7l4.5 2.6" stroke="#fd8b11" stroke-width="3" stroke-linecap="round"/>'
         '<path d="M12 2.5h10" stroke="#fd8b11" stroke-width="3" stroke-linecap="round"/></svg>')


CART_ICON = ('<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
             'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
             '<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/>'
             '<path d="M2 3h3l2.6 12.2a1.5 1.5 0 0 0 1.5 1.2h8.4a1.5 1.5 0 0 0 1.5-1.2L21 7H6"/></svg>')


def header(active, cart=False, brand=False):
    """cart=True adds the live basket count catalog.js drives. The replica pages
    have no basket, so they keep the plain icon and stay pixel-identical."""
    cur = ' aria-current="page"'
    links = "".join(
        f'<a href="{h}"{cur if h == active else ""}>{t}</a>' for h, t in NAV)
    if cart:
        basket = (f'<a class="cart" id="cartBtn" href="#" aria-label="Winkelmandje, 0 artikelen">'
                  f'{CART_ICON}<span class="cart-count" id="cartCount">0</span></a>')
    else:
        basket = f'<a href="#" aria-label="Winkelmandje">{CART_ICON}</a>'
    logo = (
        '<a class="logo sett-lockup" href="index.html" aria-label="Atelier DIY \u2014 home">\n'
        '      <img src="img/logo-brand.png" alt="Atelier DIY" width="44" height="38">\n'
        '    </a>'
        if brand else
        '<a class="logo" href="index.html" aria-label="Atelier DIY \u2014 home">\n'
        '      <img src="img/logo.png" alt="Atelier DIY" width="44" height="38">\n'
        '    </a>'
    )
    return f'''<header class="site-header">
  <div class="wrap-wide">
    {logo}
    <nav class="nav" id="nav" aria-label="Hoofdnavigatie">{links}</nav>
    <div class="header-actions">
      {basket}
      <a href="#" aria-label="Mijn account">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="8" r="3.8"/><path d="M4.5 20a7.5 7.5 0 0 1 15 0"/></svg>
      </a>
      <button class="burger" id="burger" aria-expanded="false" aria-controls="nav" aria-label="Menu">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      </button>
    </div>
  </div>
</header>'''


FOOTER = f'''<footer class="site-footer">
  <div class="wrap-wide">
    <div class="footer-grid">
      <div>
        <h2>Jouw partner in creatieve<br>DIY-projecten</h2>
        <p>Ontdek onze hoogwaardige doe-het-zelf pakketten en stap-voor-stap tutorials.
           Creëer unieke designstukken met professionele materialen en duidelijke
           instructies – eenvoudig, leuk en betaalbaar!</p>
        <a class="btn" href="webshop.html">Bekijk onze DIY-pakketten {ARROW}</a>
      </div>
      <nav aria-label="Sitemap">
        <ul class="footer-nav">
          <li><a href="index.html">Overzicht</a></li>
          <li><a href="webshop.html">Webshop</a></li>
          <li><a href="hoe-werkt-het.html">Hoe werkt het?</a></li>
          <li><a href="realisaties.html">Realisaties</a></li>
          <li><a href="tutorials.html">Tutorials</a></li>
          <li><a href="#">Mijn account</a></li>
        </ul>
      </nav>
      <nav aria-label="Klantendienst">
        <ul class="footer-nav">
          <li><a href="#">Privacy beleid</a></li>
          <li><a href="#">Algemene voorwaarden</a></li>
          <li><a href="#">Aanmelden nieuwsbrief</a></li>
          <li><a href="#">Contacteer ons</a></li>
          <li><a href="#">Bekijk bestelling-status</a></li>
        </ul>
      </nav>
      <address class="footer-contact">
        <span>Tweelindenstraat 7<br>B-8810 Lichtervelde</span>
        <span>BE 1011 359 018</span>
        <a href="mailto:info@diy-atelier.be">info@diy-atelier.be</a>
      </address>
    </div>
    <div class="footer-bottom">
      <span>© 2026 Atelier-DIY. Alle rechten voorbehouden.</span>
      <span class="socials">
        <a href="#" aria-label="Facebook"><svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14.5 8.5V6.8c0-.8.2-1.3 1.4-1.3h1.6V2.6C17.2 2.5 16.3 2.4 15.3 2.4c-2.2 0-3.8 1.4-3.8 4v2.1H9v3.2h2.5V21h3V11.7h2.5l.4-3.2z"/></svg></a>
        <a href="#" aria-label="Instagram"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor" stroke="none"/></svg></a>
      </span>
    </div>
  </div>
</footer>

<div class="cookie" id="cookie" role="region" aria-label="Cookiemelding">
  <div class="wrap-wide">
    <p>Deze website maakt gebruik van cookies om uw ervaring te verbeteren. Door op
       &ldquo;Accepteren&rdquo; te klikken, gaat u akkoord met onze cookies.</p>
    <div class="cookie-actions">
      <button type="button" data-cookie="accept">Accepteren</button>
      <button type="button" class="refuse" data-cookie="refuse">Weigeren</button>
    </div>
  </div>
</div>'''


def page(filename, title, active, body, desc=""):
    html = f'''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="img/icon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Libre+Franklin:wght@300;400;500;600;700&family=Mulish:wght@300;400;500;600;700&family=PT+Serif:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
<!-- The SETT brand layer, loaded last so it re-tints site.css from one place.
     These four pages ran without it while they were the staging replica; they
     are the brandbook build now, like webshop.html and product.html. -->
<link rel="stylesheet" href="assets/brand.css?v=1">
<!-- The set pieces the webshop worked out — the dark field, the photographic
     card, the poster block — generalised so every page can use them. -->
<link rel="stylesheet" href="assets/pages.css?v=1">
</head>
<body>
<a class="skip" href="#main">Ga naar inhoud</a>
{header(active, brand=True)}
<main id="main">
{body}
</main>
{FOOTER}
<script src="assets/site.js"></script>
</body>
</html>
'''
    (OUT / filename).write_text(html, encoding="utf-8")
    print("wrote", filename)


# --------------------------------------------------------------------------
# Realisaties masonry — 3 columns, tiles in the order they appear on the live page
# --------------------------------------------------------------------------
GALLERY = [
    ["rz-1-1", "rz-1-2"],
    ["rz-2-1", "rz-2-2", "rz-2-3"],
    ["rz-3-1", "rz-3-2", "rz-3-3", "rz-3-4"],
]
ALTS = {
    "rz-1-1": "Maker werkt een Mortex tafelblad af in het atelier",
    "rz-1-2": "Twee afgewerkte Mortex salontafels in een lichte woonkamer",
    "rz-2-1": "Bovenaanzicht van twee Mortex salontafels met magazine",
    "rz-2-2": "Langwerpige Mortex salontafel in een donker interieur",
    "rz-2-3": "Fotoshoot op een kasseiweg met hond",
    "rz-3-1": "Materiaal wordt uitgeladen bij een buitenopname",
    "rz-3-2": "Twee makers werken samen aan een tafelblad in het atelier",
    "rz-3-3": "Cameramonitor tijdens een productopname",
    "rz-3-4": "Mortex salontafel in een woonkamer met zicht op de tuin",
}


def statement(rail, eyebrow, lines, sub, lede, cta_href, cta_text, plate=None,
              plate_alt="", narrow=False):
    """The opening statement field — 05.01, and guidelines 5.1.

    "On 05.01 the website's opening statement is black, upper-case and
    justified across an open white field, and the photograph is stacked
    underneath it — not laid under the type." The webshop has run this since
    the brand layer landed; it is every page's opening now, so the four that
    still opened on a photograph with type laid over it (the .hero and
    .hero-band bands) open the way the book's own website page does.

    `lines` is a list of lists of words: each inner list is one line of the
    01.05 spread, its words pushed to opposite edges of the measure. A line
    given as a single string is set tight (flush left) instead — the device
    needs at least two words to have a gap to set.

    The caption is .t-label, not .eyebrow. Above 1180px brand.css turns the
    field into a two-column grid with a rule down the gutter, and it is
    .t-label that it lifts into the margin column beside the statement — an
    .eyebrow auto-places into the next free cell, which puts the page's name
    at the bottom of the composition on top of the lede.
    """
    spread = ""
    for line in lines:
        if isinstance(line, str):
            spread += '      <span class="tight"><b>%s</b></span>\n' % line
        else:
            spread += '      <span>%s</span>\n' % " ".join("<b>%s</b>" % w for w in line)

    below = ""
    if plate:
        # 04.02 — the photograph as a hard-edged plate UNDER the statement,
        # never behind it. Nothing is set on top of it, so it needs no scrim.
        below = ('\n\n<section class="sett-plate sett-plate-wide">\n'
                 '  <img src="img/%s.jpg" alt="%s" loading="eager">\n'
                 '</section>' % (plate, plate_alt))

    # .spread-narrow pulls the measure in to 600px — for a line of two or three
    # short words, the full 940 leaves gaps you read as columns. Only safe when
    # the longest line fits: a .spread line is nowrap, so a measure narrower
    # than the words overflows inside the line box instead of widening it.
    measure = " spread-narrow" if narrow else ""
    return '''<section class="sett-statement sett-field">
  <span class="sett-rail" aria-hidden="true">%s</span>
  <div class="sett-statement-inner">
    <p class="t-label">%s</p>
    <h1 class="t-statement spread%s" lang="en">
%s    </h1>
    <p class="sett-sub">%s</p>
    <div class="sett-statement-foot">
      <p>%s</p>
      <a class="btn" href="%s">%s %s</a>
    </div>
  </div>
</section>%s''' % (rail, eyebrow, measure, spread, sub, lede, cta_href, cta_text, ARROW, below)


def mosaic():
    """The nine plates as the book's own photography grid — 04.01 / 04.02.

    Both photography pages lay their images out the same way: a four-column
    grid with NO gutter, where a cell spans one or two columns and one or two
    rows, so the pictures butt against each other and the block reads as one
    wall rather than as nine framed pictures. 04.02's upper block is two
    uprights beside a column split into two wide halves; its lower block is a
    double-width plate beside two uprights. That is bands A and B below,
    verbatim; band C closes on the pair the book has no room for.

    The homepage runs this. realisaties.html runs the same nine as separate
    cards on the dark field — two galleries in two registers, which is the
    book's own habit.
    """
    flat = [slug for col in GALLERY for slug in col]
    # (extra classes) per plate, in order — see the bands above
    spans = ["m-h2", "m-h2", "m-w2", "m-w2",
             "m-w2 m-h2", "m-h2", "m-h2",
             "m-w2 m-h2", "m-w2 m-h2"]
    cells = ""
    for slug, span in zip(flat, spans):
        cells += ('    <figure class="%s">'
                  '<img src="img/%s.jpg" alt="%s" loading="lazy"></figure>\n'
                  % (span, slug, ALTS[slug]))
    return '<div class="sett-mosaic">\n%s  </div>' % cells


def gallery_cards():
    """The nine realisaties as photographic cards — 4.1 / 4.2.

    Same nine plates and the same alt text as mosaic(); what changes is that
    they are objects on a field here instead of one butted wall.
    """
    flat = [slug for col in GALLERY for slug in col]
    out = ""
    # one ratio for all nine: 04.01's grid is regular, and a wall that changes
    # shape every fourth plate reads as a masonry that failed rather than as a
    # rhythm. Nine plates, three across, and the poster runs under them.
    for i, slug in enumerate(flat, 1):
        out += "      " + sett_card(slug, "", num="%02d" % i,
                                    alt=ALTS[slug]) + "\n"
    return out


# --------------------------------------------------------------------------
# FAQ — (vraag, antwoord). Copy supplied by the client.
# --------------------------------------------------------------------------
FAQ = [
    ("Wat is DIY-Atelier?",
     "DIY-Atelier is hét platform voor doe-het-zelf projecten met hoogwaardige "
     "materialen en duidelijke tutorials. We helpen je om zelf design meubels en "
     "decorstukken te maken tegen een betaalbare prijs. Elk project wordt volledig "
     "ondersteund met de nodige uitleg in videoform. Hierdoor kan elk project zoals "
     "een professional tot een goed einde gebracht worden."),
    ("Hoe werkt DIY-Atelier?",
     "Heel eenvoudig! Je kiest een DIY-pakket in onze webshop, ontvangt alle "
     "benodigde materialen thuis en volgt onze stapsgewijze tutorials om jouw eigen "
     "unieke meubel of decorstuk te maken."),
    ("Hoe lang duurt de levering?",
     "Voor de DOE-HET-ZELVERS die niet kunnen wachten, kan de bestelling na 1 "
     "werkdag ook steeds opgehaald worden aan het centraal depot van DIY-atelier "
     "Belgium."),
    ("Wat zit er in een DIY-pakket?",
     "Elk pakket bevat alle materialen die je nodig hebt, plus een stap-voor-stap "
     "handleiding en toegang tot een exclusieve tutorialvideo."),
    ("Kan ik mijn bestelling retourneren?",
     "Wij kunnen enkel onbewerkte goederen rembourceren. Van zodra er bewerkingen "
     "uitgevoerd zijn op de aankoop/materialen, kunnen wij geen goederen onder "
     "garantie brengen."),
    ("Moet ik ervaring hebben met doe-het-zelven?",
     "In de webshop wordt er steeds een indicatie gegeven waarop de "
     "moeilijkheidsgraad wordt weergegeven."),
    ("Heb ik extra gereedschap nodig?",
     "Elk pakket (geen individuele stukken) wordt voorzien van ALLE nodige "
     "onderdelen die essentieel zijn om jouw project tot een goed einde te brengen. "
     "Hierbij wordt er niets van extra gereedschap vereist. Bij aankoop van "
     "individuele stukken worden geen extra tools meegeleverd."),
    ("Wat als ik vastloop tijdens het maken?",
     "Geen zorgen! Onze tutorials helpen je stap voor stap. Kom je er toch niet "
     "uit? Stuur ons een berichtje en we helpen je verder."),
    ("Welke betaalmethodes accepteren jullie?",
     "Je kunt veilig betalen met iDEAL, creditcard, PayPal en Bancontact."),
    ("Zit er garantie op de materialen?",
     "Wij kunnen enkel instaan voor ontvangen goederen die beschadigd zijn. Van "
     "zodra er bewerkingen uitgevoerd zijn op de aankoop/materialen, kunnen wij "
     "geen goederen onder garantie brengen."),
]


def faq():
    items = ""
    for i, (q, a) in enumerate(FAQ, 1):
        items += f'''      <div class="faq-item">
        <button class="faq-q" type="button" aria-expanded="false" aria-controls="faq-a{i}" id="faq-q{i}">
          <span>{i}. {q}</span><span class="faq-icon" aria-hidden="true"></span>
        </button>
        <div class="faq-a" id="faq-a{i}" role="region" aria-labelledby="faq-q{i}">
          <div><p>{a}</p></div>
        </div>
      </div>
'''
    return f'<div class="faq">\n{items}    </div>'


# ==========================================================================
# 1 — Overzicht
# ==========================================================================
COL_ICONS = [
    '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 20V9a2.6 2.6 0 0 1 5.2 0v9"/><path d="M20.2 18.5v-2a2.4 2.4 0 0 1 4.8 0v2"/><path d="M25 18.8v-1.3a2.4 2.4 0 0 1 4.8 0v8.2c0 5.4-3.4 8.8-8.6 8.8-4.6 0-6.6-1.8-8.8-5.4l-3.2-5.3a2.5 2.5 0 0 1 4.1-2.8L15 24"/></svg>',
    '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 15.5 6 11l6-5 8 3 8-3 6 5-14 4.5Z"/><path d="M6 11v15l14 5 14-5V11"/><path d="M20 15.5V31"/></svg>',
    '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><ellipse cx="20" cy="15" rx="16" ry="6"/><path d="M16 20.5V31M24 20.5V31"/></svg>',
]
COL_TEXT = [
    "Blader door onze webwinkel en kies het DIY-pakket dat bij jouw stijl en wensen past. "
    "Van tafels tot decoratie, wij hebben alles om jouw creativiteit te laten bloeien!",
    "Je ontvangt een compleet pakket met alle materialen die je nodig hebt. Volg onze "
    "eenvoudige tutorials en ontdek hoe leuk en makkelijk het is om zelf iets moois te maken.",
    "Na het bouwen heb je een prachtig handgemaakt meubel of decorstuk voor een fractie van "
    "de winkelprijs. Jouw creatie, jouw trots!",
]

PRODUCTS = [
    ("ov-prod1", "Tapijt Wit 3m²", "Vanaf €399.99", "Basis", "3 dagen",
     "Wit schapenvacht tapijt van 3 m²"),
    ("ov-prod2", "Witte Langharig", "Vanaf €50", None, None,
     "Wit langharig schapenvacht"),
    ("ov-prod3", "Model BV", "Vanaf €995", "Eenvoudig", "8 dagen",
     "Model BV eettafel in Mortex"),
]


def sett_card(img, title, sub="", pill="", tag="", num="", href="", ratio="",
              alt="", ext="jpg", el="p"):
    """One photographic card — 4.2 / 05.09, in the language the catalogue set.

    The photograph is the card; the type is set into it over a scrim. Every
    part but the image is optional, so the same object carries a product, a
    step, a gallery plate or a tutorial.
    """
    cls = "sett-card" + (" " + ratio if ratio else "")
    over = ""
    if pill:
        over += '\n    <span class="sett-card-pill">%s</span>' % pill
    if tag:
        over += '\n    <span class="sett-card-tag">%s</span>' % tag
    if num:
        over += '\n    <span class="sett-card-num" aria-hidden="true">%s</span>' % num
    # a plate with nothing to say carries no scrim: the gallery's cards are the
    # photograph and the numeral, and their description belongs in the alt text
    # rather than printed over the picture twice
    if title or sub:
        name = '<a class="sett-stretch" href="%s">%s</a>' % (href, title) if href else title
        body = '<%s class="sett-card-title">%s</%s>' % (el, name, el)
        if sub:
            body += '\n        <p class="sett-card-sub">%s</p>' % sub
        over += ('\n      <div class="sett-card-body">'
                 '\n        %s'
                 '\n      </div>' % body)
    elif href:
        over += '\n    <a class="sett-stretch" href="%s"><span class="sr-only">%s</span></a>' % (href, alt)
    return (
        '<article class="%s">\n'
        '    <img src="img/%s.%s" alt="%s" loading="lazy">%s\n'
        '    </article>' % (cls, img, ext, alt, over)
    )


def featured_cards():
    out = ""
    for i, (img, name, price, diff, lead, alt) in enumerate(PRODUCTS, 1):
        out += "    " + sett_card(img, name, sub=price, pill=diff or "Pakket",
                                  tag=lead or "", num="%02d" % i,
                                  href="webshop.html", alt=alt) + "\n"
    return out


QUOTES = [
    ("Tom - Praktische klusser",
     "Ik dacht altijd dat zelf een design tafel maken veel te ingewikkeld was, maar "
     "DIY-Atelier maakt het zo makkelijk! De instructies waren duidelijk en het resultaat "
     "is fantastisch."),
    ("Sophie - Creatieve DIY",
     "Alles werd netjes geleverd en de video&rsquo;s hielpen enorm. Het voelde alsof ik een "
     "professioneel meubelstuk maakte, maar dan gewoon in mijn eigen garage!"),
    ("Lisa &amp; Mark",
     "We wilden iets unieks voor onze eetkamer zonder de hoofdprijs te betalen. Dankzij "
     "DIY-Atelier hebben we nu een prachtige Mortex tafel waar we super trots op zijn!"),
]

cols3 = "".join(
    f'<div><div class="col-icon">{COL_ICONS[i]}</div><p>{COL_TEXT[i]}</p></div>'
    for i in range(3))

quotes = "".join(
    f'<article class="quote"><h3>{n}</h3><p>&quot;{t}&quot;</p></article>' for n, t in QUOTES)

overview_head = statement(
    "diy-atelier.be — Lichtervelde",
    "Atelier DIY — Lichtervelde",
    # Guidelines 5.1 names this line as the website's hero headline. The name
    # in it is the book's own, so the site puts its own there. Kept as ONE
    # spread unit: split in two, the justification pushes "DIY" and "ATELIER"
    # to opposite ends of the measure and the company reads as two companies.
    [["DIY ATELIER", "IS", "NOT"],
     ["JUST", "A", "PRODUCT."],
     ["IT'S", "AN", "OPPORTUNITY"],
     ["TO", "CREATE", "MEMORIES."]],
    "Jouw creativiteit, onze materialen.",
    "Zelf unieke meubels en decorstukken maken? Wij leveren de hoogwaardige materialen, "
    "het gereedschap en de tutorials. Van Mortex tafels tot schapenvachttapijten — "
    "ontdek hoe eenvoudig het is om zelf aan de slag te gaan.",
    "#hoe-werkt-het", "Ontdek de eenvoud van DIY",
    plate="ov-hero", plate_alt="Een maker werkt een Mortex tafelblad af in het atelier")

overview = f'''{overview_head}

<section class="section" id="hoe-werkt-het">
  <div class="wrap">
    <h2 class="center">Hoe werkt het?</h2>
    <div class="cols3">{cols3}</div>
  </div>
</section>

<section class="section-tight">
  <div class="wrap">
    <div class="video-cta" id="videoCta" style="background-image:url('img/ov-video.jpg')">
      <div class="video-cta-copy">
        <h2>DIY Mortex Tafel – Maak het zelf!</h2>
        <p>Benieuwd hoe je zelf een prachtige Mortex tafel maakt? In deze video laten we je
           stap voor stap zien hoe eenvoudig het is om met onze materialen en tutorials een
           hoogwaardig designstuk te creëren.</p>
        <button class="btn" type="button" id="videoCtaPlay" aria-controls="videoCtaPlayer" aria-expanded="false">Bekijk de video en ontdek {PLAY}</button>
      </div>
      <video class="video-cta-player" id="videoCtaPlayer" controls playsinline preload="none"
             poster="img/ov-video.jpg" width="1280" height="794" tabindex="-1">
        <source src="video/ov-mortex.webm" type="video/webm">
        <source src="video/ov-mortex.mp4" type="video/mp4">
        Je browser ondersteunt geen video.
      </video>
    </div>
  </div>
</section>

<!-- Uitgelicht — the catalogue's set piece, at three cards.
     The carousel arrows went with it: they were a control for a rail that
     never scrolled, and the row is three cards and a poster now. -->
<section class="sett-dark" aria-labelledby="uitgelicht-h">
  <span class="sett-rail" aria-hidden="true">diy-atelier.be — 33 pakketten</span>
  <div class="sett-dark-inner">
    <div class="sett-masthead">
      <div>
        <p class="sett-eyebrow">Uitgelicht</p>
        <h2 class="sett-masthead-h" id="uitgelicht-h">Drie om mee<br>te beginnen.</h2>
      </div>
      <div>
        <p class="sett-masthead-lede">Elk pakket komt compleet toe — de materialen, het
           professionele gereedschap en een stap-voor-stap handleiding. Geen ervaring nodig,
           geen speciaalzaak om af te lopen.</p>
        <p class="sett-index"><span>33 pakketten</span><span>25 tafels</span><span>8 tapijten</span></p>
      </div>
    </div>

    <div class="sett-grid sett-grid-4">
{featured_cards()}    <!-- 5.6 — the poster block, carrying baseline 3 of 1.3 -->
    <p class="sett-poster" lang="en">Not made to buy. Made to create.</p>
    </div>

    <p class="sett-dark-cta">
      <a class="sett-pill sett-pill-solid" href="webshop.html">Bekijk alle 33 pakketten {ARROW}</a>
    </p>
  </div>
</section>

<section class="section-tight">
  <div class="wrap">
    <img src="img/ov-pallet.jpg" alt="DIY-Atelier verpakking en materiaal op een pallet"
         style="width:100%;border-radius:var(--radius-lg)" loading="lazy">
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2 style="margin-bottom:48px">Wat zeggen mensen over ons?</h2>
    <div class="quote-grid">{quotes}</div>
  </div>
</section>

<section class="section-tight">
  <div class="wrap">
    <div class="panel">
      <p>Zelf ook een uniek meubelstuk maken? Ontdek onze DIY-pakketten en tutorials en ga
         vandaag nog aan de slag!</p>
      <a class="btn" href="webshop.html">Bekijk onze DIY-pakketten {ARROW}</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2 style="margin-bottom:48px">Realisaties</h2>
    {mosaic()}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2 class="center">FAQ (Veelgestelde vragen)</h2>
    {faq()}
  </div>
</section>'''


# ==========================================================================
# 2 — Hoe werkt het?
# ==========================================================================
STEPS = [
    ("Kies jouw DIY pakket uit ons gamma", "Stap 1: de selectie",
     ["Bij DIY Atelier hebben we een breed assortiment aan doe-het-zelf pakketten, geschikt "
      "voor zowel beginners als ervaren makers. Of je nu een stijlvolle tafel, een decoratief "
      "item of een uniek meubelstuk wilt creëren, wij hebben het perfecte pakket voor jou!"],
     "hw-stap1", "Oranje Mortex tafel op een grijze achtergrond", False),
    ("Wij voorzien alle tools &amp; producten", "Stap 2: de producten",
     ["Met onze DIY-pakketten hoef je zelf nergens naar op zoek te gaan. Wij leveren alle "
      "tools en producten die je nodig hebt om jouw project tot een succes te maken. Geen "
      "losse aankopen, geen gedoe – gewoon alles in één handig pakket!"],
     "hw-stap2", "Alle materialen en gereedschap uit een DIY-pakket", True),
    ("Onze experts geven een gedetailleerde uitleg", "Stap 3: de instructies",
     ["Met onze DIY-pakketten ben je verzekerd van een zorgeloze en succesvolle doe-het-zelf "
      "ervaring. We voorzien je van alle tools en materialen die je nodig hebt, zodat je "
      "meteen aan de slag kunt. Daarnaast krijg je gedetailleerde uitleg van onze experts, "
      "zodat je steeds de juiste techniek toepast.",
      "Dankzij onze stap-voor-stap handleidingen, videotutorials en praktische tips behaal "
      "je moeiteloos een professioneel resultaat."],
     "hw-stap3", "Videotutorial op een laptop", False),
    ("Enkel plezier staat je nog te wachten", "Stap 4: het maken",
     ["Met ons DIY-pakket heb je alles in huis om direct aan de slag te gaan. Geen gedoe, "
      "geen stress – alleen creativiteit en voldoening. Dankzij onze zorgvuldig samengestelde "
      "materialen, professionele tools en duidelijke instructies wordt jouw doe-het-zelf "
      "project een leuke en inspirerende ervaring."],
     "hw-stap4", "Twee makers tillen samen een afgewerkt tafelblad", True),
]


def steps():
    """The five steps, as one dark chapter.

    They were five stacked .split sections — a photograph beside a column of
    copy, alternating sides, five times. That is the layout the replica had for
    everything, and at five repeats it reads as a wall. The book's own way of
    listing a sequence is a numbered set (03.01), so the four working steps are
    a numbered row of photographic cards with the copy under each, and step 5 —
    which is not work, it is the result — closes the chapter as a wide plate.
    """
    cards = ""
    for i, (eyebrow, h, paras, img, alt, _reverse) in enumerate(STEPS, 1):
        body = "".join("<p>%s</p>" % p for p in paras)
        # "Stap 1: de selectie" → the numeral goes on the pill, the name stays
        short = h.split(":", 1)[1].strip().capitalize() if ":" in h else h
        card = sett_card(img, eyebrow, sub=short, pill="Stap %02d" % i,
                         num="%02d" % i, alt=alt, el="h3", ratio="sett-card-tall")
        cards += '''    <li class="sett-step">
      %s
      <div class="sett-step-copy">%s</div>
    </li>
''' % (card, body)

    return '''<section class="sett-dark" aria-labelledby="stappen-h">
  <span class="sett-rail" aria-hidden="true">diy-atelier.be — in vijf stappen</span>
  <div class="sett-dark-inner">
    <div class="sett-masthead">
      <div>
        <p class="sett-eyebrow">In vijf stappen</p>
        <h2 class="sett-masthead-h" id="stappen-h">Van doos<br>naar designstuk.</h2>
      </div>
      <div>
        <p class="sett-masthead-lede">Reken op een weekend werk, verspreid over drie dagen
           uitharden. De handleiding en de videotutorial nemen je mee van de eerste laag tot
           de finale verzegeling — en je kunt op elk moment even stoppen.</p>
        <p class="sett-index"><span>5 stappen</span><span>1 doos</span><span>0 speciaalzaken</span></p>
      </div>
    </div>

    <ol class="sett-grid sett-grid-4 sett-steps">
%s    </ol>

    <!-- Step 5 is the result, so it is the plate the chapter closes on
         (04.02) with 5.6's colour block beside it. -->
    <div class="sett-close">
      <article class="sett-card sett-card-wide sett-close-media">
        <img src="img/hw-stap5.jpg" alt="Koppel geniet van de zelfgemaakte Mortex salontafel" loading="lazy">
        <span class="sett-card-pill">Stap 05</span>
        <div class="sett-card-body">
          <h3 class="sett-card-title">Genieten</h3>
          <p class="sett-card-sub">Jouw creatie, jouw trots.</p>
        </div>
      </article>
      <p class="sett-poster sett-poster-wide" lang="en">Not made to buy. Made to create.</p>
    </div>
  </div>
</section>
''' % cards


hoewerkthet_head = statement(
    "diy-atelier.be — hoe werkt het",
    "Hoe werkt het?",
    # 1.3, baseline 2. Each page carries a different one of the three, and no
    # page prints the same baseline twice: this one closes on baseline 3.
    # broken the way the webshop's closing duo breaks it: three words a line
    # at most, and the clause boundary on the line end. At 3/3/3/1 the spread
    # strands "IS" and "THE" against the right edge and the sentence stops
    # reading as a sentence.
    [["THE", "PRODUCT"], ["IS", "THE", "RESULT."],
     ["THE", "MOMENT", "IS"], "THE REASON."],
    "In vijf stappen van doos naar designstuk.",
    "Je kiest een pakket, wij leveren alles wat erbij hoort — de materialen, het "
    "professionele gereedschap, de handleiding en de videotutorial. Geen ervaring nodig.",
    "webshop.html", "Bekijk de pakketten",
    plate="hw-hero", plate_alt="Twee makers werken samen in het atelier")

hoewerkthet = f'''{hoewerkthet_head}

<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="split-text">
        <p class="eyebrow">Design voor een betaalbare prijs?</p>
        <h2>Wat is DIY-atelier</h2>
        <p>DIY Atelier is dé plek voor creatievelingen die zelf aan de slag willen met
           hoogwaardige doe-het-zelf projecten. Wij bieden complete DIY-pakketten waarmee je
           op een eenvoudige en betaalbare manier je eigen meubels en decoratie maakt. Dankzij
           duidelijke instructies en professionele materialen haal je het vakmanschap in huis
           – zonder dure specialisten. Iedereen kan het, jij ook!</p>
      </div>
      <div class="split-media">
        <img src="img/hw-whatis.jpg" alt="DIY-Atelier verpakking en emmer op een pallet" loading="lazy">
      </div>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="wrap">
    <p class="lede"><span class="hl">Design</span> interieur voor iedereen, met onze
       <span class="hl">DIY-atelierproducten.</span></p>
  </div>
</section>

<!-- 04.02 — the photograph as a full-bleed plate, not a rounded panel inside
     the text column. It is the last light beat before the dark chapter. -->
<section class="sett-plate sett-plate-wide">
  <img src="img/hw-couple.jpg" alt="Twee makers werken samen aan een Mortex tafel" loading="lazy">
</section>

{steps()}'''


# ==========================================================================
# 3 — Realisaties
# ==========================================================================
realisaties_head = statement(
    "diy-atelier.be — realisaties",
    "Realisaties",
    # 1.3, baseline 1 — the one 5.3 puts on the brochure cover. The book can
    # write "SETT THE TABLE" because its name is the verb; here the pun has no
    # owner, so the line is simply the sentence it was punning on.
    [["SET", "THE", "TABLE"], ["FOR", "UNFORGETTABLE"], "MOMENTS."],
    "Negen stuks, negen keukens en garages.",
    "Elk stuk hieronder is met een DIY-pakket gemaakt, door makers zonder ervaring. "
    "De vorm is telkens dezelfde; de hand is dat nooit.",
    "webshop.html", "Maak er zelf een")

realisaties = f'''{realisaties_head}
<!-- The gallery, as the catalogue's chapter.
     It was a three-column masonry of bare photographs on white — the one page
     with no composition on it at all. 4.1 and 4.2 are the reason it can carry
     the dark field better than any other page: every plate on it is either a
     maker at work or a finished piece in a room, which is exactly the two
     modes the guidelines ask photography to run in. -->
<section class="sett-dark" aria-labelledby="realisaties-h">
  <span class="sett-rail" aria-hidden="true">diy-atelier.be — realisaties</span>
  <div class="sett-dark-inner">
    <div class="sett-masthead">
      <div>
        <p class="sett-eyebrow">Negen realisaties</p>
        <h2 class="sett-masthead-h" id="realisaties-h">Gemaakt in<br>Lichtervelde.</h2>
      </div>
      <div>
        <p class="sett-masthead-lede">Van de eerste laag in het atelier tot het afgewerkte
           stuk in de woonkamer. Geen twee zijn identiek: de vorm is dezelfde, de hand is dat
           nooit.</p>
        <p class="sett-index"><span>9 realisaties</span><span>Mortex &amp; schapenvacht</span></p>
      </div>
    </div>

    <div class="sett-grid sett-gallery">
{gallery_cards()}    </div>

    <!-- 5.6 — the colour block, running the width of the wall it closes -->
    <p class="sett-poster sett-poster-band" lang="en">The product is the result. The moment is the reason.</p>

    <p class="sett-dark-cta">
      <a class="sett-pill sett-pill-solid" href="webshop.html">Maak er zelf een {ARROW}</a>
      <a class="sett-pill" href="tutorials.html">Bekijk de tutorials</a>
    </p>
  </div>
</section>'''


# ==========================================================================
# 4 — Tutorials
# ==========================================================================
# (slug, title, description, size) — size is (w, h) once the real file exists, so
# the box is reserved before metadata loads; None keeps the TODO placeholder.
TUTS = [
    ("tu-vid1", "Een tutorial toevoegen",
     "Zo voeg je in het beheer een nieuwe tutorial toe.", (1280, 794)),
    ("tu-vid2", "tut 1", "desc", None),
]


def tut_card(slug, title, desc, size):
    if size:
        w, h = size
        dims = ' width="%d" height="%d"' % (w, h)
        # webm first: VP9 holds screen-recording text sharper at the same size.
        sources = ('          <source src="video/%s.webm" type="video/webm">\n'
                   '          <source src="video/%s.mp4" type="video/mp4">\n' % (slug, slug))
    else:
        dims = ""
        sources = ('          <!-- TODO: echte videobestanden toevoegen -->\n'
                   '          <source src="video/%s.mp4" type="video/mp4">\n' % slug)
    return '''      <article class="tut-card">
        <video controls playsinline preload="none" poster="img/%s.jpg"%s>
%s          Je browser ondersteunt geen video.
        </video>
        <h3>%s</h3>
        <p>%s</p>
      </article>
''' % (slug, dims, sources, title, desc)


tut_cards = "".join(tut_card(*t) for t in TUTS)

# The tutorials are the one grid whose media must stay playable, so the cards
# keep their own controls and set their type UNDER the frame rather than into
# it — a scrim over a video with a play button on it is two controls arguing.
# Everything else is the chapter the other pages carry.
tutorials_head = statement(
    "diy-atelier.be — tutorials",
    "Tutorials",
    # NOT a baseline from 1.3 — the webshop's hero already carries the third of
    # the three ("NOT MADE TO BUY. MADE TO CREATE."), and two pages opening on
    # the same words is the one place a repeated baseline stops being a system
    # and starts being a copy-paste.
    #
    # Guidelines 5.4 gives this page its own line: the instruction card
    # "highlights dynamic title READY SETT GO! with step-by-step assembly and
    # care guidelines". A tutorial is the instruction card, in video. It is the
    # only line in the book written as an instruction to the reader rather than
    # a statement about the product, which is exactly the register a page of
    # step-by-steps opens in. (05.05 in the PDF; brand.css cites it already.)
    # spelled READY SET GO! for the same reason as the line on Realisaties
    [["READY", "SET", "GO!"]],
    "Van eerste laag tot finale verzegeling.",
    "Geen handleiding om door te worstelen: je ziet elke handeling gebeuren, op ware "
    "grootte en op jouw tempo. Kijk de lastige stap zo vaak terug als je wil.",
    # .spread-narrow, unlike the other four. At the full 940 the three words
    # land a third of a screen apart and the exclamation reads as three
    # unrelated ones; 05.05 sets this as a title, not as a justified line.
    "webshop.html", "Bekijk de pakketten", narrow=True)

tutorials = f'''{tutorials_head}
<section class="sett-dark" aria-labelledby="tutorials-h">
  <span class="sett-rail" aria-hidden="true">diy-atelier.be — tutorials</span>
  <div class="sett-dark-inner">
    <div class="sett-masthead">
      <div>
        <p class="sett-eyebrow">Videotutorials</p>
        <h2 class="sett-masthead-h" id="tutorials-h">Kijk het eerst,<br>doe het daarna.</h2>
      </div>
      <div>
        <p class="sett-masthead-lede">Elke video volgt één pakket van begin tot eind, in het
           tempo waarin je zelf werkt. Pauzeer, spoel terug, en kijk de lastige stap nog een
           keer.</p>
        <p class="sett-index"><span>Stap voor stap</span><span>Geen ervaring nodig</span></p>
      </div>
    </div>

    <div class="tut-grid sett-tuts">
{tut_cards}    </div>

    <p class="sett-dark-cta">
      <a class="sett-pill sett-pill-solid" href="webshop.html">Bekijk de pakketten {ARROW}</a>
      <a class="sett-pill" href="hoe-werkt-het.html">Hoe werkt het?</a>
    </p>
  </div>
</section>'''


def sync_chrome(filename, active, cart=False, brand=False):
    """Re-inject the header and footer into a hand-authored page.

    webshop.html and product.html own their bodies but share this chrome, so
    rather than generating them whole, the regions between the chrome markers
    are replaced in place. Anything outside the markers is left untouched.
    """
    path = OUT / filename
    html = path.read_text(encoding="utf-8")
    regions = {"header": header(active, cart=cart, brand=brand), "footer": FOOTER}
    for name, markup in regions.items():
        open_m, close_m = f"<!-- chrome:{name} -->", f"<!-- /chrome:{name} -->"
        i, j = html.find(open_m), html.find(close_m)
        if i == -1 or j == -1:
            raise SystemExit(f"{filename}: missing <!-- chrome:{name} --> markers")
        html = html[:i + len(open_m)] + "\n" + markup + "\n" + html[j:]
    path.write_text(html, encoding="utf-8")
    print(f"synced chrome in {filename}")


if __name__ == "__main__":
    page("index.html", "Atelier DIY — Jouw creativiteit, onze materialen",
         "index.html", overview,
         "Zelf unieke meubels en decorstukken maken met complete DIY-pakketten, "
         "hoogwaardige materialen en duidelijke tutorials.")
    page("hoe-werkt-het.html", "Hoe werkt het? — Atelier DIY",
         "hoe-werkt-het.html", hoewerkthet,
         "In vijf stappen van DIY-pakket naar afgewerkt designstuk.")
    page("realisaties.html", "Realisaties — Atelier DIY",
         "realisaties.html", realisaties,
         "Projecten en realisaties gemaakt met DIY-Atelier pakketten.")
    page("tutorials.html", "Tutorials — Atelier DIY",
         "tutorials.html", tutorials,
         "Stap-voor-stap videotutorials voor je DIY-project.")
    # the two brandbook pages
    sync_chrome("webshop.html", "webshop.html", cart=True, brand=True)
    sync_chrome("product.html", "webshop.html", cart=True, brand=True)
