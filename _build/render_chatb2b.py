#!/usr/bin/env python3
"""Render /insights/chatb2b/ — the ChatB2B podcast hub. Sitemap round 2
(2026-08-08, "New Wire Frames 2") upgraded this from "to build" to a real
wireframe. All copy (episode titles/guests/dates/abstracts) is regex-extracted
verbatim from the source at render time — same low-risk-for-copy-fidelity
convention as render_legal.py/render_articles.py — rather than retyped.

Nav/footer/eyebrow/.ph/.btn/.link classes are the site's own shared ones from
common.py (NOT the wireframe's own competing definitions of those exact
classnames, which still carry the banned uppercase-tracked eyebrow look and a
mockup nav/footer) — this file's own CSS block only adds classnames common.py
doesn't already define.
"""
import html, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import esc, head_html, header_html, footer_html, PatternCycler, client_logo_html

# maps a chatb2b guest-wall name to its key in common.py's CLIENT_LOGOS
# when the two spellings differ, or when the guest itself has changed
# identity since the wireframe was written; anything absent here is looked
# up as-is. Round 17: PathFactory was acquired by Kaltura — Andrew's
# direction was to show the Kaltura logo in that tile instead (not a
# spelling fix, an entity change), sourced from
# ~/Downloads/Logos-for-ChatB2B/. All 16 wall tiles now have a real sourced
# logo; client_logo_html()'s plain-text fallback is now unused here but
# stays in place as the general safety net for any future unsourced name.
WALL_LOGO_KEY = {"BMC Software": "BMC", "PathFactory": "Kaltura"}

# real ChatB2B launch trailer (Andrew Au / Intercept's own YouTube upload) and the
# show's official cover art (Apple Podcasts artwork, id 1840415344, letterboxed
# from its native 1:1 into the hero's 16:9 slot — see assets/img/chatb2b/poster.webp).
# Sourced 2026-08-11; confirmed via web search the podcast/episode count (22) matches
# this build's own archive exactly.
TRAILER_URL = "https://www.youtube.com/watch?v=-D34JKW2oik"
POSTER_SRC = "assets/img/chatb2b/poster.webp"

# plain inline-SVG play triangle — see the .vplay CSS comment for why this
# replaced the source's literal Unicode glyph.
VPLAY_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>'

# real ChatB2B show-level platform links (sourced 2026-08-11, same show confirmed
# above) — used for the hero/subscribe plat-rows, which point at the SHOW, not
# a specific episode.
SHOW_LINKS = {
    "spotify": "https://open.spotify.com/show/2RTmhzjHDlCRhqQb5XyRoO",
    "apple": "https://podcasts.apple.com/us/podcast/chatb2b/id1840415344",
    "youtube": "https://www.youtube.com/channel/UCZoFGWEqh3sST6W3JSmccvA",
}

