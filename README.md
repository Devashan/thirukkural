# Thirukkural open data

An open, source-traceable dataset for reading and studying all 1,330 Kurals, with a focus on access for readers in South Africa and beyond.

**Status: foundation only.** The verified corpus has not been published yet. Do not use this repository as an authoritative source of Kural text until a versioned data release passes the source, rights and text checks described below.

## What belongs here

- The Tamil verses from the selected R. Srinivasan (1997) edition hosted on Tamil Wikisource, pinned to exact chapter revisions.
- Separate English translation editions by V. V. S. Aiyar, G. U. Pope, and W. H. Drew / John Lazarus, each with its own verified source, coverage and credit.
- Generated scholarly romanisation and reader spellings, with documented rules, engine version and input hash.
- Paal, iyal, chapter and verse structure; source and rights metadata; verified correction history.
- Later, independently labelled and credited modern explanations if contributors and reviewers are ready.

See [CONTENT_MODEL.md](CONTENT_MODEL.md), [RELEASE_FORMAT.md](RELEASE_FORMAT.md) and [SOURCES_AND_RIGHTS.md](SOURCES_AND_RIGHTS.md).

## What does not belong here

Credentials, user accounts, private reading preferences and unverified third-party corpus dumps.

## Dataset releases

The initial release format is UTF-8 JSON with a schema version, a release version, source/revision manifest and SHA-256 checksums. [The release format](RELEASE_FORMAT.md) defines its exact fields, verification and structural validator.

A release is only ready when there are 133 chapters and 1,330 correctly aligned Tamil couplets; expected translation coverage is verified per edition; rights and source locators are recorded; romanisation is regenerated from the pinned Tamil; and the relevant content review is complete. A public repository is not itself a promise that an unfinished text dump is verified.

## Contribute

Please use an issue or pull request and follow [CONTRIBUTING.md](CONTRIBUTING.md). Corrections need a precise source citation. Reader spelling suggestions are welcome; changes to generated outputs go through the shared rules and tests.

## Ownership

This data project is maintained by Devashan Naicker and intended for broad reuse and community review. Rights vary by content layer; read [SOURCES_AND_RIGHTS.md](SOURCES_AND_RIGHTS.md) before reusing a future release.
