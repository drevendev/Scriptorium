# Corpus qualification screenings

This directory records source-free decisions made **before** Scriptorium spends work freezing or analyzing a candidate for calibration, benchmark, or author-profile use.

The current corpus rule is absolute: an admitted body must contain at least **300,000 characters including spaces**. A published FantLab analysis below that floor cannot become an M2 parity benchmark under the standing gate, even if its exact analyzer input is later identified. That fact does **not** prove that every distinct edition of the same title is also below the floor; a different public source needs its own frozen body and measured count before any non-M2 corpus-admission decision.

Screenings are not corpus admissions and do not contain literary source text. They preserve the evidence that changed the project decision, plus edition/provenance caveats needed to prevent a future showcase or distinct edition from being mistaken for parity evidence.

Current records:

- [`tolstoy-aelita-ru.json`](tolstoy-aelita-ru.json) — FantLab's 18 September 2022 analysis reports 276,556 characters, 23,444 below the mandatory floor, so **FantLab work 44822 is rejected as an M2 benchmark seed**. The Russian Wikisource public-domain/source-family evidence remains useful for a possible non-corpus short-input showcase or for a separately justified freeze-and-measure pass on that distinct public source. Because Tolstoy substantially revised the 1922–1923 text, no title-level assumption is made about edition identity or the public source's eventual character count.
- [`zamyatin-we-ru.json`](zamyatin-we-ru.json) — FantLab's 17 September 2022 analysis reports 285,704 characters, 14,296 below the mandatory floor, so **FantLab work 20055 is rejected as an M2 benchmark seed**. Russian Wikisource separately exposes a public-domain source family from the 2003 five-volume collected works. Its work index currently resolves to `oldid=5633449`, but the literary body is split across 40 linked record pages; the index revision is navigation/provenance evidence only and does not freeze those body pages. The public source therefore remains unmeasured and unadmitted until a separate source-freeze-and-measure unit binds every selected body revision and deterministic composition.
