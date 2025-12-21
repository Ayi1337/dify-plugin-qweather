from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.qweather_client import build_url, geo_v2_path, get_api_host, get_json, to_json_text

TOP_CITY_SUFFIX = "/city/top"


class QWeatherGeoTopCityTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        range_ = str(tool_parameters.get("range", "")).strip()
        number = str(tool_parameters.get("number", "")).strip()
        lang = str(tool_parameters.get("lang", "")).strip()

        api_key = self.runtime.credentials["qweather_api_key"]
        base_url = get_api_host(self.runtime.credentials)
        path = geo_v2_path(base_url, TOP_CITY_SUFFIX)

        query: dict[str, str] = {"key": api_key}
        if range_:
            query["range"] = range_
        if number:
            query["number"] = number
        if lang:
            query["lang"] = lang

        url = build_url(base_url, path, query)
        data = get_json(url, timeout_seconds=10)

        code = str(data.get("code", "")).strip()
        if code and code not in ("200", "204"):
            raise RuntimeError(f"QWeather Geo Top City API error: code={code}, response={data}")

        yield self.create_json_message(data)
        yield self.create_text_message(to_json_text(data))
