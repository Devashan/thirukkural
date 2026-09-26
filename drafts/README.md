# Tamil collection drafts

`chapter-001.json` is a first reading of the ten couplets on the [pinned
Wikisource chapter page](https://ta.wikisource.org/w/index.php?title=திருக்குறள்,_மூலம்/கடவுள்_வாழ்த்து&oldid=1531581).
It is **unreviewed**, has no saved source snapshot/hash yet, and is not a
release file or a source for production imports. Its chapter and verse numbers
are derived from the page's printed numbering. Its spaces and punctuation are
left as displayed, pending comparison with the scanned edition.

Run `python3 tools/collect_tamil.py /path/to/tamil-draft` or dispatch the
"Collect Tamil review draft" workflow. The collector requests the index and
all chapter pages, captures each page's current revision, the rendered chapter
HTML and wrapper wikitext bytes, saves their SHA-256, and extracts ten numbered,
two-line verses from the saved rendered snapshot. Transcluded scan pages can
change independently of the wrapper revision; the rendered HTML snapshot hash
is therefore the text provenance key. If any chapter is missing, duplicated, misnumbered, or
unexpectedly formatted, it stops instead of guessing. Its `chapters.json` is
an extraction draft, **not** the three-file release in `RELEASE_FORMAT.md`.
The workflow stores the result as a 30-day artifact for comparison and review;
it does not publish a corpus or deploy application data.

Before a release, review all 133 snapshots against the edition, reconcile
chapter/paal/iyal structure and any numbering anomalies, document source
rights and translation editions, and complete the release review gates. Exact
source revisions and snapshot hashes from the accepted draft must be carried
into the manifest. Later edits upstream never silently alter a release.
