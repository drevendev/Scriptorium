# Private EPUB validation contract

`scriptorium epub book.epub --format markdown --output report.md` analyzes a
local unencrypted EPUB 2/3 with linear XHTML spine documents. It never extracts
archive paths to disk, executes markup, fetches remote resources, uploads a book,
or enrolls it in a public corpus. This is a supported subset, not an EPUB conformance validator.

## References and archive names

Manifest `href` values are checked **before** URL parsing or percent decoding.
Raw ASCII spaces, C0 controls and DEL are rejected; spaces in member names must
be written as `%20`. Non-ASCII NFC names remain supported. Each percent sign must
start exactly two ASCII hexadecimal digits. UTF-8 decoding is strict and occurs
once: `%25GG` names a literal `%GG`; `%252f` names a literal `%2f`, not a slash.
Encoded spaces, Cyrillic and literal encoded `#`/`?` in filenames remain valid.

Schemes, authorities, queries and fragments (including empty `?` or `#`) are
unsupported. Invalid URL syntax raises a controlled `EpubError`. Absolute paths,
backslashes, dot segments, colon-bearing components, control characters,
non-NFC names and ambiguous duplicate targets remain rejected after decoding.
All messages are path-free; they do not echo private hrefs or manuscript text.

ZIP validation checks `ZipInfo.orig_filename` before its normalized `filename`.
A NUL-truncated name is rejected even for an unreferenced resource. This closes
a validation gap, not an alleged filesystem extraction or remote-execution path.

Primary references: [RFC 3986 section 2.1](https://www.rfc-editor.org/rfc/rfc3986.html#section-2.1)
defines percent triplets; [Python URL parsing documentation](https://docs.python.org/3/library/urllib.parse.html)
documents whitespace stripping and the absence of input validation. These facts
are why strict UTF-8 `unquote` alone is insufficient.

## Resource limits

Existing bounds remain: 32 MiB archive, 256 members, 16 MiB per member, 64 MiB
expanded total, compression ratio at most 150, and 128 linear spine documents.
Container XML is limited to 64 KiB and OPF XML to 2 MiB. DTDs and entity declarations
remain unsupported. Every XML document additionally permits at most 128 nested
elements (root depth one) and 100,000 total elements. Limits are inclusive.
Chunk-fed parsing checks both counters, including events deferred until parser close,
before recursive chapter projection. Existing byte limits are still essential.

Extracted text is limited to 32 MiB of UTF-8, including the two newline bytes
between nonempty chapters. This budget is checked as chapters are accumulated,
not only after joining the full result. Empty chapters do not add separators.

## Compatibility and verification

These checks narrow invalid/over-budget input acceptance. For retained accepted
inputs, text projection, body hashes, receipt schema and extraction profile
`scriptorium-epub-spine-xhtml-v1` are unchanged. Archive and body identities remain
separate. Existing output files are never overwritten. Invalid archives are
rejected before report/provenance creation. This is not a new licensing grant,
author classifier, FantLab parity result or corpus admission; M2 remains 0/5.

`tests/test_epub_boundaries.py` uses original tiny synthetic ZIP/XHTML fixtures,
not books or donor code. The complete suite exercises extraction and real CLI
JSON/HTML/CSV/Markdown. Package CI also runs this same file with isolated Python
against the installed wheel outside the checkout. No analyzer stubs are used.
