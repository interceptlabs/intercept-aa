#!/usr/bin/env python3
"""Shared design-system pieces for InterceptAA: tokens, nav, footer, logo library."""
import json, os, re, html as _html

BUILD_DIR = os.path.dirname(os.path.abspath(__file__))

def esc(s):
    return _html.escape(s, quote=False) if s else ""

# case/hero image native dimensions (post-resize), used to set exact
# aspect-ratio per image so object-fit:cover never crops real content
IMG_DIMS = {
    "agents-of-change-card": (1600, 1172),
    "agents-of-change-hero": (1600, 700),
    "ai-in-practice-card": (1600, 1038),
    "ai-in-practice-hero": (1600, 700),
    "ai-under-the-influence-card": (1600, 1172),
    "ai-under-the-influence-hero": (1600, 700),
    "align-in-the-metaverse-card": (1600, 1172),
    "align-in-the-metaverse-hero": (1600, 700),
    "be-the-answer-card": (1600, 1172),
    "be-the-answer-hero": (1600, 700),
    "confidence-in-every-word-card": (1600, 1172),
    "confidence-in-every-word-hero": (1600, 700),
    "dev-zone-card": (1600, 1172),
    "dev-zone-hero": (1600, 700),
    "devbuilder-card": (1600, 1172),
    "devbuilder-hero": (1600, 700),
    "devhero-stories-card": (1600, 1172),
    "devhero-stories-hero": (1600, 700),
    "eyes-on-the-road-card": (1600, 1172),
    "eyes-on-the-road-hero": (1600, 700),
    "find-your-path-card": (1600, 1172),
    "find-your-path-hero": (1600, 700),
    "fly-with-dragonfly-card": (1600, 1172),
    "fly-with-dragonfly-hero": (1600, 700),
    "from-signal-to-sale-card": (1600, 1172),
    "from-signal-to-sale-hero": (1600, 700),
    "innovation-mavericks-card": (1600, 1172),
    "innovation-mavericks-hero": (1600, 700),
    "into-the-breach-card": (1600, 1172),
    "into-the-breach-hero": (1600, 700),
    "leading-in-the-era-of-ai-card": (1600, 1172),
    "leading-in-the-era-of-ai-hero": (1600, 700),
    "lights-camera-avatars-card": (1600, 1172),
    "lights-camera-avatars-hero": (1600, 700),
    "migrate-to-innovate-card": (1600, 1172),
    "migrate-to-innovate-hero": (1600, 700),
    "security-skilling-card": (1600, 1172),
    "security-skilling-hero": (1600, 1172),  # still no dedicated Figma hero art — falls back to card image
    "subscription-overload-card": (1600, 1172),
    "subscription-overload-hero": (1600, 700),
    "surface-experience-kits-card": (1600, 1172),
    "surface-experience-kits-hero": (1600, 700),
    "surface-pitch-perfect-card": (1600, 1172),
    "surface-pitch-perfect-hero": (1600, 700),
    "surface-show-and-go-card": (1600, 1172),
    "surface-show-and-go-hero": (1600, 700),
    "the-magic-of-metaphors-card": (1600, 1172),
    "the-magic-of-metaphors-hero": (1600, 700),
    "the-measure-of-a-marketer-card": (1600, 1172),
    "the-measure-of-a-marketer-hero": (1600, 700),
    "the-modern-office-card": (1600, 1172),
    "the-modern-office-hero": (1600, 700),
    "the-video-that-talks-back-card": (1600, 1172),
    "the-video-that-talks-back-hero": (1600, 700),
    "this-time-its-personal-card": (1600, 1172),
    "this-time-its-personal-hero": (1600, 700),
    "to-the-cloud-card": (1600, 1172),
    "to-the-cloud-hero": (1600, 700),
    "unbound-cfo-event-card": (1600, 1172),
    "unbound-cfo-event-hero": (1600, 700),
    "winning-future-smb-owners-card": (1600, 1172),
    "winning-future-smb-owners-hero": (1600, 700),
}

# team headshots (About Us), sourced from the same Figma file, 2026-08-11
TEAM_IMG_DIMS = {
    "andrew-au": (800, 586),
    "shaheen-yazdani": (800, 586),
    "francis-silva": (800, 586),
    "laura-white": (800, 586),
    "david-toto": (800, 586),
    "jeff-lewis": (800, 586),
}