# Per-episode platform links, keyed by normalized episode title. Sourced from
# intercept-home-concepts/concept-d/chatb2b.html (the "other staging site"
# Andrew referenced — its own archive already carries real per-episode links
# for 21 of these 22 episodes verbatim, confirmed by exact title match) plus
# one newly-published episode ("The Anatomy of AI-Powered ABM") not yet in
# concept-d's build, sourced directly from the podcast's own Apple Podcasts
# and Spotify show pages 2026-08-11 (Apple episode id 1000778734774, Spotify
# episode id 2mGiIOZRokZ9Y3c8G4zpRG, both confirmed live) — no per-episode
# YouTube video could be found for that newest episode via search, so its
# YouTube button falls back to the real show channel (SHOW_LINKS) rather
# than a fabricated watch?v= id. Where concept-d itself has no per-episode
# Spotify link (several older episodes never got a Spotify-specific URL),
# that platform also falls back to the real show-level Spotify page — never
# a fabricated per-episode URL.
EPISODE_LINKS = {
    "the anatomy of ai-powered abm": {
        "spotify": "https://open.spotify.com/episode/2mGiIOZRokZ9Y3c8G4zpRG",
        "apple": "https://podcasts.apple.com/us/podcast/chatb2b/id1840415344?i=1000778734774",
        "youtube": None,
    },
    "what it takes to be creative in the ai era at hp": {
        "spotify": "https://open.spotify.com/episode/0RvY6DPjOqQXOAMJXAO0rW",
        "apple": "https://podcasts.apple.com/us/podcast/what-it-takes-to-be-creative-in-the-ai-era-at-hp/id1840415344?i=1000774885608",
        "youtube": "https://www.youtube.com/watch?v=cbRJ9uZhWCM",
    },
    "building the backend for ai agents": {
        "spotify": "https://open.spotify.com/episode/0vnMR61WLUmS94YUeNRTby",
        "apple": "https://podcasts.apple.com/us/podcast/building-the-backend-for-ai-agents-with-patrick-vuong/id1840415344?i=1000770795263",
        "youtube": "https://www.youtube.com/watch?v=t3xY3tqU9YI",
    },
    "the rise of the senior ic in the ai era": {
        "spotify": "https://open.spotify.com/episode/1vD0gtTpZppIt61dcVH56r",
        "apple": "https://podcasts.apple.com/us/podcast/the-rise-of-the-senior-ic-in-the-ai-era-with-jaynie-miller/id1840415344?i=1000768597543",
        "youtube": "https://www.youtube.com/watch?v=uDJIwLfLeBA",
    },
    "optimizing ai search: lessons from sophos": {
        "spotify": "https://open.spotify.com/episode/63Cj9IIK1SYCgCS3BBdAtv",
        "apple": "https://podcasts.apple.com/us/podcast/optimizing-ai-search-lessons-from-sophos-with-megan/id1840415344?i=1000762801591",
        "youtube": "https://www.youtube.com/watch?v=jIv_AFVh-Rc",
    },
    "the ai-ready marketer: new rules for content and culture": {
        "spotify": "https://open.spotify.com/episode/4MAOxx9katOgon2s9gahHr",
        "apple": "https://podcasts.apple.com/us/podcast/the-ai-ready-marketer-new-rules-for-content-and/id1840415344?i=1000761296490",
        "youtube": "https://www.youtube.com/watch?v=trriGcftFmE",
    },
    "when ai meets abm: rethinking content and buyers": {
        "spotify": "https://open.spotify.com/episode/05yKr823eGPAvpRoMKjjSn",
        "apple": "https://podcasts.apple.com/us/podcast/when-ai-meets-abm-rethinking-content-and-buyers/id1840415344?i=1000760035748",
        "youtube": "https://www.youtube.com/watch?v=6xzrxOpPWYk",
    },
    "what ai pcs really change for marketers": {
        "spotify": "https://open.spotify.com/episode/2fdWo3cNfaP3h4DmTK1wjA",
        "apple": "https://podcasts.apple.com/us/podcast/what-ai-pcs-really-change-for-marketers-with-jeanette/id1840415344?i=1000758418033",
        "youtube": "https://www.youtube.com/watch?v=VhvueS3zzys",
    },
    "how ai is rewriting the rules of knowledge work": {
        "spotify": "https://open.spotify.com/episode/429SteelbLk8r32FL6IyWM",
        "apple": "https://podcasts.apple.com/us/podcast/how-ai-is-rewriting-the-rules-of-knowledge-work/id1840415344?i=1000757040243",
        "youtube": "https://www.youtube.com/watch?v=6u4nv4CeiNo",
    },
    "ai adoption inside lenovo: pilots, procurement, and progress": {
        "spotify": "https://open.spotify.com/episode/291uJi3671MxyPNC2Vb5f7",
        "apple": "https://podcasts.apple.com/us/podcast/ai-adoption-inside-lenovo-pilots-procurement-and/id1840415344?i=1000754463672",
        "youtube": "https://www.youtube.com/watch?v=Fz67PYFMjmk",
    },
    "how telus is applying ai in vertical gtm": {
        "spotify": "https://open.spotify.com/episode/3vhg67LdINmkJJpegRUTVZ",
        "apple": "https://podcasts.apple.com/us/podcast/how-telus-is-applying-ai-in-vertical-gtm-with-tristan/id1840415344?i=1000751213080",
        "youtube": "https://www.youtube.com/watch?v=ERQ8i-GpgGs",
    },
    '"sprint to agents": what agentic marketing actually means': {
        "spotify": "https://open.spotify.com/episode/5wdPY6J4CaGdEq5Oi9Vovc",
        "apple": "https://podcasts.apple.com/us/podcast/sprint-to-agents-what-agentic-marketing-actually-means/id1840415344?i=1000750170163",
        "youtube": "https://www.youtube.com/watch?v=6uZaVaL94ME",
    },
    "redefining creative work for the ai era": {
        "spotify": "https://open.spotify.com/episode/0QKU2bGnnHf7xEUAPIZvSF",
        "apple": "https://podcasts.apple.com/us/podcast/redefining-creative-work-for-the-ai-era-with/id1840415344?i=1000749079254",
        "youtube": "https://www.youtube.com/watch?v=OkibIrKCMZQ",
    },
    "scaling social without losing the human": {
        "spotify": None,
        "apple": "https://podcasts.apple.com/us/podcast/scaling-social-without-losing-the-human-with-kelly-broili/id1840415344?i=1000747860513",
        "youtube": "https://www.youtube.com/watch?v=aUUHVEfA5TA",
    },
    "the playbook for practical ai: inside procom's ai journey": {
        "spotify": None,
        "apple": "https://podcasts.apple.com/us/podcast/the-playbook-for-practical-ai-inside-procoms-ai/id1840415344?i=1000746867664",
        "youtube": "https://www.youtube.com/watch?v=k_EWIUWFDy0",
    },
    "re-wiring the marketing org": {
        "spotify": None,
        "apple": "https://podcasts.apple.com/us/podcast/re-wiring-the-marketing-org-with-audrey-davidson/id1840415344?i=1000745892151",
        "youtube": "https://www.youtube.com/watch?v=3JyjNdQlu3I",
    },
    "what it really takes to scale ai pilots": {
        "spotify": None,
        "apple": "https://podcasts.apple.com/us/podcast/what-it-really-takes-to-scale-ai-pilots-with-jessica-hreha/id1840415344?i=1000744987223",
        "youtube": "https://www.youtube.com/watch?v=v17YjMlZjp8",
    },
    "how ai can support partner growth": {
        "spotify": None,
        "apple": "https://podcasts.apple.com/us/podcast/how-ai-can-support-partner-growth-with-shelley-green/id1840415344?i=1000741526585",
        "youtube": "https://www.youtube.com/watch?v=dnEIGIV7L7g",
    },
    "future-proof your marketing career in the age of ai": {
        "spotify": None,
        "apple": "https://podcasts.apple.com/us/podcast/future-proof-your-marketing-career-in-the-age-of-ai/id1840415344?i=1000737607341",
        "youtube": "https://www.youtube.com/watch?v=KNGQlY55hBw",
    },
    "the ai opportunity for channel partner marketing": {
        "spotify": None,
        "apple": "https://podcasts.apple.com/us/podcast/the-ai-opportunity-for-channel-partner-marketing/id1840415344?i=1000737606199",
        "youtube": "https://www.youtube.com/watch?v=x2IAPBKTCrI",
    },
    "rethinking sales enablement in the ai era": {
        "spotify": None,
        "apple": "https://podcasts.apple.com/us/podcast/rethinking-sales-enablement-in-the-ai-era-with/id1840415344?i=1000737593994",
        "youtube": "https://www.youtube.com/watch?v=js5lGAc5vP4",
    },
    "introducing chatb2b": {
        "spotify": None,
        "apple": "https://podcasts.apple.com/us/podcast/introducing-chatb2b/id1840415344?i=1000736649341",
        "youtube": "https://www.youtube.com/watch?v=7Ti_zKe-nck",
    },
}


