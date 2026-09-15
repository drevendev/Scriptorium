# SCRIP-CORPUS-004 — trace a source-explicit Petersburg modernist candidate

- Issue: #77
- PR: #78
- Scope: corpus / provenance; no FantLab parity promotion and no source-text publication.
- Added `bely-petersburg-1916-ru` as a legally usable >=300,000-character candidate. FantLab's 19 September 2022 analysis reports 944,182 characters and 130,217 words.
- Selected Wikimedia Commons' 632-page facsimile of Andrei Bely's first 1916 book publication as the source-edition lead. Commons describes the volume as a mechanical reproduction of the novel parts published in three *Sirin* collections in 1913–1914 and explicitly marks the work public domain.
- Kept the 1916 first-book edition as a distinct text identity from Bely's materially revised 1922 edition. No equivalence across edition families is inferred.
- The generic Russian Wikisource landing page is recorded only as a legal/bibliographic cross-check: it explicitly sits in the `Тексты без ссылок на источники` category and therefore is not promoted as the candidate source identity.
- The candidate remains `traced_not_frozen`: Scriptorium has not yet frozen the Commons PDF byte digest, a deterministic page/OCR extraction contract, or raw/normalized literary-text digests. No scan pages, OCR, or source prose are committed.
- FantLab does not disclose which Petersburg edition or immutable byte stream was uploaded for its 2022 analysis. `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, and `m2_parity_admissible=false`; M2 remains 0/5 source-matched works.
- Generalized the catalog-level legal-policy wording from a Russian-Wikisource-specific sentence to the repository's candidate-specific public-domain/open-license/permission rule so non-Wikisource legal sources cannot inherit a false provenance claim.
- Public corpus navigation now explains why the Commons facsimile is retained and what evidence is still required before full-work diagnostics.
- This authored run leaves PR #78 open for independent later-run exact-head review. Merge is intentionally deferred under repository separation-of-production-and-judgement policy.
