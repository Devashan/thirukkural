# AI-reviewed development dataset: Kurals 1–300

This directory is a **development snapshot**, not a formal schema-1 Thirukkural release. It exists so application and API development can proceed while the full 1,330-Kural corpus is still being reviewed.

Coverage is Chapters 1–30 / Kurals 1–300. Canonical Tamil is source-pinned to the selected R. Srinivasan (1997) Tamil Wikisource edition. The idiomatic English layer is AI-assisted and all 300 records remain pending qualified Tamil-language review. The review records deliberately retain uncertainty and findings rather than representing AI review as human verification.

`manifest.json` records coverage, source pins, limitations and the SHA-256 of every chapter file. `chapters/chapter-NNN.json` contains the source-pinned Tamil, AI-assisted idiomatic draft, review state and the full review findings for each of the ten Kurals in that chapter.

Do **not** publish this directory under a `data-v*` tag or describe it as the verified corpus. The formal contract in `RELEASE_FORMAT.md` remains unchanged and still requires the complete 133 chapters / 1,330 Kurals and its release gates.

Consumers should upsert by stable `(chapter_no, position)` identity (or derived `kural_no`) and persist dataset version/source metadata. Missing layers such as transliteration must remain missing rather than being fabricated or borrowed from an untracked source.