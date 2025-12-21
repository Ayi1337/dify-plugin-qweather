from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.qweather_client import build_url, get_api_host, get_json, to_json_text

ALLOWED_HOURS = {"24h", "72h", "168h"}
WEATHER_HOURLY_PATH_TEMPLATE = "/v7/weather/{hours}"


class QWeatherWeatherHourlyForecastTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        location = str(tool_parameters.get("location", "")).strip()
        if not location:
            raise ValueError("`location` is required")

        hours = str(tool_parameters.get("hours", "")).strip().lower()
        if not hours:
            raise ValueError("`hours` is required")
        if hours not in ALLOWED_HOURS:
            raise ValueError(f"`hours` must be one of {sorted(ALLOWED_HOURS)}")

        lang = str(tool_parameters.get("lang", "")).strip()
        unit = str(tool_parameters.get("unit", "")).strip().lower()
        if unit and unit not in ("m", "i"):
            raise ValueError("`unit` must be one of ['m', 'i']")

        api_key = self.runtime.credentials["qweather_api_key"]
        base_url = get_api_host(self.runtime.credentials)

        path = WEATHER_HOURLY_PATH_TEMPLATE.format(hours=hours)

        query: dict[str, str] = {"location": location, "key": api_key}
        if lang:
            query["lang"] = lang
        if unit:
            query["unit"] = unit

        url = build_url(base_url, path, query)
        data = get_json(url, timeout_seconds=10)

        code = str(data.get("code", "")).strip()
        if code and code not in ("200", "204"):
            raise RuntimeError(f"QWeather Hourly Forecast API error: code={code}, response={data}")

        yield self.create_json_message(data)
        yield self.create_text_message(to_json_text(data))
