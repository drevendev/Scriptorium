# Dialogue model

Profile ID: `scriptorium-dialogue-v1`  
Current aggregate metric profile: `scriptorium-metrics-v4`  
Status: **inferred candidate**, not reproduced FantLab behavior.

FantLab publicly exposes mean sentence lengths for narration/dialogue, dialogue share,
and author text inside dialogue, but its exact segmentation and denominator rules are
not public. Scriptorium therefore keeps the first dialogue implementation deliberately
small, deterministic and replaceable by benchmark evidence.

## Paragraph classification

Input is normalized by `scriptorium-text-v1`. Non-blank LF-delimited lines are candidate
paragraph spans with half-open offsets into normalized text.

A paragraph is dialogue only when its first non-whitespace content is one of `—`, `–`
or `-` followed immediately by whitespace. A quoted sentence or an em dash without that
space remains narration under this profile. This is a Russian-prose candidate rule, not
a claim about FantLab's parser.

## Author remarks inside dialogue

Within a detected dialogue paragraph, an internal whitespace-dash-whitespace separator
starts an alternating segment sequence:

```text
speech -> author text -> speech -> author text -> ...
```

`author_remark_spans()` returns only those candidate author-text segments, preserving
normalized-text offsets. The rule intentionally does not infer speaker identity, quoted
speech, screenplay formatting or more complicated Russian dialogue punctuation.

## SCRIP-DIALOGUE-002 diagnostic probe

The frozen full-work *Anna Karenina* diagnostic exposed a large mismatch in author text
inside dialogue while the overall dialogue-share value was much closer to FantLab. That
is enough to justify investigating the parser, but not enough to tune production behavior:
FantLab's public article names the metric without publishing its delimiter grammar or
denominator semantics, and the exact FantLab analyzer-input edition remains unknown.

`scriptorium-dialogue-policy-diagnostic-v1` therefore runs beside the production profile
without changing it. The probe records only source-free counts and percentages. It
compares:

- the current alternating-separator author-remark spans;
- a narrower delimiter probe whose author-text opener must follow comma, question,
  exclamation or ellipsis punctuation at the source-text surface, after which the next
  internal separator closes the candidate remark;
- each author-remark numerator over the current dialogue-character denominator and over
  the whole normalized non-whitespace text denominator.

The narrower probe is intentionally diagnostic rather than linguistic authority. Its
purpose is to measure how much ordinary dash use inside speech can influence the v1
alternation rule. A numerically closer result must not be promoted to FantLab behavior
without source-matched benchmark evidence. Hosted frozen diagnostics keep
`fantlab_source_edition_match=unknown`, `diagnostic_only`, and
`m2_parity_admissible=false`.

## Scalar metrics

The current aggregate metric profile exposes four FantLab-shaped dialogue fields, all
with compatibility status `inferred`:

| Metric | Candidate v1 rule |
| --- | --- |
| `fantlab.dialogue.mean_narration_sentence_length_chars` | Mean character length of `scriptorium-text-v1` sentence spans computed independently inside narration paragraphs. |
| `fantlab.dialogue.mean_dialogue_sentence_length_chars` | Mean character length of sentence spans computed independently inside dialogue paragraphs, including candidate author remarks. |
| `fantlab.dialogue.share_percent` | Non-whitespace characters in dialogue paragraphs / all non-whitespace normalized characters × 100. |
| `fantlab.dialogue.author_text_inside_dialogue_percent` | Non-whitespace characters in detected author-remark spans / non-whitespace characters in dialogue paragraphs × 100. |

A missing denominator produces `null`; for a non-empty text with no dialogue, dialogue
share is `0.0` while dialogue-sentence and author-inside-dialogue values are `null`.

These denominators are explicit candidates. FantLab may count whitespace, punctuation,
dialogue units or embedded remarks differently. Source-matched benchmarks must decide
whether this profile is compatible.

## Benchmark surface

`scriptorium.benchmark` maps the four scalar dialogue fields when a captured FantLab
reference contains them. Their decimal precision is not independently established, so
they remain `unresolved_precision` and cannot produce a FantLab `pass` yet even with an
exact source edition.

The published dialogue-use graph is not implemented in this unit. Its window placement,
edge behavior and relation to the scalar dialogue metric remain separate research work.

## Public showcase

`showcase/anna-karenina-part1-ch2-dialogue.json` demonstrates the profile on two
dash-led dialogue paragraphs from Tolstoy's *Anna Karenina*, Part I, Chapter II, bound
to Russian Wikisource revision `oldid=4929731` and the cited Nauka 1970 edition.

The repository stores only provenance, selection identity, hashes and derived metrics;
the source prose is not committed. The 250-character selection is an illustrative
excerpt, below the 300,000-character corpus threshold and inadmissible as parity or
author-profile evidence.

## Known incompatibility risks

- FantLab's dialogue paragraph markers and quote handling are unpublished.
- The internal author-remark grammar may be substantially more sophisticated.
- Sentence boundaries inherit the still-inferred `scriptorium-text-v1` rules.
- Character-count denominators may differ on whitespace/punctuation treatment.
- A dialogue paragraph that mixes speech and narration is classified as dialogue as a
  whole for the share metric, even though author remarks are separately estimated.
- The SCRIP-DIALOGUE-002 punctuation-shaped opener probe is a sensitivity test only; it
  is not a replacement production profile until stronger evidence justifies versioning
  the dialogue contract.

No one of these edges should be silently repaired by intuition; benchmark deltas should
drive future profile revisions.
