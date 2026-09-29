#!/usr/bin/env python3
"""Collect review drafts from the selected Wikisource edition.

Output is deliberately NOT a schema-1 release. Review the snapshots, Tamil,
chapter boundaries, rights, and divisions before generating release assets.
"""

import argparse
import hashlib
import json
import re
import time
import unicodedata
from html.parser import HTMLParser
from urllib.error import HTTPError
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API = "https://ta.wikisource.org/w/api.php"
INDEX = "திருக்குறள், மூலம்"
SOURCE = "srinivasan-1997-wikisource"
USER_AGENT = "ThirukkuralCorpusResearch/0.1 (public dataset; chapter snapshots)"
NEXT_REQUEST_AT = 0.0


def fetch(**params):
    global NEXT_REQUEST_AT
    url = API + "?" + urlencode({"format": "json", "formatversion": 2, **params})
    for attempt in range(6):
        time.sleep(max(0, NEXT_REQUEST_AT - time.monotonic()))
        NEXT_REQUEST_AT = time.monotonic() + 6.5
        try:
            with urlopen(Request(url, headers={"User-Agent": USER_AGENT}), timeout=30) as response:
                return json.load(response)
        except HTTPError as error:
            if error.code != 429 or attempt == 5:
                raise
            retry_after = error.headers.get("Retry-After", "")
            wait = int(retry_after) if retry_after.isdigit() else min(120, 10 * 2**attempt)
            print(f"Wikisource rate limit; waiting {wait}s", flush=True)
            NEXT_REQUEST_AT = time.monotonic() + max(wait, 2)


def page(title):
    data = fetch(action="query", prop="revisions", rvprop="ids|content", rvslots="main", titles=title)
    result = data["query"]["pages"][0]
    if result.get("missing"):
        raise ValueError(f"missing page: {title}")
    revision = result["revisions"][0]
    return revision["revid"], revision["slots"]["main"]["content"].encode("utf-8")


def rendered(revision_id):
    data = fetch(action="parse", oldid=revision_id, prop="text")
    return data["parse"]["text"]


class ChapterIndex(HTMLParser):
    def __init__(self):
        super().__init__()
        self.titles = set()

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            title = dict(attrs).get("title", "")
            if title.startswith(INDEX + "/"):
                self.titles.add(title)


class ChapterText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_body = False
        self.in_para = False
        self.para = []
        self.paras = []
        self.capture_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "mw-parser-output" in attrs.get("class", "").split():
            self.in_body = True
            self.capture_depth += 1
        elif self.in_body and tag not in ("br", "img", "hr", "meta", "link"):
            self.capture_depth += 1
        if self.in_body and tag == "p":
            self.in_para = True
            self.para = []
        elif self.in_para and tag == "span" and re.fullmatch(r"line[0-9]+", attrs.get("id", "")):
            self.para.append("\n")
        elif self.in_para and tag == "br":
            self.para.append("\n")

    def handle_endtag(self, tag):
        if tag == "p" and self.in_para:
            self.paras.append("".join(self.para))
            self.in_para = False
        if self.in_body and tag not in ("br", "img", "hr", "meta", "link"):
            self.capture_depth -= 1
            if self.capture_depth == 0:
                self.in_body = False

    def handle_data(self, data):
        if self.in_para:
            self.para.append(data)


def extract_chapter(html):
    parser = ChapterText()
    parser.feed(html)
    # Verse paragraphs may be split at scan/page boundaries. Preserve order
    # and require exactly ten numbered two-line groups across those paragraphs.
    candidates = []
    for para in parser.paras:
        lines = [x.strip().replace("\u2060", "") for x in para.splitlines()]
        lines = [unicodedata.normalize("NFC", x.strip()) for x in lines if x.strip()]
        numbers = [x for x in lines if re.fullmatch(r"[0-9]{1,4}", x)]
        if numbers:
            candidates.extend(lines)
    lines = candidates
    if sum(bool(re.fullmatch(r"[0-9]{1,4}", x)) for x in lines) != 10:
        raise ValueError("expected ten verse numbers across chapter paragraphs")
    groups, pending = [], []
    for line in lines:
        if re.fullmatch(r"[0-9]{1,4}", line):
            if len(pending) != 2:
                raise ValueError(f"verse {line}: expected two Tamil lines, got {pending}")
            groups.append((int(line), *pending))
            pending = []
        else:
            pending.append(line)
    if pending or len(groups) != 10:
        raise ValueError("chapter has leftover text or does not have ten verses")
    first = groups[0][0]
    if first % 10 != 1:
        raise ValueError(f"unexpected first printed number {first}")
    return (first - 1) // 10 + 1, groups


