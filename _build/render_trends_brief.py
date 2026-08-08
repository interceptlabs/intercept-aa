#!/usr/bin/env python3
"""Render /insights/trends-brief/<slug>/ — the Trends Brief report template.
Sitemap round 2 (2026-08-08) added the first real instance ("When AI Becomes
an Operating Model"); the /insights/trends-brief hub index itself is still
"to build", so this page stands alone for now, same as the eBooks.

Strategy: this report's body (ahead/takeaways/at-a-glance/body-copy/convert/
related) is one enormous, internally-consistent block of real, hyper-specific
copy (exact Watchtower percentages, named-executive quotes with attribution)
running ~550 lines of source HTML. Rather than deconstruct it into Python
data structures (high risk of dropping or mis-copying a stat/citation),
extract it as ONE verbatim blob between the breadcrumb and footer, and apply
only the handful of surgical patches actually needed: (1) give the 2 mid-CTA
buttons and the convert-CTA button real hrefs, they have none in the source
(visual-only, same as every other not-yet-wired CTA on this site); (2) give
the 3 related-insight cards real hrefs — all 3 titles match real, already-
built Signals from the Edge articles, resolved by exact title match; (3) swap
in a corrected TOC scroll-spy script (source's rootMargin creates only a 10%-
tall trigger band, the exact over-narrow-IntersectionObserver bug already
found and fixed sitewide on the AI Policy page in round 10 — port the fix,
don't reproduce the bug in a new page).
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import esc, head_html, header_html, footer_html

SRC = "/Users/jontoewsinterceptgroup.com/Downloads/New Wire Frames 2/pages/insights/trends_when-ai-becomes-an-operating-model.html"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Real hrefs for the 3 related cards, resolved by exact visible-title match
# against pages this build already ships (render_articles.py's 4 Signals
# articles) — same title->page resolution technique as render_articles.py's
# own REL_MAP.
RELATED_HREFS = {
    "SEO is not dead. It is becoming findability.": "seo-is-becoming-findability/index.html",
    "Why 2026 feels heavier, and what the data says.": "why-2026-feels-heavier/index.html",
    "Who owns your marketing alpha?": "who-owns-your-marketing-alpha/index.html",
}

CSS = """
.crumb{border-bottom:1px solid var(--line);background:var(--band)}
.crumb-row{max-width:var(--maxw);margin:0 auto;padding:12px 32px;font-size:var(--fs-8);color:var(--ink-3)}
.crumb-row b{color:var(--ink);font-weight:600}

