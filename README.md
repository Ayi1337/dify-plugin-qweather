# QWeather Tool Plugin for Dify

[中文文档 (Chinese Documentation)](./README_zh.md)

A Dify **Tool Plugin** that provides a curated set of tools for calling **QWeather (和风天气)** APIs, so you can fetch weather and location data in Chatflow / Workflow / Agent.

This plugin is designed as a thin wrapper around QWeather’s official APIs: it forwards requests to QWeather and returns the response **as-is**.

---

## Overview

- **Plugin type**: Tool Plugin (Python)
- **Tools included**: 20 (Weather / GeoAPI / Minutely / Indices / Astronomy / Warning / Air Quality)
- **Output**:
  - `json`: the original QWeather JSON response
  - `text`: the same content as `json` (pretty-printed JSON string)
  - `files`: not used
- **QWeather response code**: `code=204` means “success but no data”, and is treated as success (returned without raising).

> Dify currently doesn’t support multi-level tool menus. This plugin uses tool label prefixes like `Weather -` / `GeoAPI -` for lightweight grouping.

---

## Installation

### Remote Debug (recommended for development)

1. Copy `.env.example` to `.env`
2. Fill in the values from Dify “Plugin Debug” (Remote Debug) page
3. Start the plugin process (keep it running):

```bash
source .venv/bin/activate
set -a
source .env
set +a
.venv/bin/python main.py
```

### Packaging (for uploading)

```bash
dify plugin package .
```

---

## Configuration (Provider Credentials)

In Dify, after installing the plugin, configure the provider credentials:

- `qweather_api_key` (required): your QWeather API Key
- `qweather_base_url` (required): your **QWeather API Host** (e.g. `https://xxxxxx.qweatherapi.com`)

Where to find **API Host**:
- QWeather Console → Settings: https://console.qweather.com/setting

Notes:
- **All endpoints in this plugin use the API Host** (`qweather_base_url`). No fallback to `devapi.qweather.com` / `geoapi.qweather.com`.
- You can input without scheme; the plugin will normalize it to `https://...` and strip the trailing `/`.

---

## Tools

### GeoAPI

- `qweather_geo_city_lookup`: City Lookup (`/geo/v2/city/lookup`)
- `qweather_geo_top_city`: Top City (`/geo/v2/city/top`)
- `qweather_geo_poi_lookup`: POI Lookup (`/geo/v2/poi/lookup`)
- `qweather_geo_poi_range`: POI Range (`/geo/v2/poi/range`)

### Weather (City)

- `qweather_weather_now`: Weather Now (`/v7/weather/now`)
- `qweather_weather_daily_forecast`: Daily Forecast (`/v7/weather/{days}`: 3d/7d/10d/15d/30d)
- `qweather_weather_hourly_forecast`: Hourly Forecast (`/v7/weather/{hours}`: 24h/72h/168h)

### Weather (Grid)

- `qweather_grid_weather_now`: Grid Weather Now (`/v7/grid-weather/now`)
- `qweather_grid_weather_daily_forecast`: Grid Daily Forecast (`/v7/grid-weather/{days}`: 3d/7d)
- `qweather_grid_weather_hourly_forecast`: Grid Hourly Forecast (`/v7/grid-weather/{hours}`: 24h/72h)

### Minutely

- `qweather_minutely_precipitation`: 5-min Precipitation (`/v7/minutely/5m`)

### Weather Indices

- `qweather_indices_forecast`: Indices Forecast (`/v7/indices/{days}`: 1d/3d)

### Astronomy

- `qweather_astronomy_sun`: Sunrise/Sunset (`/v7/astronomy/sun`)
- `qweather_astronomy_moon`: Moonrise/Moonset/Moon Phase (`/v7/astronomy/moon`)
- `qweather_astronomy_solar_elevation_angle`: Solar Elevation Angle (`/v7/astronomy/solar-elevation-angle`)

### Warning

- `qweather_weather_alert_current`: Weather Alert (v1, by coordinates) (`/weatheralert/v1/current/{lat}/{lon}`)

### Air Quality

- `qweather_air_quality_current`: Current Air Quality (v1) (`/airquality/v1/current/{lat}/{lon}`)
- `qweather_air_quality_hourly_forecast`: Hourly Air Quality (v1) (`/airquality/v1/hourly/{lat}/{lon}`)
- `qweather_air_quality_daily_forecast`: Daily Air Quality (v1) (`/airquality/v1/daily/{lat}/{lon}`)
- `qweather_air_quality_station`: Air Quality Station (v1) (`/airquality/v1/station/{LocationID}`)

---

## Troubleshooting

1. **Installed but no actions / `plugin runtime not found`**
   - Remote Debug requires the local plugin process to be running continuously (`.venv/bin/python main.py`).
   - Ensure `.env` matches the latest Dify debug page values (host/port/key).

2. **Dify restart changed Debug Key**
   - Update `.env` (`REMOTE_INSTALL_KEY`, and host/port if changed).
   - Restart the local plugin process, then reinstall/refresh the plugin in Dify.

3. **Credential validation failed**
   - Make sure `qweather_base_url` is your **API Host** (`*.qweatherapi.com`) from https://console.qweather.com/setting.

---

## Privacy

The plugin itself does not store user data. It sends requests to QWeather and returns responses.

See `PRIVACY.md` for details.

---

## Contributing

PRs and issues are welcome. When adding a new tool:

1. Add `tools/<name>.py` (Tool implementation)
2. Add `tools/<name>.yaml` (Tool schema: label/description/parameters)
3. Register the YAML in `qweather.yaml`
4. Return outputs as `json` + `text` (stringified JSON)

---

## Support / References

- Dify Tool Plugin docs: https://docs.dify.ai/en/develop-plugin/dev-guides-and-walkthroughs/tool-plugin
- QWeather docs site: https://dev.qweather.com/
- QWeather docs repo: https://github.com/qwd/dev-site
- QWeather Console (API Host): https://console.qweather.com/setting

---

## License

MIT

