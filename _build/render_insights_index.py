#!/usr/bin/env python3
"""Render insights/index.html — hub with real filters + load-more (per
insights-hub.html wireframe: chips filter by data-s, 12 shown by default)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import esc, head_html, header_html, footer_html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = """
.ihero{padding:52px 0 34px}
.ihero h1{font-size:var(--fs-1);line-height:1.04;letter-spacing:-.032em;margin:0 0 16px;max-width:19ch}
.feat{padding:8px 0 52px}
.feat-grid{display:grid;grid-template-columns:1.25fr 1fr;gap:52px;align-items:center}
.feat .ph{aspect-ratio:16/10}
.feat h2{font-size:var(--fs-2);line-height:1.08;letter-spacing:-.028em;margin:0 0 14px}
.feat p{font-size:var(--fs-6);line-height:1.5;color:var(--ink-2);margin:0 0 20px;max-width:46ch}
.byline{display:flex;align-items:center;gap:12px;margin:0 0 22px}
.byline .ph{width:38px;height:38px;padding:0;font-size:7px;border-radius:50%}
.byline b{display:block;font-size:var(--fs-7);font-weight:700}
.byline .meta{display:block;font-size:var(--fs-8);color:var(--ink-3)}
.props{padding:48px 0;background:var(--band)}
.prop-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:26px;margin-top:24px;align-items:stretch}
.prop{display:flex;flex-direction:column}
.prop .ph{aspect-ratio:4/3;margin-bottom:14px}
.prop b{display:block;font-size:var(--fs-4);line-height:1.22;font-weight:700;margin-bottom:8px}
.prop span{display:block;font-size:var(--fs-7);line-height:1.5;color:var(--ink-2);margin-bottom:16px}
.prop .link{margin-top:auto}
.feed{padding:48px 0 12px}
.chips{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:8px}
.chip{font-size:var(--fs-7);font-weight:600;padding:8px 16px;border-radius:99px;border:1px solid var(--line);color:var(--ink-2);cursor:pointer;transition:background .15s,color .15s,border-color .15s}
.chip:hover{border-color:var(--ink-3)}
.chip.on{background:var(--carbon-500);color:#fff;border-color:var(--carbon-500)}
.feed-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:32px 24px;margin-top:28px}
.card .ph{aspect-ratio:16/9;margin-bottom:12px}
.card .meta{display:block;margin-bottom:8px;font-size:var(--fs-8);color:var(--ink-3)}
.card h3{font-size:var(--fs-4);line-height:1.24;letter-spacing:-.014em;margin:0 0 6px;font-weight:700}
.card p{font-size:var(--fs-7);line-height:1.45;color:var(--ink-2);margin:0}
.more{text-align:center;margin-top:40px}
.sub{padding:52px 0;background:var(--band);margin-top:40px;text-align:center}
.sub h2{font-size:var(--fs-2);max-width:20ch;margin:0 auto 20px}
@media(max-width:1100px){.prop-grid{grid-template-columns:1fr 1fr}}
@media(max-width:900px){.feat-grid{grid-template-columns:1fr}}
@media(max-width:700px){.feed-grid{grid-template-columns:1fr}}
"""

FILTER_SCRIPT = """<script>
(function(){
  var grid = document.querySelector(".feed-grid");
  var cards = [].slice.call(grid.querySelectorAll(".card"));
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

CHIPS = ["Signals from the Edge", "Trends Brief", "ChatB2B", "eBooks"]

# verbatim from insights-hub.html's .feed-grid (29 cards) — only the 4
# "Signals from the Edge" articles have a real page built; everything else
# (Trends Brief, all 22 ChatB2B episodes, both eBooks) has no detail page
# per sitemap.html ("To build"), so those render as non-linked cards,
# same convention as the rest of this site's not-yet-built CTAs
FEED = [
    ("Signals from the Edge", "Signals from the Edge · Jul 2026", "Who owns your marketing alpha?", "Where durable advantage lives when every competitor rents the same frontier models.", "who-owns-your-marketing-alpha/index.html"),
    ("Signals from the Edge", "Signals from the Edge", "Why 2026 feels heavier, and what the data says", "The two-sided squeeze on B2B tech marketing, read against research from Promethean and WP Engine.", "why-2026-feels-heavier/index.html"),
    ("Signals from the Edge", "Signals from the Edge", "SEO is not dead. It is becoming findability", "What changes when buyers stop searching and start asking.", "seo-is-becoming-findability/index.html"),
    ("Signals from the Edge", "Signals from the Edge", "How AI is reshaping B2B tech marketing", "What we see across global product, field, and alliance marketing teams.", "how-ai-is-reshaping-b2b-tech-marketing/index.html"),
    ("Trends Brief", "Trends Brief", "AI in B2B marketing", "Original Watchtower research, published twice a year.", None),
    ("ChatB2B", "ChatB2B · 28 Jul 2026", "The Anatomy of AI-Powered ABM", "Hans Bunes, independent consultant, previously HP.", None),
    ("ChatB2B", "ChatB2B · 30 Jun 2026", "What it takes to be creative in the AI era at HP", "Liz Merrilees Emlay, Head of Global Creative Services and Product Marketing, HP.", None),
    ("ChatB2B", "ChatB2B · 2 Jun 2026", "Building the Backend for AI Agents", "Patrick Vuong, first Director of Product Management, Moderne.", None),
    ("ChatB2B", "ChatB2B · 19 May 2026", "The Rise of the Senior IC in the AI Era", "Jaynie Miller, Worldwide Product Marketing Lead, HP.", None),
    ("ChatB2B", "ChatB2B · 21 Apr 2026", "Optimizing AI Search: Lessons from Sophos", "Megan Cabrera, former VP of Marketing Operations, Sophos.", None),
    ("ChatB2B", "ChatB2B · 14 Apr 2026", "The AI-Ready Marketer: New Rules for Content and Culture", "Tammy Tufty, Content Strategist, BMC Software.", None),
    ("ChatB2B", "ChatB2B · 7 Apr 2026", "When AI Meets ABM: Rethinking Content and Buyers", "Murali Kandasamy, VP of Growth and Strategy, PathFactory.", None),
    ("ChatB2B", "ChatB2B · 31 Mar 2026", "What AI PCs Really Change for Marketers", "Jeanette Kennedy, Marketing Lead, Microsoft.", None),
    ("ChatB2B", "ChatB2B · 24 Mar 2026", "How AI Is Rewriting the Rules of Knowledge Work", "Mahadev Sastri, Marketing Lead for Strategic Alliances, CGI.", None),
    ("ChatB2B", "ChatB2B · 10 Mar 2026", "AI Adoption Inside Lenovo: Pilots, Procurement, and Progress", "Shoeb Shaikh, Senior Manager for Global Campaigns, Lenovo.", None),
    ("ChatB2B", "ChatB2B · 24 Feb 2026", "How TELUS is Applying AI in Vertical GTM", "Tristan Retelsdorf, VP of Marketing and RevOps, TELUS Agriculture and Consumer Goods.", None),
    ("ChatB2B", "ChatB2B · 17 Feb 2026", "“Sprint to Agents”: What Agentic Marketing Actually Means", "Francis Silva, Chief Technology Officer, Intercept.", None),
    ("ChatB2B", "ChatB2B · 10 Feb 2026", "Redefining Creative Work for the AI Era", "Catherine Richards, creative and content strategy leader, previously Dell, Adobe, and VMware.", None),
    ("ChatB2B", "ChatB2B · 3 Feb 2026", "Scaling Social Without Losing the Human", "Kelly Broili, SAP.", None),
    ("ChatB2B", "ChatB2B · 27 Jan 2026", "The Playbook for Practical AI: Inside Procom’s AI Journey", "Dylan Fedy, Procom.", None),
    ("ChatB2B", "ChatB2B · 20 Jan 2026", "Re-wiring the Marketing Org", "Audrey Davidson, integrated marketing lead for the Americas, Microsoft.", None),
    ("ChatB2B", "ChatB2B · 13 Jan 2026", "What It Really Takes to Scale AI Pilots", "Jessica Hreha, Veeam.", None),
    ("ChatB2B", "ChatB2B · 16 Dec 2025", "How AI Can Support Partner Growth", "Shelley Green, TD SYNNEX.", None),
    ("ChatB2B", "ChatB2B · 20 Nov 2025", "Future-Proof Your Marketing Career in the Age of AI", "Josh Chiavaroli, Intel.", None),
    ("ChatB2B", "ChatB2B · 20 Nov 2025", "The AI Opportunity for Channel Partner Marketing", "", None),
    ("ChatB2B", "ChatB2B · 20 Nov 2025", "Rethinking Sales Enablement in the AI Era", "", None),
    ("ChatB2B", "ChatB2B · 13 Nov 2025", "Introducing ChatB2B", "", None),
    ("eBooks", "eBook", "Cortex report", "Neuroscience-based creative measurement, and what it predicts before a campaign runs.", None),
    ("eBooks", "eBook", "AI-powered research", "How synthetic and live audience research work together.", None),
]

def render():
    def feed_card(service, meta, title, desc, href):
        tag = "a" if href else "div"
        attr = f' href="{href}"' if href else ""
        return (
            f'<{tag} class="card" data-s="{esc(service)}"{attr}>'
            f'<div class="ph">Visual</div><span class="meta">{esc(meta)}</span>'
            f'<h3>{esc(title)}</h3><p>{esc(desc)}</p></{tag}>'
        )
    feed_html = "".join(feed_card(*row) for row in FEED)
    chips_html = '<span class="chip on" data-f="">Everything</span>' + "".join(
        f'<span class="chip" data-f="{esc(s)}">{esc(s)}</span>' for s in CHIPS
    )
    props = [
        ("Signals from the Edge", "Shaheen Yazdani on what we are seeing in live client work, and what it means for the year ahead."),
        ("Trends Brief", "Original research on what is changing across the industry, and how our clients are adapting."),
        ("ChatB2B", "Andrew Au interviews marketing leaders at the largest enterprise technology companies on how they are piloting and scaling AI use cases across their organizations."),
        ("eBooks", "Papers on emerging trends such as neuroscience-based creative and AI-powered research."),
    ]
    props_html = "".join(f'<div class="prop"><div class="ph">{esc(n)}</div><b>{esc(n)}</b><span>{esc(d)}</span></div>' for n, d in props)

    return f"""<!doctype html>
<html lang="en">
<head>
{head_html("Insights · Intercept", "Our perspectives on AI, B2B tech marketing, and what's changing across the industry.")}
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header_html("../")}
<main id="main">

<section class="ihero"><div class="wrap"><span class="eyebrow">Insights</span><h1>Our perspectives</h1></div></section>

<section class="feat">
  <div class="wrap"><div class="feat-grid">
    <div class="ph" style="aspect-ratio:16/10">Featured</div>
    <div>
      <span class="eyebrow">Featured &middot; Signals from the Edge &middot; July 2026</span>
      <h2>Who owns your marketing alpha?</h2>
      <p>A field read on the ownership question now facing enterprise technology, and what it means for marketing teams building on frontier AI models.</p>
      <div class="byline"><div class="ph">Portrait</div><div><b>Shaheen Yazdani</b><span class="meta">Co-CEO &middot; 23 min read</span></div></div>
      <a class="link" href="who-owns-your-marketing-alpha/index.html">Read the blog</a>
    </div>
  </div></div>
</section>

<section class="props">
  <div class="wrap">
    <h2 style="font-size:var(--fs-2)">Where to start</h2>
    <div class="prop-grid">{props_html}</div>
  </div>
</section>

<section class="feed">
  <div class="wrap">
    <h2 style="font-size:var(--fs-2)">Insights hub</h2>
    <div class="chips">{chips_html}</div>
    <div class="feed-grid">{feed_html}</div>
    <div class="more"><span class="link" id="more">Load more</span></div>
  </div>
</section>

<section class="sub">
  <div class="wrap read">
    <span class="eyebrow">Start the conversation</span>
    <h2>Give us a hard problem. Let&rsquo;s solve it together.</h2>
    <a class="btn" href="../contact/index.html">Connect with an expert</a>
  </div>
</section>

</main>
{footer_html("../")}
{FILTER_SCRIPT}
</body>
</html>"""

if __name__ == "__main__":
    path = os.path.join(ROOT, "insights", "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(render())
    print("Wrote", path)
