#!/usr/bin/env python3
"""Parse + render the 6 "What We Do" service pages from the wireframe source, verbatim.

Source: ~/Downloads/New Wire Frames/pages/services/<slug>.html — each file shares the
identical HTML-comment-bounded section shape (HERO / CONTEXT / WHAT WE DO / AI MODULE /
PROOF / CONVERSION), confirmed against all 6 files. Output: what-we-do/<slug>/index.html.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import esc, head_html, header_html, footer_html
from render_cases import resolve_related

SRC_DIR = "/Users/jontoewsinterceptgroup.com/Downloads/New Wire Frames/pages/services"
BUILD_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BUILD_DIR)

# canonical URL slugs (confirmed against sitemap.html) in the wireframe's own sub-nav order
NAV_ORDER = ["strategy-planning", "content", "creative", "digital-media", "sales-enablement", "channel"]
NAV_LABELS = {
    "strategy-planning": "Strategy",
    "content": "Content",
    "creative": "Creative",
    "digital-media": "Digital Media",
    "sales-enablement": "Sales Enablement",
    "channel": "Channel",
}

def between(text, a, b):
    i = text.index(a) + len(a)
    j = text.index(b, i)
    return text[i:j]

def grab(pattern, text, flags=re.S):
    m = re.search(pattern, text, flags)
    return m.group(1).strip() if m else None

CSS = """
.svcnav{border-bottom:1px solid var(--line);background:var(--band)}
.svcnav-row{max-width:var(--maxw);margin:0 auto;padding:12px 32px;display:flex;gap:26px;font-size:var(--fs-8);color:var(--ink-3);overflow-x:auto}
.svcnav-row a{color:var(--ink-3)}
.svcnav-row a:hover{color:var(--ink)}
.svcnav-row .on{color:var(--ink);font-weight:600}

.shero{padding:52px 0 40px}
.shero-grid{display:grid;grid-template-columns:1fr 1.05fr;gap:56px;align-items:center}
.shero .ph{aspect-ratio:4/3}
.shero h1{font-size:var(--fs-1);line-height:1.06;letter-spacing:-.03em;margin:0 0 16px;max-width:16ch}
.shero .sub{font-size:var(--fs-5);line-height:1.4;color:var(--ink-2);margin:0}

.sec{padding:40px 0}
.sec h2{font-size:var(--fs-2);line-height:1.12;letter-spacing:-.026em;margin:0 0 18px;max-width:20ch}
.sec p{font-size:var(--fs-6);line-height:1.6;color:var(--ink-2);margin:0}

.callout{background:var(--band);padding:32px 34px;margin:8px 0 12px;max-width:var(--readw)}
.callout b{display:block;font-family:var(--font-display);font-size:var(--fs-data);line-height:1;letter-spacing:-.03em;font-weight:700}
.callout span{display:block;font-size:var(--fs-7);line-height:1.5;color:var(--ink-2);margin-top:12px}
.callout cite{display:block;font-style:normal;font-size:var(--fs-8);color:var(--ink-3);margin-top:10px}

.wwd{margin-top:8px;max-width:var(--readw);display:grid;gap:28px}
.wwd-item h3{font-size:var(--fs-5);font-weight:700;letter-spacing:-.01em;margin:0 0 8px}
.wwd-item p{font-size:var(--fs-6);line-height:1.58;color:var(--ink-2);margin:0;max-width:60ch}

.ai{padding:44px 0}
.ai h2{font-size:var(--fs-2);margin:0 0 16px;max-width:22ch}
.ai p{font-size:var(--fs-6);color:var(--ink-2);margin:0 0 26px;max-width:var(--readw)}
.toolgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;margin-top:10px}
.tcard .ph{aspect-ratio:4/3;margin-bottom:12px}
.tcard b{display:block;font-size:var(--fs-6);font-weight:700;margin-bottom:5px}
.tcard span{display:block;font-size:var(--fs-8);color:var(--ink-2)}

.proof{padding:44px 0 12px}
.proof .ph{aspect-ratio:4/3}

