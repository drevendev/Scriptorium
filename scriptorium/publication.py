"""Fail-closed helpers for the static publication manifest.

The publication manifest is a presentation allow-list. It must never upgrade the
compatibility evidence already recorded by canonical analysis artifacts.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


_METRIC_COMPATIBILITY_STATUSES = frozenset({"inferred", "reproduced", "extension"})


def derive_compatibility_claim(artifact: Mapping[str, Any]) -> str:
    """Derive a manifest-level claim from canonical per-metric status.

    A uniform metric surface keeps its single status. Any combination of two or more
    supported statuses becomes ``mixed``. Missing/empty metric surfaces and unknown
    statuses are rejected instead of being guessed into a publishable claim.
    """

    try:
        metrics = artifact["analysis"]["metrics"]
    except (KeyError, TypeError) as exc:
        raise ValueError("canonical artifact lacks analysis.metrics") from exc

    if not isinstance(metrics, Mapping) or not metrics:
        raise ValueError("canonical artifact analysis.metrics must be a non-empty object")

    statuses: set[str] = set()
    for metric_id, row in metrics.items():
        if not isinstance(row, Mapping):
            raise ValueError(f"metric {metric_id!r} is not an object")
        status = row.get("compatibility_status")
        if status not in _METRIC_COMPATIBILITY_STATUSES:
            raise ValueError(
                f"metric {metric_id!r} has unsupported compatibility_status {status!r}"
            )
        statuses.add(status)

    if len(statuses) == 1:
        return next(iter(statuses))
    return "mixed"


def validate_compatibility_claim(
    entry: Mapping[str, Any], artifact: Mapping[str, Any]
) -> str:
    """Validate that a publication entry does not upgrade canonical evidence.

    Returns the derived canonical claim when valid; otherwise raises ``ValueError`` so a
    future builder can fail closed before rendering the entry.
    """

    expected = derive_compatibility_claim(artifact)
    actual = entry.get("compatibility_claim")
    if actual != expected:
        raise ValueError(
            "publication compatibility_claim contradicts canonical artifact: "
            f"manifest={actual!r}, canonical={expected!r}"
        )
    return expected
