#!/usr/bin/env python3
"""Builds the static site for Javier Masonry Service into /home/claude/repo."""
import json
import os
from html import escape

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLOUD = "https://res.cloudinary.com/kat6qihq/image/upload"

PHONE_DISPLAY = "(713) 392-8790"
PHONE_TEL = "+17133928790"
EMAIL = "medinamasonryj92@gmail.com"
HOURS = "7:00 a.m. to 5:00 p.m."
ACCESS_KEY = "87251dcc-227d-4532-861b-80d49dae0b18"
BIZ = "Javier Masonry Service"

# key: (public_id, version, width, height, alt, caption)
IMG = {
    "kitchen_pool": ("625106623_2868687083340713_4481623718174795575_n", 1791225363, 2048, 1536,
                     "Brick outdoor kitchen with a built-in grill, granite counter, mini fridge and sink beside a pool",
                     "Brick outdoor kitchen with built-in grill"),
    "kitchen_stone": ("643744920_2892223990987022_2723584975699185659_n", 1791225327, 1168, 1665,
                      "Limestone outdoor kitchen with a built-in grill, access doors and a stone countertop",
                      "Limestone outdoor kitchen"),
    "fire_ext": ("641476610_2892223937653694_8005763880690789482_n", 1791225324, 640, 1370,
                 "Limestone fireplace with a stone hearth bench on a covered patio",
                 "Outdoor limestone fireplace"),
    "fire_int": ("642198413_2892223964320358_916010471467995791_n", 1791225325, 984, 1386,
                 "Floor-to-ceiling limestone fireplace with a stone hearth in a living room",
                 "Indoor stone fireplace"),
    "col_brick": ("643532774_2892223874320367_7782952036150035626_n", 1791225325, 928, 2040,
                  "Finished brick columns on a covered patio with travertine tile flooring",
                  "Brick columns on a covered patio"),
    "col_rebuild": ("641462504_2892223840987037_782814196364443252_n", 1791225324, 928, 2040,
                    "Brick column base going up around a patio post, with fresh brick stacked nearby",
                    "Brick column in progress"),
    "pillars_gate": ("641415291_2892223907653697_9035477214189813309_n", 1791225324, 1290, 1455,
                     "White limestone entrance pillars beside a wrought iron gate",
                     "Limestone entrance pillars"),
    "col_base": ("625883821_2868686860007402_3251370206943324485_n", 1791225364, 1080, 1440,
                 "Rough-cut white stone column base with a stone cap under a wood post",
                 "Stone column base"),
    "entry_brick": ("624887054_2868687256674029_3860236489511741282_n", 1791225363, 1536, 2048,
                    "Front entry with brick column bases and a herringbone brick porch floor",
                    "Brick entry columns and porch floor"),
    "planter_palm": ("504201184_2639248519617905_3158029721248197683_n", 1791225303, 2048, 1536,
                     "Round white stone planter around a palm tree with a long curved stone border behind it",
                     "Stone planter and curved border"),
    "planter_curve": ("503698840_2639248712951219_2088107925077471738_n", 1791225298, 2048, 1536,
                      "Curved white stone garden border along the side of a brick house",
                      "Curved stone garden border"),
    "planter_tan": ("503708734_2639249752951115_6651203705950350076_n", 1791225299, 2048, 1536,
                    "Low tan stone raised garden bed along a brick house with flowers and shrubs",
                    "Stone raised garden bed"),
    "planter_ring": ("655979651_2918834321659322_9208351963962860539_n", 1791225343, 2040, 942,
                     "Stone ring around a tree and a curved stone border in a front yard",
                     "Tree ring and garden border"),
    "planter_s": ("656836245_2918834431659311_5547661341941072905_n", 1791225344, 928, 2040,
                  "S-shaped stone garden border seen from above",
                  "S-shaped stone border"),
    "planter_magnolia": ("657247523_2918834368325984_6417163203079571899_n", 1791225343, 2040, 942,
                         "Curved stone planter wrapped around a magnolia tree beside a driveway",
                         "Stone planter around a magnolia"),
    "planter_limestone": ("658200918_2918834538325967_6688857298867304145_n", 1791225345, 1536, 2048,
                          "Curved limestone garden wall edging a flower bed beside a sidewalk",
                          "Curved limestone garden wall"),
}

SRC_WIDTHS = [400, 640, 960, 1280, 1600]


