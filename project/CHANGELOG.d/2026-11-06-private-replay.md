# Private report replay proposal — 2026-11-06

Add the offline `scriptorium verify` command to independently recompute the
current engine's 29 metrics and source hashes from the owner's own manuscript
and compare against a saved source-free JSON artifact. Reject mismatches,
malformed JSON, missing dictionary identity and unsafe local inputs without
echoing private text. This is a reproducibility check only: report-supplied
revision metadata remains a declaration, and rights, edition/input identity,
FantLab parity and M2 0/5 are unchanged. Later CI and independent acceptance
must precede merge.
