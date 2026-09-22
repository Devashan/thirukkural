# Thirukkural open data

An open, source-traceable dataset for reading and studying all 1,330 Kurals, with a focus on access for readers in South Africa and beyond.

**Status: foundation only.** The verified corpus has not been published yet. Do not use this repository as an authoritative source of Kural text until a versioned data release passes the source, rights and text checks described below.

## What belongs here

- The Tamil verses from the selected R. Srinivasan (1997) edition hosted on Tamil Wikisource, pinned to exact chapter revisions.
- Separate English translation editions by V. V. S. Aiyar, G. U. Pope, and W. H. Drew / John Lazarus, each with its own verified source, coverage and credit.
- Generated scholarly romanisation and reader spellings, with documented rules, engine version and input hash.
- Paal, iyal, chapter and verse structure; source and rights metadata; verified correction history.
- Later, independently labelled and credited modern explanations if contributors and reviewers are ready.

See [CONTENT_MODEL.md](CONTENT_MODEL.md) and [SOURCES_AND_RIGHTS.md](SOURCES_AND_RIGHTS.md). Our draft definition is tracked in [DEV-157](https://linear.app/devii-108/issue/DEV-157/define-mvp-content-model-and-translationtransliteration-rules).

## What does not belong here

Application source code, credentials, user accounts, private reading preferences, and unverified third-party corpus dumps. The application will use a pinned release of this data and store it locally; it will not depend on GitHub or Wikisource at runtime.

The app is maintained separately under NaickerCorp. The precise private app repository name can change without affecting the open data.

## Dataset releases

The initial release format is planned as UTF-8 JSON with a schema version, a release version, source/revision manifest, per-file SHA-256 checksums, and validation results. The application will import a fixed release and checksum into its own database or bundle it as an asset. This repository's public JSON structure does **not** require the application's private SQL schema.

A release is only ready when there are 133 chapters and 1,330 correctly aligned Tamil couplets; expected translation coverage is verified per edition; rights and source locators are recorded; romanisation is regenerated from the pinned Tamil; and the relevant content review is complete. A public repository is not itself a promise that an unfinished text dump is verified.

## Contribute

Please use an issue or pull request and follow [CONTRIBUTING.md](CONTRIBUTING.md). Corrections need a precise source citation. Reader spelling suggestions are welcome; changes to generated outputs go through the shared rules and tests.

## Ownership

The Thirukkural app and site are maintained by Devashan Naicker. This data project is intended for broad reuse and community review. Voluntary support for the app does not restrict access to, or reuse of, the open data. Rights vary by content layer; read [SOURCES_AND_RIGHTS.md](SOURCES_AND_RIGHTS.md) before reusing a future release.
