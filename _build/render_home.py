#!/usr/bin/env python3
"""Render index.html — the InterceptAA homepage, built from the v2 wireframe IA."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import esc, head_html, header_html, footer_html, client_logo_html

BUILD_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BUILD_DIR)
CASES = json.load(open(os.path.join(BUILD_DIR, "cases.json"), encoding="utf-8"))
BY_SLUG = {c["slug"]: c for c in CASES}

HOME_CSS = """
.hero-band{background:var(--carbon-500);color:#fff;padding:0;overflow:hidden}
.hero-flex{display:flex;align-items:stretch;height:min(85vh,720px);min-height:480px}
.hero-card{flex:1 1 auto;min-width:0;display:flex;align-items:center;justify-content:center;padding:0 min(8vw,96px)}
.hero-card-inner{max-width:520px}
.hero-card .eyebrow{color:var(--flarepop);margin-bottom:20px}
.hero-card h1{font-size:var(--fs-1);line-height:1.02;letter-spacing:-.03em;color:#fff;margin:0 0 20px}
.hero-card p.sub{font-size:var(--fs-5);line-height:1.55;color:var(--halo-500);margin:0 0 24px;max-width:44ch}
.hero-card .btn{background:transparent;border:1.5px solid var(--flarepop);color:#fff}
.hero-card .btn:hover{background:var(--flarepop);color:var(--carbon-500);border-color:var(--flarepop)}

.hero-video-wrap{position:relative;flex:none;height:100%;aspect-ratio:4/3;background:var(--carbon-400)}
.hero-video-wrap video{display:block;width:100%;height:100%;object-fit:cover}

/* headline "Intercept" morphs into an arrow while the video's closing
   sting is on screen, reverting on native loop restart — see STING_START
   in HERO_SCRIPT below; keep in sync with the reel's own cut point.
   Segmented-relay treatment (2026-08-08, replacing the old single
   continuous-shaft version): 5 discrete dashes fire left-to-right, each a
   fixed step on the existing Halo/500->Halo/100 scale (grey floor to full
   Halo white) rather than one flat white shaft — banded/stepped, not a
   gradient, using only already-locked tokens. Head is a separate element
   (not one SVG with the segments) so it keeps an equilateral shape
   regardless of how the flex row divides --arrow-w. */
.headline-word{position:relative;display:inline-block}
.headline-word .word-text{display:inline-block;transition:opacity .3s ease}
.headline-word .word-arrow{position:absolute;left:0;top:0;height:100%;width:var(--arrow-w,2.2em);opacity:0;transition:opacity .25s ease;pointer-events:none;display:flex;align-items:center;gap:5px}
.arrow-seg{flex:1 1 0;height:18px;border-radius:2px;transform:scaleX(0);transform-origin:left center;transition:transform .16s cubic-bezier(.4,0,.2,1)}
.arrow-seg:nth-child(1){background:var(--halo-500);transition-delay:0ms}
.arrow-seg:nth-child(2){background:var(--halo-400);transition-delay:70ms}
.arrow-seg:nth-child(3){background:var(--halo-300);transition-delay:140ms}
.arrow-seg:nth-child(4){background:var(--halo-200);transition-delay:210ms}
.arrow-seg:nth-child(5){background:var(--halo-100);transition-delay:280ms}
.arrow-head{flex:0 0 auto;width:0;height:0;border-top:22px solid transparent;border-bottom:22px solid transparent;border-left:38px solid var(--halo-100);opacity:0;transition:opacity .16s ease .38s}
.headline-word.sting-active .word-text{opacity:0}
.headline-word.sting-active .word-arrow{opacity:1}
.headline-word.sting-active .arrow-seg{transform:scaleX(1)}
.headline-word.sting-active .arrow-head{opacity:1}

@media(max-width:860px){
  .hero-flex{flex-direction:column;height:auto;min-height:0}
  .hero-card{padding:56px 20px 32px;width:100%}
  .hero-card-inner{max-width:none}
  .hero-video-wrap{width:100%;height:auto;aspect-ratio:16/10}
  .headline-word .word-arrow{display:none}
  .headline-word .word-text{opacity:1!important}
}

.pos{padding:64px 0}
.pos h2{font-size:var(--fs-2);line-height:1.2;letter-spacing:-.02em;width:50%}
/* Line-by-line reveal: JS (LEDE_REVEAL_SCRIPT) splits the balanced h2 into
   one .line-wrap per rendered line, each shrunk to its own text width
   (width:max-content, not the full h2 box) so overflow:hidden actually
   masks the slide — a wrapper as wide as the h2 itself would never clip a
   translateX offset that small. Revealed state toggles on the SECTION
   (#services-lede.revealed), not per line, so a resize-triggered rebuild
   (line groupings shift because h2 width is 50%, not fixed) never re-plays
   the animation: fresh .line-inner spans inherit the already-revealed CSS
   state on creation with no transition, since nothing changed after paint. */
#services-lede h2 .line-wrap{display:block;width:max-content;overflow:hidden}
#services-lede h2 .line-inner{display:inline-block;transform:translateX(48px);opacity:0;transition:transform .8s cubic-bezier(.22,.61,.36,1),opacity .8s ease}
#services-lede.revealed h2 .line-inner{transform:translateX(0);opacity:1}
@media(max-width:860px){.pos h2{width:100%}}

.logos{padding:44px 0}
.logos .lbl{text-align:center;font-size:var(--fs-8);font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--ink-3);margin:0 0 28px}
.logo-row{display:grid;grid-template-columns:repeat(6,1fr);gap:24px;align-items:center;justify-items:center}
.logo-row.row2{grid-template-columns:repeat(7,1fr);margin-top:24px}
.logo-row .brand,.logo-row .brand-text{fill:var(--ink-2);color:var(--ink-2);opacity:.82}
.brand-text{font-family:var(--font-body);font-weight:700}
@media(max-width:820px){.logo-row,.logo-row.row2{grid-template-columns:repeat(3,1fr);gap:22px}}

.work-sec{padding:72px 0 80px}
.sec-head{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:32px;gap:24px}
.sec-head h2{font-size:var(--fs-2);letter-spacing:-.025em}
.feat{display:grid;grid-template-columns:1.5fr 1fr;gap:40px;align-items:center;margin-bottom:48px}
.feat img.ph{aspect-ratio:1600/1037}
.feat-body h3{font-size:var(--fs-3);letter-spacing:-.02em;margin:0 0 14px}
.feat-body p{font-size:var(--fs-6);line-height:1.55;margin:0 0 18px;color:var(--ink-2)}
.tier2{display:grid;grid-template-columns:1fr 1fr;gap:28px;margin-bottom:28px;align-items:start}
.tier2 img.ph{aspect-ratio:1600/919}
.tier2 h3{font-size:var(--fs-3)}
.tier3{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;align-items:start}
.tier3 img.ph{aspect-ratio:1600/1172}
@media(max-width:900px){.feat,.tier2{grid-template-columns:1fr}.tier3{grid-template-columns:1fr}}

.stats-sec{padding:56px 0}

.svc{padding:72px 0 80px}
.svc h2{font-family:var(--font-body);font-weight:600;font-size:var(--fs-6);letter-spacing:0;color:var(--ink);margin:0 0 20px}
.svc-list{margin-top:20px;display:flex;flex-direction:column;gap:26px}
.svc-list .row{display:block;font-family:var(--font-display);font-weight:700;font-size:var(--fs-2);letter-spacing:-.02em}
.svc-list .row:hover{color:var(--flarepop-ink)}
.icard{display:block}

.labs{padding:68px 0 76px;background:var(--band)}
.labs-grid{display:grid;grid-template-columns:1fr 1.15fr;gap:48px;align-items:center}
.labs-grid h2{font-size:var(--fs-3);line-height:1.25;letter-spacing:-.015em;max-width:26ch}
.labs-grid img.ph{aspect-ratio:1600/1037}
@media(max-width:860px){.labs-grid{grid-template-columns:1fr}}

.ins{padding:72px 0 80px}
.ins .card-grid{align-items:start}
.icard{border:1px solid var(--line)}
.icard img.ph{aspect-ratio:1600/1172;border-bottom:1px solid var(--line)}
.icard .body{padding:18px}
.icard .kicker{font-size:var(--fs-8);font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--ink-3);margin-bottom:8px}
.icard h3{font-size:var(--fs-4);line-height:1.32;margin:0 0 8px}
.icard p{font-size:var(--fs-7);line-height:1.5;color:var(--ink-2)}

.faq-sec{padding:72px 0 80px}
.faq-sec h2{font-size:var(--fs-2);letter-spacing:-.025em;margin-bottom:8px}
.faq-item{padding:22px 0}
.faq-item summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:20px;font-family:var(--font-display);font-weight:600;font-size:var(--fs-4)}
.faq-item summary::-webkit-details-marker{display:none}
.faq-item summary::after{content:'+';font-family:var(--font-body);font-weight:400;font-size:var(--fs-3);color:var(--ink-3);flex:none}
.faq-item[open] summary::after{content:'\\2013'}
.faq-a{padding:14px 0 0;font-size:var(--fs-6);line-height:1.6;color:var(--ink-2);max-width:70ch}

