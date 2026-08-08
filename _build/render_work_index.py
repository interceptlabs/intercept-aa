#!/usr/bin/env python3
"""Render our-work/index.html — the full 31-case gallery with real filters +
load-more (per our-work.html wireframe: chips filter by data-s, 12 shown by
default, "Load more" reveals the rest — ported verbatim, not reinterpreted)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import esc, head_html, header_html, footer_html

BUILD_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BUILD_DIR)
CASES = json.load(open(os.path.join(BUILD_DIR, "cases.json"), encoding="utf-8"))
BY_H1 = {c["h1"]: c for c in CASES}

# exact presentation order from our-work.html's .gal-grid (grouped by service,
# matching the chip order Strategy/Content/Creative/Digital Media/Sales
# Enablement/Channel) — not alphabetical, ported verbatim from the wireframe
GALLERY_ORDER = [
    "HP launches subscription management to a list of 1,000 customers",
    "Intel makes complex cloud migration simple with everyday metaphors",
    "Microsoft brings the managed account experience to small businesses at scale",
    "BMC wrote the evaluation criteria buyers were missing",
    "Microsoft answers the Copilot questions users were already asking",
    "Microsoft connects free learning pathways to ten in-demand jobs",
    "Microsoft turns AI curiosity into confidence to act",
    "Microsoft turns more than 25 developer programs into one connected journey",
    "Security training IT teams could host on their own schedule",
    "A video game that put security teams inside a cyberattack",
    "HP turns a video into a conversation that recommends devices",
    "Microsoft trains Teams users with the most dysfunctional office ever",
    "Microsoft turns software developers into superheroes with their own comics",
    "SAP replaces traditional video production with photorealistic AI avatars",
    "An executive breakfast built entirely around how CFOs think",
    "HP built a personalized Micro App for 50 enterprise accounts",
    "Intuit wins educators to get QuickBooks into the classroom",
    "Microsoft brings Build highlights to developers on the big screen",
    "Microsoft hosts an AI event that is powered by AI",
    "TELUS Business took AI-powered dash cams to fleet-heavy industries",
    "A pitch challenge that refined how partner sales reps sell Surface",
    "HP put AI on the account research, people on the relationship",
    "HP ran a controlled experiment to measure what marketing added",
    "Microsoft gives resellers a showcase kit for the full Surface line-up",
    "Microsoft puts the Surface touch factor into customers’ hands",
    "An AI voice agent that qualified leads for HP’s channel partners",
    "Earning reseller sales reps’ attention for the lightest business laptop",
    "HP built Taylor, an AI content strategist for its channel partners",
    "Microsoft hosts its first metaverse event on a private island",
    "TD SYNNEX gave MSPs three paths to the cloud",
    "TD SYNNEX moves managed service providers from servers to cloud",
]
CASES_ORDERED = [BY_H1[h1] for h1 in GALLERY_ORDER]
assert len(CASES_ORDERED) == len(CASES) == 31

SERVICES = ["Strategy", "Content", "Creative", "Digital Media", "Sales Enablement", "Channel"]

INDEX_CSS = """
.whero{padding:56px 0 32px}
.whero h1{font-size:var(--fs-1);letter-spacing:-.03em;margin:0}

.feat{padding:0 0 48px}
.feat-grid{display:grid;grid-template-columns:1.3fr 1fr;gap:48px;align-items:center;border-top:1px solid var(--line);padding-top:32px}
.feat-grid .ph{aspect-ratio:16/9}
.feat-grid h2{font-size:var(--fs-2);letter-spacing:-.02em;margin:8px 0 14px}
.feat-grid p{font-size:var(--fs-6);line-height:1.55;color:var(--ink-2);margin:0 0 18px;max-width:52ch}
@media(max-width:900px){.feat-grid{grid-template-columns:1fr;gap:24px}}

