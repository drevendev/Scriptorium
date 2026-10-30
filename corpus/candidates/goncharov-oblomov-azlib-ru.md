# Candidate: Ivan Goncharov — Oblomov (1859), Russian original

Status: **source-bound deterministic measurement implementation pending hosted execution and later acceptance**. Do not count as the ninth measured Reader work until the full pinned-source CI artifact passes, is independently reviewed, retained and integrated. No FantLab parity claim.

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

The command fetches only exact Wikisource revision 5724579 transiently, rejects source/rights/chapter/size drift, measures the exact extracted literary body with the existing deterministic 29-field analyzer and creates **source-free JSON only**. Missing dictionary-dependent metrics are NOT_RUN rather than fabricated zeros. The GitHub Actions workflow retains only the derived JSON for later independent acceptance and Reader publication. It never commits full literary prose or downloads to Pages.

All measurements remain Scriptorium inferred/extension candidates, not compatible FantLab PARITY_PASS. The frozen source SHA-256, exact character count, field results and workflow CI evidence will be taken from real execution, not estimated from web previews.
