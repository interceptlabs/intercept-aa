#!/usr/bin/env python3
"""Render /insights/chatb2b/ — the ChatB2B podcast hub. Sitemap round 2
(2026-08-08, "New Wire Frames 2") upgraded this from "to build" to a real
wireframe. All copy (episode titles/guests/dates/abstracts) is regex-extracted
verbatim from the source at render time — same low-risk-for-copy-fidelity
convention as render_legal.py/render_articles.py — rather than retyped.

Nav/footer/eyebrow/.ph/.btn/.link classes are the site's own shared ones from
common.py (NOT the wireframe's own competing definitions of those exact
classnames, which still carry the banned uppercase-tracked eyebrow look and a
mockup nav/footer) — this file's own CSS block only adds classnames common.py
doesn't already define.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import esc, head_html, header_html, footer_html, PatternCycler, client_logo_html

# maps a chatb2b guest-wall name to its key in common.py's CLIENT_LOGOS
# when the two spellings differ; anything absent here is looked up as-is,
# and client_logo_html() itself falls back to plain text for names with
# no sourced vector yet (Google, Veeam, Sophos, CGI, PathFactory, Moderne, Procom)
WALL_LOGO_KEY = {"BMC Software": "BMC"}

# real ChatB2B launch trailer (Andrew Au / Intercept's own YouTube upload) and the
# show's official cover art (Apple Podcasts artwork, id 1840415344, letterboxed
# from its native 1:1 into the hero's 16:9 slot — see assets/img/chatb2b/poster.webp).
# Sourced 2026-08-11; confirmed via web search the podcast/episode count (22) matches
# this build's own archive exactly.
TRAILER_URL = "https://www.youtube.com/watch?v=-D34JKW2oik"
POSTER_SRC = "assets/img/chatb2b/poster.webp"

SRC = "/Users/jontoewsinterceptgroup.com/Downloads/New Wire Frames 2/pages/chatb2b.html"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = """
.crumb{border-bottom:1px solid var(--line);background:var(--band)}
.crumb-row{max-width:var(--maxw);margin:0 auto;padding:11px 32px;font-size:var(--fs-8);color:var(--ink-3)}
.crumb-row b{color:var(--ink);font-weight:600}

.chero{padding:56px 0 40px;border-bottom:1px solid var(--line)}
.chero-grid{display:grid;grid-template-columns:1.15fr 1fr;gap:48px;align-items:center}
.chero h1{font-size:var(--fs-1);line-height:1.04;letter-spacing:-.03em;margin:0 0 16px}
.chero p:not(.eyebrow){font-size:var(--fs-5);line-height:1.5;color:var(--ink-2);margin:0 0 24px;max-width:52ch}
.plat-row{display:flex;flex-wrap:wrap;gap:10px}
.plat{font-size:var(--fs-7);font-weight:600;border:1px solid var(--ink);padding:9px 18px;border-radius:8px;color:var(--ink)}
.plat.solid{background:var(--ink);color:var(--page)}

.vid{position:relative}
.vid .ph{aspect-ratio:16/9;margin:0}
.vid .vplay{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:56px;height:56px;border-radius:999px;background:var(--ink);color:var(--page);display:flex;align-items:center;justify-content:center;font-size:18px;padding-left:3px}
.vid .vlabel{position:absolute;left:14px;bottom:14px;background:var(--ink);color:var(--page);font-weight:600;font-size:var(--fs-8);padding:6px 10px;border-radius:4px}

.latest{padding:52px 0;border-bottom:1px solid var(--line)}
.latest-grid{display:grid;grid-template-columns:340px 1fr;gap:40px;align-items:start}
.latest h2{font-size:var(--fs-2);line-height:1.1;letter-spacing:-.028em;margin:0 0 12px}
.latest .who{font-size:var(--fs-6);color:var(--ink-2);margin:0 0 14px}
.latest .abstract{font-size:var(--fs-6);line-height:1.6;color:var(--ink-2);margin:0 0 22px;max-width:62ch}

.feat{padding:52px 0;border-bottom:1px solid var(--line)}
.feat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:26px;margin-top:22px}
.fcard .ph{aspect-ratio:16/9;margin:0 0 14px}
.fcard .ep-date{font-size:var(--fs-8);color:var(--ink-3);display:block;margin:0 0 8px}
.fcard h3{font-size:var(--fs-4);line-height:1.26;letter-spacing:-.014em;margin:0 0 9px}
.fcard p:not(.eyebrow){font-size:var(--fs-7);line-height:1.5;color:var(--ink-2);margin:0}

.wall{padding:46px 0;background:var(--band);border-bottom:1px solid var(--line)}
.wall-grid{display:grid;grid-template-columns:repeat(8,1fr);gap:14px;margin-top:20px}
.wall .ph{aspect-ratio:5/2;font-size:10px}

