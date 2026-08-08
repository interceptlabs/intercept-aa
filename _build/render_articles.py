#!/usr/bin/env python3
"""Parse + render the 4 Signals from the Edge articles, reusing the source's own
inner markup verbatim for free-form blocks (copy/FAQ/about/related) rather than
re-deriving fields — lowest-risk path for copy fidelity on rich content."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import esc, head_html, header_html, footer_html

SRC_DIR = "/Users/jontoewsinterceptgroup.com/Downloads/New Wire Frames/pages/insights"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ARTICLES = [
    ("how-ai-is-reshaping-b2b-tech-marketing", "signals_how-ai-is-reshaping-b2b-tech-marketing.html"),
    ("seo-is-becoming-findability", "signals_seo-is-becoming-findability.html"),
    ("who-owns-your-marketing-alpha", "signals_who-owns-your-marketing-alpha.html"),
    ("why-2026-feels-heavier", "signals_why-2026-feels-heavier.html"),
]

def between(text, a, b):
    i = text.index(a) + len(a)
    j = text.index(b, i)
    return text[i:j]

CSS = """
.crumb{border-bottom:1px solid var(--line);background:var(--band)}
.crumb-row{max-width:var(--maxw);margin:0 auto;padding:11px 32px;font-size:var(--fs-8);color:var(--ink-3)}
.crumb-row b{color:var(--ink);font-weight:600}
.ahead{padding:52px 0 30px}
.ahead h1{font-size:var(--fs-1);line-height:1.04;letter-spacing:-.03em;margin:0 0 18px;max-width:17ch}
.deck{font-size:var(--fs-5);line-height:1.4;color:var(--ink-2);margin:0 0 30px;max-width:54ch}
.byline{display:flex;align-items:center;gap:14px;padding:20px 0;max-width:640px}
.byline .ph{width:44px;height:44px;padding:0;font-size:8px;border-radius:50%;flex:none}
.byline b{display:block;font-size:var(--fs-7);font-weight:700;letter-spacing:-.01em}
.byline .meta{display:block;margin-top:2px;font-size:var(--fs-8);color:var(--ink-3)}
.ahero .ph{aspect-ratio:21/9}
.body{padding:36px 0 20px}
.body-grid{display:grid;grid-template-columns:220px 1fr;gap:60px;align-items:start}
.toc{position:sticky;top:90px}
.toc a{display:block;font-size:var(--fs-8);line-height:1.4;color:var(--ink-2);text-decoration:none;padding:7px 0}
.copy{max-width:var(--readw)}
.copy h2{font-size:var(--fs-2);line-height:1.14;letter-spacing:-.024em;margin:40px 0 16px;font-weight:700;max-width:22ch}
.copy h2:first-child{margin-top:0}
.copy h3{font-size:var(--fs-4);line-height:1.3;margin:26px 0 10px;font-weight:700}
.copy p{font-size:var(--fs-6);line-height:1.62;color:var(--ink-2);margin:0 0 18px}
.qt{background:var(--band-tint,var(--band));padding:26px 28px;margin:0 0 12px}
.qt p{margin:0}
.pull{padding:26px 0;margin:32px 0}
.pull blockquote{margin:0;font-size:var(--fs-3);line-height:1.25;letter-spacing:-.018em;font-weight:700;max-width:24ch}
.takeaway{background:var(--band);padding:28px 30px;margin:32px 0 0}
.takeaway p{font-size:var(--fs-6);color:var(--ink);margin:0;font-weight:600}
.acta{padding:48px 0;background:var(--band);margin-top:48px}
.acta h2{font-size:var(--fs-2);line-height:1.1;letter-spacing:-.026em;margin:0 0 16px;max-width:18ch}
.acta p{font-size:var(--fs-6);color:var(--ink-2);margin:0 0 22px;max-width:52ch}
.faq{padding:48px 0}
.faq h2{font-size:var(--fs-2);margin:0 0 8px}
.acc{margin-top:18px;max-width:860px}
.acc-item{padding:16px 0}
.acc-item h3{font-size:var(--fs-5);font-weight:700;margin:0}
.acc-item p{font-size:var(--fs-7);line-height:1.55;color:var(--ink-2);margin:8px 0 0}
.faq-close{font-size:var(--fs-7);color:var(--ink-2);margin:22px 0 0}
.about{padding:44px 0;background:var(--band)}
.about-grid{display:grid;grid-template-columns:1fr 1fr;gap:56px}
.about b{display:block;font-size:var(--fs-6);font-weight:700;margin-bottom:8px}
.about p{font-size:var(--fs-7);line-height:1.55;color:var(--ink-2);margin:0 0 10px}
.about .who{display:flex;gap:14px;align-items:flex-start}
.about .who .ph{width:56px;height:56px;padding:0;font-size:7px;border-radius:50%;flex:none}
.rel{padding:48px 0 12px}
.rel-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:22px}
.rel .ph{aspect-ratio:16/9;margin-bottom:12px}
.rel-meta{display:block;margin-bottom:6px;font-size:var(--fs-8);color:var(--ink-3)}
.rel h3{font-size:var(--fs-4);line-height:1.24;margin:0;font-weight:700}
.convert{padding:52px 0;background:var(--band-tint,var(--band));margin-top:40px;text-align:center}
.convert h2{font-size:var(--fs-2);max-width:20ch;margin:0 auto 20px}
@media(max-width:1000px){.body-grid{grid-template-columns:1fr}.toc{position:static}}
@media(max-width:900px){.about-grid,.rel-grid{grid-template-columns:1fr}}
"""

def parse(fname):
    html = open(os.path.join(SRC_DIR, fname), encoding="utf-8").read()
    crumb = re.search(r'<div class="crumb-row">(.*?)</div>', html, re.S).group(1).strip()
    ahead = between(html, '<!-- ARTICLE HEADER -->', '<!-- BODY -->')
    eyebrow = re.search(r'<p class="eyebrow">(.*?)</p>', ahead, re.S).group(1)
    h1 = re.search(r"<h1>(.*?)</h1>", ahead, re.S).group(1)
    byline = re.search(r'<div class="byline">(.*?)</div>\s*</div>\s*</section>', ahead + "</section>", re.S)
    byline_html = re.search(r'(<div class="byline">.*?</div>\s*</div>)\s*<div class="share">', ahead, re.S)
    byline_inner = byline_html.group(1) if byline_html else ""
    toc = re.search(r'<nav class="toc">(.*?)</nav>', html, re.S).group(1)
    toc_links = re.findall(r'<a[^>]*>(.*?)</a>', toc)
    copy = between(html, '<div class="copy">', '</div>\n      </div>\n    </div>\n  </div>\n</section>')
    acta = between(html, '<!-- ARTICLE CTA -->', '<!-- FAQ -->')
    acta_inner = re.search(r'<div class="wrap">(.*?)</div>\s*</section>', acta, re.S)
    acta_html = acta_inner.group(1) if acta_inner else acta
    faq_acc = re.search(r'<div class="acc">(.*?)</div>\s*(?:<p class="faq-close">(.*?)</p>)?\s*</div>\s*</section>', html, re.S)
    faq_items = re.findall(r'<div class="acc-head"><h3>(.*?)</h3><i>.*?</i></div>\s*<div class="acc-body"><p>(.*?)</p></div>', html, re.S)
    faq_close = re.findall(r'<p class="faq-close"[^>]*>(.*?)</p>', html, re.S)
    about_block = between(html, '<!-- ABOUT THE SERIES + AUTHOR -->', '<!-- RELATED -->')
    about_grid = re.search(r'<div class="about-grid">(.*?)</div>\s*</div>\s*</section>', about_block, re.S).group(1)
    rel_block = between(html, '<!-- RELATED -->', '<footer')
    rel_cards = re.findall(r'<div><div class="ph">Visual · 16:9</div><span class="meta">(.*?)</span><h3>(.*?)</h3></div>', rel_block)

    return dict(crumb=crumb, eyebrow=eyebrow, h1=h1, byline_inner=byline_inner, toc_links=toc_links,
                copy=copy, acta_html=acta_html, faq_items=faq_items, faq_close=faq_close[-1] if faq_close else "",
                about_grid=about_grid, rel_cards=rel_cards)

def slugify_heading(h):
    text = re.sub(r"<[^>]+>", "", h).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text

REL_MAP = {
    "Signals from the Edge · Why 2026 feels heavier, and what the data says": "why-2026-feels-heavier",
    "Signals from the Edge · Who owns your marketing alpha?": "who-owns-your-marketing-alpha",
    "Signals from the Edge · SEO is not dead. It is becoming findability": "seo-is-becoming-findability",
}

def rel_href(meta, title):
    key = f"{meta} · {title}"
    slug = REL_MAP.get(key)
    if slug:
        return f"../{slug}/index.html"
    return "../index.html"

def render(slug, data, base="../../"):
    # inject id anchors into copy h2 so the TOC can jump to them
    copy = data["copy"]
    def add_id(m):
        inner = m.group(1)
        return f'<h2 id="{slugify_heading(inner)}">{inner}</h2>'
    copy = re.sub(r"<h2>(.*?)</h2>", add_id, copy)

    toc_html = "".join(f'<a href="#{slugify_heading(t)}">{t}</a>' for t in data["toc_links"] if slugify_heading(t))

    faq_html = "".join(
        f'<div class="acc-item"><h3>{q}</h3><p>{a}</p></div>' for q, a in data["faq_items"]
    )
    rel_html = "".join(
        f'<a class="card rel" href="{rel_href(meta, title)}"><div class="ph">Related</div>'
        f'<span class="rel-meta">{meta}</span><h3>{title}</h3></a>'
        for meta, title in data["rel_cards"]
    )

    return f"""<!doctype html>
