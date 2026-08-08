#!/usr/bin/env python3
"""Render the Contact page. Fields are real, working form controls (typeable
inputs, a real custom select) — per Jon's explicit direction (2026-08-08) to
make this one functional, unlike the rest of the site's visual-only mockups.
There's still no real backend/CRM (sitemap.html flags this page as needing
one), so submitting shows a client-side acknowledgment rather than pretending
data went somewhere real."""
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
.field{position:relative}
.field label{display:block;font-size:var(--fs-8);font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--ink-3);margin:0 0 7px}
.field input[type=text],.field input[type=email],.field textarea{
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

SCRIPT = """<script>
(function(){
  var btn = document.getElementById("connectToggle");
  var menu = document.getElementById("connectMenu");
  var label = document.getElementById("connectLabel");
  var value = document.getElementById("connectValue");
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
  var sendBtn = document.getElementById("sendBtn");
  var sent = document.getElementById("fsent");
  var value = document.getElementById("connectValue");
  var first = document.getElementById("fFirstName");
  var last = document.getElementById("fLastName");
  var email = document.getElementById("fEmail");
  if (!sendBtn) return;
  sendBtn.addEventListener("click", function(){
    var missing = [];
    if (!value.value) missing.push(document.getElementById("connectToggle"));
    if (!first.value.trim()) missing.push(first);
    if (!last.value.trim()) missing.push(last);
    if (!email.value.trim()) missing.push(email);
    if (missing.length){ missing[0].focus(); return; }
    sent.classList.add("show");
    sent.scrollIntoView({behavior: "smooth", block: "nearest"});
  });
})();
</script>"""

def render():
    base = "../"
    menu_html = "".join(f'<li data-value="{esc(o)}">{esc(o)}</li>' for o in CONNECT_OPTIONS)

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
        <label id="connectFieldLabel">What are you looking to connect about?</label>
        <button type="button" class="select-btn" id="connectToggle" aria-haspopup="listbox" aria-expanded="false"><span id="connectLabel">Select one</span></button>
        <ul class="menu" id="connectMenu" role="listbox" hidden>{menu_html}</ul>
        <input type="hidden" id="connectValue">
      </div>
      <div class="field">
        <label for="fFirstName">First name</label>
        <input type="text" id="fFirstName" autocomplete="given-name">
      </div>
      <div class="field">
        <label for="fLastName">Last name</label>
        <input type="text" id="fLastName" autocomplete="family-name">
      </div>
      <div class="field">
        <label for="fEmail">Work email</label>
        <input type="email" id="fEmail" autocomplete="email">
      </div>
      <div class="field">
        <label for="fCompany">Company</label>
        <input type="text" id="fCompany" autocomplete="organization">
      </div>
      <div class="field">
        <label for="fRole">Role <span class="req">(optional)</span></label>
        <input type="text" id="fRole" autocomplete="organization-title">
      </div>
      <div class="field">
        <label for="fLocation">Where you are based <span class="req">(optional)</span></label>
        <input type="text" id="fLocation" placeholder="City and country">
      </div>
      <div class="field wide">
        <label for="fMore">Tell us more</label>
        <textarea id="fMore"></textarea>
      </div>
    </div>
    <div class="fsubmit"><button type="button" class="btn" id="sendBtn">Send</button></div>
    <div class="fsent" id="fsent">Thanks — we&rsquo;ve got your note and will be in touch shortly.</div>
  </div>
</section>

</main>
{footer_html(base)}
{SCRIPT}
</body>
</html>"""

if __name__ == "__main__":
    outdir = os.path.join(ROOT, "contact")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "index.html")
    open(path, "w", encoding="utf-8").write(render())
    print("Wrote", path)
