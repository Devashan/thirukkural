# Private app import contract (DEV-160)

The data repo publishes a portable release; `NaickerCorp/Thirukkural` (or its future app repo name) owns the importer, SQL tables and app builds. There is no shared SQL schema. No GitHub or Wikisource request occurs while a user reads the app.

## Pin and seed

1. In private app source control, store `release_tag`, immutable commit SHA and the literal SHA-256 of the release's `SHA256SUMS`. Do not use `main`, `latest`, a floating semver range or a mutable download URL as a pin. App builds should preferably fetch once in CI and bundle the three verified files as assets; a server deployment may seed its local DB at deploy time from the same verified files.
2. Fetch that exact commit/tag's release files in the build or seed job. Check the pinned `SHA256SUMS` hash first, then both file hashes, then run `python3 tools/validate_release.py ... --expected-sums-sha256 HEX` from the same pinned data repo commit. Reject failures before writing data. The app also rejects unsupported `schema_version`, even if checksums match.
3. Parse identities from `chapter_no` + `position`; derive the global number. Map paal, iyal, chapters, verses, translations and available generated spellings into app owned tables or bundle the validated JSON. Persist provenance (source IDs/revisions, translation set labels, release version and digest) so each displayed text remains attributable. Missing translations remain missing and labelled; never substitute another edition in the import step. Render editorial English glosses as editorial content, distinct from translations. Do not expose unreviewed pronunciation output.
4. For a DB seed, stage the new dataset and check record counts/foreign keys against the release in one transaction, then atomically activate the new dataset and store `(release_version, schema_version, commit_sha, sums_sha256, imported_at)`. If already imported with identical commit/digest, do nothing. If a version matches but bytes differ, abort. Keep existing active data if fetch, verification, parsing, staging or commit fails. For a bundled asset, verify during the build and embed its version/digest; retain the previous deployed build on failure.
5. Test offline startup and navigation across chapters 1 and 133, missing translation state, scheme selection and the actual provenance/credit display. A later release requires another explicit pin update, fresh validation and app migration checks. Rollback means restoring the previous app build/active dataset by its prior pinned digest.

## Ownership and acceptance

- Public repository: source snapshots/provenance, reviewed content, format/schema and checksum generation, validation and immutable release assets. Do not publish the corpus until the DEV-160/174 source, coverage, rights and reviewer gates pass.
- Private app: release pin, importer and local storage, idempotency/rollback, UI preferences and app database migrations. This contract does not dictate table names or on-device storage technology.
- Acceptance for DEV-160: all 133 chapters and 1,330 Tamil verses are verified and locally queryable offline, per-set translation counts match the manifest, hashes and attribution are retained, a corrupt or changed file refuses import, and a repeated import is harmless.