def norm_title(s):
    s = html.unescape(re.sub(r"<[^>]+>", "", s))
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip().lower()


def episode_links(title):
    """Real per-episode platform links, falling back to the show-level page
    for whichever platform (or whole episode) has no specific link sourced."""
    entry = EPISODE_LINKS.get(norm_title(title), {})
    return {
        plat: (entry.get(plat) or SHOW_LINKS[plat])
        for plat in ("spotify", "apple", "youtube")
    }


def plat_row_html(links, solid_first=False, apple_label="Apple Podcasts"):
    spotify_cls = "plat solid" if solid_first else "plat"
    return (
        f'<a class="{spotify_cls}" href="{links["spotify"]}" target="_blank" rel="noopener">Spotify</a>'
        f'<a class="plat" href="{links["apple"]}" target="_blank" rel="noopener">{apple_label}</a>'
        f'<a class="plat" href="{links["youtube"]}" target="_blank" rel="noopener">YouTube</a>'
    )


def ep_links_html(links):
    return (
        f'<a class="plat" href="{links["spotify"]}" target="_blank" rel="noopener">Spotify</a>'
        f'<a class="plat" href="{links["apple"]}" target="_blank" rel="noopener">Apple</a>'
        f'<a class="plat" href="{links["youtube"]}" target="_blank" rel="noopener">YouTube</a>'
    )


