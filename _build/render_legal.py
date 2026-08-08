#!/usr/bin/env python3
"""Render the 3 legal pages (Terms of Service, Privacy Policy, AI Policy).

Legal copy is extracted verbatim (byte-exact, HTML-unescaped) from the wireframe
sources at render time — same convention as render_articles.py — rather than
re-typed into Python strings, to remove any risk of transcription drift on
real legal/policy text. Terms + Privacy are the flat .ahead + .body > .wrap.read
> .copy structure (no TOC). AI Policy is longer and keeps the wireframe's real
two-column .body-grid + sticky .toc + scroll-spy <script>, ported as-is.

All three pages end with a .more > .more-grid > a.mcard cross-link row to the
other two legal docs. The wireframe's mcards have no href (visual-only, same as
other inert CTAs on this site) — but since all three targets are real pages in
this build, these are upgraded to real hrefs, matching this site's established
convention of promoting a wireframe's visual-only CTA to a real link once its
destination actually exists.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import esc, head_html, header_html, footer_html

SRC_DIR = "/Users/jontoewsinterceptgroup.com/Downloads/New Wire Frames/pages/legal"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = """
.crumb{border-bottom:1px solid var(--line);background:var(--band)}
.crumb-row{max-width:var(--maxw);margin:0 auto;padding:11px 32px;font-size:var(--fs-8);color:var(--ink-3)}
.crumb-row b{color:var(--ink);font-weight:600}
.ahead{padding:52px 0 24px}
.ahead h1{font-size:var(--fs-1);line-height:1.05;letter-spacing:-.03em;margin:0;max-width:20ch}
.body{padding:24px 0 72px}
.body-grid{display:grid;grid-template-columns:220px 1fr;gap:60px;align-items:start}
.toc{position:sticky;top:90px;display:flex;flex-direction:column;gap:8px;border-left:1px solid var(--line);padding:4px 0 4px 16px}
.toc .eyebrow{margin:0 0 10px}
.toc a{display:block;font-size:var(--fs-8);line-height:1.4;color:var(--ink-3);text-decoration:none;padding:2px 0;transition:color .15s ease}
.toc a:hover{color:var(--ink)}
.toc a.on{color:var(--ink);font-weight:600}
.copy{max-width:var(--readw)}
.copy h2{font-size:var(--fs-2);line-height:1.18;letter-spacing:-.02em;margin:40px 0 14px;font-weight:700;color:var(--ink);scroll-margin-top:120px}
.copy h2:first-child{margin-top:0}
.copy h3{font-size:var(--fs-4);line-height:1.3;margin:26px 0 10px;font-weight:600;color:var(--ink)}
.copy p{font-size:var(--fs-6);line-height:1.65;color:var(--ink-2);margin:0 0 18px}
.copy ul,.copy ol{font-size:var(--fs-6);line-height:1.65;color:var(--ink-2);margin:0 0 18px;padding-left:22px}
.copy li{margin-bottom:8px}
.copy strong{color:var(--ink);font-weight:600}
.copy a{color:var(--ink);text-decoration:underline;text-underline-offset:3px;text-decoration-thickness:1px}
.more{border-top:1px solid var(--line);padding:56px 0 64px;background:var(--band)}
.more h2{font-size:var(--fs-2);letter-spacing:-.022em;margin:0 0 22px;font-weight:700}
.more-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.mcard{display:block;padding:24px 26px;background:var(--page);border:1px solid var(--line);transition:border-color .18s ease, transform .18s ease}
.mcard:hover{border-color:var(--ink);transform:translateY(-2px)}
.mcard b{display:block;font-size:var(--fs-4);font-weight:700;letter-spacing:-.014em;color:var(--ink);margin:0 0 8px}
.mcard p{margin:0 0 16px;font-size:var(--fs-7);line-height:1.5;color:var(--ink-2)}
@media(max-width:1000px){.body-grid{grid-template-columns:1fr;gap:32px}.toc{position:static;border-left:none;border-top:1px solid var(--line);padding:16px 0 0}}
@media(max-width:820px){.more-grid{grid-template-columns:1fr}}
"""

# The scroll-spy: ported verbatim (logic unchanged) from ai-policy.html's own
# <script> — a real interactive feature the wireframe implements, not a mockup.
SCROLL_SPY_SCRIPT = """(function(){
  var links=[].slice.call(document.querySelectorAll(".toc a"));
  var sections=links.map(function(a){var id=a.getAttribute("href").slice(1);return document.getElementById(id);}).filter(Boolean);
  if(!sections.length) return;
  function setActive(idx){links.forEach(function(a,i){a.classList.toggle("on",i===idx);});}
  var obs=new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(e.isIntersecting){
        var idx=sections.indexOf(e.target);
        if(idx>=0) setActive(idx);
      }
    });
  },{rootMargin:"0px 0px -70% 0px",threshold:0});
  sections.forEach(function(s){obs.observe(s);});
})();"""

LEGAL_META = {
    "terms": {"title": "Terms of Service", "slug": "terms", "blurb": "The terms governing your use of our website."},
    "privacy": {"title": "Privacy Policy", "slug": "privacy", "blurb": "How we handle your data."},
    "ai-policy": {"title": "AI Policy", "slug": "ai-policy", "blurb": "Our approach to AI in the work we do."},
}

# cross-link order per page, taken from each source's own .more-grid order
CROSS_LINKS = {
    "terms": ["privacy", "ai-policy"],
    "privacy": ["terms", "ai-policy"],
    "ai-policy": ["terms", "privacy"],
}

DESCRIPTIONS = {
    "terms": "The terms governing use of the Intercept website.",
    "privacy": "How Intercept collects, uses, and protects your information.",
    "ai-policy": "Intercept's policy on the responsible and transparent use of AI in client work.",
}


def read_src(fname):
    return open(os.path.join(SRC_DIR, fname), encoding="utf-8").read()


def extract(pattern, text, group=1):
    m = re.search(pattern, text, re.S)
    if not m:
        raise ValueError(f"pattern not found: {pattern!r}")
    return m.group(group)


def more_grid_html(page_key, base):
    cards = []
    for target_key in CROSS_LINKS[page_key]:
        meta = LEGAL_META[target_key]
        href = f"{base}{meta['slug']}/index.html"
        cards.append(
            f'<a class="mcard" href="{href}">'
            f'<b>{esc(meta["title"])}</b>'
            f'<p>{esc(meta["blurb"])}</p>'
            f'<span class="link">Read</span>'
            f"</a>"
        )
    return "".join(cards)


def flat_page(page_key, fname):
    """Terms of Service / Privacy Policy — .ahead + .body > .wrap.read > .copy, no TOC."""
    html = read_src(fname)
    eyebrow = extract(r'<p class="eyebrow">(.*?)</p>', html)
    h1 = extract(r"<h1>(.*?)</h1>", html)
    copy = extract(r'<div class="copy">(.*?)</div>\s*</div>\s*</section>', html)
    base = "../"
    meta = LEGAL_META[page_key]

    return f"""<!doctype html>
