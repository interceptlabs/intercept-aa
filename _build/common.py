#!/usr/bin/env python3
"""Shared design-system pieces for InterceptAA: tokens, nav, footer, logo library."""
import json, os, html as _html

BUILD_DIR = os.path.dirname(os.path.abspath(__file__))

def esc(s):
    return _html.escape(s, quote=False) if s else ""

# ---- wordmark (re-sourced from intercept-home-concepts/concept-d, 2026-08-06 correction —
#      home.html's copy carried a runtime translate(0,-10) against a fractional viewBox, the
#      exact "crunchy logo" failure mode the constitution's L-1..L-5 document. concept-d's copy
#      has the offset baked into the viewBox instead (no runtime transform on the resting chain,
#      integer-safe), so it's the correct source to build from.) ----
_wm = open(os.path.join(BUILD_DIR, "wordmark_v2.txt"), encoding="utf-8").read()
WORDMARK_VIEWBOX, WORDMARK_INNER = _wm.split("\n---SPLIT---\n")

# ---- animated hover-glitch mark (also lifted verbatim from concept-d: the canon triangle mark
#      resting in the lockup's mark-slot, glitching through channel/layout variants on hover or
#      focus, settling back to canon — plus a one-time autoplay 500ms after load). ----
GLITCH_SOURCE_DEFS = open(os.path.join(BUILD_DIR, "glitch_source.svg"), encoding="utf-8").read()
LOGO_GLITCH_JS = open(os.path.join(BUILD_DIR, "logo_glitch.js"), encoding="utf-8").read()

def wordmark_svg(css_class="logo", slot_id="mark-slot", base=""):
    # L-5: 1x-DPR raster swap (see the @media(max-resolution) block in CSS below).
    # The url() is set here, inline per-page, so it resolves relative to whatever
    # depth this page sits at — a fixed relative path baked into the shared CSS
    # string would 404 on any page below site root (our-work/<slug>/, careers/
    # open-roles/<role>/, etc.), since CSS custom-property url()s resolve against
    # the document that DECLARES the property, not the one that consumes it via var().
    wm_file = "wordmark-26-ink.png" if "sm" in css_class.split() else "wordmark-30-ink.png"
    return (
        f'<svg class="{css_class}" viewBox="{WORDMARK_VIEWBOX}" role="img" aria-label="Intercept" '
        f'style="--wm-raster:url(\'{base}assets/img/{wm_file}\')">'
        f'<g fill="var(--logo-ink)">{WORDMARK_INNER}</g>'
        f'<g id="{slot_id}" transform="translate(0, 1.22)"></g></svg>'
    )

def lockup_link(base, css_class="logo", slot_id="mark-slot"):
    return (
        f'<a class="fritz-lockup-hover" href="{base}index.html" aria-label="Intercept home" '
        f'data-fritz-hover-lockup>{wordmark_svg(css_class, slot_id, base)}</a>'
    )

# ---- client logos (verbatim from home.html, + 2 more lifted from the redesign-v1-brand-applied
#      prototype's asset kit, + 1 plain wordmark for the one client with no sourced vector anywhere) ----
CLIENT_LOGOS = json.load(open(os.path.join(BUILD_DIR, "client_logos.json"), encoding="utf-8"))

def _load_lifted(name, filename, height_px):
    viewbox, inner = open(os.path.join(BUILD_DIR, filename), encoding="utf-8").read().split("\n---SPLIT---\n")
    svg = f'<svg class="brand" style="height:{height_px}px;width:auto" viewBox="{viewbox}" role="img" aria-label="{name}">{inner}</svg>'
    return {"href": None, "svg": svg}

CLIENT_LOGOS["Intel"] = _load_lifted("Intel", "intel_inner.txt", 21)
CLIENT_LOGOS["TD SYNNEX"] = _load_lifted("TD SYNNEX", "td_inner.txt", 16)

_TEXT_LOGOS = {
    "Intuit": ("https://www.intuit.com/", "intuit", 22),
}
for name, (href, label, size) in _TEXT_LOGOS.items():
    CLIENT_LOGOS[name] = {
        "href": href,
        "svg": None,
        "text": label,
        "text_size": size,
    }

def client_logo_html(name):
    """Render a client logo (or text fallback) as an unlinked mono glyph for the wall/badges."""
    entry = CLIENT_LOGOS.get(name)
    if not entry:
        return f'<span class="brand-text">{esc(name)}</span>'
    if entry.get("svg"):
        return entry["svg"]
    return f'<span class="brand-text" style="font-size:{entry["text_size"]}px">{esc(entry["text"])}</span>'