# decorative truchet-pattern placeholders (Figma "Placeholder Images" page,
# eTHq3jbEbLog3PkmurOfDw), sized to match a slot's own grid column count —
# used for genuinely-empty image slots on insights/about-us/careers, cycling
# through the 3 brand colors so adjacent slots never repeat. Not for slots
# that will eventually hold a real logo/mark (those stay text placeholders).
PATTERN_DIMS = {
    "hero": (1600, 700),
    "2col": (1280, 830),
    "3col": (756, 554),
    "4col": (671, 490),
}
PATTERN_COLORS = ["flarepop", "coolsweep", "wiretree"]

class PatternCycler:
    def __init__(self):
        self.i = 0
    def next(self, size, base=""):
        color = PATTERN_COLORS[self.i % len(PATTERN_COLORS)]
        self.i += 1
        w, h = PATTERN_DIMS[size]
        return f'{base}assets/img/patterns/{size}-{color}.webp', f"{w}/{h}"


# Team members with a real sourced headshot (round 16 — see TEAM_IMG_DIMS
# above), keyed by normalized full name. Reused for ANY author-byline avatar
# sitewide (ebooks, articles, insights hub, trends briefs) — not just the
# about-us team grid this was originally sourced for. Round 17 found the
# same "generic pattern/placeholder instead of the person's real photo" bug
# recurring independently in 3 different render scripts (Shaheen Yazdani on
# the insights hub + Signals-from-the-Edge author box, Andrew Au on both
# eBooks + the Trends Brief byline) — centralizing the lookup here so a
# future 4th occurrence doesn't repeat the same miss.
TEAM_PHOTO_SLUGS = {
    "andrew au": "andrew-au",
    "shaheen yazdani": "shaheen-yazdani",
    "francis silva": "francis-silva",
    "laura white": "laura-white",
    "david toto": "david-toto",
    "jeff lewis": "jeff-lewis",
}

def author_avatar_html(name, base, css_class="ph"):
    """Real headshot <img> for a known team-member byline author, else None
    — caller falls back to a pattern placeholder rather than fabricating a
    photo for someone with no sourced image."""
    norm = re.sub(r"<[^>]+>", "", name or "").strip().lower()
    slug = TEAM_PHOTO_SLUGS.get(norm)
    if not slug:
        return None
    w, h = TEAM_IMG_DIMS[slug]
    return f'<img class="{css_class}" style="aspect-ratio:{w}/{h}" src="{base}assets/img/team/{slug}.webp" alt="{esc(name)}">'


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

# ChatB2B guest-wall logos, round 17: Andrew supplied real files at
# ~/Downloads/Logos-for-ChatB2B/ for the 7 guests that had no sourced vector
# (previously plain "brand-text" fallbacks). Moderne + Procom were supplied
# as clean SVGs and are lifted the same way as Intel/TD SYNNEX above (real
# vector, viewBox tightened to the artwork's own bounding box). The other 5
# (CGI/Google/Kaltura/Sophos/Veeam) were supplied as raster PNGs — kept as
# raster rather than hand-traced to vector (never redraw a supplied logo).
# Files processed into assets/img/logos/*.png (trimmed, transparent bg);
# veeam.png specifically was re-extracted from the source "chip cutout" art
# (the wordmark is a knock-out hole in a solid badge, not white-on-black
# text) via enclosed-hole flood-fill, discarding the badge entirely — a
# naive invert/threshold left a faint ghost of the badge's cut corner.
CLIENT_LOGOS["Moderne"] = _load_lifted("Moderne", "moderne_inner.txt", 22)
CLIENT_LOGOS["Procom"] = _load_lifted("Procom", "procom_inner.txt", 18)

def _load_raster(name, filename, height_px):
    return {"href": None, "svg": None, "img": f"assets/img/logos/{filename}", "img_h": height_px}

CLIENT_LOGOS["CGI"] = _load_raster("CGI", "cgi.png", 20)
CLIENT_LOGOS["Google"] = _load_raster("Google", "google.png", 26)
CLIENT_LOGOS["Kaltura"] = _load_raster("Kaltura", "kaltura.png", 22)
CLIENT_LOGOS["Sophos"] = _load_raster("Sophos", "sophos.png", 18)
CLIENT_LOGOS["Veeam"] = _load_raster("Veeam", "veeam.png", 18)

