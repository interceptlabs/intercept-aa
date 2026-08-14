#!/usr/bin/env python3
"""Parse + render the 2 eBook detail pages (Intercept Cortex neuroscience report,
Watchtower AI-powered research report). Both wireframe sources share one identical
template — one shared render() function, called twice, parameterized by parsed data.

Copy is extracted verbatim (byte-exact) from the wireframe source HTML at render
time via regex, same convention as render_articles.py/render_legal.py — never
retyped. The big multi-module `.copy` block (intro paragraphs, numbered `.section`
blocks, `.exhibit`/`.ex-3col`/`.ex-2x2`/`.ex-flow` data modules, `.stat-callout`s,
`.emphasis`, the `.labs-callout` aside, and — ebook 1 only — the `.sources` block)
is lifted as ONE verbatim blob rather than re-derived field-by-field, since that is
the lowest-risk path for copy fidelity on rich, heavily-nested content. The only
surgery performed on that blob: (1) each inline image placeholder (`.fig-image`)
is re-wrapped into the site's shared `.ph` placeholder primitive instead of the
wireframe's own competing placeholder box style, with its label/sub-label text
carried over unchanged; (2) the wireframe's inert `<a class="inline">Intercept
Labs</a>` mentions are upgraded to a real href, since intercept-labs/index.html is
a real page in this build (same "upgrade an inert CTA once the destination is
real" convention as render_legal.py's cross-link cards).

ebook 2 has no `.sources` block and uses the `.ex-flow--4` 4-step modifier where
ebook 1's Exhibit 03 uses the plain 3-step `.ex-flow` — both are handled as
naturally optional: the verbatim blob simply does or doesn't contain them, and the
shared CSS defines the modifier unconditionally (harmless when unused).

Every "eyebrow"-role label in the wireframe (kicker, exhibit-label, takeaways-label,
labs-callout-eyebrow, ex-cell-tag, ex-2x2-role, toc-num, ex-flow-loop) had its
uppercase+letter-spaced+monospace CSS stripped — that visual pattern is the banned
H-12 "eyebrow" habit sitewide, regardless of which classname carries it. The
wireframe's own `--mono`/`--sans` font tokens and `--ink-4`/`--band-2` color tokens
don't exist in common.py's real design system (no mono token at all, and the site
deliberately collapsed to ONE flat --band tone, no second tier) — every rule below
maps onto the fixed fs-1..8/fs-data scale and the real --ink/--ink-2/--ink-3/--line/
--band/--page tokens only.
"""
import html as html_lib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import esc, head_html, header_html, footer_html, PatternCycler, author_avatar_html

SRC_DIR = "/Users/jontoewsinterceptgroup.com/Downloads/New Wire Frames 2/pages/insights"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EBOOKS = [
    ("hidden-neuroscience-behind-high-performing-ads", "ebook_hidden-neuroscience-behind-high-performing-ads.html"),
    ("next-era-of-ai-powered-research", "ebook_next-era-of-ai-powered-research.html"),
]

BASE = "../../../"  # insights/ebooks/<slug>/index.html is 3 dirs below site root

# Related-card titles resolved to real pages in THIS build: both ebooks link to
# each other, the 2 real Signals from the Edge articles they reference, and the
# Trends Brief detail page (built alongside these 2 ebooks in the same sitemap
# round, so it's real too by the time this runs).
REL_MAP = {
    "How AI is reshaping B2B tech marketing.": "insights/how-ai-is-reshaping-b2b-tech-marketing/index.html",
    "Who owns your marketing alpha?": "insights/who-owns-your-marketing-alpha/index.html",
    "The hidden neuroscience behind high-performing ads.": "insights/ebooks/hidden-neuroscience-behind-high-performing-ads/index.html",
    "When AI becomes an operating model.": "insights/trends-brief/when-ai-becomes-an-operating-model/index.html",
}

