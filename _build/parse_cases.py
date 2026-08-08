#!/usr/bin/env python3
"""Parse the 28 source case-study wireframes into structured JSON, verbatim."""
import glob, html, json, os, re

SRC_DIR = "/Users/jontoewsinterceptgroup.com/Downloads/case studies"
OUT = "/Users/jontoewsinterceptgroup.com/Creative-Projects/intercept-aa/_build/cases.json"

def between(text, start_marker, end_marker):
    i = text.index(start_marker) + len(start_marker)
    j = text.index(end_marker, i)
    return text[i:j]

def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s).strip())

def get_all(pattern, text, flags=re.S):
    return re.findall(pattern, text, flags)

def parse_file(path):
    html = open(path, encoding="utf-8").read()
    fname = os.path.basename(path)
    # slug/short-title from filename: intercept-case-study_CLIENT_Short-Title_2026-08-06.html
    m = re.match(r"intercept-case-study_([A-Za-z0-9\-]+)_(.+)_2026-08-06\.html", fname)
    client_slug, title_slug = m.group(1), m.group(2)
    short_title = title_slug.replace("-", " ")
    slug = (client_slug + "-" + title_slug).lower()

    hero = between(html, "<!-- HERO -->", "<!-- PROBLEM -->")
    eyebrow = strip_tags(re.search(r'<p class="eyebrow">(.*?)</p>', hero).group(1))
    client_display = eyebrow.split("·")[-1].strip()
    cred_m = re.search(r'<p class="credential"><span class="cred-mark"></span>(.*?)</p>', hero)
    credential = strip_tags(cred_m.group(1)) if cred_m else None
    h1 = strip_tags(re.search(r"<h1>(.*?)</h1>", hero).group(1))
    sub = strip_tags(re.search(r'<p class="sub">(.*?)</p>', hero).group(1))
    read_m = re.search(r'<span>(.*?-minute read)</span>', hero)
    read_time = read_m.group(1) if read_m else "3-minute read"

    problem_block = between(html, "<!-- PROBLEM -->", "<!-- SOLUTION -->")
    problem_h2 = strip_tags(re.search(r"<h2>(.*?)</h2>", problem_block).group(1))
    problem_paras = [strip_tags(p) for p in get_all(r"<p>(.*?)</p>", problem_block)]

    solution_block = between(html, "<!-- SOLUTION -->", "<!-- OUTCOME -->")
    solution_h2 = strip_tags(re.search(r"<h2>(.*?)</h2>", solution_block).group(1))
    # intro paragraph(s) live in <section class="sec">...</section> before the .acc div
    sec_only = solution_block.split('<div class="wrap read">\n  <div class="acc">')[0]
    solution_intro_paras = [strip_tags(p) for p in get_all(r"<p>(.*?)</p>", sec_only)]
    acc_items = []
    for head, body in get_all(r'<div class="acc-item">\s*<div class="acc-head"><h3>(.*?)</h3><i>.*?</i></div>\s*<div class="acc-body"><p>(.*?)</p></div>\s*</div>', solution_block):
        acc_items.append({"title": strip_tags(head), "body": strip_tags(body)})

    outcome_block = between(html, "<!-- OUTCOME -->", "<!-- RESULT CLOSE -->")
    stats = []
    for val, label in get_all(r'<div class="stat"><div class="bar"></div><b>(.*?)</b><span>(.*?)</span></div>', outcome_block):
        stats.append({"value": strip_tags(val), "label": strip_tags(label)})

    result_block = between(html, "<!-- RESULT CLOSE -->", "<!-- TEMPLATE COMPONENT 2")
    result_h2 = strip_tags(re.search(r"<h2>(.*?)</h2>", result_block).group(1))
    result_paras = [strip_tags(p) for p in get_all(r"<p>(.*?)</p>", result_block)]

    related_block = between(html, "TEMPLATE COMPONENT 2", "TEMPLATE COMPONENTS 3")
    related = []
    for title, desc in get_all(r'<div class="rel"><div class="ph">.*?</div><h3>(.*?)</h3><p>(.*?)</p></div>', related_block):
        related.append({"title": strip_tags(title), "desc": strip_tags(desc)})

    return {
        "slug": slug,
        "client_slug": client_slug,
        "client_display": client_display,
        "short_title": short_title,
        "eyebrow": eyebrow,
        "credential": credential,
        "h1": h1,
        "sub": sub,
        "read_time": read_time,
        "problem_h2": problem_h2,
        "problem_paras": problem_paras,
        "solution_h2": solution_h2,
        "solution_intro_paras": solution_intro_paras,
        "acc_items": acc_items,
        "stats": stats,
        "result_h2": result_h2,
        "result_paras": result_paras,
        "related": related,
        "source_file": fname,
    }

def main():
    files = sorted(glob.glob(os.path.join(SRC_DIR, "*.html")))
    cases = [parse_file(f) for f in files]
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(cases, f, indent=2, ensure_ascii=False)
    print(f"Parsed {len(cases)} cases -> {OUT}")
    # sanity report
    for c in cases:
        n_stats = len(c["stats"])
        n_acc = len(c["acc_items"])
        n_rel = len(c["related"])
        flag = "" if (n_stats == 3 and n_acc == 4 and n_rel == 3) else "  <-- CHECK"
        print(f"{c['slug']:45s} stats={n_stats} acc={n_acc} rel={n_rel}{flag}")

if __name__ == "__main__":
    main()