.team{padding:72px 0 80px;background:var(--band)}
.team-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:32px 28px;margin-top:28px;align-items:start}
.person img.ph{aspect-ratio:1600/1172;margin-bottom:14px}
.person b{display:block;font-size:var(--fs-6);font-weight:700}
.person span{display:block;font-size:var(--fs-8);color:var(--ink-3);margin-top:2px}
@media(max-width:820px){.team-grid{grid-template-columns:1fr 1fr}}

.contact{padding:80px 0;text-align:center}
.contact h2{font-size:var(--fs-2);line-height:1.1;letter-spacing:-.025em;margin:0 auto 18px;max-width:20ch}
.contact p{font-size:var(--fs-6);color:var(--ink-2);margin:0 auto 26px}
"""

HERO_SCRIPT = """<script>
(function(){
  var word = document.getElementById("stingWord"), videoWrap = document.querySelector(".hero-video-wrap");
  var inner = document.querySelector(".hero-card-inner");
  if (!word || !videoWrap || !inner) return;

  function updateLayout(){
    inner.style.transform = "";
    if (window.innerWidth <= 860) { word.style.removeProperty("--arrow-w"); return; }
    var videoRect = videoWrap.getBoundingClientRect();
    var wordRect = word.getBoundingClientRect();

    // arrow grows from the headline to the video panel's left edge
    var arrowTarget = videoRect.left - wordRect.left;
    if (arrowTarget > 0) word.style.setProperty("--arrow-w", arrowTarget + "px");

    // "Intercept" baseline aligns to where the reel's own wordmark sits in
    // frame (~50.5% of the video's height, measured against InterceptSting's
    // centered lockup — same reference point as the rest of this file's
    // best-effort, single-viewport alignment math)
    var targetY = videoRect.top + videoRect.height * 0.505;
    var currentCenterY = wordRect.top + wordRect.height / 2;
    inner.style.transform = "translateY(" + (targetY - currentCenterY) + "px)";
  }
  updateLayout();
  window.addEventListener("load", updateLayout);
  window.addEventListener("resize", updateLayout);
})();
(function(){
  var v = document.getElementById("heroVideo"), word = document.getElementById("stingWord");
  if (!v || !word) return;
  var STING_START = 30.73;
  var wasActive = false;
  v.addEventListener("timeupdate", function(){
    var active = v.currentTime >= STING_START;
    word.classList.toggle("sting-active", active);
    if (active && !wasActive) {
      // replay the existing nav glitch-lockup in sync with the sting —
      // reuses initLockup()'s own play(), no new effect
      document.querySelectorAll("[data-fritz-hover-lockup]").forEach(function(el){
        el.dispatchEvent(new Event("mouseenter"));
      });
    }
    wasActive = active;
  });
})();
</script>"""

LEDE_REVEAL_SCRIPT = """<script>
(function(){
  var h2 = document.querySelector("#services-lede h2");
  var section = document.getElementById("services-lede");
  if (!h2 || !section) return;
  var STAGGER_MS = 110;
  var words = h2.textContent.trim().split(/\\s+/);

  function layoutLines(){
    // Pass 1: plain inline word spans — let the browser's own text-wrap:balance
    // (h2's shared default) decide where lines break at the CURRENT width,
    // since h2 is 50% of the section and that width changes with the window.
    h2.innerHTML = words.map(function(w){ return "<span class=\\"lw\\">" + w + "</span>"; }).join(" ");
    var wordEls = [].slice.call(h2.querySelectorAll(".lw"));
    var lines = [];
    var lastTop = null;
    wordEls.forEach(function(el){
      var top = el.offsetTop;
      if (lastTop === null || Math.abs(top - lastTop) > 2){
        lines.push([]);
        lastTop = top;
      }
      lines[lines.length - 1].push(el.textContent);
    });

    // Pass 2: rebuild as one block-level, own-width wrapper per line so
    // overflow:hidden actually masks the translateX-from-the-right slide
    // (a wrapper as wide as the whole h2 would never clip a 48px offset).
    h2.innerHTML = lines.map(function(lineWords, i){
      return "<span class=\\"line-wrap\\"><span class=\\"line-inner\\" style=\\"transition-delay:" + (i * STAGGER_MS) + "ms\\">" + lineWords.join(" ") + "</span></span>";
    }).join("");
  }

  layoutLines();
  // re-run once webfonts swap in — Instrument Sans loads with font-display:swap,
  // and the fallback font's metrics can group words into the wrong line
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(layoutLines);

  var resizeTimer;
  window.addEventListener("resize", function(){
    clearTimeout(resizeTimer);
    // rebuilding is safe even after reveal: the section already carries
    // .revealed, so freshly-created .line-inner spans compute straight to
    // the revealed end-state on insertion — nothing to transition from,
    // so no replay
    resizeTimer = setTimeout(layoutLines, 150);
  });

  var obs = new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      if (entry.isIntersecting){
        section.classList.add("revealed");
        obs.unobserve(section);
      }
    });
  }, {threshold: 0.35});
  obs.observe(section);
})();
</script>"""

def case_teaser(slug, fallback_title=None, fallback_sub=None, aspect="4/3", client_label=None):
    c = BY_SLUG.get(slug)
    if c:
        href = f"our-work/{slug}/index.html"
        title, desc, client = c["short_title"], c["sub"], c["client_display"]
    else:
        href = "our-work/index.html"
        title, desc, client = fallback_title, fallback_sub, client_label or ""
    return href, title, desc, client

def render():
    # ---- work tiers ("ai-in-practice" used to be a dangling reference with no
    #      source file; the new wireframe set gave it a real case, so it's a
    #      real case_teaser() lookup now, not a hand-written fallback ----
    feat_href, feat_title, feat_desc, feat_client = case_teaser("ai-in-practice")
    t2a = case_teaser("the-measure-of-a-marketer")
    t2b = case_teaser("lights-camera-avatars")
    t3a = case_teaser("the-magic-of-metaphors")
    t3b = case_teaser("agents-of-change")
    t3c = case_teaser("be-the-answer")

    def tier_card(item, img_slug):
        href, title, desc, client = item
        return f"""<a class="card" href="{href}"><img class="ph" src="assets/img/homepage/{img_slug}.webp" alt="{esc(client)} — {esc(title)}"><h3>{esc(title)}</h3><p>{esc(desc)}</p></a>"""

    logos_row1 = "".join(f'<span>{client_logo_html(n)}</span>' for n in ["Microsoft","SAP","HP","Lenovo","Cisco","AMD"])
    logos_row2 = "".join(f'<span>{client_logo_html(n)}</span>' for n in ["Qualcomm","Logitech","Nokia","TELUS","Staples","BMC","Intel"])

    services = [
        ("Strategy", "what-we-do/strategy-planning/index.html"), ("Content", "what-we-do/content/index.html"),
        ("Creative", "what-we-do/creative/index.html"), ("Digital Media", "what-we-do/digital-media/index.html"),
        ("Channel", "what-we-do/channel/index.html"), ("Sales Enablement", "what-we-do/sales-enablement/index.html"),
    ]
    services_html = "".join(f'<a class="row" href="{href}">{s}</a>' for s, href in services)

    # verbatim from the wireframe's FAQ (homepage.html) — richer/AEO-oriented
    # copy than the round-1 build, per Round 8 site-reflow pass
    faqs = [
        ("What is Intercept?", "Intercept is the frontier B2B marketing agency for global technology companies. Our AI-native delivery model pairs codified agency expertise with AI-assisted workflows to make the keep-the-lights-on campaign work more efficient, freeing our clients to reallocate budget and team capacity toward the frontier innovation that redefines the buyer experience. We work with some of the largest technology companies in the world, including Microsoft, SAP, Intel, Lenovo, and Cisco."),
        ("What is Intercept Labs?", "Intercept Labs is the agency’s innovation engine and co-investment vehicle for enterprise tech clients exploring novel AI-driven marketing approaches. Labs partners with clients to prototype solutions before proving full viability, sharing the risk on experiments that need a partner. The model is built for the marketing leaders running ahead of the curve, not waiting for the category to settle."),
        ("What makes Intercept different?", "Three things separate Intercept from legacy and generalist agencies. First, AI-native delivery: legacy agencies still sell hours and deliverables, while Intercept’s operating model is built on codified agency expertise paired with AI-assisted workflows that produce better outcomes in less time. Second, proprietary intelligence: our Watchtower platform reads 20 million individuals globally and feeds a continuous audience-intelligence loop that sharpens every campaign decision before it ships. Third, enterprise-grade execution: 95% of our work runs internationally across 20+ languages, with established privacy, legal, and procurement review processes that meet the standards of the world’s largest technology companies."),
        ("What kinds of challenges do you help solve?", "We take on the programs where marketing has to move a business number that leadership is watching. Three archetypes come up repeatedly. The first is a category shift, when a brand's market has moved and the positioning that worked five years ago no longer holds. The second is a pipeline program measured against a controlled test, where the campaign has to prove incremental deal size or revenue against a matched holdout. The third is a scale problem that AI now solves, whether personalization, versioning, or enablement work that once required an army of humans and now runs on codified AI workflows across over 20 languages."),
        ("How do you handle security, privacy, and compliance?", "Compliance is built into our delivery model, not handled as an afterthought. Our team works alongside each client’s privacy, legal, and procurement teams to translate what innovation means in their regulatory context, runs intake reviews on data handling and tooling, and operates agentic QA layers, codified review processes paired with AI-assisted pattern matching, to maintain consistent quality at scale. The result is that marketing leaders who bring Intercept in earn a reputation as trailblazers who protect the business, not as a risk vector to their security and procurement peers. Our public AI policy documents these standards in detail for client and procurement review. This discipline is what makes enterprise-grade AI work viable for clients in regulated industries."),
        ("Who are your clients?", "Global technology companies. Named clients include Microsoft, SAP, HP, Intel, Lenovo, Cisco, AMD, Qualcomm, Logitech, Nokia, TELUS, BMC, and Staples. Roughly 90% of our work runs across international markets, and client relationships average nine years. Several of our largest programs have been running with the same buyer teams for more than a decade, which is how we developed the pattern recognition that shortens time-to-launch on new engagements."),
        ("What industries do you work in?", "B2B technology, as a discipline. Silicon and semiconductors, hyperscale cloud, enterprise software, networking infrastructure, OEM hardware, telecom, and channel-heavy technology categories. Our buyer is the enterprise IT, marketing, finance, or line-of-business leader who has to defend a purchasing decision inside a Fortune 100 governance model. That specificity is why our operating model is built with enterprise privacy, legal, and procurement review baked in from day one, rather than added on later."),
        ("How do I get started?", "Reach out through the contact form. Pick the enquiry type that fits (new project, Intercept Labs, partnerships, or press) and a senior member of our team responds directly. First conversation is usually a 30-minute scoping call with the strategist and technologist who would run the engagement, enough to understand the outcome you need to reach and whether we are the right partner for that shape of work. If we are, we scope a paid discovery next."),
        ("Can you work alongside our other agencies?", "Yes. Our clients typically work with multiple agencies across brand, demand, PR, and creative production, and we integrate cleanly into that ecosystem. Where we sit is defined at the start of the engagement, usually as the lead on AI-native execution and enterprise-scale personalization, coordinating with other agencies on shared audience insight, brand guardrails, and campaign timing. We do not need to be the agency of record to do the work well. Some of our longest-running engagements sit inside multi-agency programs where each partner owns their lane."),
        ("How do you measure success?", "Against the outcome the client is accountable for. Pipeline generated, deal size, activation rate, seller enablement uptake, whichever business metric ties to why the program exists. Every campaign has a leading measure built in that reads while the work is in-flight, and a lagging measure that ties to revenue, so leadership sees the trajectory before the post-mortem. Where a test can be structured, we structure it. HP's controlled experiment on ABX, which lifted deal size 398% against a matched control, is a live example of what measurement looks like when it is designed into the program from the start."),
    ]
    faq_html = "".join(
        f'<details class="faq-item"><summary>{esc(q)}</summary><p class="faq-a">{esc(a)}</p></details>'
        for q, a in faqs
    )

    team = [
        ("Andrew Au", "Co-CEO", "andrew-au"), ("Shaheen Yazdani", "Co-CEO", "shaheen-yazdani"),
        ("Francis Silva", "Chief Technology Officer", "francis-silva"), ("Laura White", "Chief Financial Officer", "laura-white"),
        ("David Toto", "Managing Director", "david-toto"), ("Jeff Lewis", "Head of Client Advisory", "jeff-lewis"),
    ]
    team_html = "".join(
        f'<div class="person"><img class="ph" src="assets/img/homepage/{slug}.webp" alt="{esc(name)}"><b>{esc(name)}</b><span>{esc(role)}</span></div>'
        for name, role, slug in team
    )

    ins_cards = [
        ("Signals from the Edge", "Who owns your marketing alpha?", "A field read on the ownership question now facing enterprise technology, and what it means for marketing teams building on frontier AI models.", "insights/who-owns-your-marketing-alpha/index.html", "who-owns-your-marketing-alpha"),
        ("Signals from the Edge", "Why 2026 feels heavier, and what the data says", "The two-sided squeeze on B2B tech marketing, read against research from Promethean and WP Engine.", "insights/why-2026-feels-heavier/index.html", "why-2026-feels-heavier"),
        ("Signals from the Edge", "SEO is not dead. It is becoming findability", "What changes when buyers stop searching and start asking.", "insights/seo-is-becoming-findability/index.html", "seo-is-becoming-findability"),
    ]
    ins_html = "".join(
        f'<a class="icard" href="{href}"><img class="ph" src="assets/img/homepage/{img_slug}.webp" alt="{esc(k)} — {esc(h)}"><div class="body"><div class="kicker">{esc(k)}</div><h3>{esc(h)}</h3><p>{esc(p)}</p></div></a>'
        for k, h, p, href, img_slug in ins_cards
    )

    return f"""<!doctype html>
