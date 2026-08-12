#!/usr/bin/env python3
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import esc, head_html, header_html, footer_html, PatternCycler

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- shared page CSS (careers hub + open-roles listing + apply mockup) ----
# .ph / .eyebrow / .btn / .link / .card-grid already live in common.py — not redefined here.
CSS = """
/* hub: hero */
.chero{padding:64px 0 40px}
.chero-grid{display:grid;grid-template-columns:1.05fr 1fr;gap:56px;align-items:center}
.chero .ph{aspect-ratio:4/3}
.chero h1{font-size:var(--fs-1);line-height:1.05;letter-spacing:-.03em;margin:0 0 16px;max-width:16ch}
.chero p{font-size:var(--fs-5);line-height:1.45;color:var(--ink-2);margin:0 0 24px;max-width:52ch}
@media(max-width:900px){.chero-grid{grid-template-columns:1fr}}

/* hub: positioning band */
.pos{padding:52px 0;background:var(--band)}
.pos h2{font-size:var(--fs-2);line-height:1.18;letter-spacing:-.02em;margin:0;max-width:24ch}

/* hub: credentials */
.creds{padding:44px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.cred-row{display:grid;grid-template-columns:repeat(3,1fr);gap:32px}
.cred .ph{width:56px;height:56px;font-size:8px;margin-bottom:14px}
.cred b{display:block;font-size:var(--fs-6);letter-spacing:-.01em;margin-bottom:4px}
.cred span{display:block;font-size:var(--fs-7);line-height:1.45;color:var(--ink-2)}

/* hub: career areas */
.areas{padding:48px 0}
.areas h2{font-size:var(--fs-2);line-height:1.12;letter-spacing:-.026em;margin:0}
.area-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:28px;margin-top:26px}
.area .ph{aspect-ratio:4/3;margin-bottom:14px}
.area b{display:block;font-size:var(--fs-4);letter-spacing:-.012em;margin-bottom:6px}
.area span{display:block;font-size:var(--fs-7);line-height:1.5;color:var(--ink-2)}

/* hub: open-roles teaser */
.roles-cta{padding:52px 0;background:var(--band)}
.roles-cta-grid{display:grid;grid-template-columns:1fr 1.1fr;gap:48px;align-items:center}
.roles-cta h2{font-size:var(--fs-2);line-height:1.06;letter-spacing:-.03em;margin:0 0 16px}
.roles-cta p{font-size:var(--fs-6);color:var(--ink-2);margin:0 0 24px}

/* hub: life at intercept */
.life{padding:52px 0}
.life h2{font-size:var(--fs-2);line-height:1.12;letter-spacing:-.026em;margin:0}
.life-grid{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1fr);gap:24px;margin-top:26px}
.life-grid .ph:first-child{aspect-ratio:16/10}
.life-col{display:grid;gap:24px;min-width:0}
.life-col .ph{aspect-ratio:4/3;width:100%;min-width:0}

/* hub: conversion band — pattern lifted verbatim from render_about.py's own .convert */
.convert{padding:56px 0;background:var(--band);text-align:center}
.convert h2{font-size:var(--fs-2);line-height:1.08;letter-spacing:-.028em;margin:0 auto 20px;max-width:18ch}

/* breadcrumb (open-roles, apply) */
.crumb{border-bottom:1px solid var(--line);background:var(--band)}
.crumb-row{max-width:var(--maxw);margin:0 auto;padding:11px 32px;font-size:var(--fs-8);color:var(--ink-3)}
.crumb-row b{color:var(--ink);font-weight:600}

/* compact functional hero (open-roles, apply) */
.rhero,.fhero{padding:48px 0 32px}
.rhero h1,.fhero h1{font-size:var(--fs-1);line-height:1.04;letter-spacing:-.032em;margin:0 0 14px}
.rhero p,.fhero p{font-size:var(--fs-5);line-height:1.5;color:var(--ink-2);margin:0;max-width:52ch}

/* filters (real, filters .role rows by data-s discipline) */
.filters{padding:0 0 8px}
.filter-row{display:flex;flex-wrap:wrap;gap:10px;padding:22px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.chip{font-size:var(--fs-7);font-weight:600;padding:8px 16px;border-radius:99px;border:1px solid var(--line);color:var(--ink-2);cursor:pointer;transition:background .15s,color .15s,border-color .15s}
.chip:hover{border-color:var(--ink-3)}
.chip.on{background:var(--carbon-500);color:#fff;border-color:var(--carbon-500)}
.filter-note{font-size:var(--fs-8);color:var(--ink-3);padding:14px 0 0;margin:0}

/* role list */
.role-list{padding:8px 0 40px}
a.role{display:grid;grid-template-columns:2fr 1fr 1fr auto;gap:24px;align-items:center;padding:22px 0;border-bottom:1px solid var(--line);color:inherit;text-decoration:none;transition:background .15s}
a.role[hidden]{display:none}
a.role:hover{background:var(--band)}
.role h3{font-size:var(--fs-4);line-height:1.25;letter-spacing:-.015em;margin:0}
.role .meta{font-size:var(--fs-7);color:var(--ink-2)}
.role .type{font-size:var(--fs-8);color:var(--ink-3)}
.role .go{font-size:var(--fs-7);font-weight:600;white-space:nowrap;justify-self:end}
.role-head{display:grid;grid-template-columns:2fr 1fr 1fr auto;gap:24px;padding:16px 0 12px;border-bottom:1px solid var(--ink);font-size:var(--fs-8);color:var(--ink-3)}

/* no-fit CTA */
.nofit{padding:52px 0;background:var(--band)}
.nofit h2{font-size:var(--fs-2);line-height:1.08;letter-spacing:-.028em;margin:0 0 16px;max-width:20ch}
.nofit p{font-size:var(--fs-6);color:var(--ink-2);margin:0 0 24px;max-width:52ch}

/* apply — purely visual mockup fields, nothing here submits anywhere */
.form{padding:34px 0 8px}
.fgrid{display:grid;grid-template-columns:1fr 1fr;gap:20px 24px;max-width:820px}
.fgrid .wide{grid-column:1 / -1}
.field label{display:block;font-size:var(--fs-8);color:var(--ink-3);margin:0 0 7px;font-weight:600}
.field .input{border:1px solid var(--line);background:var(--page);height:46px;display:flex;align-items:center;padding:0 14px;font-size:var(--fs-7);color:var(--ink-3)}
.field .input.area{height:120px;align-items:flex-start;padding-top:13px}
.field .input.select{display:flex}
.field .input.select::after{content:'⌄';margin-left:auto;color:var(--ink-3);font-size:15px}
.req{color:var(--ink-3);font-weight:400}
.menu{border:1px solid var(--line);border-top:0;background:var(--page)}
.menu span{display:block;padding:11px 14px;font-size:var(--fs-7);color:var(--ink-2);border-top:1px solid var(--line)}
.menu span:first-child{border-top:0;background:var(--band);color:var(--ink);font-weight:600}

@media(max-width:900px){
  .cred-row,.area-grid,.roles-cta-grid,.life-grid,.fgrid{grid-template-columns:1fr}
  a.role,.role-head{grid-template-columns:1fr;gap:6px}
  .role-head{display:none}
}
"""

