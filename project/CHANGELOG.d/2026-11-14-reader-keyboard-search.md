# 2026-11-14 — Keyboard-first catalogue search (#283)

- Add a discoverable `/` shortcut to focus verified Reader catalogue search and `Escape` to clear only its query. Preserve selected status, source-language and sort facets.
- Ignore editing/contenteditable, modifier chords, IME composition and disabled controls. Bind the shortcut only after the source-free Reader snapshot passes validation.
- Test real implementation behavior with Node and staged desktop/mobile Chromium, including an unmodified slash typed inside the search input. No-JavaScript cards, scientific claims, manuscript privacy and M2 0/5 remain unchanged.
- Later independent PR acceptance, actual Pages publication and live-browser verification are separate gates.
