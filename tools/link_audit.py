#!/usr/bin/env python3
"""Site-wide internal-link audit for daddymi777.com.

Crawls from the seed pages, collects every internal href/src (HTML
attributes, CSS url() and JS `src:` asset strings), and verifies each
unique internal URL returns HTTP 200. Exits non-zero on any failure —
this is the deploy gate defined in docs/SITE-STANDARDS.md §5.

Usage:
    python3 tools/link_audit.py [--base https://daddymi777.com]
                                [--max-pages 400] [--workers 12]

Standard library only.
"""
import argparse
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser

SEEDS = [
    "/", "/en/", "/zh-hant/", "/ja/", "/ko/",
    "/music/", "/music/en/", "/music/tc/", "/music/ja/", "/music/ko/",
    "/gospel-wisdom/", "/gospel-wisdom/theme-zh/", "/gospel-wisdom/theme-en/",
    "/gospel-wisdom/dian-deng/", "/gospel-wisdom/birthday-light/",
    "/gospel-wisdom/mixi/",
    "/music/mx005/", "/music/mx005/en/", "/music/mx005/tc/",
    "/music/mx005/ja/", "/music/mx005/ko/",
    "/music/mx005/archive/", "/album/gallery/", "/order/",
    "/publications/", "/concordance/", "/404.html",
]

REF_ATTRS = ("href", "src", "action", "poster")
URL_RE = re.compile(r'url\(\s*"?([^")]+)"?\s*\)')
JS_SRC_RE = re.compile(r'\bsrc:\s*"([^"]+)"')
SKIP = ("mailto:", "tel:", "data:", "javascript:", "sms:", "ftp:")


class RefParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in REF_ATTRS and value:
                self.refs.append(value)


def fetch(url, method="GET"):
    req = urllib.request.Request(
        url, method=method,
        headers={"User-Agent": "daddymi-link-audit/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            body = r.read() if method == "GET" else b""
            return r.status, r.headers.get_content_type(), body
    except urllib.error.HTTPError as e:
        return e.code, "", b""
    except Exception as e:  # DNS, TLS, timeouts
        return -1, str(e), b""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="https://daddymi777.com")
    ap.add_argument("--max-pages", type=int, default=400)
    ap.add_argument("--workers", type=int, default=12)
    args = ap.parse_args()
    base = args.base.rstrip("/")
    base_host = urllib.parse.urlparse(base).netloc

    def internal(raw, page_url):
        """Absolute URL if `raw` is an internal reference, else None."""
        if not raw or raw.startswith(SKIP) or raw.startswith("#"):
            return None
        u = urllib.parse.urljoin(page_url, raw)
        p = urllib.parse.urlparse(u)
        if p.netloc != base_host or p.scheme not in ("http", "https"):
            return None
        return urllib.parse.urlunparse(p._replace(fragment=""))

    # ---- crawl ------------------------------------------------------
    queue = [base + s for s in SEEDS]
    seen_pages, all_refs = set(), {}
    while queue and len(seen_pages) < args.max_pages:
        url = queue.pop(0)
        if url in seen_pages:
            continue
        seen_pages.add(url)
        status, ctype, body = fetch(url)
        if status != 200:
            all_refs.setdefault(url, set()).add("(seed)")
            continue
        if "text/html" not in ctype and "text/css" not in ctype:
            continue
        text = body.decode("utf-8", "replace")
        refs = []
        if "text/html" in ctype:
            parser = RefParser()
            parser.feed(text)
            refs += parser.refs
            refs += JS_SRC_RE.findall(text)
        refs += URL_RE.findall(text)
        for raw in refs:
            u = internal(raw, url)
            if u:
                all_refs.setdefault(u, set()).add(url)
                path = urllib.parse.urlparse(u).path
                if (path.endswith("/") or path.endswith(".html")) \
                        and u not in seen_pages and u not in queue:
                    queue.append(u)

    # ---- verify -----------------------------------------------------
    targets = sorted(all_refs)
    print("pages crawled: %d · unique internal URLs to check: %d"
          % (len(seen_pages), len(targets)))

    def check(u):
        status, _, _ = fetch(u, method="HEAD")
        if status in (405, 501, -1):
            status, _, _ = fetch(u, method="GET")
        return u, status

    failures = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for u, status in ex.map(check, targets):
            if status != 200:
                failures.append((u, status))

    print("checked: %d · OK: %d · FAILED: %d"
          % (len(targets), len(targets) - len(failures), len(failures)))
    for u, status in failures:
        srcs = ", ".join(sorted(all_refs[u])[:3])
        print("FAIL %s -> %s (referenced from: %s)" % (status, u, srcs))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