# ---- CSS ----
# Type scale = the fixed px steps from the Design OS token set (kernel/intercept/tokens.json),
# not fluid clamp()/vw sizing — 9 rungs total, sitewide, each used deliberately:
#   fs-1 56  page headline (hero h1 / case h1)
#   fs-2 40  section headline (homepage sections, case problem/solution/result heads)
#   fs-3 24  sub-headline (featured-case teaser title)
#   fs-4 20  component title (card/related/FAQ-question)
#   fs-5 18  lede/sub paragraph under a big headline
#   fs-6 16  body copy / prose
#   fs-7 14  dek/secondary copy, nav links, buttons
#   fs-8 12  labels, eyebrows, meta, legal
#   fs-data 56  stat numerals (Instrument Sans display bold — reuses the fs-1 value,
#               its own named token since several call sites reference fs-data specifically)
CSS = """
:root{
  --halo-100:#ffffff; --halo-200:#f5f7ff; --halo-300:#e6e9f5; --halo-400:#d1d6e6; --halo-500:#b8bed1;
  --carbon-100:#3a3a4a; --carbon-200:#2c2c3a; --carbon-300:#1f1f2a; --carbon-400:#14141c; --carbon-500:#0a0a0f;
  --flarepop:#ff00e5; --flarepop-500:#39003a; --flarepop-ink:#a8008c;
  --coolsweep:#1a7aff; --coolsweep-500:#08285c;
  --ink:var(--carbon-500); --ink-2:#2c2c3a; --ink-3:#5a5f70; --ink-muted:rgba(10,10,15,.45);
  --logo-ink:var(--ink);
  /* Jon-directed light-mode exception, round 4 (2026-08-08): ONE flat warm
     tone for every light surface — page, nav, .band sections, .ph boxes,
     form fields — no separate lighter/darker step between them (round 3's
     two-tier --warm-100/--warm-200 split was a mistake, called out
     directly: "you just reversed everything" — a darker second tone on
     boxes/panels recreated the same bright-surface-next-to-different-
     surface clash this whole exception exists to remove). Lighter again
     than round 3's --warm-100 (#fcfbfa). Boxes/bands now separate from the
     page ONLY via their existing 1px --line border, not a fill-color step.
     --line stays on the Halo scale — untouched, not named in the ask. */
  --warm:#fdfcfb; --warm-rgb:253,252,251;
  --page:var(--warm); --band:var(--warm); --line:var(--halo-300);
  --maxw:1200px; --readw:700px;
  --font-display:'Instrument Sans',system-ui,sans-serif;
  --font-body:'Inter',system-ui,sans-serif;
  --fs-1:56px; --fs-2:40px; --fs-3:24px; --fs-4:20px; --fs-5:18px; --fs-6:16px; --fs-7:14px; --fs-8:12px; --fs-data:56px;
}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth}
html,body{margin:0;overflow-x:clip;max-width:100%}
body{background:var(--page);color:var(--ink);font-family:var(--font-body);font-size:var(--fs-6);line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
img,svg{max-width:100%}
h1,h2,h3,h4{font-family:var(--font-display);font-weight:700;line-height:1.15;letter-spacing:-.02em;margin:0;text-wrap:balance}
p{margin:0;text-wrap:pretty}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 32px}
.read{max-width:var(--readw)}
.skip{position:absolute;left:-999px}
.skip:focus{left:12px;top:12px;background:var(--flarepop);color:#0a0a0f;padding:8px 14px;border-radius:6px;z-index:200}

/* Sentence case, not uppercase+tracked — the all-caps letter-spaced
   overline label is a generic AI-template habit (Fritz rule, 2026-08-07),
   not an Intercept convention. Source text is already written in sentence
   case (see call sites); this rule used to force it into caps on top. */
.eyebrow{font-family:var(--font-body);font-weight:600;font-size:var(--fs-8);color:var(--flarepop-ink);margin:0 0 14px;display:block}

/* lockup */
.logo{width:auto;height:30px;display:block;shape-rendering:geometricPrecision}
.logo.sm{height:26px}
.fritz-lockup-hover{display:inline-flex;align-items:center;color:inherit;text-decoration:none;outline-offset:6px}

/* L-5 (constitution): on true 1x-DPR displays, live GPU path rasterization of
   the small wordmark is uneven regardless of correct vector geometry — swap in
   a pre-rendered supersampled raster (16x render, Lanczos downscale) of the
   SAME canon geometry instead. Retina (DPR>=2) keeps pure vector. The mark
   icon (#mark-slot/#footer-mark-slot) stays vector so its hover-glitch still
   animates; only the wordmark letterform paths are hidden. Integer widths are
   required — a fractional box re-phases the paint and resamples stems. */
@media(max-resolution:1.05dppx){
  svg.logo:not(.sm){width:127px;aspect-ratio:auto;background:var(--wm-raster) 0 0/127px 30px no-repeat}
  svg.logo.sm{width:110px;aspect-ratio:auto;background:var(--wm-raster) 0 0/110px 26px no-repeat}
  svg.logo g[fill="var(--logo-ink)"]{display:none}
}

/* topbar (functional sticky divider — matches shipped site nav convention) */
.topbar{position:sticky;top:0;z-index:100;background:rgba(var(--warm-rgb),.86);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.topbar .row{max-width:var(--maxw);margin:0 auto;padding:16px 32px;display:flex;align-items:center;justify-content:space-between;gap:28px}
.nav-wrap{display:flex;align-items:center;gap:20px}
.nav-links{display:flex;align-items:center;gap:24px;font-size:var(--fs-7);font-weight:500;color:var(--ink-2)}
.nav-links a:hover{color:var(--flarepop-ink)}
.nav-links .inert{color:var(--ink);opacity:.45;cursor:default}
.cta-nav{background:var(--carbon-500);color:#fff;font-weight:600;font-size:var(--fs-7);padding:9px 18px;border-radius:8px;transition:background .15s;flex:none}
.cta-nav:hover{background:var(--flarepop);color:var(--carbon-500)}
.nav-toggle{display:none;flex-direction:column;justify-content:center;gap:5px;width:32px;height:32px;padding:0;background:none;border:0;cursor:pointer;flex:none}
.nav-toggle span{display:block;width:100%;height:2px;background:var(--ink)}
@media(max-width:860px){
  .nav-toggle{display:flex}
  .nav-links{display:none}
  .nav-links.open{display:flex;position:absolute;top:100%;left:0;right:0;flex-direction:column;align-items:flex-start;gap:18px;background:var(--page);padding:22px 24px 26px;border-bottom:1px solid var(--line)}
}

/* buttons — bg/text pairs checked for contrast: carbon/white ~19:1, flarepop/carbon ~6:1 */
.btn{display:inline-flex;align-items:center;gap:8px;font-weight:600;font-size:var(--fs-7);padding:14px 24px;border-radius:8px;background:var(--carbon-500);color:#fff;transition:background .15s,color .15s}
.btn:hover{background:var(--flarepop);color:var(--carbon-500)}
.link{font-size:var(--fs-7);font-weight:600;display:inline-flex;align-items:center;gap:6px;color:var(--ink)}
.link::after{content:'\\203A';color:var(--flarepop-ink)}

/* section rhythm — bands carry emphasis, not lines */
.sec{padding:64px 0}
.band-tint{background:var(--band)}
.band-dark{background:var(--carbon-500);color:#fff}
.band-dark .ink-2{color:var(--halo-500)}
.band-navy{background:var(--coolsweep-500);color:#fff}

.ph{background:var(--band);border:1px solid var(--line);display:flex;align-items:center;justify-content:center;text-align:center;padding:16px;color:var(--ink-3);font-family:var(--font-body);font-weight:600;font-size:var(--fs-8);letter-spacing:.09em;text-transform:uppercase}

/* stat strip (the sanctioned data-viz default). Numeral voice is Instrument
   Sans display bold, not a separate mono "data" register — ties the figure
   to the same typographic voice as the headline above/around it instead of
   defaulting to the generic dashboard convention of a monospace numeral.
   Centered both as a row (within its band) and within each column. */
.stat-row{display:grid;grid-template-columns:repeat(3,1fr);gap:40px;text-align:center}
.stat b{display:block;font-family:var(--font-display);font-size:var(--fs-data);line-height:1;letter-spacing:-.03em;font-weight:700}
.stat span{display:block;font-size:var(--fs-7);line-height:1.45;margin:12px auto 0;opacity:.9;max-width:26ch}
@media(max-width:820px){.stat-row{grid-template-columns:1fr;gap:28px}}

/* cards */
.card-grid{display:grid;gap:24px}
.g3{grid-template-columns:repeat(3,1fr)}
.g2{grid-template-columns:repeat(2,1fr)}
@media(max-width:900px){.g3,.g2{grid-template-columns:1fr}}
.card h3{font-size:var(--fs-4);letter-spacing:-.015em;margin:0 0 8px;font-weight:700}
.card p{font-size:var(--fs-7);line-height:1.5;color:var(--ink-2)}
.card .ph{margin-bottom:14px}

/* footer */
.foot{padding:56px 0 32px}
.foot-grid{display:grid;grid-template-columns:1.6fr 1fr 1fr 1fr;gap:28px}
.foot-col h4{font-size:var(--fs-8);font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--ink-3);margin:0 0 14px}
.foot-col a,.foot-col span.inert{display:block;font-size:var(--fs-7);color:var(--ink-2);margin-bottom:9px}
.foot-col a:hover{color:var(--flarepop-ink)}
.foot-col span.inert{color:var(--ink);opacity:.45}
.foot-bot{margin-top:40px;padding-top:20px;font-size:var(--fs-8);color:var(--ink-3);display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px}
@media(max-width:820px){.foot-grid{grid-template-columns:1fr 1fr;gap:24px 20px}}
"""

