#!/usr/bin/env python3
"""Statische sitegenerator voor rpadvocaten.nl. Alleen standaardbibliotheek."""
import os, shutil, html, datetime, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
sys.path.insert(0, ROOT)

from content.site import SITE
from content.rechtsgebieden import RECHTSGEBIEDEN
from content.nieuws import NIEUWS
from content.paginas import PAGINAS

BASE = SITE["base"]

MENU = [
    ("/", "Home"),
    ("/rechtsgebieden/", "Rechtsgebieden"),
    ("/nieuws/", "Nieuws"),
    ("/kennisbank/", "Kennisbank"),
    ("/over/", "Over"),
    ("/contact/", "Contact"),
]

FOOTER_KENNIS = [
    ("/kennisbank/advocaat-kiezen/", "Een advocaat kiezen"),
    ("/kennisbank/kosten-en-tarieven/", "Kosten en tarieven"),
    ("/kennisbank/gesubsidieerde-rechtsbijstand/", "Gesubsidieerde rechtsbijstand"),
    ("/kennisbank/klacht-over-een-advocaat/", "Klacht over een advocaat"),
    ("/kennisbank/begrippenlijst/", "Juridische begrippenlijst"),
]

FOOTER_LEGAL = [
    ("/privacybeleid/", "Privacybeleid"),
    ("/cookiebeleid/", "Cookiebeleid"),
    ("/disclaimer/", "Disclaimer"),
    ("/toegankelijkheid/", "Toegankelijkheid"),
]

DISCLOSURE = (
    "RPAdvocaten.nl is een onafhankelijke gids en heeft geen samenwerking, "
    "eigendomsrelatie of andere binding met de genoemde advocatenkantoren. "
    "Opname is niet te koop en kantoren betalen niet voor vermelding. "
    "Alle links naar kantoren zijn nofollow."
)

def esc(s):
    return html.escape(s, quote=True)

def page(*, path, title, description, body, breadcrumbs=None, extra_head="", jsonld=None, active=None):
    """path: '/foo/' ; schrijft dist/foo/index.html"""
    url = BASE + path
    crumbs_html = ""
    if breadcrumbs:
        items = []
        for i, (href, label) in enumerate(breadcrumbs):
            if href:
                items.append(f'<li><a href="{esc(href)}">{esc(label)}</a></li>')
            else:
                items.append(f'<li aria-current="page">{esc(label)}</li>')
        crumbs_html = '<nav class="crumbs" aria-label="Kruimelpad"><ol>' + "".join(items) + "</ol></nav>"

    nav_parts = []
    for h, l in MENU:
        cls = ' class="is-active" aria-current="page"' if active == h else ""
        nav_parts.append('<li><a href="%s"%s>%s</a></li>' % (esc(h), cls, esc(l)))
    nav = "".join(nav_parts)

    jsonld_html = ""
    if jsonld:
        jsonld_html = '<script type="application/ld+json">' + jsonld + "</script>"

    out = f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(url)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="nl_NL">
<meta property="og:site_name" content="RPAdvocaten.nl">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(url)}">
<meta name="twitter:card" content="summary">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="theme-color" content="#14202e">
<link rel="stylesheet" href="/assets/style.css">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="Nieuws van RPAdvocaten.nl" href="/nieuws/rss.xml">
{extra_head}{jsonld_html}
</head>
<body>
<a class="skip" href="#main">Naar hoofdinhoud</a>
<header class="site-head">
  <div class="wrap head-inner">
    <a class="brand" href="/">
      <span class="brand-mark" aria-hidden="true">RP</span>
      <span class="brand-text"><strong>RPAdvocaten.nl</strong><span>Onafhankelijke advocatengids</span></span>
    </a>
    <input type="checkbox" id="navtoggle" class="navtoggle">
    <label for="navtoggle" class="navburger" aria-hidden="true"><span></span><span></span><span></span></label>
    <nav class="site-nav" aria-label="Hoofdmenu"><ul>{nav}</ul></nav>
  </div>