# ---- data ----

CREDS = [
    # Great Place to Work and Chief Marketer have no generic badge to source: GPTW's
    # certification mark is personalized per company/validation-period and only issued
    # through Intercept's own certification portal; Chief Marketer's "Agency of the Year"
    # is an editorial list placement with no downloadable seal at all. Both stay honest
    # text placeholders (same convention as Intuit's un-sourced logo) rather than a
    # fabricated mark. B Corp's mark IS a real, non-personalized certification badge
    # (bcorporation.net), sourced 2026-08-11 from B Lab's official Wikimedia asset.
    ("Great Place to Work", "Certified seven years running. Protecting the culture through high growth.", False),
    ("Certified B Corp", "Measured on how we treat people and the planet, not only on what we deliver.", True),
    ("Agency of the Year", "Chief Marketer, 2025 and 2026, and counting.", False),
]

AREAS = [
    ("Strategy", "Messaging, go-to-market, and the buyer research underneath both."),
    ("Content", "Thought leadership, technical writing, and content built for humans and agents."),
    ("Creative", "Art direction, design, copywriting, video, and 3D inside Intercept Studio."),
    ("Technology", "Building the agents, web apps, and platforms the rest of the agency runs on."),
    ("Client leadership", "Owning the relationship, the brief, and whether the work lands."),
    ("Operations", "HR, finance, and the operations that keep the whole team delivering."),
]

# title -> (discipline, slug) — slug table confirmed against every role file's own <h1> by the caller
ROLES = [
    ("Director, Content", "Content", "director-content"),
    ("Senior Editorial Manager", "Content", "senior-editorial-manager"),
    ("Sr. Copywriter", "Content", "senior-copywriter"),
    ("Sr. Account Manager", "Client leadership", "senior-account-manager"),
    ("Account Manager", "Client leadership", "account-manager"),
    ("Account Associate", "Client leadership", "account-associate"),
    ("Graphic Designer, UI-UX", "Creative", "graphic-designer-ui-ux"),
    ("Graphic Designer", "Creative", "graphic-designer"),
    ("Integrated Producer", "Operations", "integrated-producer"),
]

