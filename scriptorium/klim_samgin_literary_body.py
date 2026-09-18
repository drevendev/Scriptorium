"""Public entry point for the candidate-specific Klim Samgin literary-body extractor."""
from __future__ import annotations

from .klim_samgin_literary_body_impl import (
    COMPOSITE_SEPARATOR,
    COMPOSITION_PROFILE,
    EXTRACTION_PROFILE,
    MANIFEST_VERSION,
    _extract_part_literary_body,
    _plain_poem_value,
    _raw_template_spans,
    build_manifest,
    main,
    replay_manifest,
    validate_manifest,
)

__all__ = [
    "COMPOSITE_SEPARATOR",
    "COMPOSITION_PROFILE",
    "EXTRACTION_PROFILE",
    "MANIFEST_VERSION",
    "_extract_part_literary_body",
    "_plain_poem_value",
    "_raw_template_spans",
    "build_manifest",
    "replay_manifest",
    "validate_manifest",
    "main",
]

if __name__ == "__main__":
    raise SystemExit(main())