CSS = """
.crumb{border-bottom:1px solid var(--line);background:var(--band)}
.crumb-row{max-width:var(--maxw);margin:0 auto;padding:11px 32px;font-size:var(--fs-8);color:var(--ink-3)}
.crumb-row b{color:var(--ink);font-weight:600}

.kicker{font-size:var(--fs-8);font-weight:600;color:var(--ink-3);display:block}

.ahead{padding:52px 0 36px}
.ahead-text{max-width:820px}
.ahead .kicker{margin:0 0 20px}
.ahead h1{font-size:var(--fs-1);line-height:1.04;letter-spacing:-.032em;margin:0 0 22px;max-width:20ch}
.ahead h1 em{font-style:normal;color:var(--ink)}
.dek{margin:0 0 34px;font-size:var(--fs-5);line-height:1.5;color:var(--ink-2);max-width:60ch}

.byline{display:flex;align-items:center;gap:16px;margin:0 0 8px;padding:20px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);max-width:820px}
.byline .ph{width:48px;height:48px;padding:0;font-size:8px;border-radius:50%;flex:none}
.byline-meta{display:flex;flex-direction:column;gap:3px}
.byline-meta b{font-size:var(--fs-7);font-weight:700;color:var(--ink)}
.byline-meta .meta{font-size:var(--fs-8);color:var(--ink-3)}

.cover{padding:0 0 48px;border-bottom:1px solid var(--line)}
.cover .ph{aspect-ratio:2/1;flex-direction:column;gap:12px;padding:32px}
.cover .ph .ph-sub{opacity:.72;max-width:70ch}

.takeaways{padding:40px 0;border-bottom:1px solid var(--line)}
{max-width:var(--readw);margin:0 auto;padding:30px 34px;background:var(--band);}
.takeaways-label{margin:0 0 20px}
.takeaways ul{list-style:none;margin:0;padding:0}
.takeaways li{font-size:var(--fs-6);line-height:1.6;color:var(--ink-2);padding:16px 0 16px 26px;position:relative;border-bottom:1px solid var(--line)}
.takeaways li:first-child{padding-top:0}
.takeaways li:first-child::before{top:10px}
.takeaways li:last-child{padding-bottom:0;border-bottom:0}
.takeaways li::before{content:"";position:absolute;left:2px;top:26px;width:6px;height:6px;background:var(--ink);border-radius:50%}
.takeaways li b{color:var(--ink);font-weight:600}

.body{padding:52px 0 68px}
.body-grid{display:grid;grid-template-columns:220px 1fr;gap:56px;align-items:start}
.toc{position:sticky;top:96px;font-size:var(--fs-7);line-height:1.5;display:flex;flex-direction:column;gap:6px;border-left:1px solid var(--line);padding:4px 0 4px 16px}
.toc .eyebrow{margin:0 0 10px}
.toc a{display:flex;align-items:baseline;gap:10px;color:var(--ink-3);padding:3px 0;text-decoration:none;transition:color .15s ease}
.toc a:hover{color:var(--ink)}
.toc a.on{color:var(--ink);font-weight:600}
.toc-num{font-size:var(--fs-8);color:var(--ink-3);flex:0 0 auto;min-width:16px}
.toc-text{flex:1 1 auto;min-width:0}
.toc a.on .toc-num{color:var(--ink)}

.copy{max-width:var(--readw)}
.copy p{font-size:var(--fs-6);line-height:1.7;color:var(--ink-2);margin:0 0 18px}
.copy p b,.copy p strong{color:var(--ink);font-weight:600}
.copy h2{font-size:var(--fs-2);line-height:1.18;letter-spacing:-.022em;margin:0 0 18px;font-weight:700;color:var(--ink);scroll-margin-top:110px}
.copy h3{font-size:var(--fs-4);line-height:1.3;letter-spacing:-.012em;margin:22px 0 10px;font-weight:700;color:var(--ink)}
.copy .section{margin-top:52px}
.copy .section:first-child{margin-top:0}
.copy ul.plain{list-style:none;margin:0 0 18px;padding:0}
.copy ul.plain li{padding:10px 0 10px 24px;position:relative;font-size:var(--fs-6);line-height:1.6;color:var(--ink-2);border-bottom:1px solid var(--line)}
.copy ul.plain li:last-child{border-bottom:0}
.copy ul.plain li::before{content:"";position:absolute;left:2px;top:20px;width:6px;height:6px;background:var(--ink);border-radius:50%}
.copy ul.plain li b{color:var(--ink);font-weight:600}
.copy a.inline{color:var(--ink);text-decoration:underline;text-underline-offset:3px;text-decoration-thickness:1px}
.copy sup{line-height:0}

{margin:40px 0;background:var(--page);}
.fig .ph{aspect-ratio:16/9;flex-direction:column;gap:10px;padding:22px;border:0;border-bottom:1px solid var(--line)}
.fig .ph .ph-sub{opacity:.72;max-width:60ch}
.fig-caption{padding:14px 20px;font-size:var(--fs-7);color:var(--ink-2);line-height:1.55;display:flex;gap:14px;flex-wrap:wrap;align-items:baseline}
.fig-caption b{color:var(--ink);font-weight:700;font-size:var(--fs-8);flex:0 0 auto}
.fig-caption span{flex:1 1 auto;min-width:200px}

{margin:26px 0;padding:22px 26px;background:var(--band);display:flex;gap:22px;align-items:center;flex-wrap:wrap}
.stat-callout .stat-num{font-family:var(--font-display);font-size:var(--fs-data);font-weight:700;color:var(--ink);line-height:1;letter-spacing:-.03em;flex:0 0 auto}
.stat-callout .stat-meta{flex:1 1 240px}
.stat-callout .stat-lbl{font-size:var(--fs-7);line-height:1.5;color:var(--ink);margin:0 0 8px;font-weight:500}
.stat-callout cite{display:block;font-style:normal;font-size:var(--fs-8);color:var(--ink-3)}

{margin:34px 0;padding:30px 38px;background:var(--band);text-align:center}
.emphasis p{font-size:var(--fs-3);font-weight:600;line-height:1.35;letter-spacing:-.014em;color:var(--ink);margin:0 auto;max-width:44ch}

{margin:34px 0;padding:26px;background:var(--band);}
.exhibit-label{font-size:var(--fs-8);font-weight:600;color:var(--ink);margin:0 0 20px;display:flex;gap:8px;flex-wrap:wrap;align-items:baseline}
.exhibit-label .sep{color:var(--ink-3)}
.exhibit-label .name{color:var(--ink-3);font-weight:400}
.exhibit-caption{font-size:var(--fs-7);color:var(--ink-2);line-height:1.55;margin:18px 0 0;padding-top:16px;border-top:1px solid var(--line)}

.ex-3col{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
@media(max-width:680px){.ex-3col{grid-template-columns:1fr}}
{padding:18px 20px;background:var(--page);display:flex;flex-direction:column;gap:10px}
.ex-cell-label{font-size:var(--fs-6);font-weight:700;color:var(--ink);letter-spacing:-.012em;line-height:1.25;margin:0}
.ex-cell-tag{font-size:var(--fs-8);font-weight:600;color:var(--ink-3);margin:0}
.ex-cell ul{list-style:none;margin:6px 0 0;padding:0;display:flex;flex-direction:column;gap:6px}
.ex-cell li{font-size:var(--fs-7);line-height:1.5;color:var(--ink-2);padding-left:14px;position:relative}
.ex-cell li::before{content:"";position:absolute;left:1px;top:8px;width:4px;height:4px;background:var(--ink);border-radius:50%}

.ex-2x2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:600px){.ex-2x2{grid-template-columns:1fr}}
{padding:18px 20px;background:var(--page);}
.ex-2x2-role{font-size:var(--fs-8);font-weight:600;color:var(--ink);margin:0 0 10px}
.ex-2x2-cell p{font-size:var(--fs-7);line-height:1.55;color:var(--ink-2);margin:0}

.ex-flow{display:grid;grid-template-columns:1fr auto 1fr auto 1fr;gap:12px;align-items:stretch}
.ex-flow--4{grid-template-columns:1fr auto 1fr auto 1fr auto 1fr}
@media(max-width:820px){.ex-flow,.ex-flow--4{grid-template-columns:1fr;gap:12px}.ex-flow-arrow{display:none}}
{padding:18px 20px;background:var(--page);display:flex;flex-direction:column;gap:8px}
.ex-flow-num{font-weight:700;font-size:var(--fs-3);color:var(--ink);letter-spacing:-.02em;line-height:1}
.ex-flow-title{font-size:var(--fs-6);font-weight:700;color:var(--ink);letter-spacing:-.008em;line-height:1.28;margin:0}
.ex-flow-desc{font-size:var(--fs-7);line-height:1.55;color:var(--ink-2);margin:0}
.ex-flow-arrow{display:flex;align-items:center;justify-content:center;color:var(--ink-3);font-size:var(--fs-4);font-weight:700}
.ex-flow-loop{font-size:var(--fs-8);color:var(--ink-3);text-align:center;margin:16px 0 0}

{margin:60px 0 20px;padding:38px 42px;background:var(--band);scroll-margin-top:110px}
.labs-callout-eyebrow{font-size:var(--fs-8);font-weight:600;color:var(--ink-3);margin:0 0 14px;display:block}
.labs-callout h2{font-size:var(--fs-2);line-height:1.18;letter-spacing:-.022em;color:var(--ink);margin:0 0 16px}
.labs-callout p{font-size:var(--fs-6);line-height:1.6;color:var(--ink-2);margin:0 0 16px}
.labs-callout p b{color:var(--ink);font-weight:600}
.labs-callout a.inline{color:var(--ink);text-decoration:underline;text-underline-offset:3px;text-decoration-thickness:1px}
.labs-callout ul{list-style:none;margin:18px 0 0;padding:0;border-top:1px solid var(--line)}
.labs-callout ul li{padding:14px 0;border-bottom:1px solid var(--line);font-size:var(--fs-7);line-height:1.55;color:var(--ink-2);display:flex;gap:16px;flex-wrap:wrap;align-items:baseline}
.labs-callout ul li b{color:var(--ink);font-weight:700;flex:0 0 220px}
.labs-callout ul li span{flex:1 1 300px}
@media(max-width:640px){.labs-callout ul li{flex-direction:column;gap:4px}.labs-callout ul li b{flex-basis:auto}}

.sources{margin:44px 0 0;padding:22px 0 0;border-top:1px solid var(--line);font-size:var(--fs-8);line-height:1.7;color:var(--ink-3)}
.sources b{color:var(--ink);font-weight:700;margin-right:4px}
.sources a{color:var(--ink);text-decoration:underline;text-underline-offset:2px}

.convert{padding:72px 0 64px;border-top:1px solid var(--line);margin-top:80px;background:var(--band);text-align:center}
.convert .eyebrow{margin:0 0 14px}
.convert h2{font-size:var(--fs-2);line-height:1.15;letter-spacing:-.025em;margin:0 auto 18px;max-width:20ch}
.convert-lead{font-size:var(--fs-6);color:var(--ink-2);line-height:1.6;max-width:56ch;margin:0 auto 28px}

.related{padding:64px 0}
.related h2{font-size:var(--fs-3);letter-spacing:-.02em;margin:0 0 4px}
{padding:22px 24px;background:var(--band);display:flex;flex-direction:column;gap:12px;color:inherit;text-decoration:none;transition:border-color .18s ease,transform .18s ease}
.rel-card:hover{border-color:var(--ink);transform:translateY(-2px)}
.rel-card .kicker{color:var(--ink-3)}
.rel-card h3{font-size:var(--fs-4);line-height:1.28;letter-spacing:-.012em;color:var(--ink);font-weight:700;margin:0}
.rel-card p{font-size:var(--fs-7);line-height:1.55;color:var(--ink-2);margin:0}
.rel-card .meta{font-size:var(--fs-8);color:var(--ink-3);margin-top:auto}

@media(max-width:1000px){.body-grid{grid-template-columns:1fr}.toc{position:static}}
"""

