# Reliable immutable Wikisource reads

Source replay must survive an explicit provider throttle without accepting a
wrong revision, silently choosing current content, or turning unknown into PASS.
The shared standard-library transport serves both `wikisource_freeze._api_query`
(composite capture/replay) and `single_page_revision._api_query` (single-page
capture/replay). Existing callers keep their query and identity contracts.

## Retry contract

Every GET uses the existing descriptive User-Agent, JSON format version 2 and
`maxlag=5`. Requests are sequential. The exact Request, including requested
revision IDs, is reused; retries never change the source selection.

| Response | Policy |
| --- | --- |
| API `maxlag` or `ratelimited` | Retry, unless attempts/wait budget exhausted |
| Modern `errors` array | Retry only if every error is a recognized transient code |
| HTTP 429 | Retry with provider delay, or bounded backoff if absent |
| HTTP 503 with valid `Retry-After` | Retry with provider delay |
| HTTP 503 without a delay; other HTTP failures | Fail; do not guess the cause |
| DNS, TLS, timeout, unknown network errors | Fail without automatic retry |
| Unknown/malformed/mixed API errors or malformed JSON | Fail without retry |
| Missing query, revision/title/page/hash drift | Caller fails; not a transport retry |

There are at most **three attempts**. The default waits are 5 and 10 seconds.
`Retry-After` accepts delay-seconds and timezone-qualified HTTP dates, with a
five-second minimum on the first retry and ten seconds on the second. Total
sleep is limited to **60 seconds**; the existing 30-second timeout applies to
each request separately. A provider delay exceeding the remaining budget fails
with a defer message, rather than being clipped to retry too early.

Responses are decoded in memory with a **16 MiB** limit. Duplicate JSON keys,
nonfinite numbers (including exponent overflow), invalid JSON and non-object
roots fail closed. Transport errors do not echo URLs, provider info or source
bodies. No response cache, telemetry, persisted literary text or external write
is introduced. A successful HTTP response does not itself verify provenance.

Primary provider guidance:
- [MediaWiki maxlag](https://www.mediawiki.org/wiki/Manual:Maxlag_parameter)
  describes HTTP-200 maxlag errors, Retry-After and the distinction from unmarked
  cache-layer 503 responses.
- [API etiquette](https://www.mediawiki.org/wiki/API:Etiquette) documents serial
  requests, identifying User-Agents and rate-limit backoff.
- [API errors](https://www.mediawiki.org/wiki/API:Errors_and_warnings) describes
  classic `error` and modern `errors` response shapes.

The earlier `MediaWiki response missing query` CI flake was not captured. Its
cause remains **UNKNOWN**; the new tests simulate documented transient signals,
not a claimed reproduction of that historical incident.

## Exact identity types

Before the first batch request, every expected revision ID must be an exact
positive Python/JSON integer, never Boolean, float or numeric string. Optional
page IDs follow the same rule. Duplicate titles/IDs and incomplete metadata are
rejected before fetching any batch. Provider revision/page IDs are checked
before equality; `True == 1` cannot admit a different identity.

Expanded/packed manifests enforce exact types for ordinals, chapter numbers,
revision IDs, chapter counts, encoding widths and timestamp offsets. Overflowing
timestamps yield a validation error. Single-page identity counts and scientific
Boolean flags also retain exact types. Replayed objects cannot substitute floats
or Boolean values for integer identities even when equality would otherwise hold.

Valid source artifacts retain their canonical bytes and digests. Extraction,
normalization, metric formulas, profile versions and retained measurements are
unchanged. These guards establish neither literary-body completeness nor print
edition/FantLab input identity. M2 remains **0/5**.

## Verify offline

```sh
python -m unittest discover -s tests -p 'test_mediawiki_api.py' -v
python -m unittest discover -s tests -p 'test_wikisource_identity_contract.py' -v
python -m unittest discover -s tests -p 'test_single_page_revision.py' -v
```

All responses and prose in these tests are synthetic. Network and sleep are
injected/mocked. They exercise real modules, not a rewritten stub validator.
The full repository suite and actual pinned-provider workflows are separate
exact-head CI gates; offline tests do not mark provider replay VERIFIED.

## Owner-batch outbox reconciliation, 2026-11-04

| Existing handoff | Current disposition |
| --- | --- |
| September 27 SCRIP-CORPUS-086 Boolean page-ID review | Original page-ID guard is already fixed; new executed revision-ID/packed-offset findings are tracked separately in #425 |
| October 5 SCRIP-REPRO-010 POS benchmark integration | Already implemented in `benchmark_pos.py`, wired through `benchmark.py` and covered by `test_benchmark_pos.py`; no duplicate issue |
| September 29 SCRIP-CORPUS-087 White Guard design | Already adopted by #422/#408, as documented in `white-guard-source-replay.md`; no duplicate |
| October 18 wheel QA handoff | Fetched document is empty; no implementation or acceptance evidence can be inferred from its title |
| Existing single-page retry branch | Exact code/test blobs already exist in master despite divergent ancestry; retain tests and extend the policy, do not count old code as new work |

Private storage IDs/links are intentionally absent. Issues #424 and #425 track
the executable remaining gaps. The six pre-existing science, publication,
licensing and branch-maintenance issues are not closed by this transport change.