# Jon: unify the whole wall to the flat-black-and-white treatment every
# vector logo already had by construction (none of the 12 vector entries —
# Microsoft/HP/SAP/Lenovo/Qualcomm/AMD/Cisco/Nokia/Logitech/TELUS/BMC/Intel/
# TD SYNNEX/Moderne/Procom — ever specify a fill color; SVG defaults to
# black, and TELUS/BMC's explicit fill="currentColor" resolves to the same
# ink). The 4 raster logos below shipped with their real brand colors baked
# into the pixels (CGI red, Sophos blue, Google/Kaltura multicolor) — the
# only ones breaking the wall's consistency. Recolored in place to flat
# #000 with the original alpha channel untouched (shape/anti-aliasing
# preserved exactly, only hue removed) — originals kept at
# _build/_logo-color-backups/ (gitignored) if the real-color version is
# ever wanted elsewhere. Veeam needed no change — already a pure black
# silhouette from its round-17 extraction.

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

def client_logo_html(name, base=""):
    """Render a client logo (or text fallback) as an unlinked mono glyph for the wall/badges.
    base: relative path prefix to site root, needed only for raster (img) entries —
    vector entries are self-contained inline SVG and ignore it."""
    entry = CLIENT_LOGOS.get(name)
    if not entry:
        return f'<span class="brand-text">{esc(name)}</span>'
    if entry.get("svg"):
        return entry["svg"]
    if entry.get("img"):
        return (
            f'<img class="brand-img" src="{base}{entry["img"]}" alt="{esc(name)}" '
            f'style="height:{entry["img_h"]}px;width:auto;object-fit:contain">'
        )
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
  /* fs-1 is the one rung that needs to move on mobile: hero h1 at a fixed 56px
     hand-copied into 18 render scripts overflowed its grid cell at 390px
     (long unbroken words like "commoditized." forced the cell's auto
     min-width past the viewport, and body{overflow-x:clip} ate the excess
     silently, no scrollbar). Fixing the token here, once, cascades through
     every var(--fs-1) reference sitewide with zero per-script edits — CSS
     custom properties resolve at the point of use regardless of selector
     specificity, so this reaches inline styles and heavily-scoped rules
     alike. Linear scale: 34px at <=325px viewport, up to the full 56px by
     900px (the same width the g3/g2 card-grid breakpoint already uses),
     4vw+20px between. Judgment call: fs-2 (section h2, 40px) was left fixed
     — no h2 clipped in the audit, and the overflow-wrap safety net below
     covers it if a future long word ever does. */
  --fs-1:clamp(34px, 4vw + 20px, 56px); --fs-2:40px; --fs-3:24px; --fs-4:20px; --fs-5:18px; --fs-6:16px; --fs-7:14px; --fs-8:12px; --fs-data:56px;
}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth}
html,body{margin:0;overflow-x:clip;max-width:100%}
body{background:var(--page);color:var(--ink);font-family:var(--font-body);font-size:var(--fs-6);line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
img,svg{max-width:100%}
h1,h2,h3,h4{font-family:var(--font-display);font-weight:700;line-height:1.15;letter-spacing:-.02em;margin:0;text-wrap:balance;overflow-wrap:break-word}
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
/* Priority 2 #5: shared 44px touch-target rule -- flex+min-height rather than
   padding so it works regardless of each link's own line-height/font-size. */
.nav-links a{display:flex;align-items:center;min-height:44px}
.nav-links a:hover{color:var(--flarepop-ink)}
.nav-links .inert{color:var(--ink);opacity:.45;cursor:default}
.cta-nav{display:inline-flex;align-items:center;min-height:44px;background:var(--carbon-500);color:#fff;font-weight:600;font-size:var(--fs-7);padding:0 18px;border-radius:8px;transition:background .15s;flex:none}
.cta-nav:hover{background:var(--flarepop);color:var(--carbon-500)}
.nav-toggle{display:none;flex-direction:column;justify-content:center;gap:5px;width:44px;height:44px;padding:0;background:none;border:0;cursor:pointer;flex:none}
.nav-toggle span{display:block;width:100%;height:2px;background:var(--ink);transition:transform .18s,opacity .18s}
/* icon state change: 3 bars -> X while the drawer is open, so the control
   itself reflects open/closed instead of staying static (Priority 1 #2) */
.nav-toggle.is-open span:nth-child(1){transform:translateY(7px) rotate(45deg)}
.nav-toggle.is-open span:nth-child(2){opacity:0}
.nav-toggle.is-open span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}
/* scrim: sits under the drawer (which inherits the topbar's z-index:100
   stacking context) and above page content, and is the tap-to-close target —
   fixes "tappable-through while open" (Priority 1 #2). Page content behind
   it is also made inert (see NAV_TOGGLE_SCRIPT) so it's neither hit-testable
   nor reachable by keyboard/focus while the drawer is open. */
.nav-scrim{position:fixed;inset:0;z-index:90;background:rgba(10,10,15,.4);opacity:0;pointer-events:none;transition:opacity .18s}
.nav-scrim.open{opacity:1;pointer-events:auto}
@media(max-width:860px){
  .nav-toggle{display:flex}
  .nav-links{display:none}
  .nav-links.open{display:flex;position:absolute;top:100%;left:0;right:0;z-index:100;flex-direction:column;align-items:flex-start;gap:18px;background:var(--page);padding:22px 24px 26px;border-bottom:1px solid var(--line)}
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
img.ph{width:100%;height:auto;object-fit:cover;display:block;border:0;background:none;padding:0}

/* stat strip (the sanctioned data-viz default). Numeral voice is Instrument
   Sans display bold, not a separate mono "data" register — ties the figure
   to the same typographic voice as the headline above/around it instead of
   defaulting to the generic dashboard convention of a monospace numeral.
   Centered both as a row (within its band) and within each column. */
.stat-row{display:grid;grid-template-columns:repeat(3,1fr);gap:40px;text-align:center}
.stat b{display:block;font-family:var(--font-display);font-size:var(--fs-data);line-height:1;letter-spacing:-.03em;font-weight:700}
.stat span{display:block;font-size:var(--fs-7);line-height:1.45;margin:12px auto 0;opacity:.9;max-width:26ch}
@media(max-width:860px){.stat-row{grid-template-columns:1fr;gap:28px}}

/* cards */
.card-grid{display:grid;gap:24px}
.g3{grid-template-columns:repeat(3,1fr)}
.g2{grid-template-columns:repeat(2,1fr)}
@media(max-width:860px){.g3,.g2{grid-template-columns:1fr}}
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
/* Priority 2 #4: common.py's 3 shared breakpoints (nav 860 / stat-row+foot-grid
   820 / card-grid 900) did different component-level work at 3 different
   widths — consolidated onto 860, the most load-bearing one (nav already
   used it). stat-row and foot-grid now collapse a little sooner (820->860,
   an improvement: those grids were already tight at 821-860px); card-grid
   (g3/g2) now collapses a little later (900->860) — verified at 768/820/
   860/880/900 that no 3-col card-grid instance (our-work/article/ebook
   related-cards, home insights, services proof-cards) looks cramped sitting
   un-collapsed in the 861-900px range that used to be 1-col. */
@media(max-width:860px){.foot-grid{grid-template-columns:1fr 1fr;gap:24px 20px}}
"""

NAV_TOGGLE_SCRIPT = (
    "<script>\n"
    "(function(){\n"
    '  var t = document.getElementById("navToggle"), n = document.getElementById("navLinks");\n'
    "  if (!t || !n) return;\n"
    '  var header = t.closest(".topbar") || t.closest("header");\n'
    '  var scrim = document.createElement("div");\n'
    '  scrim.className = "nav-scrim";\n'
    '  scrim.setAttribute("id", "navScrim");\n'
    "  header.insertAdjacentElement('afterend', scrim);\n"
    "  function setOpen(open){\n"
    '    n.classList.toggle("open", open);\n'
    '    t.classList.toggle("is-open", open);\n'
    '    t.setAttribute("aria-expanded", open ? "true" : "false");\n'
    '    scrim.classList.toggle("open", open);\n'
    "    // Priority 1 #2: while the drawer is open, everything below the\n"
    "    // topbar is inert -- neither hit-testable (fixes tap-through) nor\n"
    "    // reachable by keyboard focus (fixes the missing focus trap) --\n"
    "    // regardless of what a given template puts between header and footer.\n"
    "    Array.prototype.forEach.call(document.body.children, function(el){\n"
    "      if (el === header || el === scrim) return;\n"
    "      if (open) { el.setAttribute('inert', ''); }\n"
    "      else { el.removeAttribute('inert'); }\n"
    "    });\n"
    "    if (open) {\n"
    '      var first = n.querySelector("a");\n'
    "      if (first) first.focus();\n"
    "    }\n"
    "  }\n"
    '  t.addEventListener("click", function(){\n'
    '    setOpen(!n.classList.contains("open"));\n'
    "  });\n"
    '  scrim.addEventListener("click", function(){ setOpen(false); });\n'
    '  document.addEventListener("keydown", function(e){\n'
    '    if (e.key === "Escape" && n.classList.contains("open")) { setOpen(false); t.focus(); }\n'
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
        <a href="{base}insights/chatb2b/index.html">ChatB2B Podcast</a>
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