SRC = "/Users/jontoewsinterceptgroup.com/Downloads/New Wire Frames 2/pages/chatb2b.html"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = """
.crumb{border-bottom:1px solid var(--line);background:var(--band)}
.crumb-row{max-width:var(--maxw);margin:0 auto;padding:11px 32px;font-size:var(--fs-8);color:var(--ink-3)}
.crumb-row b{color:var(--ink);font-weight:600}

.chero{padding:56px 0 40px;border-bottom:1px solid var(--line)}
.chero-grid{display:grid;grid-template-columns:1.15fr 1fr;gap:48px;align-items:center}
.chero h1{font-size:var(--fs-1);line-height:1.04;letter-spacing:-.03em;margin:0 0 16px}
.chero p:not(.eyebrow){font-size:var(--fs-5);line-height:1.5;color:var(--ink-2);margin:0 0 24px;max-width:52ch}
.plat-row{display:flex;flex-wrap:wrap;gap:10px}
/* Priority 2 #5: hero .plat pills were already ~42px; the archive's
   .ep-links override below was 35px -- both unified to 44px via min-height
   (rather than vertical padding) so the height match holds regardless of
   the two contexts' different font-size/padding-x. */
.plat{display:inline-flex;align-items:center;min-height:44px;font-size:var(--fs-7);font-weight:600;border:1px solid var(--ink);padding:0 18px;border-radius:8px;color:var(--ink)}
.plat.solid{background:var(--ink);color:var(--page)}

.vid{position:relative}
.vid .ph{aspect-ratio:16/9;margin:0}
/* Round 17 fix: the source wireframe's play glyph was the literal Unicode
   character &#9658; (U+25B8) sized via font-size — a font-rendering glyph,
   not a real icon, so its exact shape/weight/centering is at the mercy of
   whatever fallback symbol font a given OS/browser substitutes (this repo
   ships no icon library — see common.py — so there's no Lucide "play" to
   reach for either). Swapped for a plain inline SVG triangle: identical
   render everywhere, no font-substitution risk. */
.vid .vplay{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:56px;height:56px;border-radius:999px;background:var(--ink);color:var(--page);display:flex;align-items:center;justify-content:center}
.vid .vplay svg{width:20px;height:20px;margin-left:2px}
.vid .vlabel{position:absolute;left:14px;bottom:14px;background:var(--ink);color:var(--page);font-weight:600;font-size:var(--fs-8);padding:6px 10px;border-radius:4px}

.latest{padding:52px 0;border-bottom:1px solid var(--line)}
.latest-grid{display:grid;grid-template-columns:340px 1fr;gap:40px;align-items:start}
.latest h2{font-size:var(--fs-2);line-height:1.1;letter-spacing:-.028em;margin:0 0 12px}
.latest .who{font-size:var(--fs-6);color:var(--ink-2);margin:0 0 14px}
.latest .abstract{font-size:var(--fs-6);line-height:1.6;color:var(--ink-2);margin:0 0 22px;max-width:62ch}

.feat{padding:52px 0;border-bottom:1px solid var(--line)}
.feat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:26px;margin-top:22px}
.fcard .ph{aspect-ratio:16/9;margin:0 0 14px}
.fcard .ep-date{font-size:var(--fs-8);color:var(--ink-3);display:block;margin:0 0 8px}
.fcard h3{font-size:var(--fs-4);line-height:1.26;letter-spacing:-.014em;margin:0 0 9px}
.fcard p:not(.eyebrow){font-size:var(--fs-7);line-height:1.5;color:var(--ink-2);margin:0}
.fcard .ep-links{margin-top:14px;flex-wrap:wrap}

.wall{padding:46px 0;background:var(--band);border-bottom:1px solid var(--line)}
.wall-grid{display:grid;grid-template-columns:repeat(8,1fr);gap:14px;margin-top:20px}
/* Round 17 fix: aspect-ratio:5/2 with no explicit height derives the box's
   width FROM whatever height its tallest logo forces during grid
   auto-sizing — one oversized logo (was Moderne at 34px, but even the
   pre-existing Qualcomm/SAP/HP vectors at 23-25px already did this)
   inflates every column uniformly, since all 8 are equal 1fr tracks. That
   pushed the last column (TELUS, then Procom) outside the 1200px .wrap on
   real viewports (measured: 8 x 170px + gaps = 1458px content in a
   1136px-wide track, silently clipped by the sitewide overflow-x:clip — no
   scrollbar to reveal it). Fixed height breaks the circular width<->height
   coupling; min-width:0 stops any single wide logo (text-fallback or an
   unusually wide mark) from doing the same thing sideways.
   Verify after any future logo-height change: no column should exceed
   ~130px (1136px content width / 8 - gap share) at 1200px+ viewports. */
.wall .ph{height:68px;font-size:10px;min-width:0}

.arch{padding:52px 0}
.arch h2{font-size:var(--fs-2);line-height:1.1;letter-spacing:-.028em;margin:0}
.ep{display:grid;grid-template-columns:128px 1fr auto;gap:22px;align-items:center;padding:20px 0;border-bottom:1px solid var(--line)}
/* load-bearing: the HTML hidden attribute is applied by the UA sheet at the
   lowest precedence, so any author rule that sets display, like .ep above,
   silently defeats it and every row renders (same bug class as the careers
   open-roles filter fix, round 10) — guarded explicitly here. */
.ep[hidden]{display:none}
.ep:first-of-type{border-top:1px solid var(--ink)}
.ep-art{aspect-ratio:16/9;font-size:10px}
.ep-date{font-size:var(--fs-8);color:var(--ink-3);display:block;margin:0 0 6px}
.ep-main h3{font-size:var(--fs-5);line-height:1.28;letter-spacing:-.012em;margin:0 0 6px}
.ep-main p:not(.eyebrow){font-size:var(--fs-7);line-height:1.45;color:var(--ink-2);margin:0}
.ep-links{display:flex;gap:8px}
.ep-links .plat{font-size:var(--fs-8);padding:0 13px;font-weight:600}
.loadmore{display:flex;justify-content:center;padding:36px 0 0}

.sub{padding:56px 0;border-top:1px solid var(--line)}
.sub-grid{display:grid;grid-template-columns:1fr 1fr;gap:40px}
.sub h2{font-size:var(--fs-3);line-height:1.1;letter-spacing:-.026em;margin:0 0 12px}
.sub p:not(.eyebrow){font-size:var(--fs-6);line-height:1.55;color:var(--ink-2);margin:0 0 20px;max-width:44ch}

@media(max-width:1000px){.wall-grid{grid-template-columns:repeat(4,1fr)}}
@media(max-width:900px){
  .chero-grid,.latest-grid,.feat-grid,.sub-grid{grid-template-columns:1fr;gap:26px}
  .ep{grid-template-columns:96px 1fr;gap:16px}
  .ep-links{grid-column:1 / -1}
}
"""