def collect(destination, limit=133):
    cached_index = list((destination / "snapshots").glob("index-oldid-*.html"))
    if len(cached_index) > 1:
        raise ValueError("multiple cached index revisions")
    if cached_index:
        index_rev = int(re.search(r"oldid-(\d+)", cached_index[0].name)[1])
        index_html = cached_index[0].read_text(encoding="utf-8")
        source = cached_index[0].with_suffix(".wikitext").read_bytes()
    else:
        index_rev, source = page(INDEX)
        index_html = rendered(index_rev)
    links = ChapterIndex()
    links.feed(index_html)
    if len(links.titles) != 133:
        raise ValueError(f"expected 133 distinct chapter links, found {len(links.titles)}")
    destination.mkdir(parents=True, exist_ok=True)
    snapshots = destination / "snapshots"
    snapshots.mkdir(exist_ok=True)
    (snapshots / f"index-oldid-{index_rev}.html").write_bytes(index_html.encode("utf-8"))
    (snapshots / f"index-oldid-{index_rev}.wikitext").write_bytes(source)
    cache = {}
    for wrapper in list(snapshots.glob("chapter-*-oldid-*.wikitext")) + list(snapshots.glob("pending-oldid-*.wikitext")):
        match = re.search(r"\|\s*section\s*=\s*(.+)", wrapper.read_text(encoding="utf-8"))
        if match and wrapper.with_suffix(".html").exists():
            title = INDEX + "/" + match[1].strip()
            if title not in links.titles or title in cache:
                raise ValueError(f"unknown or duplicate cached chapter: {title}")
            cache[title] = wrapper
    found = {}
    anomalies = []
    for title in sorted(links.titles):
        if title in cache:
            wrapper = cache[title]
            revision = int(re.search(r"oldid-(\d+)", wrapper.name)[1])
            raw = wrapper.read_bytes()
            html = wrapper.with_suffix(".html").read_text(encoding="utf-8")
        else:
            revision, raw = page(title)
            html = rendered(revision)
            # Retain failed pages too, so parser repairs do not need a refetch.
            pending = snapshots / f"pending-oldid-{revision}"
            pending.with_suffix(".html").write_bytes(html.encode("utf-8"))
            pending.with_suffix(".wikitext").write_bytes(raw)
        try:
            chapter_no, verses = extract_chapter(html)
        except ValueError as error:
            raise ValueError(f"{title} oldid={revision}: {error}") from error
        if chapter_no in found:
            raise ValueError(f"duplicate chapter {chapter_no}: {title}")
        for position, (number, _, _) in enumerate(verses, 1):
            expected = (chapter_no - 1) * 10 + position
            if number != expected:
                anomalies.append({"kural_no": expected, "source_printed_no": str(number),
                                  "chapter_no": chapter_no, "source_page": title,
                                  "review_status": "pending", "reason": "printed numbering differs from position; check scan"})
        snapshot_name = f"chapter-{chapter_no:03d}-oldid-{revision}.html"
        (snapshots / snapshot_name).write_bytes(html.encode("utf-8"))
        (snapshots / f"chapter-{chapter_no:03d}-oldid-{revision}.wikitext").write_bytes(raw)
        found[chapter_no] = {
            "chapter_no": chapter_no,
            "name_ta": title.removeprefix(INDEX + "/"),
            "source_id": SOURCE,
            "source_page": title,
            "source_revision_id": str(revision),
            "source_checksum": hashlib.sha256(html.encode("utf-8")).hexdigest(),
            "snapshot": "snapshots/" + snapshot_name,
            "wrapper_wikitext_checksum": hashlib.sha256(raw).hexdigest(),
            "kurals": [
                {"chapter_no": chapter_no, "position": position,
                 "source_printed_no": str(number), "line_1": a, "line_2": b,
                 "source_id": SOURCE}
                for position, (number, a, b) in enumerate(verses, 1)
            ],
        }
        print(f"{chapter_no:03d} oldid={revision} {title}", flush=True)
        if len(found) >= limit:
            break
    (destination / "chapters.json").write_text(
        json.dumps({"status": "unreviewed-draft", "source_index_revision": str(index_rev),
                    "source_index_checksum": hashlib.sha256(index_html.encode("utf-8")).hexdigest(),
                    "source_index_wrapper_wikitext_checksum": hashlib.sha256(source).hexdigest(),
                    "numbering_anomalies_pending_review": anomalies,
                    "chapters": [found[n] for n in sorted(found)]}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    if limit == 133 and set(found) != set(range(1, 134)):
        raise ValueError(f"incomplete chapter numbering: {sorted(set(range(1, 134)) - set(found))}")


if __name__ == "__main__":
    argp = argparse.ArgumentParser(description=__doc__)
    argp.add_argument("destination", type=Path)
    argp.add_argument("--limit", type=int, default=133, choices=range(1, 134), metavar="1..133")
    args = argp.parse_args()
    collect(args.destination, args.limit)