.arch{padding:52px 0}
.arch h2{font-size:var(--fs-2);line-height:1.1;letter-spacing:-.028em;margin:0}
.ep{display:grid;grid-template-columns:128px 1fr auto;gap:22px;align-items:center;padding:20px 0;border-bottom:1px solid var(--line)}
/* load-bearing: the HTML hidden attribute is applied by the UA sheet at the
   lowest precedence, so any author rule that sets display, like .ep above,
   silently defeats it and every row renders (same bug class as the careers
   open-roles filter fix, round 10) — guarded explicitly here. */
.ep[hidden]{display:none}
.ep:first-of-type{border-top:1px solid var(--ink)}
.ep-art{aspect-ratio:16/9;font-size:10px}
.ep-date{font-size:var(--fs-8);color:var(--ink-3);display:block;margin:0 0 6px}
.ep-main h3{font-size:var(--fs-5);line-height:1.28;letter-spacing:-.012em;margin:0 0 6px}
.ep-main p:not(.eyebrow){font-size:var(--fs-7);line-height:1.45;color:var(--ink-2);margin:0}
.ep-links{display:flex;gap:8px}
.ep-links .plat{font-size:var(--fs-8);padding:7px 13px;font-weight:600}
.loadmore{display:flex;justify-content:center;padding:36px 0 0}

.sub{padding:56px 0;border-top:1px solid var(--line)}
.sub-grid{display:grid;grid-template-columns:1fr 1fr;gap:40px}
.sub h2{font-size:var(--fs-3);line-height:1.1;letter-spacing:-.026em;margin:0 0 12px}
.sub p:not(.eyebrow){font-size:var(--fs-6);line-height:1.55;color:var(--ink-2);margin:0 0 20px;max-width:44ch}

@media(max-width:1000px){.wall-grid{grid-template-columns:repeat(4,1fr)}}
@media(max-width:900px){
  .chero-grid,.latest-grid,.feat-grid,.sub-grid{grid-template-columns:1fr;gap:26px}
  .ep{grid-template-columns:96px 1fr;gap:16px}
  .ep-links{grid-column:1 / -1}
}
"""

LOADMORE_SCRIPT = """(function(){
  var rows = [].slice.call(document.querySelectorAll(".arch .ep"));
  var more = document.getElementById("more");
  if(!more) return;
  more.addEventListener("click", function(){
    rows.forEach(function(r){ r.hidden = false; });
    more.parentNode.style.display = "none";
  });
})();"""


def between(text, a, b):
    i = text.index(a) + len(a)
    j = text.index(b, i)
    return text[i:j]


def tag(pattern, text, group=1):
    m = re.search(pattern, text, re.S)
    if not m:
        raise ValueError(f"pattern not found: {pattern!r}")
    return m.group(group).strip()


def parse():
    html = open(SRC, encoding="utf-8").read()

    hero = between(html, "<!-- HERO + TRAILER PLAYER -->", "<!-- FEATURED EPISODE")
    hero_h1 = tag(r"<h1>(.*?)</h1>", hero)
    hero_p = tag(r"<h1>.*?</h1>\s*<p>(.*?)</p>", hero)
    hero_plats = tag(r'<div class="plat-row">(.*?)</div>', hero)
    hero_vlabel = tag(r'<span class="vlabel">(.*?)</span>', hero)

    featured = between(html, "<!-- FEATURED EPISODE", "<!-- THREE NEWEST -->")
    feat_date = tag(r'<span class="ep-date">(.*?)</span>', featured)
    feat_h2 = tag(r"<h2>(.*?)</h2>", featured)
    feat_who = tag(r'<p class="who">(.*?)</p>', featured)
    feat_abstract = tag(r'<p class="abstract">(.*?)</p>', featured)
    feat_plats = tag(r'<div class="plat-row">(.*?)</div>', featured)

    more_eps = between(html, "<!-- THREE NEWEST -->", "<!-- GUEST COMPANY WALL -->")
    fcards = re.findall(
        r'<div class="fcard">\s*<div class="ph">(.*?)</div>\s*<span class="ep-date">(.*?)</span>\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>\s*</div>',
        more_eps, re.S,
    )

    wall = between(html, "<!-- GUEST COMPANY WALL -->", "<!-- ARCHIVE -->")
    wall_logos = re.findall(r'<div class="ph">(.*?)</div>', wall)

    archive = between(html, "<!-- ARCHIVE -->", "<!-- SUBSCRIBE")
    eps = re.findall(
        r'<div class="ep"(\s+hidden)?>\s*<div class="ph ep-art">(.*?)</div>\s*'
        r'<div class="ep-main">\s*<span class="ep-date">(.*?)</span>\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>\s*</div>\s*'
        r'<div class="ep-links">(.*?)</div>\s*</div>',
        archive, re.S,
    )

    sub = between(html, "<!-- SUBSCRIBE", "<footer")
    sub_h2s = re.findall(r"<h2>(.*?)</h2>", sub)
    sub_ps = re.findall(r"<p>(.*?)</p>", sub)
    sub_plats = tag(r'<div class="plat-row">(.*?)</div>', sub)
    sub_btn = tag(r'<span class="btn">(.*?)</span>', sub)

    return dict(
        hero_h1=hero_h1, hero_p=hero_p, hero_plats=hero_plats, hero_vlabel=hero_vlabel,
        feat_date=feat_date, feat_h2=feat_h2, feat_who=feat_who, feat_abstract=feat_abstract, feat_plats=feat_plats,
        fcards=fcards, wall_logos=wall_logos, eps=eps,
        sub_h2s=sub_h2s, sub_ps=sub_ps, sub_plats=sub_plats, sub_btn=sub_btn,
    )


def render(data, base="../../"):
    pc = PatternCycler()
    def fcard_html(ph, date, h3, p):
        src, ratio = pc.next("3col", base)
        return f'<div class="fcard"><img class="ph" style="aspect-ratio:{ratio}" src="{src}" alt=""><span class="ep-date">{date}</span><h3>{h3}</h3><p>{p}</p></div>'
    fcards_html = "".join(fcard_html(*c) for c in data["fcards"])
    wall_html = "".join(
        f'<div class="ph">{client_logo_html(WALL_LOGO_KEY.get(name, name))}</div>'
        for name in data["wall_logos"]
    )
    def ep_html(hidden, art, date, h3, p, links):
        src, ratio = pc.next("4col", base)
        return (
            f'<div class="ep"{hidden}>'
            f'<img class="ph ep-art" style="aspect-ratio:{ratio}" src="{src}" alt="">'
            f'<div class="ep-main"><span class="ep-date">{date}</span><h3>{h3}</h3><p>{p}</p></div>'
            f'<div class="ep-links">{links}</div>'
            f"</div>"
        )
    eps_html = "".join(ep_html(*e) for e in data["eps"])
    feat_vid_src, feat_vid_ratio = pc.next("2col", base)

    return f"""<!doctype html>