<html lang="en">
<head>
{head_html(f"{meta['title']} · Intercept", DESCRIPTIONS[page_key])}
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header_html(base)}
<div class="crumb"><div class="crumb-row">Legal &middot; <b>{esc(meta['title'])}</b></div></div>
<main id="main">

<section class="ahead">
  <div class="wrap read">
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1}</h1>
  </div>
</section>

<section class="body">
  <div class="wrap read">
    <div class="copy">{copy}</div>
  </div>
</section>

<section class="more">
  <div class="wrap">
    <h2>Other legal documents</h2>
    <div class="more-grid">{more_grid_html(page_key, base)}</div>
  </div>
</section>

</main>
{footer_html(base)}
</body>
</html>"""


def ai_policy_page(fname):
    """AI Policy — real two-column .body-grid + sticky .toc + scroll-spy script."""
    html = read_src(fname)
    eyebrow = extract(r'<p class="eyebrow">(.*?)</p>', html)
    h1 = extract(r"<h1>(.*?)</h1>", html)
    toc_inner = extract(r'<nav class="toc"[^>]*>(.*?)</nav>', html)
    copy = extract(r'<div class="copy">(.*?)</div>\s*</div>\s*</div>\s*</section>', html)
    base = "../"
    meta = LEGAL_META["ai-policy"]

    return f"""<!doctype html>
<html lang="en">
<head>
{head_html(f"{meta['title']} · Intercept", DESCRIPTIONS["ai-policy"])}
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header_html(base)}
<div class="crumb"><div class="crumb-row">Legal &middot; <b>{esc(meta['title'])}</b></div></div>
<main id="main">

<section class="ahead">
  <div class="wrap">
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1}</h1>
  </div>
</section>

<section class="body">
  <div class="wrap">
    <div class="body-grid">
      <nav class="toc" aria-label="On this page">{toc_inner}</nav>
      <div class="copy">{copy}</div>
    </div>
  </div>
</section>

<section class="more">
  <div class="wrap">
    <h2>Other legal documents</h2>
    <div class="more-grid">{more_grid_html("ai-policy", base)}</div>
  </div>
</section>

</main>
{footer_html(base)}
<script>{SCROLL_SPY_SCRIPT}</script>
</body>
</html>"""


def main():
    pages = [
        ("terms", flat_page("terms", "terms-of-service.html")),
        ("privacy", flat_page("privacy", "privacy-policy.html")),
        ("ai-policy", ai_policy_page("ai-policy.html")),
    ]
    for slug, out in pages:
        outdir = os.path.join(ROOT, slug)
        os.makedirs(outdir, exist_ok=True)
        path = os.path.join(outdir, "index.html")
        open(path, "w", encoding="utf-8").write(out)
        print("Wrote", path)


if __name__ == "__main__":
    main()
