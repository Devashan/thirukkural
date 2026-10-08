# AI review prompt

Upload `english-review.json`. Review one chapter (10 records) per response,
then continue in chapter order. Retain this instruction for every batch:

```text
Review the attached Thirukkural draft for the requested chapter. I cannot read
Tamil, so explain each finding in plain English. Preserve every Tamil string,
source number, source reference, credited historical English translation and
speaker heading exactly as supplied; propose corrections separately.

For each record, compare the Tamil with the credited English translation.
Identify suspected extraction problems, alignment errors, ambiguities,
archaic wording, and any meaning the historical witness adds or omits. Do not
infer Tamil accuracy merely from fluent English. State explicitly when a
conclusion needs a scan, a second translation, or a qualified Tamil reviewer.
If the supplied data cannot support a check, say unable_to_verify.

Where idiomatic_translations is empty, propose one concise modern idiomatic
English rendering. Preserve the verse's meaning, imagery and speaker context;
do not add life advice, a practical takeaway, an invented interpretation, or
unverified commentary. Label it ai_assisted_draft, never a sourced historical
translation or an approved Tamil translation. Identify its basis (Tamil plus
the supplied Aiyar witness), and explain any uncertain translation choice.
Do not claim independent corroboration unless an additional source is supplied.

Return JSON with chapter_no and results, one entry per original kural_no.
Each result must contain:
- kural_no, chapter_no, position
- status: no_issue_found | flagged | unable_to_verify
- findings: [{field, issue, proposed_correction, evidence, confidence}]
- idiomatic_candidate: {text, status: ai_assisted_draft, basis_set_ids,
  uncertain_choices}
- needs_scan_review, needs_tamil_reviewer (booleans)
- reason_in_plain_english

Confidence is not approval. Do not rewrite the input file, mark any release
gate approved, fill transliterations from the English, or erase a flag.
Specifically preserve the pending printed-number anomaly for Kural 72.
Return all ten identities exactly once and no identities from other chapters.
```

Save each returned chapter separately alongside the exact input file/hash.
Record the actual model, date and prompt used; do not invent model provenance.
Review flagged results and proposed idiomatic wording before merging any edits.
Repeated AI agreement is not independent source evidence or Tamil sign-off.