</header>
<main id="main">
{crumbs_html}
{body}
</main>
<footer class="site-foot">
  <div class="wrap foot-grid">
    <div class="foot-col foot-about">
      <span class="brand-mark" aria-hidden="true">RP</span>
      <p class="foot-lead">RPAdvocaten.nl brengt de Nederlandse advocatuur per rechtsgebied in kaart en licht per gebied een gespecialiseerd kantoor uit.</p>
      <p class="foot-note">{esc(DISCLOSURE)}</p>
    </div>
    <div class="foot-col">
      <h2>Navigatie</h2>
      <ul>{''.join(f'<li><a href="{esc(h)}">{esc(l)}</a></li>' for h, l in MENU)}</ul>
    </div>
    <div class="foot-col">
      <h2>Kennisbank</h2>
      <ul>{''.join(f'<li><a href="{esc(h)}">{esc(l)}</a></li>' for h, l in FOOTER_KENNIS)}</ul>
    </div>
    <div class="foot-col">
      <h2>Juridisch</h2>
      <ul>{''.join(f'<li><a href="{esc(h)}">{esc(l)}</a></li>' for h, l in FOOTER_LEGAL)}</ul>
      <p class="foot-mail"><a href="mailto:info@rpadvocaten.nl">info@rpadvocaten.nl</a></p>
    </div>
  </div>
  <div class="wrap foot-bottom">
    <p>&copy; {datetime.date.today().year} RPAdvocaten.nl</p>
    <p>Geen juridisch advies. Voor een concrete zaak is contact met een advocaat nodig.</p>
  </div>
</footer>
</body>
</html>
"""
    target_dir = os.path.join(DIST, path.strip("/"))
    os.makedirs(target_dir, exist_ok=True)
    with open(os.path.join(target_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(out)
    return path


def firm_card(k, gebied):
    waarom = "".join(f"<li>{p}</li>" for p in k["waarom"])
    return f"""<aside class="firm" aria-labelledby="uitgelicht">
  <p class="firm-eyebrow" id="uitgelicht">Uitgelicht kantoor voor {esc(gebied.lower())}</p>
  <h2 class="firm-name">{esc(k['naam'])}</h2>
  <p class="firm-meta">{esc(k['plaats'])}</p>
  <ul class="firm-why">{waarom}</ul>
  <p class="firm-link"><a class="btn" href="{esc(k['url'])}" rel="nofollow noopener" target="_blank">{esc(k['anchor'])}</a></p>
  <p class="firm-url">{esc(k['url'])}</p>
  <p class="firm-disclose">{esc(DISCLOSURE)}</p>
</aside>"""


def build():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(DIST, "assets"))

    urls = []

    # ---------- Home ----------
    top = [g for g in RECHTSGEBIEDEN]
    cards = "".join(
        f"""<li class="gcard"><a href="/rechtsgebieden/{esc(g['slug'])}/">
        <h3>{esc(g['titel'])}</h3>
        <p>{esc(g['kort'])}</p>
        <span class="gcard-firm">{esc(g['kantoor']['naam'])}</span></a></li>"""
        for g in top
    )
    latest = sorted(NIEUWS, key=lambda a: a["datum"], reverse=True)[:3]
    news_items = "".join(
        f"""<li><a href="/nieuws/{esc(a['slug'])}/"><time datetime="{esc(a['datum'])}">{esc(nl_date(a['datum']))}</time>
        <h3>{esc(a['titel'])}</h3><p>{esc(a['samenvatting'])}</p></a></li>"""
        for a in latest
    )
    home_body = f"""
<section class="hero">
  <div class="wrap hero-inner">
    <p class="eyebrow">Onafhankelijke advocatengids</p>
    <h1>De Nederlandse advocatuur, per rechtsgebied uitgesplitst</h1>
    <p class="lead">RPAdvocaten.nl beschrijft {len(RECHTSGEBIEDEN)} rechtsgebieden in gewone taal: welke regels gelden, welke termijnen lopen en welke rechter bevoegd is. Per rechtsgebied staat een gespecialiseerd Nederlands advocatenkantoor uitgelicht, met de onderbouwing erbij.</p>
    <p class="hero-actions"><a class="btn" href="/rechtsgebieden/">Bekijk alle rechtsgebieden</a> <a class="btn btn-ghost" href="/over/">Over dit platform</a></p>
    <p class="hero-note">{esc(DISCLOSURE)}</p>
  </div>
</section>

<section class="wrap section">
  <div class="section-head">
    <h2>Rechtsgebieden</h2>
    <p>Van adoptierecht tot belastingprocedures. Elke pagina behandelt de kern van het rechtsgebied en noemt een kantoor dat zich er aantoonbaar in heeft gespecialiseerd.</p>
  </div>
  <ul class="grid gcards">{cards}</ul>
</section>