@media(max-width:900px){.shero-grid{grid-template-columns:1fr}.toolgrid{grid-template-columns:1fr 1fr}}
"""

def parse(slug):
    html = open(os.path.join(SRC_DIR, f"{slug}.html"), encoding="utf-8").read()

    hero = between(html, "<!-- HERO -->", "<!-- CONTEXT -->")
    eyebrow = grab(r'<p class="eyebrow">(.*?)</p>', hero)
    h1 = grab(r"<h1>(.*?)</h1>", hero)
    sub = grab(r'<p class="sub">(.*?)</p>', hero)

    ctx = between(html, "<!-- CONTEXT -->", "<!-- WHAT WE DO -->")
    ctx_p = grab(r"<p>(.*?)</p>", ctx)
    stat_value, stat_desc, stat_source = None, None, None
    callout_m = re.search(
        r'<div class="callout">\s*<b>(.*?)</b>\s*<span>(.*?)<br>\s*<em[^>]*>(.*?)</em>\s*</span>',
        ctx, re.S,
    )
    if callout_m:
        stat_value, stat_desc, stat_source = (g.strip() for g in callout_m.groups())

    wwd = between(html, "<!-- WHAT WE DO -->", "<!-- AI MODULE -->")
    wwd_h2 = grab(r"<h2>(.*?)</h2>", wwd)
    acc_items = re.findall(
        r'<div class="acc-head"><h3>(.*?)</h3><i>.*?</i></div>\s*<div class="acc-body"><p>(.*?)</p></div>',
        wwd, re.S,
    )
    acc_items = [(t.strip(), b.strip()) for t, b in acc_items]

    ai = between(html, "<!-- AI MODULE -->", "<!-- PROOF -->")
    ai_h2 = grab(r"<h2>(.*?)</h2>", ai)
    ai_p = grab(r"<p>(.*?)</p>", ai)
    tools = re.findall(r'<div class="tcard"><div class="ph">.*?</div><b>(.*?)</b><span>(.*?)</span></div>', ai, re.S)
    tools = [(a.strip(), b.strip()) for a, b in tools]

    proof = between(html, "<!-- PROOF -->", "<!-- CONVERSION -->")
    proof_h2 = grab(r"<h2[^>]*>(.*?)</h2>", proof)
    proof_cards = re.findall(r'<div><div class="ph">.*?</div><h3>(.*?)</h3><p>(.*?)</p></div>', proof, re.S)
    proof_cards = [(t.strip(), d.strip()) for t, d in proof_cards]

    return dict(
        eyebrow=eyebrow, h1=h1, sub=sub, ctx_p=ctx_p,
        stat_value=stat_value, stat_desc=stat_desc, stat_source=stat_source,
        wwd_h2=wwd_h2, acc_items=acc_items,
        ai_h2=ai_h2, ai_p=ai_p, tools=tools,
        proof_h2=proof_h2, proof_cards=proof_cards,
    )

def svcnav_html(active_slug, base):
    items = []
    for slug in NAV_ORDER:
        label = esc(NAV_LABELS[slug])
        if slug == active_slug:
            items.append(f'<span class="on">{label}</span>')
        else:
            items.append(f'<a href="{base}what-we-do/{slug}/index.html">{label}</a>')
    return f'<div class="svcnav"><div class="svcnav-row">{"".join(items)}</div></div>'

def render(slug, data, base="../../"):
    callout_html = ""
    if data["stat_value"]:
        callout_html = (
            f'<div class="wrap"><div class="callout">'
            f'<b>{esc(data["stat_value"])}</b>'
            f'<span>{esc(data["stat_desc"])}</span>'
            f'<cite>{esc(data["stat_source"])}</cite>'
            f'</div></div>'
        )

    wwd_html = "".join(
        f'<div class="wwd-item"><h3>{esc(t)}</h3><p>{esc(b)}</p></div>'
        for t, b in data["acc_items"]
    )

    tool_cols = min(len(data["tools"]), 4) or 4
    tools_html = "".join(
        f'<div class="tcard"><div class="ph">Tool</div><b>{esc(a)}</b><span>{esc(b)}</span></div>'
        for a, b in data["tools"]
    )

    proof_html = ""
    for title, desc in data["proof_cards"]:
        match = resolve_related(title)
        href = f'{base}our-work/{match["slug"]}/index.html' if match else f'{base}our-work/index.html'
        caption = esc(match["client_display"]) if match else "Related work"
        proof_html += (
            f'<a class="card" href="{href}">'
            f'<div class="ph">{caption}</div>'
            f'<h3>{esc(title)}</h3><p>{esc(desc)}</p></a>'
        )

    return f"""<!doctype html>
<html lang="en">
<head>
{head_html(f'{data["h1"]} · Intercept', data["sub"])}
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header_html(base)}
{svcnav_html(slug, base)}
<main id="main">

<section class="shero">
  <div class="wrap"><div class="shero-grid">
    <div class="ph">Service hero</div>
    <div>
      <p class="eyebrow">{esc(data["eyebrow"])}</p>
      <h1>{esc(data["h1"])}</h1>
      <p class="sub">{esc(data["sub"])}</p>
    </div>
  </div></div>
</section>

<section class="sec"><div class="wrap read"><p>{esc(data["ctx_p"])}</p></div></section>
{callout_html}

<section class="sec">
  <div class="wrap">
    <h2>{esc(data["wwd_h2"])}</h2>
    <div class="wwd">{wwd_html}</div>
  </div>
</section>

<section class="ai band-tint">
  <div class="wrap">
    <h2>{esc(data["ai_h2"])}</h2>
    <p>{esc(data["ai_p"])}</p>
    <div class="toolgrid" style="grid-template-columns:repeat({tool_cols},1fr)">{tools_html}</div>
  </div>
</section>

<section class="proof">
  <div class="wrap">
    <h2 style="font-size:var(--fs-3);margin-bottom:0">{esc(data["proof_h2"])}</h2>
    <div class="card-grid g3" style="margin-top:24px">{proof_html}</div>
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
    outdir = os.path.join(ROOT, "what-we-do")
    unresolved = set()
    for slug in NAV_ORDER:
        data = parse(slug)
        for title, _ in data["proof_cards"]:
            if not resolve_related(title):
                unresolved.add(title)
        out = render(slug, data)
        page_dir = os.path.join(outdir, slug)
        os.makedirs(page_dir, exist_ok=True)
        path = os.path.join(page_dir, "index.html")
        open(path, "w", encoding="utf-8").write(out)
        print("Wrote", path)

    print("Unresolved proof-section case titles (no matching case, linked to work index):")
    for u in sorted(unresolved):
        print(" -", u)

if __name__ == "__main__":
    main()
