# Run receipt — SCRIP-CORPUS-032

Date: 2026-09-19
Issue: #151
Pull request: #152 (`scrip-corpus-032-darwin-scan-metadata`)
Mode: normal-flow P2 corpus/provenance strengthening

## Selected bounded unit

Strengthen the retained Darwin/Rachinsky 1864 nonfiction candidate by freezing the official provider-reported identity metadata of the DjVu file behind the already pinned Wikisource/ProofreadPage family, while keeping independent binary-byte identity and all Page/literary-body claims fail-closed.

## Evidence captured

The retained Russian Wikisource file surface, transcluding Wikimedia Commons metadata, reports the exact DjVu as:

- data size: **27,368,263 bytes**;
- MIME type: **`image/vnd.djvu`**;
- dimensions: **3744 × 5616**;
- page count: **432**;
- provider-reported SHA-1: **`75ef508588194ae74874272ce290f3ec1043ea9b`**;
- current file-history display: **`11:45, 8 March 2016`**;
- uploader: **`Nonexyst`**;
- upstream source locator: `https://archive.org/details/oproiskhozhdenii00darw`.

The same file surface describes the object as a mechanical scan/public-domain source file and shows Public Domain Mark 1.0. These are retained as source declarations, not independent legal or cryptographic verification.

## Durable result

- Updated `corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.source-graph.json` with provider-reported remote scan metadata and a stricter binary-identity boundary.
- Updated `corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.json` to synchronize the source identity, legal provenance and binary-verification boundary.
- Updated the dedicated public candidate page to make the scan provenance inspectable without publishing scan bytes or source prose.
- Added this semantic changelog fragment and advanced canonical state to hand Draft PR #152 to a later independent exact-head review.

## Freeze boundary

Frozen at this stage:

- all previously retained Rachinsky/Glazunov 1864 parent/index/rendered-route metadata;
- provider-reported remote scan data size, MIME type, dimensions and page count;
- provider-reported remote scan SHA-1;
- current provider file-history display/uploader;
- Archive.org source locator and source-declared mechanical-scan/public-domain status.

Still unfrozen:

- exact underlying Page-namespace revision IDs/timestamps/MediaWiki SHA-1 identities;
- displayed-print-page ↔ scan/Page sequence mapping;
- independent retrieval of one exact DjVu byte stream and a Scriptorium-computed SHA-256;
- classification of displayed print page 388;
- OCR/Page-markup extraction semantics;
- deterministic literary-body extraction/composition, count and raw/normalized digests;
- FantLab analyzer-input/source-edition identity.

## Corpus and gate status

Provider file metadata cannot prove the repository's >=300,000-character literary-body threshold and does not identify the Page-level transcription inputs. The candidate therefore remains a retained diversification lead, not an admitted calibration/profile work.

- `admitted_for_calibration=false`
- `fantlab_source_edition_match=unknown`
- `diagnostic_ready=false`
- `gate_ready=false`
- `m2_parity_admissible=false`
- M2 remains **0/5 source-matched works**

## Handoff

Draft PR #152 must be reviewed on its exact final head by a later run. That review should independently verify the official provider metadata against the current source surface, inspect changed files for any binary/source-prose leak or boundary promotion, and require exact-head CI before any Ready/merge decision.

## Independent exact-head review and merge

A later run independently reviewed exact authored head **`638c30a329f49f1afa55ecb39b8f5b98a55cebc7`** against unchanged base **`c6b1567ff9918dbf7b9d024256eb8743ebd633ad`**.

- The current official Russian Wikisource/Commons file surface independently re-confirmed 27,368,263 bytes, `image/vnd.djvu`, 3744 × 5616, 432 pages, SHA-1 `75ef508588194ae74874272ce290f3ec1043ea9b`, file-history display `11:45, 8 March 2016` by `Nonexyst`, the Archive.org source locator, and the mechanical-scan/public-domain declaration.
- All six changed paths were inspected and remained source-free metadata/control records; no literary prose, Page payload, OCR, DjVu/PDF bytes, or other binary content was introduced.
- The provider/local-verification boundary remained intact: no independently recomputed SHA-1, local scan-byte freeze, binary SHA-256, Page-level identity, p.388 classification, literary-body count/digest, >=300k admission, FantLab source match, or M2 promotion was claimed.
- All **13/13** pull-request-triggered workflows completed successfully on the exact head. `Scriptorium Pages` run `35459774460`, job `105941434196`, passed the standard-library suite, canonical build, deterministic rebuild and artifact upload; artifact `10588992640` is tied to the reviewed head with digest `sha256:4042d0e49a2054a24de678ae4d4e6e05b0a9a619f7c9f12cebf5e825c893d793`. `Scriptorium pinned pylem provider` run `35459774480` also completed successfully.
- No inline review threads or blocking defects were present.

PR #152 was marked Ready and squash-merged as **`63e1de382af32866cc669b9549017899fbe9b399`**. Issue #151 closed as completed. The unit is complete; normal-flow P2 corpus/provenance selection may resume on the next wake.