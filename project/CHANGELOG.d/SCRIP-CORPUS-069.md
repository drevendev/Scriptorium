# SCRIP-CORPUS-069 — durable `Модуль:String` probe freeze

- Selected a bounded Darwin/Rachinsky durability unit from the P2 corpus/provenance continuation after SCRIP-CORPUS-068 left its reviewed source-free probe only in a seven-day Actions artifact plus prose summaries.
- Committed the exact reviewed `scriptorium-darwin-module-string-dependency-probe-v1` output as repository-native canonical evidence. Its embedded probe SHA-256 is `e27a2af9f01c760f995c633e296e1d5825642d4c4bcbeb5fba8ae0a697c234cb`; the exact source metadata remains 18,468 UTF-8 bytes / SHA-256 `258cec6ab8b4c1e3eb0e812d72d39f4302f321a4d1fdd7aa3883187db0eecb03` without retaining Lua source.
- Added focused freeze tests that recompute the canonical probe digest, verify exact `Модуль:String@3684569` identity, enforce the source-free guard and keep downstream gates closed.
- Updated the live exact-revision workflow to run the freeze tests and `cmp` regenerated probe bytes against the committed canonical artifact before upload; any provider/output drift now fails closed instead of silently replacing durable evidence.
- Updated the public direct-dependency companion with a stable canonical-artifact link and explicit durability boundary.
- No replay binding or semantic promotion occurred: `module_string_identity_bound=false`, `semantic_dependency_closure_proved=false`, `dependency_closure_complete=false`, forced/non-forced outputs remain unverified, renderer/body/>=300k/FantLab/M2 gates remain closed and M2 remains 0/5.
- Draft PR #228 / Issue #227 carry the authored unit for independent exact-head judgement. Merge is deliberately deferred to a later wake.