NAV_TOGGLE_SCRIPT = (
    "<script>\n"
    "(function(){\n"
    '  var t = document.getElementById("navToggle"), n = document.getElementById("navLinks");\n'
    "  if (!t || !n) return;\n"
    '  t.addEventListener("click", function(){\n'
    '    var open = n.classList.toggle("open");\n'
    '    t.setAttribute("aria-expanded", open ? "true" : "false");\n'
    "  });\n"
    "})();\n"
    "</script>"
)

def nav_html(base=""):
    """base = '../' repeated once per directory level below site root
    (e.g. '' on /, '../' on /our-work/, '../../' on /our-work/<slug>/,
    '../../../' on /careers/open-roles/<role>/). Site reflow v2 (2026-08-07):
    Careers and Contact became real pages, Our Work/About Us moved under
    clean directory URLs (/our-work/, /about-us/) per sitemap.html."""
    def item(label, href, inert=False):
        if inert:
            return f'<span class="inert">{label}</span>'
        return f'<a href="{href}">{label}</a>'
    return f"""{lockup_link(base)}
    <div class="nav-wrap">
      <nav class="nav-links" id="navLinks" aria-label="Primary">
        {item("Our Work", f"{base}our-work/index.html")}
        {item("What We Do", f"{base}index.html#services")}
        {item("Insights", f"{base}insights/index.html")}
        {item("About Us", f"{base}about-us/index.html")}
        {item("Careers", f"{base}careers/index.html")}
      </nav>
      <button class="nav-toggle" id="navToggle" type="button" aria-expanded="false" aria-controls="navLinks" aria-label="Menu"><span></span><span></span><span></span></button>
      <a class="cta-nav" href="{base}contact/index.html">Contact</a>
    </div>"""

