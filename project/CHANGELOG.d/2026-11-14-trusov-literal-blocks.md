# 2026-11-14 — Preserve literal MediaWiki blocks in historical Trusov projection

- Reuse the accepted #511 Page projector; guard active-line `nop` / `heading` projection and opt-in `ВАР` preview against `<nowiki>` and `<pre>` literal regions, including case-insensitive tags and attributes.
- Keep calls outside a correctly closed region eligible; ignore faux opening tags in HTML comments, respect self-closing `<nowiki />`, and refuse ambiguous unmatched or malformed closing tags rather than silently rewriting literal source.
- Add positive/negative regressions; the pinned 150-Page capture and 145-Page diagnostic must remain unchanged on exact-head CI. The projection is still a synthetic source-free *partial* diagnostic, not historical MediaWiki rendering or a complete Trusov literary body.
- MediaWiki's official XML-style tag / wikitext guides document these literal strip blocks: https://www.mediawiki.org/wiki/Help:XML-style_tags and https://www.mediawiki.org/wiki/Help:Wikitext_examples.
- No manuscript/source prose, morphology change, corpus admission, FantLab input match or M2 promotion.
