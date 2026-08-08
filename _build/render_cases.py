#!/usr/bin/env python3
"""Render all 31 case-study pages from cases.json into ../our-work/<slug>/index.html."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import esc, head_html, header_html, footer_html, CSS

BUILD_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BUILD_DIR)
CASES = json.load(open(os.path.join(BUILD_DIR, "cases.json"), encoding="utf-8"))

def norm(s):
    s = s.replace("’", "'").lower()
    s = re.sub(r"[^a-z0-9 ]", "", s)
    return re.sub(r"\s+", " ", s).strip()

LOOKUP = {norm(c["short_title"]): c for c in CASES}

CLIENT_PREFIXES = ["intel", "hp", "microsoft", "sap", "bmc", "intuit", "td synnex", "telus"]

def resolve_related(title):
    key = norm(title)
    if key in LOOKUP:
        return LOOKUP[key]
    for p in CLIENT_PREFIXES:
        if key.startswith(p + " "):
            stripped = key[len(p):].strip()
            if stripped in LOOKUP:
                return LOOKUP[stripped]
    if key.startswith("intel "):  # "intel: the magic of metaphors" already stripped colon by norm
        pass
    # substring containment fallback (longest match)
    candidates = [(k, c) for k, c in LOOKUP.items() if k in key or key in k]
    if candidates:
        candidates.sort(key=lambda kc: -len(kc[0]))
        return candidates[0][1]
    return None

CASE_CSS = """
.chero{padding:52px 0 40px}
.chero .eyebrow{margin-bottom:16px}
.chero h1{font-size:var(--fs-1);line-height:1.05;letter-spacing:-.03em;margin:0 0 16px;max-width:19ch}
.chero .sub{font-family:var(--font-body);font-size:var(--fs-5);line-height:1.5;color:var(--ink-2);margin:0 0 22px;max-width:44ch}
.credential{display:inline-flex;align-items:center;gap:8px;font-size:var(--fs-8);font-weight:600;letter-spacing:.07em;text-transform:uppercase;color:var(--ink-2);border:1px solid var(--line);border-radius:99px;padding:6px 14px;margin:0 0 20px}
.meta-row{display:flex;align-items:center;gap:14px}
.meta-row .label{font-size:var(--fs-8);font-weight:600;letter-spacing:.07em;text-transform:uppercase;color:var(--ink-3)}
.chero-media{aspect-ratio:21/9}

.prose h2{font-size:var(--fs-2);line-height:1.15;letter-spacing:-.02em;margin:0 0 18px;max-width:22ch}
.prose p{font-size:var(--fs-6);line-height:1.62;color:var(--ink-2);margin:0 0 18px}
.prose p:last-child{margin-bottom:0}

.spotlight{display:grid;gap:32px;margin-top:8px}
.spotlight-item h3{font-size:var(--fs-5);font-weight:700;letter-spacing:-.01em;margin:0 0 8px}
.spotlight-item p{font-size:var(--fs-6);line-height:1.58;color:var(--ink-2);margin:0;max-width:60ch}

.result h2{font-size:var(--fs-2);margin:0 0 16px;max-width:20ch}

.related-h{font-size:var(--fs-2);letter-spacing:-.02em}
.rel h3{font-size:var(--fs-4);line-height:1.22;margin:0 0 6px;font-weight:700}
.rel p{font-size:var(--fs-7);line-height:1.45;color:var(--ink-2);margin:0}

.convert{text-align:center}
.convert h2{font-size:var(--fs-2);line-height:1.1;letter-spacing:-.025em;margin:0 auto 14px;max-width:18ch}
.convert p{font-size:var(--fs-6);color:var(--ink-2);margin:0 auto 20px}
"""

def render_case(c):
    base = "../../"
    slot_stats = "".join(
        f'<div class="stat"><b>{esc(s["value"])}</b><span>{esc(s["label"])}</span></div>'
        for s in c["stats"]
    )
    problem_paras = "".join(f"<p>{esc(p)}</p>" for p in c["problem_paras"])
    solution_intro = "".join(f"<p>{esc(p)}</p>" for p in c["solution_intro_paras"])
    spotlight = "".join(
        f'<div class="spotlight-item"><h3>{esc(a["title"])}</h3><p>{esc(a["body"])}</p></div>'
        for a in c["acc_items"]
    )
    result_paras = "".join(f"<p>{esc(p)}</p>" for p in c["result_paras"])

    rel_cards = ""
    for r in c["related"]:
        match = resolve_related(r["title"])
        href = f'{base}our-work/{match["slug"]}/index.html' if match else f'{base}our-work/index.html'
        rel_cards += (
            f'<a class="card rel" href="{href}">'
            f'<div class="ph" style="aspect-ratio:4/3">{esc(match["client_display"]) if match else "Related work"}</div>'
            f'<h3>{esc(r["title"])}</h3><p>{esc(r["desc"])}</p></a>'
        )

    credential_html = ""
    if c["credential"]:
        credential_html = f'<span class="credential">{esc(c["credential"])}</span>'

    body = f"""<!doctype html>
<html lang="en">
<head>
{head_html(f'{c["h1"]} · Intercept case study', c["sub"])}
<style>{CASE_CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header_html(base)}

<main id="main">
<section class="chero">
  <div class="wrap">
    <span class="eyebrow">{esc(c["eyebrow"])}</span>
    {credential_html}
    <h1>{esc(c["h1"])}</h1>
    <p class="sub">{esc(c["sub"])}</p>
    <div class="meta-row"><span class="label">{esc(c["read_time"])}</span></div>
  </div>
</section>

<div class="wrap"><div class="ph chero-media">Case hero</div></div>

<section class="sec prose">
  <div class="wrap read">
    <h2>{esc(c["problem_h2"])}</h2>
    {problem_paras}
  </div>
</section>

<section class="sec prose band-tint" style="padding-bottom:52px">
  <div class="wrap read">
    <h2>{esc(c["solution_h2"])}</h2>
    {solution_intro}
    <div class="spotlight">{spotlight}</div>
  </div>
</section>

<section class="sec band-navy">
  <div class="wrap">
    <div class="stat-row">{slot_stats}</div>
  </div>
</section>

<section class="sec prose result">
  <div class="wrap read">
    <h2>{esc(c["result_h2"])}</h2>
    {result_paras}
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap">
    <h2 class="related-h" style="margin:0 0 24px">Related work</h2>
    <div class="card-grid g3">{rel_cards}</div>
  </div>
</section>

<section class="sec convert band-tint">
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
    return body

def main():
    outdir = os.path.join(ROOT, "our-work")
    for c in CASES:
        case_dir = os.path.join(outdir, c["slug"])
        os.makedirs(case_dir, exist_ok=True)
        out_path = os.path.join(case_dir, "index.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(render_case(c))
    print(f"Rendered {len(CASES)} case pages -> {outdir}/<slug>/index.html")

    # report unresolved related links for the summary
    unresolved = set()
    for c in CASES:
        for r in c["related"]:
            if not resolve_related(r["title"]):
                unresolved.add(r["title"])
    print("Unresolved related-work titles (no matching case, linked to work index):")
    for u in sorted(unresolved):
        print(" -", u)

if __name__ == "__main__":
    main()
