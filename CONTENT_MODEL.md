# Content model (draft)

This is the portable data model. Schema 1 is specified in [RELEASE_FORMAT.md](RELEASE_FORMAT.md).

## Identity and structure

- `paal`: book number 1–3, Tamil name, provenance, and separately labelled editorial English gloss if used.
- `iyal`: division within a paal, order, Tamil name and an explicit source for its chapter boundaries. No uncredited mixing of commentators' divisions.
- `chapter`: number 1–133, paal and verified iyal association, Tamil name, exact source page URL, revision ID and raw-snapshot SHA-256.
- `kural`: `chapter_no` (1–133) plus `position` (1–10) is the stable identity. The global number is derived as `(chapter_no - 1) * 10 + position`; keep a distinct `source_printed_no` and record anomalies. Preserve both Tamil lines in their source order and their verified printed line break.

The source may contain joined word forms, significant spaces and punctuation. Keep an immutable raw snapshot and record every mechanical extraction/normalisation step. The importer must review unexpected controls, format characters or numbering mismatches rather than silently rewriting text.

## English renderings

An edition or `translation_set` records its title, translator(s), edition/year, source, source version, rights basis, expected and verified coverage, and reader-facing credit. Individual `translation` records join a Kural to a set and retain the exact text, source locator, and responsible translator where attribution differs within an edition (for example Drew/Lazarus). A verified omission is explicit, never filled from another edition without a new record.

Historical translations and our own future explanations are different content types. Do not silently modernise or paraphrase a translation.

## Romanisation

Each generated result records the input identity, source-text hash, scheme ID and rule/engine version. Planned options are ISO 15919 (confirm the published standard's details before making conformance claims), a simple Latin spelling and a pronunciation-oriented reader spelling. The last option needs Tamil-speaker review before release. No inherited third-party romanisation or unexplained per-verse overrides are shipped.

## Future explanations

Modern English explanations are outside the initial dataset. If introduced, each explanation has an author, review state, version and its own licence. It is labelled as an explanation and cannot occupy a translation slot.

## Release checks

Validate unique chapter/position keys, 133 × 10 Tamil entries, source revisions and hashes, Unicode handling, attribution, translation coverage per set, scheme freshness and absence of prohibited or unreviewed content. Emit a machine-readable manifest with the release.
