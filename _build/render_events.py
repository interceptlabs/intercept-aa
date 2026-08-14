#!/usr/bin/env python3
"""Render /events/<slug>/ — the reusable event-landing template from sitemap
round 2 (2026-08-08, "New Wire Frames 2"), URL pattern /events/[event]/.

Unlike every other page type built so far, this wireframe IS a template, not
a single real event ("Reusable template for one-off event/conference pages,
not a single instance" — sitemap.html's own words). Its own copy is entirely
generic placeholder text ("Three to five word headline", "Name", "Title") —
there is no real event brief yet. render_event(data) below is the reusable
piece; main() renders exactly one demo instance at /events/template/ using
the wireframe's own placeholder strings verbatim (nothing invented — this
IS the wireframe's literal content), so the template's markup/CSS/booking-
form structure exists and is checkable on the live site.

Not linked from nav or footer: the wireframe's own sitemap note flags that
"parent section/nav placement not specified by the wireframe" — flagging,
not inventing one, same convention as every other unresolved-IA case on
this site (Intuit's missing vector logo, the 2 unmatched related-work
refs, etc). When a real event exists, call render_event() with its real
copy and give main() a slug list.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import esc, head_html, header_html, footer_html, PatternCycler

SRC = "/Users/jontoewsinterceptgroup.com/Downloads/New Wire Frames 2/pages/event-template.html"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = """
.ebar{background:var(--carbon-500);color:#fff;padding:13px 0}
.ebar-row{max-width:var(--maxw);margin:0 auto;padding:0 32px;display:flex;flex-wrap:wrap;gap:10px 22px;align-items:baseline;font-size:var(--fs-8);font-weight:600}
.ebar-row b{font-weight:700}
.ebar-row span:not(.link){color:var(--halo-500)}

.ehero{padding:60px 0 54px;border-bottom:1px solid var(--line)}
.ehero-grid{display:grid;grid-template-columns:1.15fr 1fr;gap:56px;align-items:start}
.ehero h1{font-size:var(--fs-1);line-height:1.02;letter-spacing:-.036em;margin:0 0 20px}
.ehero p:not(.eyebrow){font-size:var(--fs-5);line-height:1.56;color:var(--ink-2);margin:0;max-width:48ch}

{padding:28px}
.book h2{font-size:var(--fs-5);line-height:1.2;letter-spacing:-.014em;margin:0 0 20px}
.book .field{margin:0 0 13px}
.book label{display:block;font-size:var(--fs-8);color:var(--ink-3);margin:0 0 6px}
/* Priority 3 #8: real inputs, same technique as render_contact.py -- was a
   visual-only <div class="input"></div> box. 44px min-height (bumped from
   the mockup's 42px) matches the sitewide touch-target floor now that this
   is a real tappable control, not decoration. */
.book input[type=text],.book input[type=email]{
  width:100%;box-sizing:border-box;border:1px solid var(--line);background:var(--page);min-height:44px;
  padding:0 14px;font-size:var(--fs-7);font-family:var(--font-body);color:var(--ink);
}
.book input:focus{outline:2px solid var(--flarepop-ink);outline-offset:2px}
.book .btn{display:block;width:100%;box-sizing:border-box;text-align:center;margin-top:18px;border:0;cursor:pointer;font-family:inherit}
.book .rsent{display:none;padding:14px 16px;background:var(--band);border-left:3px solid var(--flarepop);font-size:var(--fs-8);color:var(--ink);margin-top:16px}
.book .rsent.show{display:block}

.esec{padding:54px 0;border-bottom:1px solid var(--line)}
.esec h2{font-size:var(--fs-2);line-height:1.1;letter-spacing:-.026em;margin:0 0 26px}

.takes{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}
.take{border-top:2px solid var(--ink);padding:15px 0 0}
.take span:not(.link){font-size:var(--fs-8);color:var(--ink-3);display:block;margin:0 0 10px}
.take b{display:block;font-size:var(--fs-5);line-height:1.26;letter-spacing:-.014em;margin:0 0 8px}
.take p:not(.eyebrow){font-size:var(--fs-7);line-height:1.5;color:var(--ink-2);margin:0}

.acards{display:grid;grid-template-columns:repeat(2,1fr);gap:30px}
.acard .ph{aspect-ratio:16/9;margin:0 0 16px}
.acard .kind{font-size:var(--fs-8);color:var(--ink-3);display:block;margin:0 0 8px}
.acard b{display:block;font-size:var(--fs-3);line-height:1.2;letter-spacing:-.018em;margin:0 0 9px}
.acard p:not(.eyebrow){font-size:var(--fs-6);line-height:1.5;color:var(--ink-2);margin:0 0 12px}

.ccards{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}
.ccard .ph{aspect-ratio:16/9;margin:0 0 14px}
.ccard b{display:block;font-size:var(--fs-4);line-height:1.24;letter-spacing:-.016em;margin:0 0 8px}
.ccard p:not(.eyebrow){font-size:var(--fs-7);line-height:1.5;color:var(--ink-2);margin:0}

.people{display:grid;grid-template-columns:repeat(4,1fr);gap:26px}
.person .ph{aspect-ratio:1/1;margin:0 0 13px}
.person b{display:block;font-size:var(--fs-6);margin:0 0 3px}
.person span:not(.link){font-size:var(--fs-7);color:var(--ink-3);display:block}
.person .mail{font-size:var(--fs-8);color:var(--ink-3);margin-top:5px}

.lwall{display:grid;grid-template-columns:repeat(8,1fr);gap:14px}
.lwall .ph{aspect-ratio:5/2;font-size:10px}

.feed{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
{padding:18px;display:flex;flex-direction:column;gap:11px}
.post .top{display:flex;align-items:center;gap:10px}
.post .av{width:34px;height:34px;border-radius:999px;background:var(--band);flex:none}
.post .who{font-size:var(--fs-8);color:var(--ink-3)}
.post .ph{min-height:62px;font-size:10px}
.feed-note{font-size:var(--fs-8);color:var(--ink-3);margin:18px 0 0}

.eclose{padding:60px 0}
.eclose h2{font-size:var(--fs-2);line-height:1.06;letter-spacing:-.032em;margin:0 0 22px;max-width:18ch}

@media(max-width:1000px){.lwall{grid-template-columns:repeat(4,1fr)}.people{grid-template-columns:repeat(2,1fr)}}
@media(max-width:900px){.ehero-grid,.acards,.ccards,.takes,.feed{grid-template-columns:1fr;gap:26px}}
"""


def between(text, a, b):
    i = text.index(a) + len(a)
    j = text.index(b, i)
    return text[i:j]


def parse_template_demo():
    """Pull the wireframe's own placeholder strings verbatim — this file has
    no real event copy yet, so the 'data' IS the template's literal filler
    text (e.g. 'Three to five word headline'), not anything invented here."""
    html = open(SRC, encoding="utf-8").read()

    ebar = re.search(r'<b>(.*?)</b>\s*<span>(.*?)</span>\s*<span>(.*?)</span>\s*<span>(.*?)</span>', html, re.S)
    ehero = between(html, '<section class="ehero">', '<section class="esec">')
    ehero_h1 = re.search(r"<h1>(.*?)</h1>", ehero).group(1)
    ehero_p = re.search(r"<p>(.*?)</p>", ehero).group(1)
    book_h2 = re.search(r'<div class="book">\s*<h2>(.*?)</h2>', ehero, re.S).group(1)
    book_labels = re.findall(r"<label>(.*?)</label>", ehero)
    book_btn = re.search(r'<div class="book">.*?<span class="btn">(.*?)</span>', ehero, re.S).group(1)

    takes = re.findall(
        r'<div class="take"><span>(.*?)</span><b>(.*?)</b><p>(.*?)</p></div>', html,
    )

    acards = re.findall(
        r'<div class="acard">\s*<div class="ph">(.*?)</div>\s*<b>(.*?)</b>\s*<p>(.*?)</p>\s*<span class="link">(.*?)</span>\s*</div>',
        html, re.S,
    )

    ccards = re.findall(
        r'<div class="ccard">\s*<div class="ph">(.*?)</div>\s*<b>(.*?)</b>\s*<p>(.*?)</p>\s*</div>',
        html, re.S,
    )

    people = re.findall(
        r'<div class="person">\s*<div class="ph">(.*?)</div>\s*<b>(.*?)</b>\s*<span>(.*?)</span>\s*<div class="mail">(.*?)</div>\s*</div>',
        html, re.S,
    )

    lwall_section = between(html, 'You are in good company</p>', '</section>')
    lwall_count = len(re.findall(r'<div class="ph">Client logo</div>', lwall_section))

    feed_section = between(html, '<h2>What people are saying</h2>', '<p class="feed-note">')
    posts = re.findall(r'<span class="who">(.*?)</span></div>\s*<div class="ph">(.*?)</div>', feed_section)
    feed_note = re.search(r'<p class="feed-note">(.*?)</p>', html).group(1)

    eclose = between(html, '<section class="eclose">', '<footer')
    eclose_h2 = re.search(r"<h2>(.*?)</h2>", eclose).group(1)
    eclose_btn = re.search(r'<span class="btn">(.*?)</span>', eclose).group(1)

    return dict(
        ebar_title=ebar.group(1), ebar_host=ebar.group(2), ebar_dates=ebar.group(3), ebar_format=ebar.group(4),
        h1=ehero_h1, dek=ehero_p,
        book_h2=book_h2, book_labels=book_labels, book_btn=book_btn,
        takes=takes, acards=acards, ccards=ccards, people=people,
        lwall_count=lwall_count, posts=posts, feed_note=feed_note,
        eclose_h2=eclose_h2, eclose_btn=eclose_btn,
    )


def _book_input_attrs(label):
    """Guess a sensible type/autocomplete for a registration-field label,
    so render_event() stays reusable for a future real event whose field
    labels may differ from this demo's Name/Work email/Company."""
    key = label.lower()
    if "email" in key:
        return "email", "email"
    if "phone" in key:
        return "tel", "tel"
    if "company" in key or "organization" in key:
        return "text", "organization"
    if key == "name" or "your name" in key:
        return "text", "name"
    return "text", "off"


def _book_field_html(i, label):
    fid = f"regField{i}"
    input_type, autocomplete = _book_input_attrs(label)
    return f'<div class="field"><label for="{fid}">{esc(label)}</label><input type="{input_type}" id="{fid}" autocomplete="{autocomplete}"></div>'


def registration_script(field_ids):
    ids_js = ", ".join(f'"{fid}"' for fid in field_ids)
    return f"""<script>
(function(){{
  var ids = [{ids_js}];
  var btn = document.getElementById("regBtn");
  var sent = document.getElementById("regSent");
  if (!btn) return;
  btn.addEventListener("click", function(){{
    var missing = [];
    ids.forEach(function(id){{
      var el = document.getElementById(id);
      if (el && !el.value.trim()) missing.push(el);
    }});
    if (missing.length){{ missing[0].focus(); return; }}
    sent.classList.add("show");
    sent.scrollIntoView({{behavior: "smooth", block: "nearest"}});
  }});
}})();
</script>"""


def render_event(data, base="../../"):
    """data: the dict shape returned by parse_template_demo() above. Pass a
    real event's copy in this same shape to generate a real instance."""
    takes_html = "".join(
        f'<div class="take"><span>{num}</span><b>{esc(h)}</b><p>{esc(p)}</p></div>'
        for num, h, p in data["takes"]
    )
    pc = PatternCycler()
    def ph_img(size):
        src, ratio = pc.next(size, base)
        return f'<img class="ph" style="aspect-ratio:{ratio}" src="{src}" alt="">'
    acards_html = "".join(
        f'<div class="acard">{ph_img("2col")}<b>{esc(h)}</b><p>{esc(p)}</p><span class="link">{esc(link)}</span></div>'
        for kind, h, p, link in data["acards"]
    )
    ccards_html = "".join(
        f'<div class="ccard">{ph_img("3col")}<b>{esc(h)}</b><p>{esc(p)}</p></div>'
        for kind, h, p in data["ccards"]
    )
    people_html = "".join(
        f'<div class="person">{ph_img("4col")}<b>{esc(name)}</b><span>{esc(title)}</span><div class="mail">{esc(mail)}</div></div>'
        for kind, name, title, mail in data["people"]
    )
    lwall_html = "".join(ph_img("4col") for _ in range(data["lwall_count"]))
    posts_html = "".join(
        f'<div class="post"><div class="top"><span class="av"></span><span class="who">{esc(who)}</span></div><div class="ph">{esc(body)}</div></div>'
        for who, body in data["posts"]
    )

    return f"""<!doctype html>
<html lang="en">
<head>
{head_html(f"{data['h1']} · Intercept", data["dek"])}
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header_html(base)}
<div class="ebar"><div class="ebar-row">
  <b>{esc(data["ebar_title"])}</b><span>{esc(data["ebar_host"])}</span><span>{esc(data["ebar_dates"])}</span><span>{esc(data["ebar_format"])}</span>
</div></div>

<main id="main">

<section class="ehero">
  <div class="wrap">
    <div class="ehero-grid">
      <div>
        <h1>{esc(data["h1"])}</h1>
        <p>{esc(data["dek"])}</p>
      </div>
      <div class="book">
        <h2>{esc(data["book_h2"])}</h2>
        {"".join(_book_field_html(i, l) for i, l in enumerate(data["book_labels"]))}
        <button type="button" class="btn" id="regBtn">{esc(data["book_btn"])}</button>
        <div class="rsent" id="regSent">Thanks — you&rsquo;re registered. We&rsquo;ll send the details to your inbox.</div>
      </div>
    </div>
  </div>
</section>

<section class="esec">
  <div class="wrap">
    <span class="eyebrow">From our session</span>
    <h2>Key takeaways</h2>
    <div class="takes">{takes_html}</div>
  </div>
</section>

<section class="esec">
  <div class="wrap">
    <span class="eyebrow">Explore further</span>
    <h2>Curated resources</h2>
    <div class="acards">{acards_html}</div>
  </div>
</section>

<section class="esec">
  <div class="wrap">
    <h2>Featured case studies</h2>
    <div class="ccards">{ccards_html}</div>
  </div>
</section>

<section class="esec">
  <div class="wrap">
    <span class="eyebrow">In attendance</span>
    <h2>Meet the team</h2>
    <div class="people">{people_html}</div>
  </div>
</section>

<section class="esec">
  <div class="wrap">
    <span class="eyebrow">You are in good company</span>
    <div class="lwall">{lwall_html}</div>
  </div>
</section>

<section class="esec">
  <div class="wrap">
    <span class="eyebrow">Live feed</span>
    <h2>What people are saying</h2>
    <div class="feed">{posts_html}</div>
    <p class="feed-note">{esc(data["feed_note"])}</p>
  </div>
</section>

<section class="eclose">
  <div class="wrap read">
    <h2>{esc(data["eclose_h2"])}</h2>
    <span class="btn">{esc(data["eclose_btn"])}</span>
  </div>
</section>

</main>
{footer_html(base)}
{registration_script([f"regField{i}" for i in range(len(data["book_labels"]))])}
</body>
</html>"""


def main():
    data = parse_template_demo()
    out = render_event(data)
    outdir = os.path.join(ROOT, "events", "template")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "index.html")
    open(path, "w", encoding="utf-8").write(out)
    print("Wrote", path)


if __name__ == "__main__":
    main()
