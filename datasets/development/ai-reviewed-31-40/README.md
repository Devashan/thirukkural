# AI-reviewed development dataset: Kurals 301–400

This directory is an **immutable development batch**, not a formal schema-1 Thirukkural release. It extends the earlier `ai-reviewed-1-30` batch so application/data work can progress while the full 1,330-Kural corpus is still being reviewed.

Coverage is Chapters 31–40 / Kurals 301–400. Together with `../ai-reviewed-1-30`, the repository currently has AI-reviewed development data for Chapters 1–40 / Kurals 1–400.

Canonical Tamil is source-pinned to the selected R. Srinivasan (1997) Tamil Wikisource edition. The idiomatic English layer is AI-assisted and all 100 records remain pending qualified Tamil-language review. Review records retain uncertainty and findings rather than representing AI review as human verification.

`manifest.json` records coverage, source pins, limitations and the SHA-256 of every chapter file. `chapters/chapter-NNN.json` contains the source-pinned Tamil, AI-assisted idiomatic draft, review state and the full review findings for each of the ten Kurals in that chapter.

Chapter 31 is pinned to Wikisource oldid `1531627`, but its HTML snapshot was absent from the recovered collection artifact, so its `source_snapshot_sha256` remains `null` and the capture status is `verified_oldid_without_local_snapshot`. Chapters 32–40 use recovered artifact snapshots and record their snapshot SHA-256 values.

Do **not** publish this directory under a `data-v*` tag or describe it as the verified corpus. The formal contract in `RELEASE_FORMAT.md` remains unchanged and still requires the complete 133 chapters / 1,330 Kurals and its release gates.

Consumers that combine development batches should upsert by stable `(chapter_no, position)` identity (or derived `kural_no`) and persist dataset/source metadata. Missing layers such as transliteration must remain missing rather than being fabricated or borrowed from an untracked source.