<section class="band">
  <div class="wrap section">
    <div class="section-head">
      <h2>Hoe deze gids werkt</h2>
    </div>
    <ol class="steps">
      <li><h3>Selectie op specialisatie</h3><p>Per rechtsgebied wordt gezocht naar een kantoor met aantoonbare focus: lidmaatschap van een specialisatievereniging, registratie in het rechtsgebiedenregister van de Nederlandse orde van advocaten, gepubliceerde vakinhoud of een praktijk die zich tot dat gebied beperkt.</p></li>
      <li><h3>Onderbouwing zichtbaar</h3><p>Bij elk uitgelicht kantoor staat waarom het genoemd wordt. Die punten zijn afkomstig van de eigen website van het kantoor of uit openbare registers, en zijn na te lopen.</p></li>
      <li><h3>Geen betaalde plaatsing</h3><p>Vermelding is niet te koop. Er bestaat geen commerciele of andere band met de genoemde kantoren, en verzoeken tot opname tegen betaling worden niet gehonoreerd.</p></li>
    </ol>
  </div>
</section>

<section class="wrap section">
  <div class="section-head">
    <h2>Actuele thema-artikelen</h2>
    <p>Ontwikkelingen in wetgeving en rechtspraak, vertaald naar wat er in de praktijk verandert.</p>
  </div>
  <ul class="grid newslist">{news_items}</ul>
  <p class="more"><a href="/nieuws/">Alle artikelen</a></p>
</section>
"""
    org_ld = ('{"@context":"https://schema.org","@type":"WebSite","name":"RPAdvocaten.nl",'
              '"url":"' + BASE + '/","inLanguage":"nl-NL","description":"Onafhankelijke Nederlandse advocatengids per rechtsgebied."}')
    urls.append(page(path="/", title="RPAdvocaten.nl | Onafhankelijke advocatengids per rechtsgebied",
                     description=f"Onafhankelijke gids voor de Nederlandse advocatuur. {len(RECHTSGEBIEDEN)} rechtsgebieden uitgelegd, met per gebied een gespecialiseerd advocatenkantoor uitgelicht. Geen betaalde plaatsing.",
                     body=home_body, jsonld=org_ld, active="/"))

    # ---------- Rechtsgebieden overzicht ----------
    rows = "".join(
        f"""<li class="gcard"><a href="/rechtsgebieden/{esc(g['slug'])}/">
        <h3>{esc(g['titel'])}</h3><p>{esc(g['kort'])}</p>
        <span class="gcard-firm">{esc(g['kantoor']['naam'])}</span></a></li>"""
        for g in RECHTSGEBIEDEN
    )
    body = f"""
<section class="wrap page-head">
  <h1>Rechtsgebieden</h1>
  <p class="lead">{len(RECHTSGEBIEDEN)} rechtsgebieden binnen het Nederlandse recht, elk met de belangrijkste regels, termijnen en procedures. Per rechtsgebied staat een gespecialiseerd advocatenkantoor uitgelicht.</p>
  <p class="notice">{esc(DISCLOSURE)}</p>
</section>
<section class="wrap section"><ul class="grid gcards">{rows}</ul></section>
"""
    urls.append(page(path="/rechtsgebieden/", title="Rechtsgebieden | RPAdvocaten.nl",
                     description=f"Overzicht van {len(RECHTSGEBIEDEN)} rechtsgebieden binnen het Nederlandse recht, met per gebied een gespecialiseerd advocatenkantoor.",
                     body=body, breadcrumbs=[("/", "Home"), (None, "Rechtsgebieden")], active="/rechtsgebieden/"))

    # ---------- Rechtsgebied detail ----------
    by_slug = {g["slug"]: g for g in RECHTSGEBIEDEN}
    for g in RECHTSGEBIEDEN:
        secties = "".join(f'<h2 id="{slugify(k)}">{esc(k)}</h2>{v}' for k, v in g["secties"])
        faq = ""
        faq_ld = ""
        if g.get("faq"):
            items = "".join(
                f'<details><summary>{esc(q)}</summary><div>{a}</div></details>' for q, a in g["faq"]
            )
            faq = f'<section class="faq"><h2 id="veelgestelde-vragen">Veelgestelde vragen</h2>{items}</section>'
            entities = ",".join(
                '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
                % (jstr(q), jstr(strip_tags(a))) for q, a in g["faq"]
            )
            faq_ld = '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[' + entities + "]}"

        verwant = ""
        if g.get("verwant"):
            links = "".join(
                f'<li><a href="/rechtsgebieden/{esc(s)}/">{esc(by_slug[s]["titel"])}</a></li>'
                for s in g["verwant"] if s in by_slug
            )
            verwant = f'<section class="related"><h2>Verwante rechtsgebieden</h2><ul>{links}</ul></section>'

        toc_items = "".join(f'<li><a href="#{slugify(k)}">{esc(k)}</a></li>' for k, _ in g["secties"])
        if g.get("faq"):
            toc_items += '<li><a href="#veelgestelde-vragen">Veelgestelde vragen</a></li>'

        body = f"""
