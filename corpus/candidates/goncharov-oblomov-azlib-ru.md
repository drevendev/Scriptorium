# Candidate: Ivan Goncharov — Oblomov (1859), Russian original

Status: **source-bound deterministic measurement completed on GitHub Actions and retained as an unmerged PR artifact; independent acceptance and Reader integration pending**. Do not count as the ninth published Reader work until the source-free snapshot is accepted and integrated. No FantLab parity claim.

## Source and rights

- Work: Иван Александрович Гончаров, «Обломов» (1859); Russian original, not a translation.
- Permanently selected public-domain Russian Wikisource transcription: [Обломов (Гончаров)/Версия 2, oldid 5724579](https://ru.wikisource.org/w/index.php?title=Обломов_(Гончаров)/Версия_2&oldid=5724579).
- Source family: az.lib.ru, as recorded by Wikisource; original external witness [text_0020.shtml](http://az.lib.ru/g/goncharow_i_a/text_0020.shtml). The Wikisource footer states that the az.lib text was checked against a 1954 Moscow edition. **That editorial note has not been independently collation-verified**; it is a source-family claim, not an exact print-identity determination.
- Rights basis: Goncharov died in 1891; Russian Wikisource marks this original-language work PD-old / PD-old-70. No publishing of its full source text in Scriptorium.
- Source quality: Wikisource marks the imported transcription as 25% / without scans; editorial correctness remains uncertain.
- Completeness boundary: the selected single page visibly includes all four parts and the novel's concluding sentence. The measurement parser requires exactly 46 chapter headings in [11,12,12,11], title and footer anchors, at least 300,000 extracted characters including spaces, and no unexpected markup.
- FantLab analyzer-input edition: **UNKNOWN**; no verified matching FantLab analysis or parity reference. M2 contribution: **0**.

## Executable deliverable

Run from a source checkout:

```sh
python -m unittest discover -s tests -p test_oblomov_diagnostic.py -v
python -m scriptorium.oblomov_diagnostic --output /tmp/oblomov-measured.json
```

The command fetches only exact Wikisource revision 5724579 transiently, rejects source/rights/chapter/size drift, measures the exact extracted literary body with the existing deterministic 29-field analyzer and creates **source-free JSON only**. The hosted replay on 2026-10-30 confirmed **930,248 literary characters (including spaces), 147,447 words, 25,533 unique words, 14,353 sentences**, **24 numeric fields and 5 explicitly NOT_RUN dictionary fields**. The raw/normalized body SHA-256 is `144a5ea17195e7ce10d69a5855a67781510dac51fd44237e1bc856536c3b3887`; the pinned Wikisource wikitext SHA-256 is `fb3e3817792ed1769aa5cd9cc5b33a8326c56ff76007ca92331ac9fad516b394`. Missing dictionary-dependent metrics are NOT_RUN rather than fabricated zeros. The GitHub Actions workflow retains only the derived JSON for later independent acceptance and Reader publication. It never commits full literary prose or downloads to Pages.

All measurements remain Scriptorium inferred/extension candidates, not compatible FantLab PARITY_PASS. The retained source-free observed JSON is `corpus/candidates/diagnostics/goncharov-oblomov-ru.json`, checked against a fresh replay in the CI workflow, sourced from [GitHub Actions run #41077141367](https://github.com/drevendev/Scriptorium/actions/runs/41077141367) and artifact `12988365968`. This does not independently verify the claimed 1954 print collation or FantLab input identity; M2 remains 0/5.