<html lang="en">
<head>
{head_html("Intercept · The frontier B2B agency for global tech", "We run an AI-native delivery model that brings enterprise rigor to campaigns built for global scale.")}
<style>{HOME_CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header_html("")}

<main id="main">

<section class="hero-band">
  <div class="hero-flex">
    <div class="hero-card">
      <div class="hero-card-inner">
        <span class="eyebrow">The frontier B2B agency for global tech</span>
        <h1>We are<br><span class="headline-word" id="stingWord"><span class="word-text">Intercept</span><span class="word-arrow" aria-hidden="true"><span class="arrow-seg"></span><span class="arrow-seg"></span><span class="arrow-seg"></span><span class="arrow-seg"></span><span class="arrow-seg"></span><span class="arrow-head"></span></span></span></h1>
        <p class="sub">We run an AI-native delivery model that brings enterprise rigor to campaigns built for global scale.</p>
        <a class="btn" href="#work">Explore our work</a>
      </div>
    </div>
    <div class="hero-video-wrap">
      <video id="heroVideo" autoplay muted loop playsinline poster="media/intercept-campaign-reel-poster.jpg">
        <source src="media/intercept-campaign-reel.mp4" type="video/mp4">
      </video>
    </div>
  </div>
</section>
{HERO_SCRIPT}

