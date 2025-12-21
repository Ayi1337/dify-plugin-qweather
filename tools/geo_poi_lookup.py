from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.qweather_client import build_url, geo_v2_path, get_api_host, get_json, to_json_text

POI_LOOKUP_SUFFIX = "/poi/lookup"


class QWeatherGeoPoiLookupTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        location = str(tool_parameters.get("location", "")).strip()
        if not location:
            raise ValueError("`location` is required")

        poi_type = str(tool_parameters.get("type", "")).strip()
        if not poi_type:
            raise ValueError("`type` is required")

        city = str(tool_parameters.get("city", "")).strip()
        number = str(tool_parameters.get("number", "")).strip()
        lang = str(tool_parameters.get("lang", "")).strip()

        api_key = self.runtime.credentials["qweather_api_key"]
        base_url = get_api_host(self.runtime.credentials)
        path = geo_v2_path(base_url, POI_LOOKUP_SUFFIX)

        query: dict[str, str] = {"type": poi_type, "location": location, "key": api_key}
        if city:
            query["city"] = city
        if number:
            query["number"] = number
        if lang:
            query["lang"] = lang

        url = build_url(base_url, path, query)
        data = get_json(url, timeout_seconds=10)

        code = str(data.get("code", "")).strip()
        if code and code not in ("200", "204"):
            raise RuntimeError(f"QWeather Geo POI Lookup API error: code={code}, response={data}")

        yield self.create_json_message(data)
        yield self.create_text_message(to_json_text(data))
