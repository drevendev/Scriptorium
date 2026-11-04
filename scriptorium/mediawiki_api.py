"""Bounded read-only MediaWiki transport; provenance validation stays with callers.

Only explicit provider throttling is retried. Never retry malformed evidence,
unknown API errors, authentication failures or a caller's identity mismatch.
See docs/WIKISOURCE_RELIABILITY.md for the policy and primary-source rationale.
"""
from __future__ import annotations

from email.utils import parsedate_to_datetime
import json
import math
import re
import time
from typing import Callable, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

MAX_ATTEMPTS = 3
MAX_TOTAL_WAIT_SECONDS = 60
MAX_RESPONSE_BYTES = 16 * 1024 * 1024
_TRANSIENT_CODES = frozenset({"maxlag", "ratelimited"})


class MediaWikiReadError(ValueError):
    """Safe, source-free transport error; provider prose is never included."""


class MediaWikiRetryError(RuntimeError):
    """The provider's requested delay or retry count exceeds this bounded read."""


def _pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise MediaWikiReadError("duplicate key in MediaWiki JSON response")
        result[key] = value
    return result


def _nonfinite(_value: str) -> None:
    raise MediaWikiReadError("nonfinite value in MediaWiki JSON response")


def _finite_float(value: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise MediaWikiReadError("nonfinite value in MediaWiki JSON response")
    return result


def _transient_error(payload: dict[str, object]) -> bool:
    """Recognize both classic and modern errors, without hiding mixed failures."""
    errors: list[object] = []
    if "error" in payload:
        errors.append(payload["error"])
    if "errors" in payload:
        modern = payload["errors"]
        if not isinstance(modern, list) or not modern:
            raise MediaWikiReadError("malformed MediaWiki API errors")
        errors.extend(modern)
    if not errors:
        return False
    for error in errors:
        if not isinstance(error, dict) or not isinstance(error.get("code"), str):
            raise MediaWikiReadError("malformed MediaWiki API error")
        if error["code"] not in _TRANSIENT_CODES:
            raise MediaWikiReadError("non-retryable MediaWiki API error")
    return True


def _retry_delay(header: object, attempt: int, now: Callable[[], float]) -> int:
    minimum = 5 * (2 ** (attempt - 1))
    if header is None:
        return minimum
    if not isinstance(header, str):
        raise MediaWikiRetryError("invalid MediaWiki Retry-After; not retrying early")
    value = header.strip()
    if re.fullmatch(r"[0-9]+", value):
        # Avoid unbounded integer conversion even for adversarial headers.
        significant = value.lstrip("0") or "0"
        if len(significant) > 2:
            raise MediaWikiRetryError("Retry-After exceeds bounded capture; defer read")
        delay = int(significant)
    else:
        try:
            date = parsedate_to_datetime(value)
            if date.tzinfo is None:
                raise ValueError("timezone required")
            delay = max(0, math.ceil(date.timestamp() - now()))
        except (ValueError, TypeError, OverflowError):
            raise MediaWikiRetryError("invalid MediaWiki Retry-After; not retrying early") from None
    delay = max(minimum, delay)
    if delay > MAX_TOTAL_WAIT_SECONDS:
        raise MediaWikiRetryError("Retry-After exceeds bounded capture; defer read")
    return delay


def query_json(
    params: Mapping[str, str], *, api_url: str, user_agent: str,
    opener: Callable[..., object] | None = None,
    sleep: Callable[[float], None] | None = None,
    now: Callable[[], float] | None = None,
) -> dict[str, object]:
    """Perform at most three sequential GETs of the exact same request.

    Sleeps total at most 60 seconds (separate from the 30-second request timeout).
    A longer server delay fails/defer rather than being clipped. Response bytes
    live only in memory; errors never echo the URL, body or provider info field.
    """
    opener = urlopen if opener is None else opener
    sleep = time.sleep if sleep is None else sleep
    now = time.time if now is None else now
    encoded = urlencode({**params, "maxlag": "5", "format": "json", "formatversion": "2"})
    request = Request(f"{api_url}?{encoded}", headers={
        "User-Agent": user_agent, "Accept": "application/json",
    })
    waited = 0
    for attempt in range(1, MAX_ATTEMPTS + 1):
        retry_after = None
        try:
            with opener(request, timeout=30) as response:
                headers = getattr(response, "headers", None)
                retry_after = headers.get("Retry-After") if headers is not None else None
                raw = response.read(MAX_RESPONSE_BYTES + 1)
            if len(raw) > MAX_RESPONSE_BYTES:
                raise MediaWikiReadError("MediaWiki JSON response exceeds byte limit")
            try:
                payload = json.loads(raw, object_pairs_hook=_pairs, parse_constant=_nonfinite, parse_float=_finite_float)
            except (ValueError, UnicodeError, RecursionError):
                raise MediaWikiReadError("invalid MediaWiki JSON response") from None
            if not isinstance(payload, dict):
                raise MediaWikiReadError("unexpected MediaWiki API response")
            if not _transient_error(payload):
                return payload
        except HTTPError as exc:
            status = exc.code
            retry_after = exc.headers.get("Retry-After") if exc.headers is not None else None
            exc.close()
            # Unmarked 503 may be a cache timeout, not a transient API throttle.
            if status != 429 and not (status == 503 and retry_after is not None):
                raise MediaWikiReadError(f"non-retryable MediaWiki HTTP status {status}") from None
        except (URLError, TimeoutError, OSError):
            # No retry storm on DNS, TLS, authentication or unknown network errors.
            raise MediaWikiReadError("MediaWiki transport failed; no automatic retry") from None
        if attempt == MAX_ATTEMPTS:
            raise MediaWikiRetryError("MediaWiki throttling persisted after three attempts")
        delay = _retry_delay(retry_after, attempt, now)
        if waited + delay > MAX_TOTAL_WAIT_SECONDS:
            raise MediaWikiRetryError("Retry-After exceeds remaining wait budget; defer read")
        sleep(delay)
        waited += delay
    raise AssertionError("unreachable MediaWiki retry state")
