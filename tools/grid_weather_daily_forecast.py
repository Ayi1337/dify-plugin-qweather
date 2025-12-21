from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.qweather_client import build_url, get_api_host, get_json, to_json_text

ALLOWED_DAYS = {"3d", "7d"}
GRID_WEATHER_DAILY_PATH_TEMPLATE = "/v7/grid-weather/{days}"


class QWeatherGridWeatherDailyForecastTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        location = str(tool_parameters.get("location", "")).strip()
        if not location:
            raise ValueError("`location` is required")

        days = str(tool_parameters.get("days", "")).strip()
        if not days:
            raise ValueError("`days` is required")
        if days not in ALLOWED_DAYS:
            raise ValueError(f"`days` must be one of {sorted(ALLOWED_DAYS)}")

        lang = str(tool_parameters.get("lang", "")).strip()
        unit = str(tool_parameters.get("unit", "")).strip()

        api_key = self.runtime.credentials["qweather_api_key"]
        base_url = get_api_host(self.runtime.credentials)

        path = GRID_WEATHER_DAILY_PATH_TEMPLATE.format(days=days)

        query: dict[str, str] = {"location": location, "key": api_key}
        if lang:
            query["lang"] = lang
        if unit:
            query["unit"] = unit

        url = build_url(base_url, path, query)
        data = get_json(url, timeout_seconds=10)

        code = str(data.get("code", "")).strip()
        if code and code not in ("200", "204"):
            raise RuntimeError(f"QWeather Grid Daily Forecast API error: code={code}, response={data}")

        yield self.create_json_message(data)
        yield self.create_text_message(to_json_text(data))
