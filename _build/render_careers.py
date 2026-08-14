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
.cred .ph{width:96px;height:96px;font-size:8px;margin-bottom:18px}
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
.chip{display:inline-flex;align-items:center;min-height:44px;font-size:var(--fs-7);font-weight:600;padding:0 16px;border-radius:99px;border:1px solid var(--line);color:var(--ink-2);cursor:pointer;transition:background .15s,color .15s,border-color .15s}
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

/* apply — Priority 3 #7: real form, same technique as render_contact.py
   (real inputs, a real custom select, client-side ack -- no backend/CRM
   exists, so nothing here pretends to submit anywhere real). */
.form{padding:34px 0 8px}
.fgrid{display:grid;grid-template-columns:1fr 1fr;gap:20px 24px;max-width:820px}
.fgrid .wide{grid-column:1 / -1}
.field{position:relative}
.field label{display:block;font-size:var(--fs-8);font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--ink-3);margin:0 0 7px}
.field input[type=text],.field input[type=email],.field input[type=tel],.field input[type=url],.field textarea{
  width:100%;box-sizing:border-box;border:1px solid var(--line);background:var(--page);height:46px;
  padding:0 14px;font-size:var(--fs-7);font-family:var(--font-body);color:var(--ink);
}
.field input:focus,.field textarea:focus,.select-btn:focus{outline:2px solid var(--flarepop-ink);outline-offset:2px}
.field textarea{height:120px;padding-top:13px;resize:vertical}
.select-btn{width:100%;box-sizing:border-box;border:1px solid var(--line);background:var(--page);height:46px;padding:0 14px;font-size:var(--fs-7);font-family:var(--font-body);color:var(--ink-3);display:flex;align-items:center;cursor:pointer;text-align:left}
.select-btn.chosen{color:var(--ink)}
.select-btn::after{content:'⌄';margin-left:auto;color:var(--ink-3);font-size:15px}
.select-btn[aria-expanded="true"]::after{content:'⌃'}
.req{color:var(--ink-3);font-weight:400;text-transform:none;letter-spacing:0}
.fsubmit{padding:26px 0 4px}
.menu{list-style:none;margin:0;padding:0;position:absolute;left:0;right:0;top:100%;z-index:5;border:1px solid var(--line);border-top:0;background:var(--page);box-shadow:0 8px 20px rgba(10,10,15,.08)}
.menu li{padding:11px 14px;font-size:var(--fs-7);color:var(--ink-2);border-top:1px solid var(--line);cursor:pointer}
.menu li:first-child{border-top:0}
.menu li:hover,.menu li.on{background:var(--band);color:var(--ink);font-weight:600}
.fsubmit .btn{border:0;cursor:pointer;font-family:inherit}
.fsent{display:none;padding:16px 18px;background:var(--band);border-left:3px solid var(--flarepop);font-size:var(--fs-7);color:var(--ink);margin-top:18px;max-width:820px}
.fsent.show{display:block}

