#!/usr/bin/env python3
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import esc, head_html, header_html, footer_html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = """
.shero{padding:64px 0 40px}
.shero-grid{display:grid;grid-template-columns:1fr 1.05fr;gap:56px;align-items:center}
.shero video{aspect-ratio:4/3;width:100%;object-fit:cover;display:block;background:var(--halo-200)}
.shero h1{font-size:var(--fs-1);line-height:1.05;letter-spacing:-.03em;margin:0 0 16px;max-width:16ch}
.shero .sub{font-size:var(--fs-5);line-height:1.4;color:var(--ink-2);margin:0}
.sec{padding:44px 0}
.sec h2{font-size:var(--fs-2);line-height:1.12;letter-spacing:-.026em;margin:0 0 18px;max-width:20ch}
.sec p{font-size:var(--fs-6);line-height:1.6;color:var(--ink-2);margin:0 0 18px}
.vidband{position:relative;overflow:hidden}
.vidband video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.5;z-index:0}
.vidband.dark{background:var(--carbon-500);color:#fff}
.vidband-inner{position:relative;z-index:1;max-width:var(--maxw);margin:0 auto;padding:56px 32px}
.stat-row{display:grid;grid-template-columns:repeat(3,1fr);gap:40px}
.acc{margin-top:8px;max-width:var(--readw)}
.acc-item{padding:18px 0}
.acc-head{display:flex;justify-content:space-between;align-items:center;gap:24px}
.acc-head h3{font-size:var(--fs-4);line-height:1.3;margin:0;font-weight:700}
.acc-body{padding-top:8px}
.acc-body p{font-size:var(--fs-7);line-height:1.55;color:var(--ink-2);margin:0}
.recog h2{font-size:var(--fs-2);margin:0 0 16px}
.recog p{max-width:var(--readw)}
.cardgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:24px}
.tcard .ph{aspect-ratio:4/3;margin-bottom:12px}
.tcard b{display:block;font-size:var(--fs-6);font-weight:700;margin-bottom:5px}
.tcard span{display:block;font-size:var(--fs-8);color:var(--ink-2)}
.bio-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:36px 28px;margin-top:24px}
.bio .ph{aspect-ratio:4/3;margin-bottom:14px}
.bio b{display:block;font-size:var(--fs-6);letter-spacing:-.01em}
.bio em{display:block;font-style:normal;font-size:var(--fs-8);color:var(--ink-3);margin:2px 0 10px}
.bio p{font-size:var(--fs-7);line-height:1.5;color:var(--ink-2);margin:0}
.two-up{display:grid;grid-template-columns:1fr 1.05fr;gap:56px;align-items:center}
.careers-grid{display:grid;grid-template-columns:1.15fr 1fr;gap:48px;align-items:center}
.convert{padding:56px 0;background:var(--band);margin-top:40px;text-align:center}
.convert h2{font-size:var(--fs-2);line-height:1.08;letter-spacing:-.028em;margin:0 auto 20px;max-width:18ch}
@media(max-width:900px){.shero-grid,.two-up,.careers-grid{grid-template-columns:1fr}.bio-grid{grid-template-columns:1fr 1fr}.cardgrid,.stat-row{grid-template-columns:1fr 1fr}}
"""

def vid(name, ext="mp4"):
    return f'<source src="assets/video/{name}.{ext}" type="video/{ext}">'