def url(key, w):
    pid, ver, ow, oh, _a, _c = IMG[key]
    w = min(w, ow)
    return f"{CLOUD}/f_auto,q_auto,c_limit,w_{w}/v{ver}/{pid}.jpg"


def img(key, sizes="100vw", pos=None, eager=False, cls=None):
    pid, ver, ow, oh, alt, _c = IMG[key]
    widths = [w for w in SRC_WIDTHS if w < ow] + [ow if ow <= SRC_WIDTHS[-1] else SRC_WIDTHS[-1]]
    widths = sorted(set(widths))
    srcset = ", ".join(f"{url(key, w)} {w}w" for w in widths)
    attrs = [
        f'src="{url(key, widths[-1] if widths[-1] < 960 else 960)}"',
        f'srcset="{srcset}"',
        f'sizes="{sizes}"',
        f'width="{ow}"', f'height="{oh}"',
        f'alt="{escape(alt)}"',
    ]
    if eager:
        attrs += ['fetchpriority="high"', 'decoding="async"']
    else:
        attrs += ['loading="lazy"', 'decoding="async"']
    if pos:
        attrs.append(f'style="object-position:{pos}"')
    if cls:
        attrs.append(f'class="{cls}"')
    return "<img " + " ".join(attrs) + ">"


NAV = [
    ("index.html", "Home"),
    ("outdoor-kitchens.html", "Outdoor Kitchens"),
    ("services.html", "Services"),
    ("gallery.html", "Gallery"),
    ("about.html", "About"),
    ("contact.html", "Contact"),
]

MARK = ('<svg viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="4" fill="#A53A2D"/>'
        '<path d="M0 10h40M0 20h40M0 30h40M20 0v10M10 10v10M30 10v10M20 20v10M10 30v10M30 30v10" '
        'stroke="#F7F5EF" stroke-width="2" fill="none"/></svg>')

CITIES = [
    ("katy-tx.html", "Katy", "Home base"),
    ("cypress-tx.html", "Cypress", "Brick and stone work"),
    ("tomball-tx.html", "Tomball", "Brick and stone work"),
    ("houston-tx.html", "Houston", "Brick and stone work"),
]


def head(title, desc, og_key="kitchen_pool", noindex=False, schema=None):
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    og = url(og_key, 1200)
    ld = ""
    if schema:
        ld = '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False) + "</script>\n"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
{robots}<meta property="og:type" content="website">
<meta property="og:site_name" content="{BIZ}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F7F5EF">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://res.cloudinary.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600;700&family=Zilla+Slab:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
{ld}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def header(current):
    links = "".join(
        f'<a href="{h}"' + (' aria-current="page"' if h == current else "") + f">{t}</a>"
        for h, t in NAV
    )
    return f"""<header class="site-header">
<div class="wrap header-in">
<a class="brand" href="index.html" aria-label="{BIZ}, home">{MARK}<span>{BIZ}<small>Brick and stone masonry, Katy, TX</small></span></a>
<nav class="nav" id="site-nav" aria-label="Main">{links}</nav>
<a class="btn btn-brick header-phone" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
</div>
</header>
<main id="main">
"""


def footer(quote_href):
    city_links = "".join(f'<li><a href="{h}">{c}, TX</a></li>' for h, c, _ in CITIES)
    return f"""</main>
<div class="bond" aria-hidden="true"></div>
<footer class="site-footer">
<div class="wrap footer-in">
<div>
<h3>{BIZ}</h3>
<p>Brick and stone masonry in Katy, Cypress, Tomball and Houston, TX.</p>
<p><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p>
<p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p>Hours: {HOURS}</p>
</div>
<div>
<h3>Services</h3>
<ul>
<li><a href="outdoor-kitchens.html">Outdoor kitchens</a></li>
<li><a href="services.html#fireplaces">Fireplaces</a></li>
<li><a href="services.html#columns-pillars">Columns, pillars and walls</a></li>
<li><a href="services.html#garden-beds">Garden beds and borders</a></li>
<li><a href="services.html#mailboxes">Mailboxes</a></li>
<li><a href="services.html#repairs">Brick repair</a></li>
</ul>
</div>
<div>
<h3>Areas served</h3>
<ul>{city_links}</ul>
</div>
</div>
<div class="wrap copyright">&copy; <span id="year">2026</span> {BIZ}. All rights reserved.</div>
</footer>
<div class="callbar">
<a class="btn btn-brick" href="tel:{PHONE_TEL}">Call now</a>
<a class="btn btn-outline" href="{quote_href}">Request a quote</a>
</div>
<script src="assets/js/main.js" defer></script>
</body>
</html>
"""