LOADMORE_SCRIPT = """(function(){
  var rows = [].slice.call(document.querySelectorAll(".arch .ep"));
  var more = document.getElementById("more");
  if(!more) return;
  more.addEventListener("click", function(){
    rows.forEach(function(r){ r.hidden = false; });
    more.parentNode.style.display = "none";
  });
})();"""


def between(text, a, b):
    i = text.index(a) + len(a)
    j = text.index(b, i)
    return text[i:j]


def tag(pattern, text, group=1):
    m = re.search(pattern, text, re.S)
    if not m:
        raise ValueError(f"pattern not found: {pattern!r}")
    return m.group(group).strip()


def parse():
    html = open(SRC, encoding="utf-8").read()

    hero = between(html, "<!-- HERO + TRAILER PLAYER -->", "<!-- FEATURED EPISODE")
    hero_h1 = tag(r"<h1>(.*?)</h1>", hero)
    hero_p = tag(r"<h1>.*?</h1>\s*<p>(.*?)</p>", hero)
    hero_plats = tag(r'<div class="plat-row">(.*?)</div>', hero)
    hero_vlabel = tag(r'<span class="vlabel">(.*?)</span>', hero)

    featured = between(html, "<!-- FEATURED EPISODE", "<!-- THREE NEWEST -->")
    feat_date = tag(r'<span class="ep-date">(.*?)</span>', featured)
    feat_h2 = tag(r"<h2>(.*?)</h2>", featured)
    feat_who = tag(r'<p class="who">(.*?)</p>', featured)
    feat_abstract = tag(r'<p class="abstract">(.*?)</p>', featured)
    feat_plats = tag(r'<div class="plat-row">(.*?)</div>', featured)

    more_eps = between(html, "<!-- THREE NEWEST -->", "<!-- GUEST COMPANY WALL -->")
    fcards = re.findall(
        r'<div class="fcard">\s*<div class="ph">(.*?)</div>\s*<span class="ep-date">(.*?)</span>\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>\s*</div>',
        more_eps, re.S,
    )

    wall = between(html, "<!-- GUEST COMPANY WALL -->", "<!-- ARCHIVE -->")
    wall_logos = re.findall(r'<div class="ph">(.*?)</div>', wall)

    archive = between(html, "<!-- ARCHIVE -->", "<!-- SUBSCRIBE")
    eps = re.findall(
        r'<div class="ep"(\s+hidden)?>\s*<div class="ph ep-art">(.*?)</div>\s*'
        r'<div class="ep-main">\s*<span class="ep-date">(.*?)</span>\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>\s*</div>\s*'
        r'<div class="ep-links">(.*?)</div>\s*</div>',
        archive, re.S,
    )

    sub = between(html, "<!-- SUBSCRIBE", "<footer")
    sub_h2s = re.findall(r"<h2>(.*?)</h2>", sub)
    sub_ps = re.findall(r"<p>(.*?)</p>", sub)
    sub_plats = tag(r'<div class="plat-row">(.*?)</div>', sub)
    sub_btn = tag(r'<span class="btn">(.*?)</span>', sub)

    return dict(
        hero_h1=hero_h1, hero_p=hero_p, hero_plats=hero_plats, hero_vlabel=hero_vlabel,
        feat_date=feat_date, feat_h2=feat_h2, feat_who=feat_who, feat_abstract=feat_abstract, feat_plats=feat_plats,
        fcards=fcards, wall_logos=wall_logos, eps=eps,
        sub_h2s=sub_h2s, sub_ps=sub_ps, sub_plats=sub_plats, sub_btn=sub_btn,
    )


