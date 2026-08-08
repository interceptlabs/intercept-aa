#!/usr/bin/env python3
"""Walk every .html file in the built site and verify every internal
(relative, non-anchor-only, non-external) href resolves to a real file on
disk. Reports broken links grouped by source file."""
import os, re, sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {"_build", ".git"}

def find_html_files():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            if f.endswith(".html"):
                out.append(os.path.join(dirpath, f))
    return sorted(out)

class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.parse_errors = []
    def error(self, message):
        self.parse_errors.append(message)
    def handle_starttag(self, tag, attrs):
        for name, val in attrs:
            if name == "href" and val:
                self.hrefs.append(val)

def is_external_or_special(href):
    return href.startswith(("http://", "https://", "mailto:", "tel:", "#"))

def main():
    files = find_html_files()
    print(f"Checking {len(files)} HTML files...\n")
    total_links = 0
    broken = {}
    parse_error_files = {}

    for f in files:
        html = open(f, encoding="utf-8").read()
        p = LinkExtractor()
        p.feed(html)
        if p.parse_errors:
            parse_error_files[f] = p.parse_errors

        src_dir = os.path.dirname(f)
        for href in p.hrefs:
            if is_external_or_special(href):
                continue
            total_links += 1
            # strip any #fragment off a relative link
            path_part = href.split("#")[0]
            if not path_part:
                continue
            target = os.path.normpath(os.path.join(src_dir, path_part))
            if not os.path.isfile(target):
                broken.setdefault(f, []).append(href)

    print(f"Total internal links checked: {total_links}")
    print(f"Files with parse errors: {len(parse_error_files)}")
    for f, errs in parse_error_files.items():
        print(f"  {os.path.relpath(f, ROOT)}: {errs}")

    print(f"\nFiles with broken links: {len(broken)}")
    for f, hrefs in sorted(broken.items()):
        rel = os.path.relpath(f, ROOT)
        print(f"\n{rel}:")
        for h in hrefs:
            print(f"  -> {h}")

    if not broken and not parse_error_files:
        print("\nAll clear — no broken internal links, no parse errors.")
        return 0
    return 1

if __name__ == "__main__":
    sys.exit(main())
