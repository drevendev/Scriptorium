# SCRIP-TEXT-SAME-INPUT-BOUNDARIES — controlled tokenizer comparison (2026-11-07)

- Add `scriptorium word-boundaries LOCAL.txt` with JSON/Markdown source-free count deltas for independent hyphen, apostrophe, dotted-initialism and numeric-token counterfactuals on **the identical normalized local input**.
- Reuse unchanged `scriptorium-text-v1`, existing Unicode-hyphen/numeric sensitivity and protected 32 MiB local read; never upload prose or overwrite reports. Zero denominators are `NOT_RUN`, not numeric zero.
- Synthetic tests cover count arithmetic, Unicode connector and punctuation, invalid/non-UTF8 inputs, symlink refusal, create-only output, deterministic replay, CLI discoverability and no source-prose leakage.
- Prior frozen Anna diagnostic already found numeric exclusion changes only 17 tokens and U+2010/U+2011 joining changes zero. This tool does **not** replay Anna or establish a FantLab analyzer-input edition; any full-book boundary decomposition is NOT_RUN.
- Compatibility metrics, historical evidence, corpus admissions and scientific gates remain untouched. **DIAGNOSTIC_ONLY; M2 0/5**. Fresh exact-head CI and later independent acceptance are required before merge. Root Pages has no change.