def quote_form(prefix):
    opts = [
        "Outdoor kitchen", "Fireplace", "Columns, pillars or walls",
        "Garden bed or border", "Mailbox", "Brick repair", "Something else",
    ]
    options = '<option value="" disabled selected>Choose one</option>' + "".join(
        f'<option>{o}</option>' for o in opts
    )
    return f"""<form class="quote-form" action="https://api.web3forms.com/submit" method="POST">
<input type="hidden" name="access_key" value="{ACCESS_KEY}">
<input type="hidden" name="subject" value="NEW QUOTE REQUEST">
<input type="hidden" name="from_name" value="{BIZ} Website">
<input type="hidden" name="source_page" value="">
<input type="checkbox" name="botcheck" style="display:none" tabindex="-1" autocomplete="off">
<div class="field"><label for="{prefix}-name">Your name</label><input id="{prefix}-name" name="name" type="text" autocomplete="name" required></div>
<div class="field"><label for="{prefix}-phone">Phone number</label><input id="{prefix}-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" required></div>
<div class="field"><label for="{prefix}-type">Type of work</label><select id="{prefix}-type" name="type_of_work" required>{options}</select></div>
<div class="field"><label for="{prefix}-msg">Project details <span class="opt">(optional)</span></label><textarea id="{prefix}-msg" name="message" placeholder="What would you like built or repaired, and where?"></textarea></div>
<button class="btn btn-brick" type="submit">Send my request</button>
<p class="form-status" role="status" aria-live="polite"></p>
<p class="form-alt">Prefer to talk? Call <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>.</p>
</form>"""


def quote_section(prefix="q", photo="kitchen_stone", pos="50% 40%", heading="Tell Javier about your project"):
    return f"""<section class="section alt" id="quote">
<div class="wrap quote-grid">
<div class="quote-photo">{img(photo, sizes="(max-width: 820px) 100vw, 560px", pos=pos)}</div>
<div class="quote-panel">
<h2>{heading}</h2>
<p class="sub">Leave your name, number and the type of work. Javier will get back to you.</p>
{quote_form(prefix)}
</div>
</div>
</section>
"""


def closing(quote_href):
    return f"""<section class="closing">
<div class="wrap closing-in">
<div>
<h2>Ready to talk about your project?</h2>
<p>Call Javier, or send your details and he will get back to you.</p>
</div>
<div>
<a class="big-phone" href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>
<a class="btn btn-brick" href="{quote_href}">Request a quote</a>
</div>
</div>
</section>
"""


def checks(items):
    return '<ul class="checks">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


