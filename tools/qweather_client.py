from __future__ import annotations

import gzip
import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

DEFAULT_TIMEOUT_SECONDS = 10

USER_AGENT = "dify-qweather-tool/0.0.7"


def normalize_base_url(raw_base_url: str | None, default: str) -> str:
    base_url = (raw_base_url or "").strip() or default
    if not base_url.startswith(("http://", "https://")):
        base_url = "https://" + base_url
    return base_url.rstrip("/")


def get_api_host(credentials: dict[str, Any]) -> str:
    raw_base_url = str(credentials.get("qweather_base_url", "")).strip()
    if not raw_base_url:
        raise ValueError(
            "`qweather_base_url` is required. Use your QWeather API Host from https://console.qweather.com/setting"
        )

    base_url = normalize_base_url(raw_base_url, raw_base_url)
    if not is_qweather_api_host(base_url):
        raise ValueError(
            "`qweather_base_url` must be your QWeather API Host (e.g. https://xxxxxx.qweatherapi.com). "
            "Find it at https://console.qweather.com/setting"
        )

    return base_url


def is_qweather_api_host(base_url: str) -> bool:
    try:
        parsed = urlparse(base_url if base_url.startswith(("http://", "https://")) else "https://" + base_url)
        host = (parsed.hostname or "").lower()
    except Exception:
        return False
    return host.endswith("qweatherapi.com")


def geo_v2_path(base_url: str, suffix: str) -> str:
    if not suffix.startswith("/"):
        suffix = "/" + suffix
    prefix = "/geo/v2" if is_qweather_api_host(base_url) else "/v2"
    return prefix + suffix


def build_url(base_url: str, path: str, query: dict[str, str], *, safe: str = ",") -> str:
    return base_url.rstrip("/") + path + "?" + urlencode(query, safe=safe)


def to_json_text(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def get_json(url: str, *, timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS) -> dict[str, Any]:
    request = Request(
        url=url,
        headers={
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="GET",
    )

    status_code: int | None = None
    content_encoding = ""

    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            raw = response.read()
            status_code = getattr(response, "status", None)
            content_encoding = (response.headers.get("Content-Encoding") or "").lower().strip()
    except HTTPError as e:
        status_code = e.code
        raw = e.read()
        content_encoding = (e.headers.get("Content-Encoding") or "").lower().strip()
    except URLError as e:
        raise RuntimeError(f"Network error: {e.reason}") from e

    if content_encoding == "gzip" or raw[:2] == b"\x1f\x8b":
        try:
            raw = gzip.decompress(raw)
        except Exception as e:
            raise RuntimeError(f"Failed to decompress gzip response: {raw[:2000]!r}") from e

    try:
        data = json.loads(raw.decode("utf-8"))
    except Exception as e:
        prefix = f"HTTP {status_code}: " if status_code is not None else ""
        raise RuntimeError(f"{prefix}Invalid JSON response: {raw[:2000]!r}") from e

    if status_code is not None and status_code >= 400:
        raise RuntimeError(f"HTTP {status_code}: {data}")

    return data
