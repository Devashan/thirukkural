#!/usr/bin/env python3
"""Validate the structural and byte-integrity parts of release schema 1."""

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path


HEX = re.compile(r"[0-9a-f]{64}\Z")
SEMVER = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+\Z")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def check(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    def unique_pairs(pairs):
        value = {}
        for key, item in pairs:
            check(key not in value, f"{path.name}: duplicate JSON key {key}")
            value[key] = item
        return value

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_pairs)


def unique(rows, key, label):
    keys = [key(row) for row in rows]
    check(len(keys) == len(set(keys)), f"duplicate {label}")
    return set(keys)


def nonempty(value, label):
    check(isinstance(value, str) and bool(value.strip()), f"missing {label}")
    check(value == unicodedata.normalize("NFC", value), f"non-NFC {label}")
    check("\ufffd" not in value, f"replacement character in {label}")


def validate(directory, expected_sums):
    check(set(p.name for p in directory.iterdir()) == {"manifest.json", "corpus.json", "SHA256SUMS"}, "release files must be exactly manifest.json, corpus.json and SHA256SUMS")
    sums = (directory / "SHA256SUMS").read_bytes()
    check(digest(sums) == expected_sums, "SHA256SUMS does not match pinned digest")
    check(sums.endswith(b"\n"), "SHA256SUMS must end with newline")
    lines = sums.decode("ascii").splitlines()
    check(len(lines) == 2, "SHA256SUMS must contain two entries")
    for line, name in zip(lines, ("corpus.json", "manifest.json")):
        check(re.fullmatch(r"[0-9a-f]{64}  " + re.escape(name), line) is not None, f"invalid checksum line for {name}")
        check(digest((directory / name).read_bytes()) == line[:64], f"checksum mismatch: {name}")

    manifest, corpus = (read_json(directory / name) for name in ("manifest.json", "corpus.json"))
    check(type(manifest.get("schema_version")) is int and manifest["schema_version"] == 1, "unsupported schema version")
    check(isinstance(manifest.get("release_version"), str) and SEMVER.fullmatch(manifest["release_version"]), "invalid release version")
    nonempty(manifest.get("created_at"), "created_at")
    check(set(corpus) == {"paal", "iyal", "chapters", "kurals", "translations", "transliterations"}, "wrong corpus collections")
    for name in corpus:
        check(isinstance(corpus[name], list), f"{name} must be an array")

    review = manifest["review"]
    check(all(review.get(key) == "approved" for key in ("source_rights", "tamil_text", "translation_coverage", "transliteration")), "release review gates not approved")
    sources = manifest["sources"]
    source_ids = unique(sources, lambda x: x["source_id"], "source ID")
    check(source_ids, "no sources")
    for src in sources:
        check(src["role"] in ("canonical", "witness"), "invalid source role")
        for field in ("work", "author_translator_editor", "publisher", "year", "url", "retrieved_at", "rights_basis", "licence"):
            nonempty(src.get(field), f"source {src['source_id']} {field}")
        check(isinstance(src["transform_steps"], list) and isinstance(src["numbering_anomalies"], list), "source transforms/anomalies must be arrays")
        for snap in src["snapshots"]:
            nonempty(snap.get("locator"), "snapshot locator")
            nonempty(snap.get("revision_id"), "snapshot revision")
            check(HEX.fullmatch(snap["sha256"]) is not None, "invalid snapshot hash")
    snapshots = {(src["source_id"], x["revision_id"], x["sha256"]) for src in sources for x in src["snapshots"]}
    check(len(snapshots) == sum(len(src["snapshots"]) for src in sources), "duplicate source snapshot")

    books = corpus["paal"]
    check(unique(books, lambda x: x["paal_no"], "paal") == {1, 2, 3}, "expected paal 1–3")
    divisions = {x["iyal_id"]: x for x in corpus["iyal"]}
    check(len(divisions) == len(corpus["iyal"]), "duplicate iyal ID")
    unique(corpus["iyal"], lambda x: (x["paal_no"], x["order_in_paal"]), "iyal order")
    for row in books + corpus["iyal"]:
        nonempty(row.get("name_ta"), "Tamil name")
        if "name_en" in row or "gloss_author" in row:
            nonempty(row.get("name_en"), "editorial gloss")
            nonempty(row.get("gloss_author"), "gloss author")
        check(row.get("source_id", row.get("division_source_id")) in source_ids, "unknown structural source")
    for row in corpus["iyal"]:
        check(row["paal_no"] in {1, 2, 3} and type(row["order_in_paal"]) is int and row["order_in_paal"] > 0, "invalid iyal placement")

    chapters = corpus["chapters"]
    check(unique(chapters, lambda x: x["chapter_no"], "chapter") == set(range(1, 134)), "expected chapters 1–133")
    check(len({(x["source_id"], x["source_revision_id"], x["source_checksum"]) for x in chapters}) == 133, "expected 133 distinct pinned chapter snapshots")
    for row in chapters:
        check(row["paal_no"] in {1, 2, 3}, "invalid chapter paal")
        iyal = row.get("iyal_id")
        check(iyal is None or iyal in divisions and divisions[iyal]["paal_no"] == row["paal_no"], "invalid chapter iyal")
        check((row["source_id"], row["source_revision_id"], row["source_checksum"]) in snapshots, "chapter has no pinned snapshot")
        nonempty(row.get("name_ta"), "chapter Tamil name")
        if "name_en" in row or "gloss_author" in row:
            nonempty(row.get("name_en"), "chapter gloss")
            nonempty(row.get("gloss_author"), "chapter gloss author")

    kurals = corpus["kurals"]
    kural_keys = unique(kurals, lambda x: (x["chapter_no"], x["position"]), "kural")
    check(kural_keys == {(c, p) for c in range(1, 134) for p in range(1, 11)}, "expected exactly 10 positions in each of 133 chapters")
    anomalies = {a["kural_no"]: a for src in sources for a in src["numbering_anomalies"]}
    for row in kurals:
        n = (row["chapter_no"] - 1) * 10 + row["position"]
        check("kural_no" not in row, "global number must be derived")
        check(row["source_id"] in source_ids, "unknown kural source")
        for field in ("line_1", "line_2"):
            nonempty(row.get(field), f"kural {n} {field}")
            check(not any(unicodedata.category(ch) in ("Cc", "Cf") for ch in row[field]), f"unexpected control/format character in kural {n}")
        printed = row.get("source_printed_no")
        if printed is not None:
            nonempty(printed, "source printed number")
        if printed != str(n):
            check(n in anomalies and anomalies[n]["source_printed_no"] == printed and anomalies[n].get("reason"), f"undocumented printed number at kural {n}")

    sets = manifest["translation_sets"]
    set_ids = unique(sets, lambda x: x["set_id"], "translation set")
    translations = corpus["translations"]
    unique(translations, lambda x: (x["chapter_no"], x["position"], x["set_id"]), "translation")
    by_set = {name: set() for name in set_ids}
    for row in translations:
        n = (row["chapter_no"] - 1) * 10 + row["position"]
        check((row["chapter_no"], row["position"]) in kural_keys, "translation references missing kural")
        check(row["set_id"] in set_ids and row["source_id"] in source_ids, "translation references unknown set/source")
        for field in ("text", "translator", "source_locator"):
            nonempty(row.get(field), f"translation {field}")
        by_set[row["set_id"]].add(n)
    for row in sets:
        check(row["source_id"] in source_ids, "unknown translation set source")
        for field in ("title", "year", "edition", "rights_basis", "display_label"):
            nonempty(row.get(field), f"translation set {field}")
        check(row["kind"] in ("verse", "prose", "literal") and isinstance(row["translators"], list) and row["translators"], "invalid translation set kind/translators")
        omissions = row["omitted_kural_nos"]
        check(len(omissions) == len(set(omissions)) and set(omissions) == set(range(1, 1331)) - by_set[row["set_id"]], "translation coverage/omissions disagree")
        check(type(row["expected_count"]) is int and type(row["imported_count"]) is int and row["expected_count"] == row["imported_count"] == len(by_set[row["set_id"]]), "translation count mismatch")

    schemes = manifest["transliteration_schemes"]
    scheme_ids = unique(schemes, lambda x: x["scheme"], "transliteration scheme")
    check(scheme_ids <= {"iso15919_2001", "reader_simple", "reader_pronunciation"}, "unknown scheme")
    check(all(x["review_status"] == "approved" and SEMVER.fullmatch(x["engine_version"]) for x in schemes), "unreviewed or invalid scheme")
    scheme_versions = {x["scheme"]: x["engine_version"] for x in schemes}
    inputs = {f"{k['chapter_no']}:{k['position']}:{line}": k[line] for k in kurals for line in ("line_1", "line_2")}
    inputs.update({f"chapter:{x['chapter_no']}": x["name_ta"] for x in chapters})
    inputs.update({f"iyal:{x['iyal_id']}": x["name_ta"] for x in corpus["iyal"]})
    inputs.update({f"paal:{x['paal_no']}": x["name_ta"] for x in books})
    unique(corpus["transliterations"], lambda x: (x["target_key"], x["scheme"]), "transliteration")
    for row in corpus["transliterations"]:
        key = row["target_key"]
        kind = "kural_line" if re.fullmatch(r"\d+:\d+:line_[12]", key) else key.split(":")[0] + "_name"
        check(row["target_type"] == kind and key in inputs, "invalid transliteration target")
        check(row["scheme"] in scheme_ids and row["engine_version"] == scheme_versions[row["scheme"]], "unreviewed or stale transliteration scheme")
        check(row["input_hash"] == digest(inputs[key].encode("utf-8")), "stale transliteration input hash")
        nonempty(row.get("output"), "transliteration output")
    check(len(corpus["transliterations"]) == len(inputs) * len(scheme_ids), "transliteration coverage mismatch")

    actual = {"paal": len(books), "iyal": len(divisions), "chapters": len(chapters), "kurals": len(kurals)}
    check(manifest["counts"] == actual, "manifest counts mismatch")
    print(f"Valid release {manifest['release_version']}: {actual['chapters']} chapters, {actual['kurals']} kurals")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--expected-sums-sha256", required=True, help="SHA-256 of exact SHA256SUMS bytes, pinned outside the release")
    args = parser.parse_args()
    try:
        check(HEX.fullmatch(args.expected_sums_sha256) is not None, "invalid pinned SHA-256")
        validate(args.directory, args.expected_sums_sha256)
    except (ValueError, KeyError, TypeError, OSError, UnicodeError) as error:
        print(f"Invalid release: {error}", file=sys.stderr)
        sys.exit(1)
