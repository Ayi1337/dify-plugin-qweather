from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.qweather_client import build_url, get_api_host, get_json, to_json_text

AIR_QUALITY_STATION_PATH_TEMPLATE = "/airquality/v1/station/{location_id}"


class QWeatherAirQualityStationTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        location_id = str(tool_parameters.get("location_id", "")).strip()
        if not location_id:
            raise ValueError("`location_id` is required")

        lang = str(tool_parameters.get("lang", "")).strip()

        api_key = self.runtime.credentials["qweather_api_key"]
        base_url = get_api_host(self.runtime.credentials)

        path = AIR_QUALITY_STATION_PATH_TEMPLATE.format(location_id=location_id)

        query: dict[str, str] = {"key": api_key}
        if lang:
            query["lang"] = lang

        url = build_url(base_url, path, query)
        data = get_json(url, timeout_seconds=10)

        code = str(data.get("code", "")).strip()
        if code and code not in ("200", "204"):
            raise RuntimeError(f"QWeather Air Quality Station API error: code={code}, response={data}")

        yield self.create_json_message(data)
        yield self.create_text_message(to_json_text(data))