def render():
    team = [
        ("Andrew Au", "Co-CEO", "Leads strategy and AI integration for clients including Microsoft, SAP, Intel, and HP. One of the youngest members inducted into the Entrepreneurs' Organization, named to Forbes 30 Under 30, and a regular keynote speaker on AI in B2B."),
        ("Shaheen Yazdani", "Co-CEO", "Bio to come. Target 40 to 50 words."),
        ("Francis Silva", "Chief Technology Officer", "Designs the AI platforms and go-to-market systems behind the work. Previously EVP of Digital and AI at a North American loyalty technology company, leading teams of 250. Teaches analytics and AI marketing at Queen’s Smith School of Business."),
        ("Laura White", "Chief Financial Officer", "Bio to come. Target 40 to 50 words."),
        ("David Toto", "Managing Director", "Bio to come. Target 40 to 50 words."),
        ("Jeff Lewis", "Head of Client Advisory", "Bio to come. Target 40 to 50 words."),
    ]
    bio_html = "".join(
        f'<div class="bio"><div class="ph">{esc(n)}</div><b>{esc(n)}</b><em>{esc(r)}</em><p>{esc(b)}</p></div>'
        for n, r, b in team
    )
    awards = [
        ("Agency of the Year", "Chief Marketer, 2025 and 2026"),
        ("Great Place to Work", "Certified seven years running"),
        ("B Corp", "Certified"),
        ("The Drum Honors", "Recommended agencies, 2026"),
    ]
    awards_html = "".join(f'<div class="tcard"><div class="ph">Award</div><b>{esc(a)}</b><span>{esc(d)}</span></div>' for a, d in awards)

    acc_items = [
        ("Time-tested industry expertise", "The best B2B work comes from practitioners who know which audience signals matter and which proof points shift perception. We built that pattern recognition across silicon, hyperscalers, OEMs, ISVs, and networking infrastructure."),
        ("Proprietary buyer intelligence", "No single data asset tells the whole story, so we built our own layer. Watchtower tracks what B2B buyers say when you are not in the room, alongside direct decision-maker interviews and partner data."),
        ("A full technology practice", "We build agentic solutions in-house instead of waiting on an external technology partner, which moves work from concept to production faster and keeps the thinking with the people doing it."),
        ("Enterprise-grade execution", "We work with the world’s largest enterprises, so privacy, legal, and compliance review are built into the operating model from day one instead of slowing the work down later."),
    ]
    acc_html = "".join(
        f'<div class="acc-item"><div class="acc-head"><h3>{esc(t)}</h3></div><div class="acc-body"><p>{esc(d)}</p></div></div>'
        for t, d in acc_items
    )

    return f"""<!doctype html>
<html lang="en">
<head>
{head_html("About Us · Intercept", "We are an award-winning B2B marketing agency built for the technology sector, and we have been at it since 2006.")}
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header_html("../")}
<main id="main">

<section class="shero">
  <div class="wrap"><div class="shero-grid">
    <div class="ph" style="aspect-ratio:4/3">Team or office</div>
    <div>
      <span class="eyebrow">About us</span>
      <h1>Twenty years inside global tech</h1>
      <p class="sub">We are an award-winning B2B marketing agency built for the technology sector, and we have been at it since 2006.</p>
    </div>
  </div></div>
</section>

<section class="sec">
  <div class="wrap read">
    <h2>What changed, and why we did</h2>
    <p>The traditional agency was a body-shop business. Stack more people, bill more hours, and let the size of the firm set its capacity. That stopped working in the AI era.</p>
    <p>So we rebuilt how the work gets done. AI handles the keep-the-lights-on work, which frees our people for the work that has no precedent. Both run as managed services, so clients are not procuring another vendor every time the technology moves.</p>
  </div>
</section>

<section class="sec band-navy">
  <div class="wrap">
    <div class="stat-row">
      <div class="stat"><b>2006</b><span>our founding year</span></div>
      <div class="stat"><b>135+</b><span>awards for B2B marketing</span></div>
      <div class="stat"><b>9</b><span>years average client tenure</span></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <h2>How we are different</h2>
    <div class="acc">{acc_html}</div>
  </div>
</section>

<section class="sec band-tint recog">
  <div class="wrap">
    <h2>Recognition</h2>
    <div class="cardgrid">{awards_html}</div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <h2 style="font-size:var(--fs-3)">Leadership</h2>
    <div class="bio-grid">{bio_html}</div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="two-up">
      <div class="ph" style="aspect-ratio:4/3">Team grid or map</div>
      <div>
        <h2 style="margin-bottom:16px">A team built to find the best people, anywhere</h2>
        <p style="margin:0">We work remotely across North America, from San Francisco and San Diego to Toronto, Calgary, and Vancouver, with a growing team of specialists in Islamabad and Oman.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec band-tint">
  <div class="wrap">
    <div class="careers-grid">
      <div class="ph" style="aspect-ratio:4/3">Team visual</div>
      <div>
        <span class="eyebrow">Careers</span>
        <h2>We hire people who want the harder brief</h2>
        <a class="link" href="../careers/open-roles/index.html">See open roles</a>
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

if __name__ == "__main__":
    outdir = os.path.join(ROOT, "about-us")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "index.html")
    open(path, "w", encoding="utf-8").write(render())
    print("Wrote", path)
