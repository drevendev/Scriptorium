# Run receipt — SCRIP-CORPUS-080

Status: REVIEW_PENDING

## Orientation

- Connected GitHub identity: `andy-zen-dev`.
- Repository: `drevendev/Scriptorium`; push permission available.
- Exact base: `51c38fbeed3f7583df74c814f7b3580be0628153`.
- Selection: normal-flow P2 SCRIP-CORPUS continuation after SCRIP-CORPUS-079 completed.
- Issue: #249.
- Branch: `scrip-corpus-080-darwin-references-promotion`.
- Draft PR: #250.

## Produced

- Candidate-local `<references/>` promotion contract.
- Effective semantic backlog v3.
- Deterministic builder/validator and six focused regressions.
- Public source-free semantic-backlog companion update.

## Evidence boundary

The promotion consumes only the independently reviewed 388/388 noinclude-containment evidence. It does not replay MediaWiki Cite semantics and does not claim historical transclusion or a general/offline MediaWiki runtime.

Promotion SHA-256: `4052973abc6c413503f26c27419770a2214bf3253ecb31ec9d4cf3c1276dec39`.
Backlog v3 SHA-256: `4b68de749eec8bbacf0e07cb9f87e2c5c2db0c81d438a191fadd15f4dffbda18`.

## Authoring verification / handoff

- Substantive implementation commit: `0a0a436b1b74ae8b469306258e7317c05c769853`.
- Final control-only handoff commit advances the PR head after this receipt/state update; independent review must inspect that final exact head and its checks rather than treating the authoring commit as independent judgement.
- PR #250 intentionally remains Draft. This run must not self-approve or self-merge the substantive change.

## Gates

`renderer_semantics_complete`, `renderer_implementation_ready`, `inter_page_composition_frozen`, `literary_body_count_and_digests_frozen`, `minimum_300k_proved`, `admitted_for_calibration`, `diagnostic_ready`, and `m2_parity_admissible` remain false; `fantlab_source_edition_match=unknown`. M2 remains 0/5.
