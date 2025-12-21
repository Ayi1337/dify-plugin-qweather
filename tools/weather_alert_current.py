from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.qweather_client import build_url, get_api_host, get_json, to_json_text

WEATHER_ALERT_CURRENT_PATH_TEMPLATE = "/weatheralert/v1/current/{latitude}/{longitude}"


class QWeatherWeatherAlertCurrentTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        latitude = str(tool_parameters.get("latitude", "")).strip()
        if not latitude:
            raise ValueError("`latitude` is required")

        longitude = str(tool_parameters.get("longitude", "")).strip()
        if not longitude:
            raise ValueError("`longitude` is required")

        local_time = str(tool_parameters.get("localTime", "")).strip()
        lang = str(tool_parameters.get("lang", "")).strip()

        api_key = self.runtime.credentials["qweather_api_key"]
        base_url = get_api_host(self.runtime.credentials)

        path = WEATHER_ALERT_CURRENT_PATH_TEMPLATE.format(latitude=latitude, longitude=longitude)

        query: dict[str, str] = {"key": api_key}
        if local_time:
            query["localTime"] = local_time
        if lang:
            query["lang"] = lang

        url = build_url(base_url, path, query)
        data = get_json(url, timeout_seconds=10)

        code = str(data.get("code", "")).strip()
        if code and code not in ("200", "204"):
            raise RuntimeError(f"QWeather Weather Alert Current API error: code={code}, response={data}")

        yield self.create_json_message(data)
        yield self.create_text_message(to_json_text(data))