<section class="wrap page-head">
  <p class="eyebrow">Rechtsgebied</p>
  <h1>{esc(g['titel'])}</h1>
  <p class="lead">{g['intro']}</p>
</section>
<div class="wrap layout">
  <article class="prose">
    <nav class="toc" aria-label="Inhoud"><h2>Op deze pagina</h2><ul>{toc_items}</ul></nav>
    {secties}
    {faq}
    {verwant}
  </article>
  {firm_card(g['kantoor'], g['titel'])}
</div>
"""
        urls.append(page(path=f"/rechtsgebieden/{g['slug']}/",
                         title=f"{g['titel']} | RPAdvocaten.nl",
                         description=g["meta"],
                         body=body,
                         breadcrumbs=[("/", "Home"), ("/rechtsgebieden/", "Rechtsgebieden"), (None, g["titel"])],
                         jsonld=faq_ld or None,
                         active="/rechtsgebieden/"))

    # ---------- Nieuws ----------
    arts = sorted(NIEUWS, key=lambda a: a["datum"], reverse=True)
    items = "".join(
        f"""<li><a href="/nieuws/{esc(a['slug'])}/"><time datetime="{esc(a['datum'])}">{esc(nl_date(a['datum']))}</time>
        <h3>{esc(a['titel'])}</h3><p>{esc(a['samenvatting'])}</p></a></li>"""
        for a in arts
    )
    body = f"""
<section class="wrap page-head">
  <h1>Nieuws</h1>
  <p class="lead">Wetswijzigingen, nieuwe termijnen en ontwikkelingen in de rechtspraak, uitgelegd in gewone taal.</p>
</section>
<section class="wrap section"><ul class="grid newslist newslist-full">{items}</ul></section>
"""
    urls.append(page(path="/nieuws/", title="Nieuws en achtergrond | RPAdvocaten.nl",
                     description="Actuele thema-artikelen over Nederlands recht: wetswijzigingen, termijnen en ontwikkelingen in de rechtspraak.",
                     body=body, breadcrumbs=[("/", "Home"), (None, "Nieuws")], active="/nieuws/"))

    for a in arts:
        secties = "".join(f'<h2 id="{slugify(k)}">{esc(k)}</h2>{v}' for k, v in a["secties"])
        rel = ""
        if a.get("rechtsgebieden"):
            links = "".join(
                f'<li><a href="/rechtsgebieden/{esc(s)}/">{esc(by_slug[s]["titel"])}</a></li>'
                for s in a["rechtsgebieden"] if s in by_slug
            )
            rel = f'<section class="related"><h2>Meer over dit onderwerp</h2><ul>{links}</ul></section>'
        ld = ('{"@context":"https://schema.org","@type":"Article","headline":%s,"datePublished":"%s",'
              '"inLanguage":"nl-NL","author":{"@type":"Organization","name":"RPAdvocaten.nl"},'
              '"publisher":{"@type":"Organization","name":"RPAdvocaten.nl"},"mainEntityOfPage":"%s"}'
              % (jstr(a["titel"]), a["datum"], BASE + "/nieuws/" + a["slug"] + "/"))
        body = f"""
<section class="wrap page-head">
  <p class="eyebrow"><time datetime="{esc(a['datum'])}">{esc(nl_date(a['datum']))}</time></p>
  <h1>{esc(a['titel'])}</h1>
  <p class="lead">{esc(a['samenvatting'])}</p>
</section>
<div class="wrap layout layout-narrow">
  <article class="prose">
    {secties}
    {rel}
    <p class="art-foot">Dit artikel geeft algemene informatie en is geen juridisch advies. Regelgeving verandert; voor een concrete zaak is contact met een advocaat nodig.</p>
  </article>
</div>
"""
        urls.append(page(path=f"/nieuws/{a['slug']}/", title=f"{a['titel']} | RPAdvocaten.nl",
                         description=a["meta"], body=body,
                         breadcrumbs=[("/", "Home"), ("/nieuws/", "Nieuws"), (None, a["titel"])],
                         jsonld=ld, active="/nieuws/"))

    # ---------- Losse pagina's ----------
    for p in PAGINAS:
        secties = "".join(f'<h2 id="{slugify(k)}">{esc(k)}</h2>{v}' for k, v in p["secties"])
        body = f"""
