# JSON release format (schema 1)

This is the public handoff for DEV-160. A tagged release is a directory containing exactly `manifest.json`, `corpus.json` and `SHA256SUMS`. All are UTF-8; JSON is encoded without a BOM. The first populated release is gated on source, rights, coverage and Tamil review. No draft JSON in this repository is a published corpus.

## Version and integrity

- Use immutable Git tags of the form `data-vMAJOR.MINOR.PATCH` and set `manifest.release_version` to the same numeric version, without `data-v`. Schema version is the integer `1`. Breaking field/meaning changes increment the schema version and the release major version. Corrections to content use a new release version; never move or replace a published tag or asset.
- `SHA256SUMS` contains lowercase SHA-256 hex, two spaces, then the filename, one line each for `manifest.json` and `corpus.json`, sorted by filename. It does not include itself. Checksums are computed over exact file bytes. The app pins the tag/commit **and** the expected SHA-256 of `SHA256SUMS` in its own source. This is an integrity pin, not a signature or a statement that a source is trustworthy.
- A release archive, if offered, preserves these three files at its root. Consumers verify the pinned checksum of `SHA256SUMS`, then both entries, before parsing either JSON file. Git tag and archive URLs are retrieval mechanisms; they are not version resolution at runtime.
- JSON numbers are integers for identifiers/counts; strings are NFC. No `null` substitutes for missing text. Empty optional collections are `[]`. Files may be prettified; consumers must hash bytes before parsing, not re-serialised JSON.

## `manifest.json`

```json
{
  "schema_version": 1,
  "release_version": "1.0.0",
  "created_at": "2026-09-23T00:00:00Z",
  "counts": {"paal": 3, "iyal": 0, "chapters": 133, "kurals": 1330},
  "sources": [{
    "source_id": "srinivasan-1997-wikisource",
    "role": "canonical",
    "work": "திருக்குறள், மூலம்",
    "author_translator_editor": "R. Srinivasan",
    "publisher": "publisher or host, explicitly distinguished",
    "year": "1997",
    "url": "https://ta.wikisource.org/",
    "retrieved_at": "2026-09-23T00:00:00Z",
    "rights_basis": "reviewed statement for this source",
    "licence": "reviewed source notice or public-domain status",
    "transform_steps": ["documented mechanical extraction steps"],
    "numbering_anomalies": [],
    "snapshots": [{"locator": "exact chapter page URL", "revision_id": "page oldid", "sha256": "64 lowercase hex characters"}]
  }],
  "translation_sets": [{
    "set_id": "edition-slug",
    "title": "exact edition title",
    "translators": ["credited translator"],
    "year": "edition year",
    "edition": "edition description",
    "kind": "verse",
    "source_id": "verified-english-source-id",
    "rights_basis": "reviewed statement",
    "display_label": "reader-facing credit",
    "expected_count": 1330,
    "imported_count": 1330,
    "omitted_kural_nos": []
  }],
  "transliteration_schemes": [{"scheme": "reader_simple", "engine_version": "1.0.0", "review_status": "approved"}],
  "review": {"source_rights": "approved", "tamil_text": "approved", "translation_coverage": "approved", "transliteration": "approved"}
}
```

This example is illustrative and contains placeholders, not an approved release. `iyal` may be zero while the division audit is pending; if present, every iyal needs an explicit division source. Each shipped translation set must have its exact source pinned, not just a translator name. `expected_count` is the verified coverage of that edition (0–1330), `imported_count` must equal the actual record count, and `omitted_kural_nos` lists every verified absence relative to 1–1330. A source snapshot records the raw bytes used to extract each chapter; retain those bytes in the project's source archive and pin all 133 chapter revisions. Each metadata or textual layer links to a source by ID. Record rights for original editorial metadata separately before using it in a release. Only `approved` review states permit publication.

## `corpus.json`

Top-level keys are exactly `paal`, `iyal`, `chapters`, `kurals`, `translations`, `transliterations`. Each is an array, ordered by numeric identity then set/scheme. Sample shapes below omit repeated rows; the actual release contains the complete verified corpus.

```json
{
  "paal": [{"paal_no": 1, "name_ta": "Tamil name", "name_en": "editorial English gloss", "source_id": "srinivasan-1997-wikisource", "gloss_author": "named editorial author"}],
  "iyal": [{"iyal_id": 1, "paal_no": 1, "order_in_paal": 1, "name_ta": "Tamil name", "name_en": "editorial gloss", "division_source_id": "srinivasan-1997-wikisource", "gloss_author": "named editorial author"}],
  "chapters": [{"chapter_no": 1, "paal_no": 1, "iyal_id": 1, "name_ta": "Tamil name", "name_en": "editorial gloss", "gloss_author": "named editorial author", "source_id": "srinivasan-1997-wikisource", "source_revision_id": "page oldid", "source_checksum": "raw snapshot SHA-256"}],
  "kurals": [{"chapter_no": 1, "position": 1, "source_printed_no": "1", "line_1": "Tamil line as printed", "line_2": "Tamil line as printed", "source_id": "srinivasan-1997-wikisource"}],
  "translations": [{"chapter_no": 1, "position": 1, "set_id": "edition-slug", "text": "verified edition text", "translator": "credited translator for this verse", "source_locator": "page or anchor", "source_id": "verified-english-source-id"}],
  "transliterations": [{"target_type": "kural_line", "target_key": "1:1:line_1", "scheme": "reader_simple", "output": "generated output", "engine_version": "1.0.0", "input_hash": "SHA-256 of NFC input UTF-8 bytes"}]
}
```

`name_en` and `gloss_author` are optional **together** for paal/iyal/chapter; if present, the gloss is editorial, never attributed to a historical translator. `iyal_id` on a chapter is an integer or `null` while its division is unverified; it must point to an iyal of the same paal when present. Every chapter points to the matching pinned raw snapshot via `(source_id, source_revision_id, source_checksum)`. `kural_no` is deliberately absent; derive `(chapter_no - 1) * 10 + position`. A verse is identified by `(chapter_no, position)`, not by `source_printed_no`. Unexpected printed-number mismatches need a documented entry in `numbering_anomalies` with `kural_no`, `source_printed_no`, and `reason`; never silently renumber text.

Translation omissions are explicit in the manifest and have **no** corresponding translation row. `source_id` on a translation is its exact source and may differ from the set default only when documented. Transliteration `target_type` is `kural_line`, `chapter_name`, `iyal_name` or `paal_name`; `target_key` is respectively `chapter:position:line_1|line_2`, `chapter:N`, `iyal:N`, or `paal:N`. An output is derived only from the matching Tamil field, never edited by hand. `input_hash` is SHA-256 of that field's NFC UTF-8 bytes; scheme and engine version are pinned separately from Tamil revisions. Only reviewed schemes appear in a published release. Explanation text is outside schema 1.

## Release checks

Run `python3 tools/validate_release.py path/to/release --expected-sums-sha256 HEX` before tagging. Validation checks checksums, schema/version, references, unique identities, exactly 3 books/133 chapters/1,330 verses and ten positions per chapter, translation coverage per set, input hashes and approved review gates. The publisher additionally audits raw snapshots, rights, source locators, punctuation/Unicode allowlist, translator segments and generated outputs against pinned rules and reviewer sign-off (DEV-160/174). Passing the structural validator alone never establishes textual or legal accuracy.
