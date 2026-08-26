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


def header(active, cart=False):
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
    return f'''<header class="site-header">
  <div class="wrap-wide">
    <a class="logo" href="index.html" aria-label="Atelier DIY — home">
      <img src="img/logo.png" alt="Atelier DIY" width="44" height="38">
    </a>
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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<a class="skip" href="#main">Ga naar inhoud</a>
{header(active)}
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


def masonry():
    cols = ""
    for col in GALLERY:
        tiles = "".join(
            f'<img src="img/{n}.jpg" alt="{ALTS[n]}" loading="lazy">' for n in col)
        cols += f'<div class="masonry-col">{tiles}</div>'
    return f'<div class="masonry">{cols}</div>'


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


def product_cards():
    out = ""
    for img, name, price, diff, lead, alt in PRODUCTS:
        specs = ""
        if diff:
            specs = (f'<div class="prod-specs">'
                     f'<span class="prod-spec">{GAUGE}{diff}</span>'
                     f'<span class="prod-spec">{CLOCK}{lead}</span></div>')
        out += f'''      <article class="prod-card">
        <div class="prod-media"><img src="img/{img}.jpg" alt="{alt}" loading="lazy"></div>
        <div class="prod-meta">
          <div><h3>{name}</h3><p class="prod-price">{price}</p></div>
          {specs}
        </div>
        <a class="btn-outline" href="webshop.html">Bekijk details {ARROW}</a>
      </article>
'''
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

overview = f'''<section class="hero" style="background-image:url('img/ov-hero.jpg')">
  <div class="wrap-wide">
    <h1>Jouw creativiteit, onze materialen DIY met topkwaliteit</h1>
    <p>Zelf unieke meubels en decorstukken maken? Bij DIY-Atelier helpen we je met
       hoogwaardige materialen en duidelijke tutorials. Van Mortex tafels tot andere
       stijlvolle creaties – ontdek hoe eenvoudig het is om zelf aan de slag te gaan!</p>
    <a class="btn" href="#hoe-werkt-het">Ontdek de eenvoud van DIY {ARROW}</a>
  </div>
</section>

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

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>Uitgelichte producten</h2>
      <div class="carousel-nav">
        <button type="button" aria-label="Vorige producten" disabled>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 5 8 12l7 7"/></svg>
        </button>
        <button type="button" aria-label="Volgende producten">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 5 7 7-7 7"/></svg>
        </button>
      </div>
    </div>
    <div class="prod-grid">
{product_cards()}    </div>
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
    {masonry()}
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
    out = ""
    for eyebrow, h, paras, img, alt, reverse in STEPS:
        body = "".join(f"<p>{p}</p>" for p in paras)
        cls = "split reverse" if reverse else "split"
        out += f'''<section class="section">
  <div class="wrap">
    <div class="{cls}">
      <div class="split-text">
        <p class="eyebrow">{eyebrow}</p>
        <h2>{h}</h2>
        {body}
      </div>
      <div class="split-media"><img src="img/{img}.jpg" alt="{alt}" loading="lazy"></div>
    </div>
  </div>
</section>

'''
    return out


hoewerkthet = f'''<section class="hero-band" style="background-image:url('img/hw-hero.jpg')">
  <h1>Hoe werkt het?</h1>
</section>

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

<section class="section-tight">
  <div class="wrap">
    <img src="img/hw-couple.jpg" alt="Twee makers werken samen aan een Mortex tafel"
         style="width:100%;border-radius:var(--radius)" loading="lazy">
  </div>
</section>

{steps()}<section class="section">
  <div class="wrap">
    <h2 class="center" style="margin-bottom:48px">Stap 5: genieten</h2>
    <img src="img/hw-stap5.jpg" alt="Koppel geniet van de zelfgemaakte Mortex salontafel"
         style="width:100%;border-radius:var(--radius)" loading="lazy">
  </div>
</section>'''


# ==========================================================================
# 3 — Realisaties
# ==========================================================================
realisaties = f'''<h1 class="sr-only">Realisaties</h1>
<section style="padding-block:24px 80px">
  <div class="wrap-bleed">
    {masonry()}
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
        dims = f' width="{w}" height="{h}"'
        # webm first: VP9 holds screen-recording text sharper at the same size.
        sources = f'''          <source src="video/{slug}.webm" type="video/webm">
          <source src="video/{slug}.mp4" type="video/mp4">
'''
    else:
        dims = ""
        sources = f'''          <!-- TODO: echte videobestanden toevoegen -->
          <source src="video/{slug}.mp4" type="video/mp4">
'''
    return f'''      <article class="tut-card">
        <video controls playsinline preload="none" poster="img/{slug}.jpg"{dims}>
{sources}          Je browser ondersteunt geen video.
        </video>
        <h3>{title}</h3>
        <p>{desc}</p>
      </article>
'''


tut_cards = "".join(tut_card(*t) for t in TUTS)

tutorials = f'''<h1 class="sr-only">Tutorials</h1>
<section class="section-tight">
  <div class="wrap">
    <h2 class="sr-only">Videotutorials</h2>
    <div class="tut-grid">
{tut_cards}    </div>
  </div>
</section>'''


def sync_chrome(filename, active, cart=False):
    """Re-inject the header and footer into a hand-authored page.

    webshop.html and product.html own their bodies but share this chrome, so
    rather than generating them whole, the regions between the chrome markers
    are replaced in place. Anything outside the markers is left untouched.
    """
    path = OUT / filename
    html = path.read_text(encoding="utf-8")
    regions = {"header": header(active, cart=cart), "footer": FOOTER}
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
    sync_chrome("webshop.html", "webshop.html", cart=True)