<section class="wrap page-head">
  <h1>{esc(p['h1'])}</h1>
  <p class="lead">{p['lead']}</p>
</section>
<div class="wrap layout layout-narrow">
  <article class="prose">{secties}</article>
</div>
"""
        urls.append(page(path=p["path"], title=p["title"], description=p["meta"], body=body,
                         breadcrumbs=p.get("crumbs"), active=p.get("active")))

    # ---------- 404 ----------
    nf = """
<section class="wrap page-head">
  <h1>Pagina niet gevonden</h1>
  <p class="lead">Deze pagina bestaat niet of is verplaatst.</p>
  <p class="hero-actions"><a class="btn" href="/rechtsgebieden/">Naar de rechtsgebieden</a> <a class="btn btn-ghost" href="/">Naar de homepage</a></p>
</section>
"""
    with open(os.path.join(DIST, "404.html"), "w", encoding="utf-8") as f:
        tmp = page(path="/404-tmp/", title="Pagina niet gevonden | RPAdvocaten.nl",
                   description="De opgevraagde pagina bestaat niet.", body=nf)
        src = open(os.path.join(DIST, "404-tmp", "index.html"), encoding="utf-8").read()
        src = src.replace('<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">',
                          '<meta name="robots" content="noindex, follow">')
        src = src.replace('<link rel="canonical" href="' + BASE + '/404-tmp/">\n', "")
        src = src.replace('<meta property="og:url" content="' + BASE + '/404-tmp/">\n', "")
        f.write(src)
    shutil.rmtree(os.path.join(DIST, "404-tmp"))

    # ---------- sitemap / robots / rss ----------
    today = datetime.date.today().isoformat()
    entries = []
    for u in urls:
        prio = "1.0" if u == "/" else ("0.8" if u.startswith("/rechtsgebieden/") or u.startswith("/nieuws/") else "0.5")
        entries.append(f"  <url><loc>{BASE}{u}</loc><lastmod>{today}</lastmod><priority>{prio}</priority></url>")
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + "\n".join(entries) + "\n</urlset>\n")
    open(os.path.join(DIST, "sitemap.xml"), "w", encoding="utf-8").write(sitemap)

    robots = f"""User-agent: *
Allow: /

Sitemap: {BASE}/sitemap.xml
"""
    open(os.path.join(DIST, "robots.txt"), "w", encoding="utf-8").write(robots)

    rss_items = "".join(
        f"""  <item>
    <title>{esc(a['titel'])}</title>
    <link>{BASE}/nieuws/{a['slug']}/</link>
    <guid isPermaLink="true">{BASE}/nieuws/{a['slug']}/</guid>
    <pubDate>{rfc822(a['datum'])}</pubDate>
    <description>{esc(a['samenvatting'])}</description>
  </item>
""" for a in arts)
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
  <title>Nieuws van RPAdvocaten.nl</title>
  <link>{BASE}/nieuws/</link>
  <description>Actuele thema-artikelen over Nederlands recht.</description>
  <language>nl-nl</language>
{rss_items}</channel></rss>
"""
    os.makedirs(os.path.join(DIST, "nieuws"), exist_ok=True)
    open(os.path.join(DIST, "nieuws", "rss.xml"), "w", encoding="utf-8").write(rss)

    open(os.path.join(DIST, "_headers"), "w", encoding="utf-8").write(
        """/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
  Permissions-Policy: geolocation=(), microphone=(), camera=(), interest-cohort=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains

/assets/*
  Cache-Control: public, max-age=31536000, immutable
""")

    print(f"{len(urls)} pagina's gebouwd in dist/")


MONTHS = ["januari","februari","maart","april","mei","juni","juli","augustus","september","oktober","november","december"]

def nl_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {MONTHS[d.month-1]} {d.year}"

def rfc822(iso):
    d = datetime.datetime.fromisoformat(iso)
    return d.strftime("%a, %d %b %Y 09:00:00 +0100")

def slugify(s):
    s = s.lower()
    for a, b in [("á","a"),("é","e"),("ë","e"),("ï","i"),("ó","o"),("ö","o"),("ü","u"),("è","e")]:
        s = s.replace(a, b)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s

def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()

def jstr(s):
    import json
    return json.dumps(s, ensure_ascii=False)

if __name__ == "__main__":
    build()