<html lang="en">
<head>
{head_html("ChatB2B · Insights · Intercept", "Inspiration starts with a good conversation — the ChatB2B podcast.")}
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header_html(base)}
<div class="crumb"><div class="crumb-row">Insights &middot; <b>ChatB2B</b></div></div>
<main id="main">

<section class="chero">
  <div class="wrap">
    <div class="chero-grid">
      <div>
        <span class="eyebrow">ChatB2B</span>
        <h1>{data["hero_h1"]}</h1>
        <p>{data["hero_p"]}</p>
        <div class="plat-row">{data["hero_plats"]}</div>
      </div>
      <a class="vid" href="{TRAILER_URL}" target="_blank" rel="noopener" aria-label="Watch the ChatB2B trailer on YouTube">
        <img class="ph" style="aspect-ratio:16/9" src="{base}{POSTER_SRC}" alt="ChatB2B podcast cover art">
        <span class="vplay">&#9658;</span>
        <span class="vlabel">{data["hero_vlabel"]}</span>
      </a>
    </div>
  </div>
</section>

<section class="latest">
  <div class="wrap">
    <span class="eyebrow">Featured episode</span>
    <div class="latest-grid">
      <div class="vid">
        <img class="ph" style="aspect-ratio:{feat_vid_ratio}" src="{feat_vid_src}" alt="">
        <span class="vplay">&#9658;</span>
      </div>
      <div>
        <span class="ep-date">{data["feat_date"]}</span>
        <h2>{data["feat_h2"]}</h2>
        <p class="who">{data["feat_who"]}</p>
        <p class="abstract">{data["feat_abstract"]}</p>
        <div class="plat-row">{data["feat_plats"]}</div>
      </div>
    </div>
  </div>
</section>

<section class="feat">
  <div class="wrap">
    <span class="eyebrow">More episodes</span>
    <div class="feat-grid">{fcards_html}</div>
  </div>
</section>

<section class="wall">
  <div class="wrap">
    <span class="eyebrow">Featuring guests from</span>
    <div class="wall-grid">{wall_html}</div>
  </div>
</section>

<section class="arch">
  <div class="wrap">
    <h2>All episodes</h2>
    {eps_html}
    <div class="loadmore"><span class="btn" id="more">Load more episodes</span></div>
  </div>
</section>

<section class="sub">
  <div class="wrap">
    <div class="sub-grid">
      <div>
        <h2>{data["sub_h2s"][0]}</h2>
        <p>{data["sub_ps"][0]}</p>
        <div class="plat-row">{data["sub_plats"]}</div>
      </div>
      <div>
        <h2>{data["sub_h2s"][1]}</h2>
        <p>{data["sub_ps"][1]}</p>
        <span class="btn">{data["sub_btn"]}</span>
      </div>
    </div>
  </div>
</section>

</main>
{footer_html(base)}
<script>{LOADMORE_SCRIPT}</script>
</body>
</html>"""


def main():
    data = parse()
    out = render(data)
    outdir = os.path.join(ROOT, "insights", "chatb2b")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "index.html")
    open(path, "w", encoding="utf-8").write(out)
    print("Wrote", path)


if __name__ == "__main__":
    main()
