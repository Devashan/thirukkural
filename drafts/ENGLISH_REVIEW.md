# English review packet

`english-review.json` contains all 1,330 Tamil records paired with all 1,330
entries from V. V. S. Aiyar's 1916 English translation, using the Standard
Ebooks edited transcription pinned to commit
`0d14a398d6886391c369f0c3e00b0e9e1e7f4ee1`.
It is an **unreviewed draft**, not a published release or import file.

The JSON records carry the original printed Tamil numbers, chapter/position
identity, Tamil snapshot hashes, English source locators, note links and
speaker headings. Kural 72 remains flagged: the Tamil source prints `71`
at chapter 8 position 2. Joining by chapter/position gives Aiyar's entry 72:
“Those that love not live only for themselves: as to those that love, their
very bones are for others’ occasions.” The translated meaning offers a
comparison, but does not by itself approve the Tamil edition or its numbering.

## Idiomatic English

`idiomatic_translations` is a separate array and is currently empty for every
record. No reusable modern idiomatic source has been verified and imported.
Aiyar's prose is retained as a historical translation; prose does not establish
that a translation is idiomatic or literal. We found modern readings at
[TheKural](https://thekural.org/) and
[nramc/thirukkural-api](https://github.com/nramc/thirukkural-api), but did not
verify a redistribution grant for their relevant texts. The latter explicitly
distinguishes its MIT-licensed code from third-party text rights. These
candidates were not copied into this packet. This is a limited source search,
not a finding that no licensed idiomatic translation exists.

You can use the accompanying AI review prompt to propose an idiomatic draft
from the Tamil and credited English witness. Such wording must remain labelled
as AI-assisted editorial content, with its input sources and actual model/run
recorded, until separately reviewed. Practical advice and explanation belong
in a separate layer, not inside the idiomatic translation.

## Reproduce and verify

Use the saved Tamil collection artifact ZIP as the first argument:

```sh
python3 tools/build_english_review.py tamil-review-draft.zip drafts/english-review.json --snapshot-archive drafts/aiyar-source-snapshots.json
python3 -m unittest discover -s tools -p test_build_english_review.py -v
```

`aiyar-source-snapshots.json` retains all 133 raw XHTML source files with their
Git blob hashes and pinned repository commit. The builder verifies every saved
English blob hash, every Tamil snapshot hash, chapter coverage, consecutive
English list starts, and ten entries/positions per chapter. Split lists and
speaker headings in the love chapters are preserved. Footnote marker digits
are removed from the translation text and retained as source links. Standard
Ebooks typography and wording are preserved; layout whitespace is collapsed.
The source archive and corpus can be regenerated without live English requests.

The transcription's rights notice is in its pinned
[content.opf](https://github.com/standardebooks/thiruvalluvar_the-kural_v-v-s-aiyar/blob/0d14a398d6886391c369f0c3e00b0e9e1e7f4ee1/src/epub/content.opf).
It describes the original source as believed public domain in the US and
dedicates Standard Ebooks contributions under CC0. This packet retains those
credits and leaves the release rights review pending. It does not assert
worldwide public-domain status for the historical work.

## What remains

- Compare the Tamil against its saved source and scan, and resolve the Kural 72
  printed-number anomaly. AI may flag errors; it cannot establish expert approval.
- Review Aiyar's extraction/meaning and rights. Pope and Drew/Lazarus are not
  included in this packet and still require independently attributed collection.
- Choose a verified idiomatic source or review newly drafted idiomatic wording.
- Generate and review transliterations from the accepted Tamil text.
- Reconcile taxonomy and prepare the versioned release with the required review
  gates and checksums. Adding an idiomatic layer to the release requires an
  explicit schema/content-model decision; this draft does not change schema 1.
- Import the approved pinned release into a consuming application.