# The wireframe's own TOC scroll-spy, with its rootMargin corrected — the
# source's "-30% 0px -60% 0px" leaves only a 10%-tall trigger band, the exact
# over-narrow-IntersectionObserver bug already found and fixed sitewide on
# the AI Policy page (render_legal.py) and again on the Trends Brief page
# (render_trends_brief.py) — ported the fix here too instead of reproducing
# the bug a third time.
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

FIG_IMAGE_RE = re.compile(
    r'<div class="fig-image">\s*<span class="fig-label">(.*?)</span>\s*<span class="fig-sub">(.*?)</span>\s*</div>',
    re.S,
)


def _phify_figs(copy_html, pc):
    """Re-wrap every inline `.fig-image` placeholder box into a real truchet-pattern
    image, carrying the label/sub-label text into alt text. This is the only
    structural surgery performed on the verbatim `.copy` blob."""
    def repl(m):
        label, sub = m.group(1), m.group(2)
        src, ratio = pc.next("3col", BASE)
        alt = re.sub(r"<[^>]+>", "", f"{label} — {sub}")
        return f'<img class="ph" style="aspect-ratio:{ratio}" src="{src}" alt="{esc(alt)}">'
    return FIG_IMAGE_RE.sub(repl, copy_html)


def parse(fname, pc):
    html = open(os.path.join(SRC_DIR, fname), encoding="utf-8").read()

    kicker = re.search(r'<p class="kicker">(.*?)</p>', html, re.S).group(1)
    h1 = re.search(r"<h1>(.*?)</h1>", html, re.S).group(1)
    dek = re.search(r'<p class="dek">(.*?)</p>', html, re.S).group(1)
    byline_name = re.search(r'<div class="byline-meta">\s*<b>(.*?)</b>\s*<span>(.*?)</span>', html, re.S)
    byline_b, byline_meta = byline_name.group(1), byline_name.group(2)

    cover_label = re.search(r'<span class="cover-image-label">(.*?)</span>', html, re.S).group(1)
    cover_sub = re.search(r'<span class="cover-image-sub">(.*?)</span>', html, re.S).group(1)

    takeaways_label = re.search(r'<span class="takeaways-label">(.*?)</span>', html, re.S).group(1)
    takeaways_ul = re.search(r'<span class="takeaways-label">.*?</span>\s*(<ul>.*?</ul>)', html, re.S).group(1)

    toc_inner = re.search(r'<nav class="toc"[^>]*>(.*?)</nav>', html, re.S).group(1)

    m = re.search(r'<div class="copy">(.*?)<!-- CONVERT CTA -->', html, re.S)
    copy_raw = re.sub(r"\s*</div>\s*</div>\s*</div>\s*</section>\s*$", "", m.group(1))
    copy_inner = _phify_figs(copy_raw, pc)
    # Upgrade the inert "Intercept Labs" mention to a real href — intercept-labs/
    # index.html is a real page in this build (render_labs.py).
    copy_inner = copy_inner.replace(
        '<a class="inline">Intercept Labs</a>',
        f'<a class="inline" href="{BASE}intercept-labs/index.html">Intercept Labs</a>',
    )

    convert_block = re.search(r"<!-- CONVERT CTA -->(.*?)<!-- RELATED INSIGHTS -->", html, re.S).group(1)
    convert_eyebrow = re.search(r'<p class="eyebrow">(.*?)</p>', convert_block, re.S).group(1)
    convert_h2 = re.search(r"<h2>(.*?)</h2>", convert_block, re.S).group(1)
    convert_lead = re.search(r'<p class="convert-lead">(.*?)</p>', convert_block, re.S).group(1)
    convert_btn = re.search(r'<a class="btn btn-primary">(.*?)</a>', convert_block, re.S).group(1)

    rel_cards = re.findall(
        r'<a class="rel-card">\s*<span class="kicker">(.*?)</span>\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>\s*<span class="meta">(.*?)</span>\s*</a>',
        html, re.S,
    )

    return dict(
        kicker=kicker, h1=h1, dek=dek, byline_b=byline_b, byline_meta=byline_meta,
        cover_label=cover_label, cover_sub=cover_sub,
        takeaways_label=takeaways_label, takeaways_ul=takeaways_ul,
        toc_inner=toc_inner, copy_inner=copy_inner,
        convert_eyebrow=convert_eyebrow, convert_h2=convert_h2,
        convert_lead=convert_lead, convert_btn=convert_btn,
        rel_cards=rel_cards,
    )


