# rpadvocaten.nl

Statische website voor rpadvocaten.nl, een onafhankelijke advocatengids per rechtsgebied.

## Opzet

Geen framework en geen dependencies. De site wordt gegenereerd door een Python-script dat alleen de standaardbibliotheek gebruikt. De gegenereerde HTML staat in `dist/` en is meegecommit, zodat Cloudflare Pages niets hoeft te bouwen.

```
build.py                 generator
check.py                 controle op kapotte links en ongewenste tekst
assets/style.css         stylesheet (geen externe fonts, geen scripts)
assets/favicon.svg       favicon
content/site.py          basis-URL
content/rg_1..3.py       de 18 rechtsgebieden
content/rechtsgebieden.py  bundelt en sorteert
content/nieuws.py        de nieuwsartikelen
content/paginas.py       losse pagina's (over, contact, kennisbank, legal)
dist/                    gegenereerde site, dit is wat live staat
```

## Bouwen

```
python3 build.py
python3 check.py
```

`build.py` gooit `dist/` leeg en bouwt opnieuw. Er is geen Node, npm of virtualenv nodig.

## Cloudflare Pages

Instellingen bij het koppelen van deze repo:

| Veld | Waarde |
| --- | --- |
| Framework preset | None |
| Build command | leeg laten |
| Build output directory | `dist` |
| Root directory | leeg laten |

Elke push naar `main` leidt tot een nieuwe deploy.

## Een nieuw artikel toevoegen

Voeg een blok toe aan `content/nieuws.py` met `slug`, `datum` (ISO), `titel`, `samenvatting`, `meta`, `rechtsgebieden` en `secties`. Draai daarna `python3 build.py` en commit `dist/`. De sitemap, de RSS-feed en het overzicht worden automatisch bijgewerkt.

## Uitgangspunten in de content

- Geen betaalde plaatsing. Alle uitgaande links naar advocatenkantoren zijn `rel="nofollow noopener"`.
- Geen cookies, geen analytics, geen externe fonts, geen contactformulier.
- Elke pagina met een uitgelicht kantoor toont de disclosure over niet-affiliatie.