.gal{padding:8px 0 76px}
.chips{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:32px}
.chip{font-size:var(--fs-7);font-weight:600;padding:8px 16px;border-radius:99px;border:1px solid var(--line);color:var(--ink-2);cursor:pointer;transition:background .15s,color .15s,border-color .15s}
.chip:hover{border-color:var(--ink-3)}
.chip.on{background:var(--carbon-500);color:#fff;border-color:var(--carbon-500)}
.gal-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.wcard h3{font-size:var(--fs-4);line-height:1.25;margin:0 0 6px;font-weight:700}
.wcard .client{font-size:var(--fs-8);font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);margin-bottom:10px;display:block}
.wcard .credential{display:inline-flex;align-items:center;gap:6px;font-size:var(--fs-8);font-weight:600;letter-spacing:.05em;color:var(--ink-3);margin-top:8px}
.wcard .cred-mark{width:8px;height:8px;border-radius:50%;background:var(--flarepop);display:inline-block}
.more{text-align:center;margin-top:40px}
@media(max-width:900px){.gal-grid{grid-template-columns:1fr 1fr}}
@media(max-width:600px){.gal-grid{grid-template-columns:1fr}}
"""

FILTER_SCRIPT = """<script>
(function(){
  var grid = document.querySelector(".gal-grid");
  var cards = [].slice.call(grid.querySelectorAll(".case"));
  var more = document.getElementById("more");
  var filter = "", expanded = false;
  function apply(){
    var shown = 0;
    cards.forEach(function(c){
      var match = !filter || c.dataset.s === filter;
      var within = expanded || filter || shown < 12;
      c.hidden = !(match && within);
      if (match) shown++;
    });
    var hiddenLeft = cards.filter(function(c){ return c.hidden; }).length;
    more.parentNode.style.display = hiddenLeft ? "" : "none";
  }
  document.querySelector(".chips").addEventListener("click", function(e){
    var chip = e.target.closest(".chip"); if(!chip) return;
    [].forEach.call(document.querySelectorAll(".chip"), function(c){ c.classList.remove("on"); });
    chip.classList.add("on"); filter = chip.dataset.f || ""; expanded = false; apply();
  });
  more.addEventListener("click", function(){ expanded = true; apply(); });
  apply();
})();
</script>"""

def render():
    # "AI in Practice" is the featured case (matches the wireframe's own
    # featured band + the homepage's featured tile)
    feat = next(c for c in CASES if c["slug"] == "ai-in-practice")

    chips_html = '<span class="chip on" data-f="">All work</span>' + "".join(
        f'<span class="chip" data-f="{esc(s)}">{esc(s)}</span>' for s in SERVICES
    )

    cards = ""
    for c in CASES_ORDERED:
        credential_html = (
            f'<span class="credential"><span class="cred-mark"></span>{esc(c["credential"])}</span>'
            if c["credential"] else ""
        )
        cards += f"""<a class="card wcard case" data-s="{esc(c['service'])}" href="{c['slug']}/index.html">
  <div class="ph" style="aspect-ratio:4/3">{esc(c['client_display'])}</div>
  <span class="client">{esc(c['service'])}</span>
  <h3>{esc(c['h1'])}</h3>
  {credential_html}
</a>"""

    return f"""<!doctype html>
<html lang="en">
<head>
{head_html("Our Work · Intercept", "Award-winning B2B marketing case studies for Microsoft, HP, SAP, Intel, BMC, TD SYNNEX, TELUS, Intuit and more.")}
<style>{INDEX_CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header_html("../")}

<main id="main">
<section class="whero">
  <div class="wrap">
    <span class="eyebrow">Our work</span>
    <h1>Case studies</h1>
  </div>
</section>

<section class="feat">
  <div class="wrap">
    <div class="feat-grid">
      <div class="ph" style="aspect-ratio:16/9">{esc(feat['client_display'])}</div>
      <div>
        <span class="eyebrow">Featured</span>
        <h2>AI in Practice</h2>
        <p>{esc(feat['sub'])}</p>
        <a class="link" href="{feat['slug']}/index.html">Read the case study</a>
      </div>
    </div>
  </div>
</section>

<section class="gal">
  <div class="wrap">
    <div class="chips">{chips_html}</div>
    <div class="gal-grid">{cards}</div>
    <div class="more"><span class="link" id="more">Load more</span></div>
  </div>
</section>
</main>

{footer_html("../")}
{FILTER_SCRIPT}
</body>
</html>"""

def main():
    outdir = os.path.join(ROOT, "our-work")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "index.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(render())
    print("Wrote", path)

if __name__ == "__main__":
    main()