def header_html(base=""):
    return f"""<header class="topbar"><div class="row">{nav_html(base)}</div></header>
{NAV_TOGGLE_SCRIPT}"""

def footer_html(base=""):
    return f"""<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>{lockup_link(base, "logo sm", "footer-mark-slot")}</div>
      <div class="foot-col"><h4>Site</h4>
        <a href="{base}our-work/index.html">Our Work</a>
        <a href="{base}index.html#services">What We Do</a>
        <a href="{base}insights/index.html">Insights</a>
        <a href="{base}about-us/index.html">About Us</a>
        <a href="{base}careers/index.html">Careers</a>
        <a href="{base}contact/index.html">Contact</a>
      </div>
      <div class="foot-col"><h4>Trust</h4>
        <a href="{base}ai-policy/index.html">AI Policy</a>
        <a href="{base}privacy/index.html">Privacy Policy</a>
        <a href="{base}terms/index.html">Terms of Service</a>
      </div>
      <div class="foot-col"><h4>Socials</h4>
        <a href="https://www.linkedin.com/company/interceptagency/" target="_blank" rel="noopener">LinkedIn</a>
      </div>
    </div>
    <div class="foot-bot">
      <span>&copy; 2026 Intercept.</span>
      <span>Powered by curiosity.</span>
    </div>
  </div>
</footer>
{GLITCH_SOURCE_DEFS}
<script>{LOGO_GLITCH_JS}</script>"""

def head_html(title, description):
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:ital,wght@0,400;0,500;0,600;0,700;1,600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>"""