<section class="pos band-tint" id="services-lede">
  <div class="wrap">
    <span class="eyebrow">An agency for the AI era</span>
    <h2>We use AI to make the keep-the-lights-on work more efficient, freeing our people to drive innovation.</h2>
  </div>
</section>
{LEDE_REVEAL_SCRIPT}

<section class="logos">
  <div class="wrap">
    <p class="lbl">You&rsquo;re in good company</p>
    <div class="logo-row">{logos_row1}</div>
    <div class="logo-row row2">{logos_row2}</div>
  </div>
</section>

<section class="work-sec" id="work">
  <div class="wrap">
    <div class="sec-head"><h2>Our work</h2><a class="link" href="our-work/index.html">View all</a></div>

    <div class="feat">
      <img class="ph" src="assets/img/homepage/ai-in-practice.webp" alt="{esc(feat_client)} — {esc(feat_title)}">
      <div class="feat-body">
        <span class="eyebrow">{esc(feat_client)}</span>
        <h3>{esc(feat_title)}</h3>
        <p>{esc(feat_desc)}</p>
        <a class="link" href="{feat_href}">Read more</a>
      </div>
    </div>

    <div class="tier2">{tier_card(t2a, "the-measure-of-a-marketer")}{tier_card(t2b, "lights-camera-avatars")}</div>
    <div class="tier3">{tier_card(t3a, "the-magic-of-metaphors")}{tier_card(t3b, "agents-of-change")}{tier_card(t3c, "be-the-answer")}</div>
  </div>