.ahead{padding:64px 0 44px;border-bottom:1px solid var(--line)}
.ahead-grid{display:grid;grid-template-columns:1.3fr 1fr;gap:56px;align-items:center}
.ahead .kicker{font-size:var(--fs-8);font-weight:700;color:var(--ink);margin:0 0 20px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.ahead .kicker .powered{color:var(--ink-3);font-weight:400}
.ahead .kicker .powered b{color:var(--ink);font-weight:700}
.ahead h1{font-size:var(--fs-1);line-height:1.02;letter-spacing:-.035em;margin:0 0 28px;max-width:16ch;text-wrap:balance}
.epigraph{margin:0 0 32px;font-size:var(--fs-5);line-height:1.45;color:var(--ink-2);font-style:italic;max-width:52ch;font-weight:500}
.epigraph cite{display:block;font-size:var(--fs-8);color:var(--ink-3);font-style:normal;margin-top:12px}
.byline{display:flex;align-items:center;gap:18px;margin:0 0 28px;padding:22px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.byline-portrait{width:52px;height:52px;background:var(--band);border:1px solid var(--line);border-radius:50%;flex-shrink:0;display:flex;align-items:center;justify-content:center}
.byline-portrait span{font-size:9px;font-weight:700;color:var(--ink-3)}
.byline-meta{display:flex;flex-direction:column;gap:3px;flex:1;min-width:0}
.byline-meta b{font-size:var(--fs-7);font-weight:700;color:var(--ink)}
.byline-meta span{font-size:var(--fs-8);color:var(--ink-3)}
.byline-social{display:flex;gap:6px;flex-shrink:0}
.byline-social-btn{width:36px;height:36px;border:1px solid var(--line);background:var(--page);display:flex;align-items:center;justify-content:center;font-size:var(--fs-7);font-weight:500;color:var(--ink-3);text-decoration:none}
.byline-social-btn:hover{border-color:var(--ink);color:var(--ink)}
@media(max-width:560px){.byline-social{display:none}}

.hero-nums{padding:32px;border:1px solid var(--line);background:var(--band);position:relative}
.hero-nums::before{content:"";position:absolute;top:0;left:0;right:0;height:2px;background:var(--ink)}
.hero-nums-label{font-size:var(--fs-8);font-weight:700;color:var(--ink);margin:0 0 22px;display:flex;align-items:center;gap:10px}
.hero-nums-label::before{content:"";width:8px;height:8px;background:var(--ink)}
.hn{display:grid;grid-template-columns:minmax(64px,max-content) 1fr;gap:18px;align-items:start;padding-top:20px;border-top:1px solid var(--line)}
.hn:first-of-type{padding-top:0;border-top:0}
.hn-num{font-family:var(--font-display);font-size:32px;font-weight:700;color:var(--ink);line-height:1;letter-spacing:-.02em;margin:0}
.hn-label{font-size:var(--fs-7);line-height:1.55;color:var(--ink-2);margin:0}

.takeaways{padding:44px 0;border-bottom:1px solid var(--line)}
.takeaways-inner{max-width:var(--readw);margin:0 auto;padding:32px 36px;background:var(--band);border:1px solid var(--line)}
.takeaways-label{font-size:var(--fs-8);font-weight:700;color:var(--ink);margin:0 0 22px;display:block}
.takeaways ul{list-style:none;margin:0;padding:0}
.takeaways li{font-size:var(--fs-6);line-height:1.6;color:var(--ink-2);padding:16px 0 16px 26px;position:relative;border-bottom:1px solid var(--line)}
.takeaways li:first-child{padding-top:0}
.takeaways li:first-child::before{top:10px}
.takeaways li:last-child{padding-bottom:0;border-bottom:0}
.takeaways li::before{content:"";position:absolute;left:2px;top:26px;width:6px;height:6px;background:var(--ink);border-radius:50%}
.takeaways li b{color:var(--ink);font-weight:600}

.at-glance{padding:64px 0;background:var(--band);border-bottom:1px solid var(--line)}
.at-glance-head{margin-bottom:32px;max-width:var(--readw);margin-left:auto;margin-right:auto}
.at-glance .eyebrow{margin:0 0 12px}
.at-glance h2{font-size:var(--fs-3);letter-spacing:-.022em;margin:0 0 12px;color:var(--ink)}
.at-glance-lead{font-size:var(--fs-6);color:var(--ink-2);margin:0;line-height:1.55}
.pillar-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.pillar-mini{display:flex;flex-direction:column;gap:10px;padding:22px 24px;background:var(--page);border:1px solid var(--line);text-decoration:none;color:inherit}
.pillar-mini:hover{border-color:var(--ink)}
.pillar-mini.is-outlier{background:var(--halo-200);border-color:var(--ink)}
.pillar-mini-head{display:flex;justify-content:space-between;align-items:baseline;gap:12px}
.pillar-mini-num{font-size:var(--fs-8);color:var(--ink-3);font-weight:700}
.pillar-mini-score{font-family:var(--font-display);font-size:26px;font-weight:700;color:var(--ink);letter-spacing:-.03em;line-height:1}
.pillar-mini-name{font-size:var(--fs-6);font-weight:700;color:var(--ink);line-height:1.25;margin:2px 0 2px}
.pillar-mini-thesis{font-size:var(--fs-7);line-height:1.5;color:var(--ink-2);margin:0}
.pillar-mini-delta{font-size:var(--fs-8);color:var(--ink-3);margin-top:auto;padding-top:8px}
.pillar-mini.is-outlier .pillar-mini-delta{color:var(--ink);font-weight:700}
@media(max-width:900px){.pillar-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:560px){.pillar-grid{grid-template-columns:1fr}}

.body{padding:56px 0 72px}
.body-grid{display:grid;grid-template-columns:220px 1fr;gap:60px;align-items:start}
.toc{position:sticky;top:96px;font-size:var(--fs-7);line-height:1.5;display:flex;flex-direction:column;gap:6px;border-left:1px solid var(--line);padding:4px 0 4px 16px;max-height:calc(100vh - 120px);overflow-y:auto}
.toc .eyebrow{margin:0 0 12px}
.toc a{display:flex;align-items:baseline;gap:10px;color:var(--ink-3);padding:3px 0;text-decoration:none}
.toc a:hover{color:var(--ink)}
.toc a.on{color:var(--ink);font-weight:600}
.toc-num{font-size:var(--fs-8);color:var(--ink-3);flex:0 0 auto;min-width:16px}
.toc-text{flex:1 1 auto;min-width:0}
.toc a.on .toc-num{color:var(--ink)}
.toc-divider{border-top:1px solid var(--line);margin:8px 0}

.copy{max-width:var(--readw)}
.copy p{font-size:var(--fs-6);line-height:1.7;color:var(--ink-2);margin:0 0 18px}
.copy p b,.copy p strong{color:var(--ink);font-weight:600}
.copy h2{font-size:var(--fs-2);line-height:1.15;letter-spacing:-.025em;margin:0 0 22px;color:var(--ink);scroll-margin-top:100px}
.copy .section{margin-top:64px}
.copy .section:first-child{margin-top:0}

.chapter-opener{margin:72px 0 40px;padding:48px 40px;background:var(--band);border:1px solid var(--line)}
.chapter-opener:first-of-type{margin-top:0}
.chapter-opener-eyebrow{font-size:var(--fs-8);font-weight:700;color:var(--ink);margin:0 0 16px}
.chapter-opener-title{font-size:var(--fs-3);line-height:1.18;letter-spacing:-.024em;color:var(--ink);margin:0 0 14px}
.chapter-opener-thesis{font-size:var(--fs-7);line-height:1.6;color:var(--ink-2);margin:0;max-width:52ch}
.chapter-opener-range{font-size:var(--fs-8);color:var(--ink-3);margin-top:20px;display:inline-block;padding-top:14px;border-top:1px solid var(--line)}

.stat-callout{margin:28px 0;padding:24px 28px;background:var(--band);border:1px solid var(--line);display:flex;gap:24px;align-items:center;flex-wrap:wrap}
.stat-callout .stat-num{font-family:var(--font-display);font-size:clamp(36px,4.6vw,52px);font-weight:700;color:var(--ink);line-height:1;letter-spacing:-.03em;flex:0 0 auto}
.stat-callout .stat-meta{flex:1 1 240px}
.stat-callout .stat-lbl{font-size:var(--fs-6);line-height:1.5;color:var(--ink);margin:0 0 8px;font-weight:500}
.stat-callout cite{display:block;font-size:var(--fs-8);color:var(--ink-3)}

.pull-quote{margin:40px 0;padding:32px 36px;background:var(--band);border:1px solid var(--line)}
.pull-quote p{margin:0 0 16px;font-size:var(--fs-3);font-weight:500;line-height:1.35;letter-spacing:-.014em;color:var(--ink);font-style:italic}
.pull-quote cite{display:block;font-size:var(--fs-8);color:var(--ink-3)}
.pull-quote cite b{color:var(--ink);font-weight:700}

.viz{margin:28px 0;padding:22px 24px;background:var(--band);border:1px dashed var(--halo-400)}
.viz-eyebrow{font-size:var(--fs-8);color:var(--ink-3);margin:0 0 6px}
.viz-title{font-size:var(--fs-7);font-weight:600;color:var(--ink);margin:0 0 12px}
.viz-body{font-size:var(--fs-8);color:var(--ink-3);padding:22px;text-align:center;background:var(--page);border:1px solid var(--line);line-height:1.6}
.viz-note{font-size:var(--fs-7);color:var(--ink-2);line-height:1.5;margin:12px 0 0}

.radar{margin:28px 0;padding:28px;background:var(--band);border:1px solid var(--line)}
.radar-legend{padding:14px 18px;background:var(--page);border:1px solid var(--line);margin-bottom:22px;font-size:var(--fs-7);line-height:1.5;color:var(--ink-2)}
.radar-legend b{color:var(--ink);font-weight:600}
.radar-viz{min-height:260px;background:var(--page);border:1px solid var(--line);display:flex;align-items:center;justify-content:center;text-align:center;padding:24px;font-size:var(--fs-8);color:var(--ink-3);line-height:1.7}

.pillar{margin-top:64px;scroll-margin-top:100px}
.pillar-head{display:grid;grid-template-columns:auto 1fr auto;gap:20px;align-items:end;padding-bottom:18px;margin-bottom:22px;border-bottom:1px solid var(--line)}
.pillar-num-lg{font-family:var(--font-display);font-weight:700;font-size:40px;color:var(--ink);line-height:1;letter-spacing:-.03em}
.pillar-meta{display:flex;flex-direction:column;gap:6px}
.pillar-eyebrow{font-size:var(--fs-8);color:var(--ink-3)}
.pillar-title{font-size:var(--fs-3);font-weight:700;line-height:1.22;letter-spacing:-.02em;color:var(--ink);margin:0}
.pillar-score-block{text-align:right;display:flex;flex-direction:column;gap:4px;align-items:flex-end}
.pillar-score{font-family:var(--font-display);font-weight:700;font-size:32px;color:var(--ink);line-height:1;letter-spacing:-.03em}
.pillar-score-meta{font-size:var(--fs-8);color:var(--ink-3)}
.pillar-score-delta{font-size:var(--fs-7);font-weight:500;color:var(--ink-2)}
.pillar.is-outlier .outlier-banner{display:inline-flex;align-items:center;gap:10px;font-size:var(--fs-8);font-weight:700;background:var(--ink);color:var(--page);padding:6px 14px;margin:0 0 18px}

.pillar-summary{margin:0 0 28px;padding:22px 26px;background:var(--band);border:1px solid var(--line);display:grid;grid-template-columns:1fr;gap:8px}
.pillar-summary-thesis{font-size:var(--fs-6);line-height:1.55;color:var(--ink);font-weight:500;margin:0}
.pillar-summary-eyebrow{font-size:var(--fs-8);color:var(--ink-3);margin:0}

.si-pair{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:24px 0}
@media(max-width:680px){.si-pair{grid-template-columns:1fr}}
.si-pair>div{background:var(--band);padding:20px;border:1px solid var(--line)}
.si-pair h4{font-size:var(--fs-8);font-weight:700;color:var(--ink);margin:0 0 10px}
.si-pair p{font-size:var(--fs-7);line-height:1.55;color:var(--ink-2);margin:0}

.mid-cta{margin:56px 0;padding:32px 36px;background:var(--band);border:1px solid var(--line);display:flex;gap:24px;align-items:center;justify-content:space-between;flex-wrap:wrap}
.mid-cta-body{flex:1 1 400px}
.mid-cta .mid-cta-eyebrow{font-size:var(--fs-8);color:var(--ink-3);margin:0 0 8px}
.mid-cta h3{font-size:var(--fs-4);font-weight:700;line-height:1.22;letter-spacing:-.014em;color:var(--ink);margin:0 0 10px}
.mid-cta p{font-size:var(--fs-7);line-height:1.55;color:var(--ink-2);margin:0;max-width:46ch}

.deep-dives{margin-top:64px;scroll-margin-top:100px}
.dd-accordion{margin-top:24px;border-top:1px solid var(--line)}
.dd-item{border-bottom:1px solid var(--line)}
.dd-summary{display:flex;justify-content:space-between;align-items:flex-start;gap:20px;padding:20px 0;cursor:pointer;list-style:none;user-select:none}
.dd-summary::-webkit-details-marker{display:none}
.dd-summary::after{content:"+";font-size:22px;color:var(--ink);font-weight:400;line-height:1;flex-shrink:0;margin-top:2px}
.dd-item[open] .dd-summary::after{content:"\\2212"}
.dd-item[open] .dd-summary{border-bottom:1px solid var(--halo-400)}
.dd-summary-left{display:flex;flex-direction:column;gap:6px;flex:1;min-width:0}
.dd-summary-eyebrow{font-size:var(--fs-8);font-weight:700;color:var(--ink-3)}
.dd-summary-title{font-size:var(--fs-6);font-weight:700;color:var(--ink);letter-spacing:-.012em;line-height:1.32;margin:0}
.dd-body{padding:16px 0 22px}
.dd-body p{font-size:var(--fs-7);line-height:1.6;color:var(--ink-2);margin:0}
.dd-body p b{color:var(--ink);font-weight:600}

.lq{margin-top:64px;scroll-margin-top:100px}
.lq-lead{font-size:var(--fs-6);line-height:1.6;color:var(--ink-2);margin:0 0 32px;max-width:60ch}
.lq-list{display:flex;flex-direction:column;gap:14px}
.lq-item{display:grid;grid-template-columns:auto 1fr;gap:22px;padding:26px 30px;background:var(--band);border:1px solid var(--line)}
@media(max-width:560px){.lq-item{grid-template-columns:1fr;padding:24px}}
.lq-num{font-family:var(--font-display);font-weight:700;font-size:26px;color:var(--ink);line-height:1;letter-spacing:-.02em}
.lq-body h3{font-size:var(--fs-4);font-weight:700;line-height:1.3;letter-spacing:-.012em;color:var(--ink);margin:0 0 10px}
.lq-body p{font-size:var(--fs-7);line-height:1.6;color:var(--ink-2);margin:0}

.conclusion{margin-top:64px;scroll-margin-top:100px}

.convert{padding:80px 0 72px;border-top:1px solid var(--line);margin-top:88px;background:var(--band);text-align:center}
.convert .eyebrow{margin:0 0 14px}
.convert h2{font-size:var(--fs-2);line-height:1.15;letter-spacing:-.025em;margin:0 0 18px;max-width:20ch;margin-left:auto;margin-right:auto}
.convert-lead{font-size:var(--fs-6);color:var(--ink-2);line-height:1.6;max-width:56ch;margin:0 auto 30px}

.related{padding:72px 0}
.related-label{font-size:var(--fs-8);color:var(--ink-3);margin:0 0 12px}
.related h2{font-size:var(--fs-3);letter-spacing:-.02em;margin:0 0 28px}
.related-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
@media(max-width:820px){.related-grid{grid-template-columns:1fr}}
.rel-card{padding:22px 24px;background:var(--band);border:1px solid var(--line);display:flex;flex-direction:column;gap:12px;color:inherit;text-decoration:none}
.rel-card:hover{border-color:var(--ink)}
.rel-card .kicker{font-size:var(--fs-8);font-weight:700;color:var(--ink-3)}
.rel-card h3{font-size:var(--fs-4);line-height:1.28;letter-spacing:-.012em;color:var(--ink);font-weight:700;margin:0}
.rel-card p{font-size:var(--fs-7);line-height:1.55;color:var(--ink-2);margin:0}
.rel-card .meta{font-size:var(--fs-8);color:var(--ink-3);margin-top:auto}

@media(max-width:1000px){
  .ahead-grid{grid-template-columns:1fr;gap:36px}
  .body-grid{grid-template-columns:1fr;gap:32px}
  .toc{position:static;border-left:none;border-top:1px solid var(--line);padding:16px 0 0;max-height:none;overflow-y:visible}
}
@media(max-width:820px){
  .pillar-head{grid-template-columns:1fr;gap:12px}
  .pillar-score-block{align-items:flex-start;text-align:left}
  .chapter-opener{padding:36px 28px}
}
"""

# Fixed sitewide, per Round 10's ai-policy scroll-spy fix — the source's own
# "-30% 0px -60% 0px" rootMargin leaves only a 10%-tall trigger band (same
# over-narrow-IntersectionObserver bug already found and corrected once).
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


def parse():
    html = open(SRC, encoding="utf-8").read()
    h1 = re.search(r"<h1>(.*?)</h1>", html, re.S).group(1)
    crumb = re.search(r'(<div class="crumb">.*?</div>\s*</div>)', html, re.S).group(1)
    blob = html[html.index("<!-- ARTICLE HEAD -->"):html.index('<footer class="foot">')]

    # 1: wire the 2 mid-cta buttons + the convert-cta button to real pages —
    # visual-only in the source (no href at all), same "upgrade once the
    # destination is real" convention as the rest of this site.
    blob = blob.replace(
        '<a class="btn btn-primary">Explore Intercept Labs &rarr;</a>',
        '<a class="btn btn-primary" href="{base}intercept-labs/index.html">Explore Intercept Labs &rarr;</a>',
        1,
    )
    blob = blob.replace(
        '<a class="btn btn-primary">Start the conversation &rarr;</a>',
        '<a class="btn btn-primary" href="{base}contact/index.html">Start the conversation &rarr;</a>',
        1,
    )
    blob = blob.replace(
        '<a class="btn btn-primary">Open the form &rarr;</a>',
        '<a class="btn btn-primary" href="{base}contact/index.html">Open the form &rarr;</a>',
        1,
    )

    # 2: wire the 3 related cards to the real Signals from the Edge pages
    # whose titles they match exactly.
    def wire_related(m):
        card = m.group(0)
        title_match = re.search(r"<h3>(.*?)</h3>", card)
        title_text = re.sub(r"&rsquo;", "'", title_match.group(1))
        href = RELATED_HREFS.get(title_text)
        if not href:
            raise ValueError(f"no related href for {title_text!r}")
        return card.replace('<a class="rel-card">', f'<a class="rel-card" href="{{base}}insights/{href}">', 1)

    blob = re.sub(r'<a class="rel-card">.*?</a>', wire_related, blob, flags=re.S)

    return h1, crumb, blob


def render(base="../../../"):
    h1, crumb, blob = parse()
    blob = blob.replace("{base}", base)
    title_plain = re.sub(r"<[^>]+>", "", h1)

    return f"""<!doctype html>
<html lang="en">
<head>
{head_html(f"{title_plain} · Trends Brief · Intercept", "H1 2026 edition. Six Watchtower pillars, n=11,249–467,863.")}
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header_html(base)}
{crumb}
<main id="main">
{blob}
</main>
{footer_html(base)}
<script>{SCROLL_SPY_SCRIPT}</script>
</body>
</html>"""


def main():
    out = render()
    outdir = os.path.join(ROOT, "insights", "trends-brief", "when-ai-becomes-an-operating-model")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "index.html")
    open(path, "w", encoding="utf-8").write(out)
    print("Wrote", path)


if __name__ == "__main__":
    main()
