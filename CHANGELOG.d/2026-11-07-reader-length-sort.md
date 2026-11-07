# SCRIP-SITE-012 — source-bound length ordering (PR candidate)

- Reader catalogue can sort by measured normalized text character count including spaces, descending, using existing checked per-edition `fantlab.general.characters` actuals.
- Missing measurements and research-only cards sort after known values. Numeric zero stays a measurement, not `NOT_RUN`; no FantLab parity is asserted.
- The order is permalink-allow-listed (`catalog_order=length`) and physically reorders cards for keyboard navigation; static no-JavaScript order remains readable.
- Exact-head CI, later acceptance and live desktop/mobile verification remain separate; M2 stays 0/5.
