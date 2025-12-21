from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from tools.geo_city_lookup import QWeatherGeoCityLookupTool
from tools.qweather_client import get_api_host
from tools.weather_now import QWeatherWeatherNowTool


class QWeatherProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        api_key = str(credentials.get("qweather_api_key", "")).strip()
        if not api_key:
            raise ToolProviderCredentialValidationError("`qweather_api_key` is required")

        try:
            get_api_host(credentials)
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e)) from e

        errors: list[str] = []
        try:
            for _ in QWeatherWeatherNowTool.from_credentials(credentials).invoke(tool_parameters={"location": "101010100"}):
                pass
            return
        except Exception as e:
            errors.append(f"Weather Now: {e}")

        try:
            for _ in QWeatherGeoCityLookupTool.from_credentials(credentials).invoke(tool_parameters={"location": "beij"}):
                pass
            return
        except Exception as e:
            errors.append(f"Geo City Lookup: {e}")

        raise ToolProviderCredentialValidationError("; ".join(errors))
