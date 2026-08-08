#!/usr/bin/env python3
"""Render the Contact page. Source is a purely visual, non-functional wireframe
(/Downloads/New Wire Frames/pages/contact.html) — every 'field' is a
<div class="field"><label>...</label><div class="input"></div></div>, the same
non-functional grammar as careers-apply.html. No real <form>/<input>/<select>;
nothing on this page submits. The 'what are you looking to connect about'
select is drawn open (matching the wireframe) so the option set stays visible
rather than only living in a build-team comment."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import esc, head_html, header_html, footer_html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = """
.fhero{padding:52px 0 8px}
.fhero h1{font-size:var(--fs-1);line-height:1.05;letter-spacing:-.03em;margin:0;font-weight:700}
.form{padding:34px 0 8px}
.fgrid{display:grid;grid-template-columns:1fr 1fr;gap:20px 24px;max-width:820px}
.fgrid .wide{grid-column:1 / -1}
.field label{display:block;font-size:var(--fs-8);font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--ink-3);margin:0 0 7px}
.field .input{border:1px solid var(--line);background:#fff;height:46px;display:flex;align-items:center;padding:0 14px;font-size:var(--fs-7);color:var(--ink-3)}
.field .input.area{height:120px;align-items:flex-start;padding-top:13px}
.field .input.select::after{content:'⌄';margin-left:auto;color:var(--ink-3);font-size:15px}
.req{color:var(--ink-3);font-weight:400;text-transform:none;letter-spacing:0}
.fsubmit{padding:26px 0 4px}
/* menu drawn open, matching the wireframe, so the option set the build
   team has to account for stays visible on the page rather than only
   living in a source comment */
.menu{border:1px solid var(--line);border-top:0;background:#fff;max-width:820px}
.menu span{display:block;padding:11px 14px;font-size:var(--fs-7);color:var(--ink-2);border-top:1px solid var(--line)}
.menu span:first-child{border-top:0;background:var(--band);color:var(--ink);font-weight:600}
@media(max-width:900px){.fgrid{grid-template-columns:1fr}}
"""

# verbatim option list from the wireframe's <div class="menu"> — read, not invented
CONNECT_OPTIONS = [
    "New project",
    "Intercept Labs",
    "Careers",
    "Press and media",
    "Partnerships",
    "Other",
]

def render():
    base = "../"
    menu_html = "".join(f"<span>{esc(o)}</span>" for o in CONNECT_OPTIONS)

    return f"""<!doctype html>
<html lang="en">
<head>
{head_html("Contact · Intercept", "Get in touch with Intercept about a new project, Intercept Labs, partnerships, press, or a role on the team.")}
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header_html(base)}
<main id="main">

<section class="fhero">
  <div class="wrap">
    <span class="eyebrow">Contact</span>
    <h1>Let&rsquo;s connect</h1>
  </div>
</section>

<section class="form">
  <div class="wrap">
    <div class="fgrid">
      <div class="field wide">
        <label>What are you looking to connect about?</label>
        <div class="input select">Select one</div>
        <div class="menu">{menu_html}</div>
      </div>
      <div class="field">
        <label>First name</label>
        <div class="input"></div>
      </div>
      <div class="field">
        <label>Last name</label>
        <div class="input"></div>
      </div>
      <div class="field">
        <label>Work email</label>
        <div class="input"></div>
      </div>
      <div class="field">
        <label>Company</label>
        <div class="input"></div>
      </div>
      <div class="field">
        <label>Role <span class="req">(optional)</span></label>
        <div class="input"></div>
      </div>
      <div class="field">
        <label>Where you are based <span class="req">(optional)</span></label>
        <div class="input">City and country</div>
      </div>
      <div class="field wide">
        <label>Tell us more</label>
        <div class="input area"></div>
      </div>
    </div>
    <div class="fsubmit"><span class="btn">Send</span></div>
  </div>
</section>

</main>
{footer_html(base)}
</body>
</html>"""

if __name__ == "__main__":
    outdir = os.path.join(ROOT, "contact")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "index.html")
    open(path, "w", encoding="utf-8").write(render())
    print("Wrote", path)