ICON_MAILBOX = ('<svg class="ico" viewBox="0 0 44 44" fill="none" stroke="currentColor" stroke-width="2.2" '
                'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                '<path d="M12 38V18a8 8 0 0 1 16 0v20M8 38h24M20 24h6"/><path d="M28 12h10v8H28"/></svg>')
ICON_REPAIR = ('<svg class="ico" viewBox="0 0 44 44" fill="none" stroke="currentColor" stroke-width="2.2" '
               'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
               '<path d="M6 14h32M6 24h32M6 34h32M18 4v10M30 14v10M18 24v10"/></svg>')


def write(name, html):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(html)


def business_schema():
    return {
        "@context": "https://schema.org",
        "@type": "HomeAndConstructionBusiness",
        "name": BIZ,
        "description": "Brick and stone masonry: outdoor kitchens, fireplaces, columns, garden borders and brick repair.",
        "telephone": PHONE_TEL,
        "email": EMAIL,
        "image": url("kitchen_pool", 1200),
        "address": {"@type": "PostalAddress", "addressLocality": "Katy", "addressRegion": "TX", "addressCountry": "US"},
        "areaServed": [{"@type": "City", "name": c} for c in ("Katy", "Cypress", "Tomball", "Houston")],
    }


# ---------------------------------------------------------------- pages
def page_index():
    h = head(f"{BIZ} | Brick Mason in Katy, TX",
             "Outdoor kitchens, fireplaces, columns, garden borders and brick repair in Katy, Cypress, Tomball and Houston, TX. Call (713) 392-8790.",
             schema=business_schema())
    h += header("index.html")
    h += f"""<section class="hero">
<div class="wrap hero-grid">
<div>
<h1>Outdoor kitchens and stonework in Katy, TX</h1>
<p class="lead">{BIZ} builds outdoor kitchens, fireplaces, columns and garden borders in brick and stone, and repairs existing brickwork. Serving Katy, Cypress, Tomball and Houston.</p>
<div class="btn-row">
<a class="btn btn-brick" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
<a class="btn btn-outline" href="#quote">Request a quote</a>
</div>
<p class="hero-note">Hours: {HOURS}</p>
</div>
<div class="hero-media"><div class="frame">{img("kitchen_pool", sizes="(max-width: 820px) 100vw, 620px", eager=True)}</div></div>
</div>
</section>
<div class="strip">
<div class="wrap strip-grid">
<a href="outdoor-kitchens.html"><strong>Outdoor kitchens</strong><span>Stone or brick base, countertop, built-in grill and cabinets.</span></a>
<a href="services.html#fireplaces"><strong>Fireplaces</strong><span>Indoor and outdoor, in natural stone.</span></a>
<a href="services.html#columns-pillars"><strong>Columns and pillars</strong><span>Brick and limestone for patios, entries and gates.</span></a>
<a href="services.html#garden-beds"><strong>Garden beds and borders</strong><span>Raised planters, tree rings and curved edging.</span></a>
<a href="services.html#mailboxes"><strong>Mailboxes and repairs</strong><span>New brick mailboxes and repairs to existing brickwork.</span></a>
</div>
</div>
"""
    h += quote_section("q")
    h += f"""<section class="section">
<div class="wrap">
<div class="section-head"><h2>What Javier builds</h2><p>From a single mailbox to a full outdoor kitchen, all in brick and natural stone.</p></div>

<div class="feature">
<div class="feature-media media-landscape">{img("kitchen_stone", sizes="(max-width: 820px) 100vw, 560px", pos="50% 45%")}</div>
<div>
<h3>Outdoor kitchens, start to finish</h3>
<p>Javier builds the brick or stone structure, sets the countertop and installs the built-in grill and cabinet doors. You work with one builder instead of coordinating several crews.</p>
{checks(["Brick or limestone base built to your layout", "Countertop set and finished", "Built-in grill and cabinet doors installed"])}
<a class="text-link" href="outdoor-kitchens.html">See outdoor kitchens</a>
</div>
</div>

<div class="feature reverse">
<div class="feature-media media-duo">{img("fire_ext", sizes="(max-width: 820px) 50vw, 280px", pos="50% 30%")}{img("fire_int", sizes="(max-width: 820px) 50vw, 280px", pos="50% 35%")}</div>
<div>
<h3>Stone fireplaces, inside and out</h3>
<p>Natural stone fireplaces for the living room or the covered patio, finished with a stone hearth that can double as a bench.</p>
{checks(["Indoor and outdoor fireplaces", "Stone hearth and surround"])}
<a class="text-link" href="services.html#fireplaces">More about fireplaces</a>
</div>
</div>

<div class="feature">
<div class="feature-media media-duo">{img("col_brick", sizes="(max-width: 820px) 50vw, 280px", pos="50% 30%")}{img("pillars_gate", sizes="(max-width: 820px) 50vw, 280px", pos="50% 50%")}</div>
<div>
<h3>Columns, pillars and walls</h3>
<p>Brick or limestone columns for covered patios, entry pillars beside a gate, and brick bases for porch posts.</p>
{checks(["Patio and porch columns", "Entry pillars and garden walls"])}
<a class="text-link" href="services.html#columns-pillars">More about columns and pillars</a>
</div>
</div>

<div class="minor">
<div>
<h3>Garden beds, borders and tree rings</h3>
<p>Stone edging gives a front yard a clean, finished line. Javier builds raised planters, curved borders and rings around trees.</p>
</div>
<div>
<h3>Mailboxes and brick repair</h3>
<p>New brick mailboxes built to match your home, and repairs to cracked mortar and damaged brickwork.</p>
<a class="text-link" href="services.html#mailboxes">See all services</a>
</div>
</div>
<div class="trio">
{img("planter_palm", sizes="(max-width: 560px) 50vw, 360px")}
{img("planter_tan", sizes="(max-width: 560px) 50vw, 360px")}
{img("planter_curve", sizes="(max-width: 560px) 50vw, 360px")}
</div>
</div>
</section>

<section class="section white">
<div class="wrap">
<div class="section-head"><h2>Recent work</h2><p>A few projects from around the Katy area.</p></div>
<div class="teaser">
<a href="gallery.html">{img("kitchen_pool", sizes="(max-width: 820px) 50vw, 360px")}</a>
<a href="gallery.html">{img("planter_palm", sizes="(max-width: 820px) 50vw, 360px")}</a>
<a href="gallery.html">{img("fire_ext", sizes="(max-width: 820px) 50vw, 360px", pos="50% 30%")}</a>
<a href="gallery.html">{img("col_brick", sizes="(max-width: 820px) 50vw, 360px", pos="50% 30%")}</a>
<a href="gallery.html">{img("planter_limestone", sizes="(max-width: 820px) 50vw, 360px", pos="50% 55%")}</a>
<a href="gallery.html">{img("entry_brick", sizes="(max-width: 820px) 50vw, 360px", pos="50% 45%")}</a>
</div>
<div class="btn-row"><a class="btn btn-outline" href="gallery.html">See the full gallery</a></div>
</div>
</section>

<section class="section">
<div class="wrap">
<div class="section-head"><h2>Where Javier works</h2><p>Based in Katy, serving nearby communities.</p></div>
<div class="areas">
""" + "".join(f'<a href="{href}"><strong>{c}, TX</strong><span>{note}</span></a>' for href, c, note in CITIES) + """
</div>
</div>
</section>
"""
    h += closing("#quote")
    h += footer("#quote")
    write("index.html", h)


def page_kitchens():
    h = head("Outdoor Kitchens in Katy, TX | " + BIZ,
             "Brick and stone outdoor kitchens built start to finish in Katy, Cypress, Tomball and Houston. Call Javier at (713) 392-8790.",
             og_key="kitchen_pool")
    h += header("outdoor-kitchens.html")
    h += f"""<section class="page-head">
<div class="wrap">
<h1>Outdoor kitchens in Katy, TX</h1>
<p>A well-built outdoor kitchen turns the patio into the place where everyone gathers. Javier builds them in brick or natural stone, from the structure to the finishing details.</p>
<div class="btn-row"><a class="btn btn-brick" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a><a class="btn btn-outline" href="#quote">Request a quote</a></div>
</div>
</section>
<section class="section" style="padding-top:1rem">
<div class="wrap">
<div class="feature">
<div class="feature-media media-landscape">{img("kitchen_pool", sizes="(max-width: 820px) 100vw, 560px")}</div>
<div>
<h3>One builder, from the base to the countertop</h3>
<p>Javier handles the whole build, so there is one person to talk to from the first call to the finished kitchen.</p>
{checks(["Brick or limestone base in the layout that fits your patio", "Countertop set and finished", "Built-in grill and cabinet doors installed", "Space for a built-in fridge and storage"])}
</div>
</div>
<div class="feature reverse">
<div class="feature-media media-portrait">{img("kitchen_stone", sizes="(max-width: 820px) 100vw, 460px", pos="50% 40%")}</div>
<div>
<h3>Brick or natural stone</h3>
<p>The same kitchen looks very different in warm brick than in pale limestone. Javier works in both, so the kitchen can match your home and your patio.</p>
<p>Tell him what you have in mind and where, and he will talk through the options with you.</p>
</div>
</div>
</div>
</section>
<section class="section white">
<div class="wrap">
<div class="section-head"><h2>How a project goes</h2></div>
<ol class="steps">
<li><strong>Tell Javier about your space</strong><p>Call or send the form with your idea and where you live.</p></li>
<li><strong>Choose the layout and materials</strong><p>Decide on brick or stone and the look you want.</p></li>
<li><strong>Javier builds it</strong><p>Structure, countertop and built-in installation, handled by one builder.</p></li>
</ol>
</div>
</section>
"""
    h += quote_section("k", photo="kitchen_pool", pos="50% 50%", heading="Planning an outdoor kitchen?")
    h += closing("#quote")
    h += footer("#quote")
    write("outdoor-kitchens.html", h)


def page_services():
    h = head(f"Masonry Services in Katy, Cypress, Tomball and Houston | {BIZ}",
             "Outdoor kitchens, fireplaces, columns, pillars, garden borders, mailboxes and brick repair by Javier Masonry Service in the Katy, TX area.",
             og_key="planter_palm")
    h += header("services.html")
    h += f"""<section class="page-head">
<div class="wrap">
<h1>Brick and stone masonry services</h1>
<p>New builds and repairs for homes in Katy, Cypress, Tomball and Houston. Pick the job you have in mind, or call and describe it.</p>
</div>
</section>
<section class="section" style="padding-top:1rem">
<div class="wrap">

<div class="feature" id="outdoor-kitchens">
<div class="feature-media media-landscape">{img("kitchen_pool", sizes="(max-width: 820px) 100vw, 560px")}</div>
<div>
<h3>Outdoor kitchens</h3>
<p>The brick or stone structure, the countertop and the built-in grill and cabinet doors, all from one builder.</p>
<a class="text-link" href="outdoor-kitchens.html">See outdoor kitchens</a>
</div>
</div>

<div class="feature reverse" id="fireplaces">
<div class="feature-media media-duo">{img("fire_ext", sizes="(max-width: 820px) 50vw, 280px", pos="50% 30%")}{img("fire_int", sizes="(max-width: 820px) 50vw, 280px", pos="50% 35%")}</div>
<div>
<h3>Fireplaces</h3>
<p>Natural stone fireplaces for the living room or the covered patio, with a stone hearth and surround.</p>
</div>
</div>

<div class="feature" id="columns-pillars">
<div class="feature-media media-duo">{img("col_brick", sizes="(max-width: 820px) 50vw, 280px", pos="50% 30%")}{img("pillars_gate", sizes="(max-width: 820px) 50vw, 280px", pos="50% 50%")}</div>
<div>
<h3>Columns, pillars and walls</h3>
<p>Support columns for covered patios, entry pillars beside a gate, brick bases for porch posts and low garden walls, in brick or limestone.</p>
</div>
</div>

<div id="garden-beds" style="padding-top:1.5rem">
<h3>Garden beds, borders and tree rings</h3>
<p>Raised planters, curved borders and rings around trees, built in white or tan stone to frame the yard.</p>
<div class="trio">
{img("planter_ring", sizes="(max-width: 560px) 50vw, 360px")}
{img("planter_magnolia", sizes="(max-width: 560px) 50vw, 360px")}
{img("planter_limestone", sizes="(max-width: 560px) 50vw, 360px", pos="50% 55%")}
</div>
</div>

<div class="minor">
<div id="mailboxes">{ICON_MAILBOX}<h3>Mailboxes</h3><p>A new brick mailbox built to match your home, or a rebuild of one that has seen better days.</p></div>
<div id="repairs">{ICON_REPAIR}<h3>Brick repair</h3><p>Cracked mortar, loose or damaged bricks and worn walls. Javier repairs existing brickwork as well as building new.</p></div>
</div>
</div>
</section>
"""
    h += quote_section("s", photo="kitchen_stone")
    h += closing("#quote")
    h += footer("#quote")
    write("services.html", h)


GALLERY = [
    ("kitchen_pool", "kitchens"), ("planter_palm", "garden"), ("fire_ext", "fireplaces"),
    ("col_brick", "columns"), ("planter_limestone", "garden"), ("kitchen_stone", "kitchens"),
    ("entry_brick", "columns"), ("planter_curve", "garden"), ("pillars_gate", "columns"),
    ("fire_int", "fireplaces"), ("planter_ring", "garden"), ("col_base", "columns"),
    ("planter_tan", "garden"), ("planter_magnolia", "garden"), ("planter_s", "garden"),
    ("col_rebuild", "columns"),
]


def page_gallery():
    h = head(f"Project Gallery | {BIZ}",
             "Photos of outdoor kitchens, fireplaces, columns, pillars and stone garden borders built by Javier Masonry Service in the Katy, TX area.",
             og_key="planter_palm")
    h += header("gallery.html")
    figs = ""
    for key, cat in GALLERY:
        pid, ver, ow, oh, alt, cap = IMG[key]
        figs += (f'<figure data-cat="{cat}"><button type="button" data-large="{url(key, 1600)}" data-alt="{escape(alt)}" '
                 f'aria-label="Enlarge photo: {escape(cap)}">{img(key, sizes="(max-width: 560px) 100vw, (max-width: 980px) 50vw, 360px")}</button>'
                 f'<figcaption>{escape(cap)}</figcaption></figure>\n')
    h += f"""<section class="page-head">
<div class="wrap">
<h1>Project gallery</h1>
<p>Outdoor kitchens, fireplaces, columns and stone garden borders from around the Katy area. Tap a photo to enlarge it.</p>
</div>
</section>
<section class="section" style="padding-top:1rem">
<div class="wrap">
<div class="filters" role="group" aria-label="Filter photos">
<button type="button" data-filter="all" aria-pressed="true">All</button>
<button type="button" data-filter="kitchens" aria-pressed="false">Outdoor kitchens</button>
<button type="button" data-filter="fireplaces" aria-pressed="false">Fireplaces</button>
<button type="button" data-filter="columns" aria-pressed="false">Columns and pillars</button>
<button type="button" data-filter="garden" aria-pressed="false">Garden beds and borders</button>
</div>
<div class="masonry">
{figs}</div>
</div>
</section>
<div class="lightbox" role="dialog" aria-modal="true" aria-label="Photo viewer"><button class="lb-close" type="button">Close</button><div><img alt=""><p></p></div></div>
"""
    h += closing("contact.html#quote")
    h += footer("contact.html#quote")
    write("gallery.html", h)


def page_about():
    h = head(f"About {BIZ} | Brick Mason in Katy, TX",
             "Javier Masonry Service is a brick and stone masonry business based in Katy, TX, serving Cypress, Tomball and Houston.",
             og_key="entry_brick")
    h += header("about.html")
    h += f"""<section class="page-head">
<div class="wrap"><h1>About {BIZ}</h1></div>
</section>
<section class="section" style="padding-top:1rem">
<div class="wrap two-col">
<div>
<p>{BIZ} is a brick and stone masonry business based in Katy, Texas. Javier builds and repairs brickwork for homeowners in Katy, Cypress, Tomball and Houston.</p>
<p>The work ranges from small repairs and garden borders to full outdoor kitchens. On bigger jobs he handles the whole build, from the structure to the finishing details, so there is one person to talk to from start to finish.</p>
<p>If you are planning a project, call or send your details and Javier will get back to you.</p>
<div class="btn-row"><a class="btn btn-brick" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a><a class="btn btn-outline" href="contact.html#quote">Request a quote</a></div>
<h3 style="margin-top:2.2rem">What Javier builds</h3>
{checks(["Outdoor kitchens", "Stone fireplaces", "Columns, pillars and walls", "Garden beds, borders and tree rings", "Mailboxes and brick repair"])}
</div>
<div>{img("entry_brick", sizes="(max-width: 820px) 100vw, 440px", pos="50% 45%", cls="plain-img")}</div>
</div>
</section>
"""
    h += closing("contact.html#quote")
    h += footer("contact.html#quote")
    write("about.html", h)


def page_contact():
    h = head(f"Contact {BIZ} | Brick Mason in Katy, TX",
             "Call (713) 392-8790 or send your project details to Javier Masonry Service. Serving Katy, Cypress, Tomball and Houston, TX.",
             schema=business_schema())
    h += header("contact.html")
    h += f"""<section class="page-head">
<div class="wrap">
<h1>Contact Javier</h1>
<p>Call, email or send the form. Tell Javier what you want built or repaired, and where.</p>
</div>
</section>
<section class="section alt" id="quote" style="padding-top:2.4rem">
<div class="wrap two-col">
<div>
<ul class="contact-list">
<li><b>Phone</b><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
<li><b>Email</b><a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li><b>Hours</b>{HOURS}</li>
<li><b>Areas served</b>Katy, Cypress, Tomball and Houston, TX</li>
</ul>
</div>
<div class="quote-panel">
<h2>Request a quote</h2>
<p class="sub">Leave your name, number and the type of work. Javier will get back to you.</p>
{quote_form("c")}
</div>
</div>
</section>
"""
    h += footer("#quote")
    write("contact.html", h)


CITY_PAGES = {
    "katy-tx.html": dict(
        city="Katy",
        lead="Javier is based in Katy, so this is where he works most. If you want an outdoor kitchen, a fireplace, new columns or a brick repair, call and talk through your project.",
        body="Whether you are finishing a backyard or fixing a brick wall, the work is done in brick and natural stone. On larger jobs like outdoor kitchens, Javier handles the full build.",
        side="kitchen_pool",
        trio=[("fire_ext", "50% 30%"), ("col_brick", "50% 30%"), ("planter_limestone", "50% 55%")],
        og="kitchen_pool"),
    "cypress-tx.html": dict(
        city="Cypress",
        lead="Cypress homeowners can call Javier for outdoor kitchens, fireplaces, columns, garden beds and mailboxes, built in brick and natural stone.",
        body="Stone borders and tree rings are a quick way to give a front yard a finished look, and an outdoor kitchen makes the backyard worth using. Tell Javier what you have in mind.",
        side="planter_palm",
        trio=[("planter_ring", None), ("entry_brick", "50% 45%"), ("fire_int", "50% 35%")],
        og="planter_palm"),
    "tomball-tx.html": dict(
        city="Tomball",
        lead="Javier travels from Katy to Tomball for masonry projects of every size, from a single mailbox to a full outdoor kitchen.",
        body="Fireplaces, entry pillars, garden walls and brick repairs are all part of the work. Call or send your details and he will get back to you.",
        side="planter_tan",
        trio=[("pillars_gate", "50% 50%"), ("fire_ext", "50% 30%"), ("planter_magnolia", None)],
        og="planter_tan"),
    "houston-tx.html": dict(
        city="Houston",
        lead="Javier takes brick and stone projects across Houston, from new outdoor kitchens and fireplaces to garden borders and repairs.",
        body="Houston heat, humidity and heavy rain are hard on mortar and brick. If you have cracked mortar or damaged bricks, Javier can repair them, and he builds new work too.",
        side="planter_curve",
        trio=[("entry_brick", "50% 45%"), ("planter_s", "50% 40%"), ("col_base", "50% 45%")],
        og="planter_curve"),
}


def page_city(fname, d):
    city = d["city"]
    h = head(f"Brick Mason in {city}, TX | {BIZ}",
             f"Brick and stone mason serving {city}, TX: outdoor kitchens, fireplaces, columns, garden borders and brick repair. Call (713) 392-8790.",
             og_key=d["og"])
    h += header(fname)
    trio = "".join(img(k, sizes="(max-width: 560px) 50vw, 360px", pos=p) for k, p in d["trio"])
    side = img(d["side"], sizes="(max-width: 820px) 100vw, 480px")
    svc = checks([
        '<a href="outdoor-kitchens.html">Outdoor kitchens</a>',
        '<a href="services.html#fireplaces">Fireplaces</a>',
        '<a href="services.html#columns-pillars">Columns, pillars and walls</a>',
        '<a href="services.html#garden-beds">Garden beds and borders</a>',
        '<a href="services.html#mailboxes">Mailboxes</a>',
        '<a href="services.html#repairs">Brick repair</a>',
    ])
    h += f"""<section class="page-head">
<div class="wrap">
<h1>Brick and stone mason in {city}, TX</h1>
<p>{d["lead"]}</p>
<div class="btn-row"><a class="btn btn-brick" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a><a class="btn btn-outline" href="#quote">Request a quote</a></div>
</div>
</section>
<section class="section" style="padding-top:1rem">
<div class="wrap">
<div class="two-col">
<div>
<h2>Masonry services in {city}</h2>
<p>{d["body"]}</p>
{svc}
<p>Hours: {HOURS}</p>
</div>
<div class="feature-media media-landscape">{side}</div>
</div>
<div class="trio">{trio}</div>
</div>
</section>
"""
    h += quote_section("t", photo="kitchen_stone", heading=f"Request a quote in {city}")
    h += closing("#quote")
    h += footer("#quote")
    write(fname, h)


def page_thanks():
    h = head(f"Request sent | {BIZ}", "Thanks, your request was sent to Javier Masonry Service.", noindex=True)
    h += header("")
    h += f"""<section class="thanks">
<div class="wrap">
<h1>Thanks, your request was sent</h1>
<p>Javier will get back to you. If it is urgent, call <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>.</p>
<div class="btn-row"><a class="btn btn-brick" href="index.html">Back to home</a><a class="btn btn-outline" href="gallery.html">See the gallery</a></div>
</div>
</section>
"""
    h += footer("contact.html#quote")
    write("thanks.html", h)


def page_404():
    h = head(f"Page not found | {BIZ}", "That page could not be found.", noindex=True)
    h += header("")
    h += f"""<section class="thanks">
<div class="wrap">
<h1>We could not find that page</h1>
<p>The link may be old or mistyped. Go back to the home page or call <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>.</p>
<div class="btn-row"><a class="btn btn-brick" href="index.html">Back to home</a></div>
</div>
</section>
"""
    h += footer("contact.html#quote")
    write("404.html", h)


if __name__ == "__main__":
    page_index()
    page_kitchens()
    page_services()
    page_gallery()
    page_about()
    page_contact()
    for f, d in CITY_PAGES.items():
        page_city(f, d)
    page_thanks()
    page_404()
    print("OK")
