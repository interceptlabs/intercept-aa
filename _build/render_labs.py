#!/usr/bin/env python3
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import esc, head_html, header_html, footer_html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = """
.shero{padding:64px 0 40px}
.shero-grid{display:grid;grid-template-columns:1fr 1.05fr;gap:56px;align-items:center}
.shero .ph{aspect-ratio:4/3}
.shero h1{font-size:var(--fs-1);line-height:1.05;letter-spacing:-.03em;margin:0 0 16px;max-width:16ch}
.shero .sub{font-size:var(--fs-5);line-height:1.4;color:var(--ink-2);margin:0}
.sec{padding:44px 0}
.sec h2{font-size:var(--fs-2);line-height:1.12;letter-spacing:-.026em;margin:0 0 18px;max-width:20ch}
.sec p{font-size:var(--fs-6);line-height:1.6;color:var(--ink-2);margin:0 0 18px}
.how{padding:56px 0}
.how-grid{display:grid;grid-template-columns:1fr 1.2fr;gap:60px;margin-top:30px;align-items:start}
.hitem{padding:22px 0}
.hitem .row{display:flex;align-items:flex-start;justify-content:space-between;gap:20px}
.hitem i{display:block;font-style:normal;font-family:var(--font-body);font-weight:600;font-size:var(--fs-8);letter-spacing:.09em;color:var(--ink-3);margin-bottom:8px}
.hitem b{display:block;font-size:var(--fs-4);line-height:1.25;letter-spacing:-.016em;font-weight:700}
.hitem span{display:block;font-size:var(--fs-7);line-height:1.55;color:var(--ink-2);margin-top:10px;max-width:44ch}
.how-panel .ph{aspect-ratio:4/3}
.quote{background:var(--carbon-500);color:#fff}
.quote-inner{max-width:var(--maxw);margin:0 auto;padding:80px 32px}
.quote blockquote{margin:0;font-size:var(--fs-1);line-height:1.14;letter-spacing:-.03em;font-weight:700;max-width:20ch}
.quote cite{display:block;font-style:normal;font-size:var(--fs-8);letter-spacing:.09em;text-transform:uppercase;color:var(--halo-500);margin-top:26px}
.proof{padding:56px 0 12px}
.proof-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:32px;margin-top:24px}
.proof .ph{aspect-ratio:16/9;margin-bottom:16px}
.proof h3{font-size:var(--fs-4);line-height:1.2;letter-spacing:-.018em;margin:0 0 8px;font-weight:700}
.proof p{font-size:var(--fs-7);line-height:1.5;color:var(--ink-2);margin:0 0 14px}
.pending{font-size:var(--fs-8);letter-spacing:.09em;text-transform:uppercase;color:var(--ink-3)}
.convert{padding:56px 0;background:var(--band);margin-top:40px;text-align:center}
.convert h2{font-size:var(--fs-2);line-height:1.08;letter-spacing:-.028em;margin:0 auto 20px;max-width:18ch}
@media(max-width:900px){.shero-grid,.proof-grid{grid-template-columns:1fr}.how-grid{grid-template-columns:1fr}}
"""

STEPS = [
    ("Find the use case", "We look for the unproven approach worth testing, then scope it to run inside the data estate, privacy posture, and legal constraints the environment requires."),
    ("Split the cost", "Intercept puts in capital, time, and expertise against the client budget, and funds up to half of delivery."),
    ("Measure what happens", "We design the pilot, put it in front of a real audience, and read the result."),
    ("Optimize continuously", "Learnings from the pilot directly inform recurring optimization loops."),
    ("Move it into production", "What works goes into production faster than the conventional cycle allows, and runs as a managed service so the client carries no model risk."),
]

def render():
    steps_html = "".join(
        f'<div class="hitem"><div class="row"><div><i>Step {i+1}</i><b>{esc(t)}</b></div></div><span>{esc(d)}</span></div>'
        for i, (t, d) in enumerate(STEPS)
    )
    return f"""<!doctype html>
<html lang="en">
<head>
{head_html("Intercept Labs · Intercept", "A co-investment model where we explore unproven agentic use cases and share the risk and the learnings.")}
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header_html("../")}
<main id="main">

<section class="shero">
  <div class="wrap"><div class="shero-grid">
    <div class="ph" style="aspect-ratio:4/3">Labs</div>
    <div>
      <span class="eyebrow">Intercept Labs</span>
      <h1>Exploring the frontier together</h1>
      <p class="sub">A co-investment model where we explore unproven agentic use cases and share the risk and the learnings</p>
    </div>
  </div></div>
</section>

<section class="sec">
  <div class="wrap read">
    <p>Our clients are under pressure to innovate faster and do more with less. Labs is how we make that possible, putting our own capital, time, and expertise alongside the client budget.</p>
  </div>
</section>

<section class="how band-tint">
  <div class="wrap">
    <h2>How it works</h2>
    <div class="how-grid">
      <div>{steps_html}</div>
      <div class="how-panel"><div class="ph" style="aspect-ratio:4/3">Labs process</div></div>
    </div>
  </div>
</section>

<section class="quote">
  <div class="quote-inner">
    <blockquote>&ldquo;If you know in advance that it&rsquo;s going to work, it&rsquo;s not an experiment.&rdquo;</blockquote>
    <cite>Jeff Bezos&rsquo; letter to Amazon shareholders</cite>
  </div>
</section>

<section class="proof">
  <div class="wrap">
    <h2 style="font-size:var(--fs-3);margin-bottom:8px">What has come out of Labs</h2>
    <div class="proof-grid">
      <div>
        <div class="ph" style="aspect-ratio:16/9">AMD</div>
        <h3>One-of-one content engine</h3>
        <p>Built for AMD, it tailors every asset to the individual downloading it and the organization they represent.</p>
        <span class="pending">Case study in the works</span>
      </div>
      <div>
        <div class="ph" style="aspect-ratio:16/9">SAP</div>
        <h3>AI avatar video series</h3>
        <p>An agentic workflow built for SAP that cut production costs by 55% and timelines by 23%.</p>
        <a class="link" href="../our-work/lights-camera-avatars/index.html">Read the case study</a>
      </div>
    </div>
  </div>
</section>

<section class="convert">
  <div class="wrap read">
    <span class="eyebrow">Start the conversation</span>
    <h2>Have a wild idea? We&rsquo;d love to hear it.</h2>
    <a class="btn" href="../contact/index.html">Talk to Intercept Labs</a>
  </div>
</section>

</main>
{footer_html("../")}
</body>
</html>"""

if __name__ == "__main__":
    outdir = os.path.join(ROOT, "intercept-labs")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "index.html")
    open(path, "w", encoding="utf-8").write(render())
    print("Wrote", path)
