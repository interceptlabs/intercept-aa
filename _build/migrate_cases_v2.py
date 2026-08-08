#!/usr/bin/env python3
"""Migrate cases.json to the new wireframe-set slug scheme + service tags.

Copy for the 30 existing cases is already verbatim-identical to the new
wireframe set (confirmed by diff) — this script only renames slugs (drops
the client- prefix, per sitemap.html's proposed /our-work/<slug> URLs),
adds a `service` field (from our-work.html's data-s attributes), and parses
the one net-new case (microsoft_ai-in-practice.html) that didn't exist in
the old 30.
"""
import glob, html, json, os, re

BUILD_DIR = os.path.dirname(os.path.abspath(__file__))
WIRE_DIR = "/Users/jontoewsinterceptgroup.com/Downloads/New Wire Frames"
CASES_JSON = os.path.join(BUILD_DIR, "cases.json")
OUR_WORK_SRC = os.path.join(WIRE_DIR, "pages", "our-work.html")
NEW_CASE_FILE = os.path.join(WIRE_DIR, "pages", "case-studies", "microsoft_ai-in-practice.html")


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s).strip())


def between(text, start_marker, end_marker):
    i = text.index(start_marker) + len(start_marker)
    j = text.index(end_marker, i)
    return text[i:j]


def get_all(pattern, text, flags=re.S):
    return re.findall(pattern, text, flags)


def parse_new_case(path):
    src = open(path, encoding="utf-8").read()
    fname = os.path.basename(path)
    client_slug_raw, slug = fname[:-5].split("_", 1)
    client_slug = client_slug_raw.upper()

    hero = between(src, "<!-- HERO -->", "<!-- PROBLEM -->")
    eyebrow = strip_tags(re.search(r'<p class="eyebrow">(.*?)</p>', hero).group(1))
    client_display = eyebrow.split("·")[-1].strip()
    cred_m = re.search(r'<p class="credential"><span class="cred-mark"></span>(.*?)</p>', hero)
    credential = strip_tags(cred_m.group(1)) if cred_m else None
    h1 = strip_tags(re.search(r"<h1>(.*?)</h1>", hero).group(1))
    sub = strip_tags(re.search(r'<p class="sub">(.*?)</p>', hero).group(1))
    read_m = re.search(r'<span>(.*?-minute read)</span>', hero)
    read_time = read_m.group(1) if read_m else "3-minute read"

    problem_block = between(src, "<!-- PROBLEM -->", "<!-- SOLUTION -->")
    problem_h2 = strip_tags(re.search(r"<h2>(.*?)</h2>", problem_block).group(1))
    problem_paras = [strip_tags(p) for p in get_all(r"<p>(.*?)</p>", problem_block)]

    solution_block = between(src, "<!-- SOLUTION -->", "<!-- OUTCOME -->")
    solution_h2 = strip_tags(re.search(r"<h2>(.*?)</h2>", solution_block).group(1))
    sec_only = solution_block.split('<div class="wrap read">\n  <div class="acc">')[0]
    solution_intro_paras = [strip_tags(p) for p in get_all(r"<p>(.*?)</p>", sec_only)]
    acc_items = []
    for head, body in get_all(
        r'<div class="acc-item">\s*<div class="acc-head"><h3>(.*?)</h3><i>.*?</i></div>\s*<div class="acc-body"><p>(.*?)</p></div>\s*</div>',
        solution_block,
    ):
        acc_items.append({"title": strip_tags(head), "body": strip_tags(body)})

    outcome_block = between(src, "<!-- OUTCOME -->", "<!-- RESULT CLOSE -->")
    stats = []
    for val, label in get_all(r'<div class="stat"><div class="bar"></div><b>(.*?)</b><span>(.*?)</span></div>', outcome_block):
        stats.append({"value": strip_tags(val), "label": strip_tags(label)})

    result_block = between(src, "<!-- RESULT CLOSE -->", "<!-- TEMPLATE COMPONENT 2")
    result_h2 = strip_tags(re.search(r"<h2>(.*?)</h2>", result_block).group(1))
    result_paras = [strip_tags(p) for p in get_all(r"<p>(.*?)</p>", result_block)]

    related_block = between(src, "TEMPLATE COMPONENT 2", "TEMPLATE COMPONENTS 3")
    related = []
    for title, desc in get_all(r'<div class="rel"><div class="ph">.*?</div><h3>(.*?)</h3><p>(.*?)</p></div>', related_block):
        related.append({"title": strip_tags(title), "desc": strip_tags(desc)})

    return {
        "slug": slug,
        "client_slug": client_slug,
        "client_display": client_display,
        "short_title": slug.replace("-", " "),
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


def build_service_map():
    """our-work.html: <div class="case" data-s="Channel">...<h3>title</h3>..."""
    src = open(OUR_WORK_SRC, encoding="utf-8").read()
    starts = [m.start() for m in re.finditer(r'<div class="case" data-s="', src)]
    m = {}
    for i, pos in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(src)
        block = src[pos:end]
        data_s = re.match(r'<div class="case" data-s="([^"]+)">', block).group(1)
        h3 = re.search(r"<h3>(.*?)</h3>", block, re.S)
        if h3:
            m[strip_tags(h3.group(1))] = data_s
    return m


def main():
    cases = json.load(open(CASES_JSON, encoding="utf-8"))

    backup_path = CASES_JSON.replace(".json", ".pre-v2-migration.json")
    json.dump(cases, open(backup_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Backed up original -> {backup_path}")

    for c in cases:
        prefix = c["client_slug"].lower() + "-"
        assert c["slug"].startswith(prefix), f"unexpected slug/client_slug mismatch: {c['slug']} / {c['client_slug']}"
        c["slug"] = c["slug"][len(prefix):]

    new_case = parse_new_case(NEW_CASE_FILE)
    cases.append(new_case)

    service_map = build_service_map()
    print(f"Service map has {len(service_map)} entries")
    unmatched = []
    for c in cases:
        svc = service_map.get(c["h1"])
        if not svc:
            unmatched.append(c["h1"])
        c["service"] = svc

    if unmatched:
        print("UNMATCHED (no service found via exact h1 match):")
        for h1 in unmatched:
            print(" -", h1)
    else:
        print("All 31 cases matched to a service.")

    json.dump(cases, open(CASES_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Wrote {len(cases)} cases -> {CASES_JSON}")
    for c in cases:
        print(f"{c['slug']:35s} service={c.get('service')}")


if __name__ == "__main__":
    main()
