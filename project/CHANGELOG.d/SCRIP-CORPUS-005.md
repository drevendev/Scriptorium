# SCRIP-CORPUS-005 — trace an early Soviet science-fiction candidate

- Issue: #79
- PR: #80
- Scope: corpus / provenance; no source-text publication, diagnostic promotion, or FantLab parity claim.
- Added Alexey N. Tolstoy's `Гиперболоид инженера Гарина` as a legally usable >=300,000-character diversity candidate. FantLab's 18 September 2022 linguistic analysis reports 495,539 characters and 69,126 words.
- Russian Wikisource provides a stable reviewed full-work page, explicitly marks the literary work public domain, cites `az.lib.ru` as its source, and exposes permanent revision `oldid=5014458` dated 30 August 2023.
- Preserved revision-family ambiguity instead of manufacturing an edition match. The Wikisource text itself says the novel was written in 1926–1927 and revised with new chapters in 1937; FantLab independently says Tolstoy reworked the novel four times, notes a new ending published in 1927, and identifies a 1939 last lifetime edition.
- The candidate therefore remains `traced_not_frozen`: no MediaWiki SHA-1/wikitext digest, deterministic body extraction, raw/normalized literary-text digest, or source prose is committed by this unit.
- `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, and `m2_parity_admissible=false`; M2 remains 0/5 source-matched works.
- Public corpus navigation records the candidate as early Soviet science fiction/adventure and points to the source-edition trace while making the revision ambiguity explicit.
- Two other twentieth-century leads screened during selection, Zamyatin's `Мы` (285,704 FantLab characters) and Tolstoy's `Аэлита` (276,556), were not admitted because they fail the repository's >=300,000-character calibration threshold.
- Independent later-run review of exact head `4973d0166acf156b4d5789974f7777983201fe19` found no blocking defect: the branch was 6 commits ahead / 0 behind base `813f415d7c4ad6c04fb344455110cfcb2187d494`, changed exactly five expected files, had no pre-existing submitted reviews or review threads, and exact-head Pages `35016895745` plus pinned-provider `35016895806` both succeeded.
- Fresh review independently reconfirmed the FantLab counts/date and revision-family notes plus Wikisource permanent revision `oldid=5014458`, public-domain notice, `az.lib.ru` source pointer and 1937-revision note; those facts support a trace-only candidate, not an edition or FantLab-input identity claim.
- PR #80 was squash-merged as `5941c6e158faf27f9a20ad31cf2549c8dc9cf31e`; Issue #79 closed completed. M2 remains 0/5.