HEARD_ABOUT_OPTIONS = [
    "LinkedIn",
    "Referral from someone at Intercept",
    "Job board",
    "Our website",
    "Event or podcast",
    "Other",
]


def render_hub():
    pc = PatternCycler()
    def cred_card(b, d, has_mark):
        if has_mark:
            mark = '<img class="ph" style="padding:8px" src="../assets/img/badges/bcorp.svg" alt="Certified B Corporation">'
        else:
            src, ratio = pc.next("4col", "../")
            mark = f'<img class="ph" style="aspect-ratio:{ratio}" src="{src}" alt="">'
        return f'<div class="cred">{mark}<b>{esc(b)}</b><span>{esc(d)}</span></div>'
    cred_html = "".join(cred_card(b, d, has_mark) for b, d, has_mark in CREDS)
    def area_card(b, d):
        src, ratio = pc.next("3col", "../")
        return f'<div class="area"><img class="ph" style="aspect-ratio:{ratio}" src="{src}" alt=""><b>{esc(b)}</b><span>{esc(d)}</span></div>'
    area_html = "".join(area_card(b, d) for b, d in AREAS)
    chero_src, chero_ratio = pc.next("2col", "../")
    rolescta_src, rolescta_ratio = pc.next("2col", "../")
    life1_src, life1_ratio = pc.next("2col", "../")
    life2_src, life2_ratio = pc.next("4col", "../")
    life3_src, life3_ratio = pc.next("4col", "../")

    return f"""<!doctype html>
<html lang="en">
<head>
{head_html("Careers · Intercept", "We are a global team working with the largest enterprise technology companies in the world, on the hardest frontier marketing problems.")}
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header_html("../")}
<main id="main">

<section class="chero">
  <div class="wrap"><div class="chero-grid">
    <div>
      <span class="eyebrow">Careers</span>
      <h1>Come work at the frontier</h1>
      <p>We are a global team working with the largest enterprise technology companies in the world, on the hardest frontier marketing problems.</p>
      <a class="link" href="open-roles/index.html">See open roles</a>
    </div>
    <img class="ph" style="aspect-ratio:{chero_ratio}" src="{chero_src}" alt="">
  </div></div>
</section>

<section class="pos">
  <div class="wrap">
    <span class="eyebrow">Who does well here</span>
    <h2>We hire people who are curious, and unconvinced that how it has always been done is how it should be done.</h2>
  </div>
</section>

<section class="creds">
  <div class="wrap">
    <div class="cred-row">{cred_html}</div>
  </div>
</section>

<section class="areas">
  <div class="wrap">
    <h2>Where you could sit</h2>
    <div class="area-grid">{area_html}</div>
  </div>
</section>

<section class="roles-cta">
  <div class="wrap">
    <div class="roles-cta-grid">
      <div>
        <h2>We are hiring now</h2>
        <p>Roles open across strategy, creative, technology, and client leadership, all remote. If none of these call out to you, apply anyway and tell us where your superpower is.</p>
        <a class="btn" href="open-roles/index.html">See open roles</a>
      </div>
      <img class="ph" style="aspect-ratio:{rolescta_ratio}" src="{rolescta_src}" alt="">
    </div>
  </div>
</section>

<section class="life">
  <div class="wrap">
    <h2>Life at Intercept</h2>
    <div class="life-grid">
      <img class="ph" style="aspect-ratio:{life1_ratio}" src="{life1_src}" alt="">
      <div class="life-col">
        <img class="ph" style="aspect-ratio:{life2_ratio}" src="{life2_src}" alt="">
        <img class="ph" style="aspect-ratio:{life3_ratio}" src="{life3_src}" alt="">
      </div>
    </div>
  </div>
</section>

<section class="convert">
  <div class="wrap read">
    <span class="eyebrow">Start the conversation</span>
    <h2>Give us a hard problem. Let&rsquo;s solve it together.</h2>
    <a class="btn" href="../contact/index.html">Connect with an expert</a>
  </div>
</section>

</main>
{footer_html("../")}
</body>
</html>"""