<html lang="en">
<head>
{head_html(re.sub("<[^>]+>", "", data["h1"]) + " · Signals from the Edge · Intercept", re.sub("<[^>]+>", "", data["h1"]))}
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header_html(base)}
<div class="crumb"><div class="crumb-row">{data["crumb"]}</div></div>
<main id="main">

<section class="ahead">
  <div class="wrap">
    <p class="eyebrow">{data["eyebrow"]}</p>
    <h1>{data["h1"]}</h1>
    <div class="byline">{data["byline_inner"]}</div>
  </div>
</section>

<section class="ahero"><div class="wrap"><div class="ph">Article hero</div></div></section>

<section class="body">
  <div class="wrap">
    <div class="body-grid">
      <nav class="toc">{toc_html}</nav>
      <div class="copy">{copy}</div>
    </div>
  </div>
</section>

<section class="acta">
  <div class="wrap">{data["acta_html"]}</div>
</section>

<section class="faq">
  <div class="wrap">
    <h2>Frequently asked questions</h2>
    <div class="acc">{faq_html}</div>
    <p class="faq-close">{data["faq_close"]}</p>
  </div>
</section>

<section class="about">
  <div class="wrap"><div class="about-grid">{data["about_grid"]}</div></div>
</section>

<section class="rel">
  <div class="wrap">
    <h2 style="font-size:var(--fs-3);margin-bottom:0">Keep reading</h2>
    <div class="card-grid g3" style="margin-top:22px">{rel_html}</div>
  </div>
</section>

<section class="convert">
  <div class="wrap read">
    <span class="eyebrow">Start the conversation</span>
    <h2>Give us a hard problem. Let&rsquo;s solve it together.</h2>
    <a class="btn" href="{base}contact/index.html">Connect with an expert</a>
  </div>
</section>

</main>
{footer_html(base)}
</body>
</html>"""

def main():
    outdir = os.path.join(ROOT, "insights")
    for slug, fname in ARTICLES:
        data = parse(fname)
        out = render(slug, data)
        article_dir = os.path.join(outdir, slug)
        os.makedirs(article_dir, exist_ok=True)
        path = os.path.join(article_dir, "index.html")
        open(path, "w", encoding="utf-8").write(out)
        print("Wrote", path)

if __name__ == "__main__":
    main()