def rel_card_html(kicker, title, desc, meta):
    href = REL_MAP.get(title)
    if href:
        return (f'<a class="rel-card" href="{BASE}{href}">'
                f'<span class="kicker">{kicker}</span><h3>{title}</h3><p>{desc}</p>'
                f'<span class="meta">{meta}</span></a>')
    return (f'<div class="rel-card"><span class="kicker">{kicker}</span><h3>{title}</h3><p>{desc}</p>'
            f'<span class="meta">{meta}</span></div>')


def render(slug, data, pc):
    base = BASE
    plain_h1 = re.sub(r"<[^>]+>", "", data["h1"])
    plain_dek = html_lib.unescape(re.sub(r"<[^>]+>", "", data["dek"]))
    title = f"{plain_h1} · eBook · Intercept"

    rel_html = "".join(rel_card_html(*c) for c in data["rel_cards"])
    # Byline author photo: use the real sourced headshot when the byline
    # names a known team member (both ebooks credit Andrew Au) rather than
    # the generic pattern-fill this used to render as.
    byline_avatar_html = author_avatar_html(data["byline_b"], BASE)
    if not byline_avatar_html:
        src, ratio = pc.next("4col", BASE)
        byline_avatar_html = f'<img class="ph" style="aspect-ratio:{ratio}" src="{src}" alt="">'
    cover_src, cover_ratio = pc.next("2col", BASE)
    cover_alt = esc(re.sub(r"<[^>]+>", "", data["cover_label"]))

    return f"""<!doctype html>
<html lang="en">
<head>
{head_html(title, plain_dek)}
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header_html(base)}
<div class="crumb"><div class="crumb-row">Insights &middot; eBooks &middot; <b>{plain_h1}</b></div></div>
<main id="main">

<section class="ahead">
  <div class="wrap">
    <div class="ahead-text">
      <p class="kicker">{data["kicker"]}</p>
      <h1>{data["h1"]}</h1>
      <p class="dek">{data["dek"]}</p>
      <div class="byline">
        {byline_avatar_html}
        <div class="byline-meta">
          <b>{data["byline_b"]}</b>
          <span class="meta">{data["byline_meta"]}</span>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="cover">
  <div class="wrap">
    <img class="ph" style="aspect-ratio:{cover_ratio}" src="{cover_src}" alt="{cover_alt}">
  </div>
</section>

<section class="takeaways">
  <div class="wrap">
    <div class="takeaways-inner">
      <span class="eyebrow takeaways-label">{data["takeaways_label"]}</span>
      {data["takeaways_ul"]}
    </div>
  </div>
</section>

<section class="body">
  <div class="wrap">
    <div class="body-grid">
      <nav class="toc" aria-label="On this page">{data["toc_inner"]}</nav>
      <div class="copy">{data["copy_inner"]}</div>
    </div>
  </div>
</section>

<section class="convert">
  <div class="wrap">
    <p class="eyebrow">{data["convert_eyebrow"]}</p>
    <h2>{data["convert_h2"]}</h2>
    <p class="convert-lead">{data["convert_lead"]}</p>
    <a class="btn" href="{base}contact/index.html">{data["convert_btn"]}</a>
  </div>
</section>

<section class="related">
  <div class="wrap">
    <p class="eyebrow">Related Insights</p>
    <h2>Read next</h2>
    <div class="card-grid g3" style="margin-top:22px">{rel_html}</div>
  </div>
</section>

</main>
{footer_html(base)}
<script>{SCROLL_SPY_SCRIPT}</script>
</body>
</html>"""


def main():
    for slug, fname in EBOOKS:
        pc = PatternCycler()
        data = parse(fname, pc)
        out = render(slug, data, pc)
        outdir = os.path.join(ROOT, "insights", "ebooks", slug)
        os.makedirs(outdir, exist_ok=True)
        path = os.path.join(outdir, "index.html")
        open(path, "w", encoding="utf-8").write(out)
        print("Wrote", path)


if __name__ == "__main__":
    main()