def render_open_roles():
    role_html = "".join(
        f'<a class="role" data-s="{esc(disc)}" href="{slug}/index.html"><h3>{esc(title)}</h3>'
        f'<span class="meta">{esc(disc)}</span><span class="type">Full-time · Remote</span>'
        f'<span class="go link">View</span></a>'
        for title, disc, slug in ROLES
    )
    # discipline chips in first-seen order (not alphabetical)
    seen = []
    for _, disc, _ in ROLES:
        if disc not in seen:
            seen.append(disc)
    disciplines = seen
    chips_html = '<span class="chip on" data-f="">All roles</span>' + "".join(
        f'<span class="chip" data-f="{esc(d)}">{esc(d)}</span>' for d in disciplines
    )

    return f"""<!doctype html>
<html lang="en">
<head>
{head_html("Open Roles · Intercept", "Nine open roles across strategy, content, creative, technology, client leadership, and operations at Intercept, all remote.")}
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header_html("../../")}
<main id="main">

<div class="crumb"><div class="crumb-row">Careers · <b>Open roles</b></div></div>

<section class="rhero">
  <div class="wrap">
    <span class="eyebrow">Careers</span>
    <h1>Open roles</h1>
  </div>
</section>

<section class="filters">
  <div class="wrap">
    <div class="filter-row">{chips_html}</div>
    <p class="filter-note" id="filterNote">{len(ROLES)} open roles</p>
  </div>
</section>

<section class="role-list">
  <div class="wrap">
    <div class="role-head"><span>Role</span><span>Discipline</span><span>Type</span><span></span></div>
    <div id="roleList">{role_html}</div>
  </div>
</section>
<script>
(function(){{
  var list = document.getElementById("roleList");
  var roles = [].slice.call(list.querySelectorAll(".role"));
  var note = document.getElementById("filterNote");
  document.querySelector(".filter-row").addEventListener("click", function(e){{
    var chip = e.target.closest(".chip"); if(!chip) return;
    [].forEach.call(document.querySelectorAll(".chip"), function(c){{ c.classList.remove("on"); }});
    chip.classList.add("on");
    var filter = chip.dataset.f || "";
    var shown = 0;
    roles.forEach(function(r){{
      var match = !filter || r.dataset.s === filter;
      r.hidden = !match;
      if (match) shown++;
    }});
    note.textContent = shown + (shown === 1 ? " open role" : " open roles");
  }});
}})();
</script>

<section class="nofit">
  <div class="wrap read">
    <h2>None of these call out to you?</h2>
    <p>Apply anyway and tell us where your superpower is, and which role you think would use it best.</p>
    <a class="btn" href="../apply/index.html">Send us your work</a>
  </div>
</section>

</main>
{footer_html("../../")}
</body>
</html>"""


def render_apply():
    menu_html = "".join(f"<span>{esc(o)}</span>" for o in HEARD_ABOUT_OPTIONS)

    return f"""<!doctype html>
<html lang="en">
<head>
{head_html("Apply · Intercept", "Tell us which role you are after and show us your work.")}
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header_html("../../")}
<main id="main">

<div class="crumb"><div class="crumb-row">Careers · Open roles · <b>Apply</b></div></div>

<section class="fhero">
  <div class="wrap">
    <span class="eyebrow">Careers</span>
    <h1>Apply</h1>
    <p>Tell us which role you are after and show us your work.</p>
  </div>
</section>

<section class="form">
  <div class="wrap">
    <div class="fgrid">
      <div class="field">
        <label>First name</label>
        <div class="input"></div>
      </div>
      <div class="field">
        <label>Last name</label>
        <div class="input"></div>
      </div>
      <div class="field">
        <label>Email</label>
        <div class="input"></div>
      </div>
      <div class="field">
        <label>Phone <span class="req">(optional)</span></label>
        <div class="input"></div>
      </div>
      <div class="field">
        <label>Where you are based</label>
        <div class="input">City and time zone</div>
      </div>
      <div class="field">
        <label>Portfolio or LinkedIn</label>
        <div class="input">https://</div>
      </div>
      <div class="field wide">
        <label>Anything you want us to know <span class="req">(optional)</span></label>
        <div class="input area"></div>
      </div>
      <div class="field wide">
        <label>How you heard about us</label>
        <div class="input select">Select one</div>
        <div class="menu">{menu_html}</div>
      </div>
    </div>
  </div>
</section>

</main>
{footer_html("../../")}
</body>
</html>"""


if __name__ == "__main__":
    targets = [
        (os.path.join(ROOT, "careers"), render_hub),
        (os.path.join(ROOT, "careers", "open-roles"), render_open_roles),
        (os.path.join(ROOT, "careers", "apply"), render_apply),
    ]
    for outdir, fn in targets:
        os.makedirs(outdir, exist_ok=True)
        path = os.path.join(outdir, "index.html")
        open(path, "w", encoding="utf-8").write(fn())
        print("Wrote", path)
