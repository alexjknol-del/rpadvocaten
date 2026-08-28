import os, re, sys, html
DIST="dist"
pages=[]
for r,d,f in os.walk(DIST):
    for n in f:
        if n.endswith(".html"): pages.append(os.path.join(r,n))
print("HTML-bestanden:", len(pages))

def exists(path):
    p=path.split("#")[0].split("?")[0]
    if p in ("/","" ): return os.path.isfile(os.path.join(DIST,"index.html"))
    t=os.path.join(DIST,p.strip("/"))
    return os.path.isfile(t) or os.path.isfile(os.path.join(t,"index.html"))

bad=[]; ext=set()
TAG=re.compile(r'<(?:a|link)[^>]*href="([^"]+)"')
for pg in pages:
    s=open(pg,encoding="utf-8").read()
    for href in TAG.findall(s):
        if href.startswith(("http://","https://")): ext.add(href)
        elif href.startswith("mailto:") or href.startswith("#"): pass
        elif href.startswith("/"):
            if not exists(href): bad.append((pg,href))
print("Kapotte interne links:", len(bad))
for b in bad[:20]: print("  ", b)
print("Unieke externe links:", len(ext))
open("_ext.txt","w").write("\n".join(sorted(ext)))

# tekstcontrole
BODY=re.compile(r"<body.*?</body>", re.S)
STRIP=re.compile(r"<script.*?</script>|<style.*?</style>|<[^>]+>", re.S)
PRON=re.compile(r"\b(je|jij|jou|jouw|jullie|uw|wij|onze|ons)\b", re.I)
UWORD=re.compile(r"(?<![\w-])u(?![\w-])")
EMDASH=re.compile(r"[—–]")
LOREM=re.compile(r"lorem|ipsum|TODO|TK\b|XXX|placeholder|voorbeeldtekst|\[.*?invullen.*?\]", re.I)
issues=0
for pg in pages:
    s=open(pg,encoding="utf-8").read()
    m=BODY.search(s)
    txt=html.unescape(STRIP.sub(" ", m.group(0) if m else s))
    for name,rx in (("pronoun",PRON),("u-los",UWORD),("emdash",EMDASH),("dummy",LOREM)):
        hits=rx.findall(txt)
        if hits:
            issues+=1
            ctx=[]
            for mm in rx.finditer(txt):
                ctx.append(txt[max(0,mm.start()-60):mm.end()+60].replace("\n"," "))
            print(f"[{name}] {pg}: {len(hits)}")
            for c in ctx[:3]: print("     ...", re.sub(r'\s+',' ',c))
print("Tekstissues:", issues)