@media(max-width:900px){
  .cred-row,.area-grid,.roles-cta-grid,.life-grid,.fgrid{grid-template-columns:1fr}
  a.role,.role-head{grid-template-columns:1fr;gap:6px}
  .role-head{display:none}
}
"""

# ---- data ----

CREDS = [
    # All 3 now real, personalized certification marks. B Corp sourced 2026-08-11 from
    # B Lab's official Wikimedia SVG (bcorporation.net). Great Place to Work + Chief
    # Marketer's "Agency of the Year" are personalized per company/period and can only
    # come from Intercept's own portal — Jon supplied both real files 2026-08-13
    # (~/Downloads/Badges.zip): Intercept's Aug 2025-Aug 2026 Canada GPTW certificate and
    # the Chief Marketer 2026 Honoree seal, trimmed to their own bbox and alpha-safely
    # resized into assets/img/badges/.
    ("Great Place to Work", "Certified seven years running. Protecting the culture through high growth.", "great-place-to-work.png"),
    ("Certified B Corp", "Measured on how we treat people and the planet, not only on what we deliver.", "bcorp.svg"),
    ("Agency of the Year", "Chief Marketer, 2025 and 2026, and counting.", "agency-of-the-year.png"),
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
    def cred_card(b, d, mark_file):
        if mark_file:
            # object-fit:contain (not the base img.ph cover) — these marks aren't square,
            # and GPTW's personalized cert text sits right at the top/bottom edges, so a
            # cover-crop in the 56x56 box would cut off the exact detail that makes it real.
            mark = f'<img class="ph" style="padding:6px;object-fit:contain" src="../assets/img/badges/{mark_file}" alt="{esc(b)}">'
        else:
            src, ratio = pc.next("4col", "../")
            mark = f'<img class="ph" style="aspect-ratio:{ratio}" src="{src}" alt="">'
        return f'<div class="cred">{mark}<b>{esc(b)}</b><span>{esc(d)}</span></div>'
    cred_html = "".join(cred_card(b, d, mark_file) for b, d, mark_file in CREDS)
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


APPLY_SCRIPT = """<script>
(function(){
  var btn = document.getElementById("heardToggle");
  var menu = document.getElementById("heardMenu");
  var label = document.getElementById("heardLabel");
  var value = document.getElementById("heardValue");
  if (!btn || !menu) return;

  function closeMenu(){ menu.hidden = true; btn.setAttribute("aria-expanded", "false"); }
  function openMenu(){ menu.hidden = false; btn.setAttribute("aria-expanded", "true"); }

  btn.addEventListener("click", function(e){
    e.stopPropagation();
    if (menu.hidden) openMenu(); else closeMenu();
  });
  menu.addEventListener("click", function(e){
    var li = e.target.closest("li"); if (!li) return;
    [].forEach.call(menu.querySelectorAll("li"), function(o){ o.classList.remove("on"); });
    li.classList.add("on");
    label.textContent = li.dataset.value;
    value.value = li.dataset.value;
    btn.classList.add("chosen");
    closeMenu();
  });
  document.addEventListener("click", function(e){
    if (!btn.contains(e.target) && !menu.contains(e.target)) closeMenu();
  });
  document.addEventListener("keydown", function(e){
    if (e.key === "Escape") closeMenu();
  });
})();
(function(){
  var sendBtn = document.getElementById("applyBtn");
  var sent = document.getElementById("fsent");
  var value = document.getElementById("heardValue");
  var first = document.getElementById("fFirstName");
  var last = document.getElementById("fLastName");
  var email = document.getElementById("fEmail");
  var location = document.getElementById("fLocation");
  var portfolio = document.getElementById("fPortfolio");
  if (!sendBtn) return;
  sendBtn.addEventListener("click", function(){
    var missing = [];
    if (!first.value.trim()) missing.push(first);
    if (!last.value.trim()) missing.push(last);
    if (!email.value.trim()) missing.push(email);
    if (!location.value.trim()) missing.push(location);
    if (!portfolio.value.trim()) missing.push(portfolio);
    if (!value.value) missing.push(document.getElementById("heardToggle"));
    if (missing.length){ missing[0].focus(); return; }
    sent.classList.add("show");
    sent.scrollIntoView({behavior: "smooth", block: "nearest"});
  });
})();
</script>"""


def render_apply():
    menu_html = "".join(f'<li data-value="{esc(o)}">{esc(o)}</li>' for o in HEARD_ABOUT_OPTIONS)

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
        <label for="fFirstName">First name</label>
        <input type="text" id="fFirstName" autocomplete="given-name">
      </div>
      <div class="field">
        <label for="fLastName">Last name</label>
        <input type="text" id="fLastName" autocomplete="family-name">
      </div>
      <div class="field">
        <label for="fEmail">Email</label>
        <input type="email" id="fEmail" autocomplete="email">
      </div>
      <div class="field">
        <label for="fPhone">Phone <span class="req">(optional)</span></label>
        <input type="tel" id="fPhone" autocomplete="tel">
      </div>
      <div class="field">
        <label for="fLocation">Where you are based</label>
        <input type="text" id="fLocation" placeholder="City and time zone">
      </div>
      <div class="field">
        <label for="fPortfolio">Portfolio or LinkedIn</label>
        <input type="url" id="fPortfolio" autocomplete="url" placeholder="https://">
      </div>
      <div class="field wide">
        <label for="fMore">Anything you want us to know <span class="req">(optional)</span></label>
        <textarea id="fMore"></textarea>
      </div>
      <div class="field wide">
        <label id="heardFieldLabel">How you heard about us</label>
        <button type="button" class="select-btn" id="heardToggle" aria-haspopup="listbox" aria-expanded="false"><span id="heardLabel">Select one</span></button>
        <ul class="menu" id="heardMenu" role="listbox" hidden>{menu_html}</ul>
        <input type="hidden" id="heardValue">
      </div>
    </div>
    <div class="fsubmit"><button type="button" class="btn" id="applyBtn">Submit application</button></div>
    <div class="fsent" id="fsent">Thanks — we&rsquo;ve received your application and will be in touch if there&rsquo;s a fit.</div>
  </div>
</section>

</main>
{footer_html("../../")}
{APPLY_SCRIPT}
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
