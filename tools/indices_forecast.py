from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.qweather_client import build_url, get_api_host, get_json, to_json_text

ALLOWED_DAYS = {"1d", "3d"}
INDICES_FORECAST_PATH_TEMPLATE = "/v7/indices/{days}"


class QWeatherIndicesForecastTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        days = str(tool_parameters.get("days", "")).strip()
        if not days:
            raise ValueError("`days` is required")
        if days not in ALLOWED_DAYS:
            raise ValueError(f"`days` must be one of {sorted(ALLOWED_DAYS)}")

        location = str(tool_parameters.get("location", "")).strip()
        if not location:
            raise ValueError("`location` is required")

        idx_type = str(tool_parameters.get("type", "")).strip()
        if not idx_type:
            raise ValueError("`type` is required")

        lang = str(tool_parameters.get("lang", "")).strip()

        api_key = self.runtime.credentials["qweather_api_key"]
        base_url = get_api_host(self.runtime.credentials)

        path = INDICES_FORECAST_PATH_TEMPLATE.format(days=days)

        query: dict[str, str] = {"location": location, "type": idx_type, "key": api_key}
        if lang:
            query["lang"] = lang

        url = build_url(base_url, path, query)
        data = get_json(url, timeout_seconds=10)

        code = str(data.get("code", "")).strip()
        if code and code not in ("200", "204"):
            raise RuntimeError(f"QWeather Indices Forecast API error: code={code}, response={data}")

        yield self.create_json_message(data)
        yield self.create_text_message(to_json_text(data))