</section>

<section class="stats-sec band-navy">
  <div class="wrap">
    <div class="stat-row">
      <div class="stat"><b>90%</b><span>of our work is global</span></div>
      <div class="stat"><b>135+</b><span>awards for B2B marketing excellence and innovation</span></div>
      <div class="stat"><b>9</b><span>years average client tenure</span></div>
    </div>
  </div>
</section>

<section class="svc" id="services">
  <div class="wrap">
    <h2>What we do. The work behind the work.</h2>
    <div class="svc-list">{services_html}</div>
  </div>
</section>

<section class="labs">
  <div class="wrap">
    <div class="labs-grid">
      <img class="ph" src="assets/img/homepage/intercept-labs.webp" alt="Intercept Labs">
      <div>
        <span class="eyebrow">Intercept Labs</span>
        <h2>When you want to try something nobody has done, we fund up to half the cost and share the risk.</h2>
        <a class="link" href="intercept-labs/index.html">Explore Intercept Labs</a>
      </div>
    </div>
  </div>
</section>

<section class="ins" id="insights">
  <div class="wrap">
    <div class="sec-head"><h2>Insights</h2><a class="link" href="insights/index.html">Explore more</a></div>
    <div class="card-grid g3">{ins_html}</div>
  </div>
</section>

<section class="faq-sec">
  <div class="wrap read">
    <span class="eyebrow">Common questions</span>
    <h2>FAQs</h2>
    <div style="margin-top:20px">{faq_html}</div>
  </div>
</section>

<section class="team" id="team">
  <div class="wrap">
    <div class="sec-head"><h2>Meet the leadership team</h2><a class="link" href="about-us/index.html">About us</a></div>
    <div class="team-grid">{team_html}</div>
  </div>
</section>

<section class="contact" id="contact">
  <div class="wrap read">
    <span class="eyebrow">Start the conversation</span>
    <h2>Give us a hard problem. Let&rsquo;s solve it together.</h2>
    <a class="btn" href="contact/index.html">Connect with an expert</a>
  </div>
</section>

</main>

{footer_html("")}
</body>
</html>"""

def main():
    path = os.path.join(ROOT, "index.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(render())
    print("Wrote", path)

if __name__ == "__main__":
    main()