def render(data, base="../../"):
    pc = PatternCycler()
    def fcard_html(ph, date, h3, p):
        # Round 17.1 fix: this "More episodes" 3-card teaser had NO click-through
        # at all (no wrapping <a>, no platform links) — same underlying gap the
        # "All episodes" archive already had fixed via episode_links()/
        # ep_links_html(), just never ported to this second, separate section.
        src, ratio = pc.next("3col", base)
        return (
            f'<div class="fcard"><img class="ph" style="aspect-ratio:{ratio}" src="{src}" alt="">'
            f'<span class="ep-date">{date}</span><h3>{h3}</h3><p>{p}</p>'
            f'<div class="ep-links">{ep_links_html(episode_links(h3))}</div></div>'
        )
    fcards_html = "".join(fcard_html(*c) for c in data["fcards"])
    wall_html = "".join(
        f'<div class="ph">{client_logo_html(WALL_LOGO_KEY.get(name, name), base)}</div>'
        for name in data["wall_logos"]
    )
    def ep_html(hidden, art, date, h3, p, _raw_links):
        # _raw_links (the wireframe's own <div class="ep-links">...) is discarded —
        # it was identical unlinked "Spotify/Apple/YouTube" text on every one of
        # the 22 rows. Real per-episode links come from episode_links()/EPISODE_LINKS.
        src, ratio = pc.next("4col", base)
        return (
            f'<div class="ep"{hidden}>'
            f'<img class="ph ep-art" style="aspect-ratio:{ratio}" src="{src}" alt="">'
            f'<div class="ep-main"><span class="ep-date">{date}</span><h3>{h3}</h3><p>{p}</p></div>'
            f'<div class="ep-links">{ep_links_html(episode_links(h3))}</div>'
            f"</div>"
        )
    eps_html = "".join(ep_html(*e) for e in data["eps"])
    feat_vid_src, feat_vid_ratio = pc.next("2col", base)
    # Round 17 fix: the featured-episode video block had a play-button circle
    # sitting on a decorative pattern placeholder with no href at all — a
    # real-looking "click to play" affordance that did nothing (unlike the
    # hero trailer's .vid, which is a real link). Wire it to that episode's
    # real YouTube link (falls back to the show channel when no per-episode
    # video was found, same as its own plat-row two lines below).
    feat_links = episode_links(data["feat_h2"])

    return f"""<!doctype html>
<html lang="en">
<head>
{head_html("ChatB2B · Insights · Intercept", "Inspiration starts with a good conversation — the ChatB2B podcast.")}
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header_html(base)}
<div class="crumb"><div class="crumb-row">Insights &middot; <b>ChatB2B</b></div></div>
<main id="main">

<section class="chero">
  <div class="wrap">
    <div class="chero-grid">
      <div>
        <span class="eyebrow">ChatB2B</span>
        <h1>{data["hero_h1"]}</h1>
        <p>{data["hero_p"]}</p>
        <div class="plat-row">{plat_row_html(SHOW_LINKS, solid_first=True)}</div>
      </div>
      <a class="vid" href="{TRAILER_URL}" target="_blank" rel="noopener" aria-label="Watch the ChatB2B trailer on YouTube">
        <img class="ph" style="aspect-ratio:16/9" src="{base}{POSTER_SRC}" alt="ChatB2B podcast cover art">
        <span class="vplay">{VPLAY_SVG}</span>
        <span class="vlabel">{data["hero_vlabel"]}</span>
      </a>
    </div>
  </div>
</section>

<section class="latest">
  <div class="wrap">
    <span class="eyebrow">Featured episode</span>
    <div class="latest-grid">
      <a class="vid" href="{feat_links["youtube"]}" target="_blank" rel="noopener" aria-label="Watch {data["feat_h2"]} on YouTube">
        <img class="ph" style="aspect-ratio:{feat_vid_ratio}" src="{feat_vid_src}" alt="">
        <span class="vplay">{VPLAY_SVG}</span>
      </a>
      <div>
        <span class="ep-date">{data["feat_date"]}</span>
        <h2>{data["feat_h2"]}</h2>
        <p class="who">{data["feat_who"]}</p>
        <p class="abstract">{data["feat_abstract"]}</p>
        <div class="plat-row">{plat_row_html(feat_links)}</div>
      </div>
    </div>
  </div>
</section>

<section class="feat">
  <div class="wrap">
    <span class="eyebrow">More episodes</span>
    <div class="feat-grid">{fcards_html}</div>
  </div>
</section>

<section class="wall">
  <div class="wrap">
    <span class="eyebrow">Featuring guests from</span>
    <div class="wall-grid">{wall_html}</div>
  </div>
</section>

<section class="arch">
  <div class="wrap">
    <h2>All episodes</h2>
    {eps_html}
    <div class="loadmore"><span class="btn" id="more">Load more episodes</span></div>
  </div>
</section>

<section class="sub">
  <div class="wrap">
    <div class="sub-grid">
      <div>
        <h2>{data["sub_h2s"][0]}</h2>
        <p>{data["sub_ps"][0]}</p>
        <div class="plat-row">{plat_row_html(SHOW_LINKS)}</div>
      </div>
      <div>
        <h2>{data["sub_h2s"][1]}</h2>
        <p>{data["sub_ps"][1]}</p>
        <a class="btn" href="{base}contact/index.html">{data["sub_btn"]}</a>
      </div>
    </div>
  </div>
</section>

</main>
{footer_html(base)}
<script>{LOADMORE_SCRIPT}</script>
</body>
</html>"""


def main():
    data = parse()
    out = render(data)
    outdir = os.path.join(ROOT, "insights", "chatb2b")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "index.html")
    open(path, "w", encoding="utf-8").write(out)
    print("Wrote", path)


if __name__ == "__main__":
    main()
