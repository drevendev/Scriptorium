# SCRIP-TEXT-SOURCE-SPANS-V1 — original-coordinate provenance

- Optional local Python API binds normalized token/sentence offsets to conservative original code-point intervals after CRLF/CR canonicalization and Unicode NFC.
- Canonical combining-class reordering is tracked through NFD and blocked NFC composition; exact inversion is refused at crossing boundaries instead of manufacturing offsets.
- Self-contained positive and negative tests exercise the local word/sentence consumer, ambiguous interiors, Hangul and invalid bounds. Default text-v1, metric profiles and public artifacts remain unchanged.
- Review/CI/merge remain separate; no manuscript content is published.
