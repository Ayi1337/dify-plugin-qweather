# QWeather Tool Plugin for Dify

**Author**: [Ayi1337](https://github.com/Ayi1337)  
**Repository**: [dify-plugin-qweather](https://github.com/Ayi1337/dify-plugin-qweather)

[中文文档](https://github.com/Ayi1337/dify-plugin-qweather/blob/main/readme/README_zh_Hans.md) | [日本語ドキュメント](https://github.com/Ayi1337/dify-plugin-qweather/blob/main/readme/README_ja_JP.md) | [Documentação em Português](https://github.com/Ayi1337/dify-plugin-qweather/blob/main/readme/README_pt_BR.md)

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

#### **City Lookup** (`qweather_geo_city_lookup`)
- **Description**: City search and reverse geocoding, supports multi-language and fuzzy search
- **Endpoint**: `/geo/v2/city/lookup`
- **Parameters**:
  - `location` (required): Location keyword, coordinates, LocationID, or Adcode
  - `adm` (optional): Superior administrative divisions filter
  - `range` (optional): Search within country/region (ISO 3166 code)
  - `number` (optional): Number of results (1-20, default 10)
  - `lang` (optional): Response language

#### **Top City** (`qweather_geo_top_city`)
- **Description**: Get a list of popular cities around the world
- **Endpoint**: `/geo/v2/city/top`
- **Parameters**:
  - `range` (optional): Country/region (ISO 3166 code)
  - `number` (optional): Number of results (1-20, default 10)
  - `lang` (optional): Response language

#### **POI Lookup** (`qweather_geo_poi_lookup`)
- **Description**: Search POI information (scenic spots, tide stations, etc.) using keywords and coordinates
- **Endpoint**: `/geo/v2/poi/lookup`
- **Parameters**:
  - `type` (required): POI type (`scenic` or `TSTA`)
  - `location` (required): Location keyword, coordinates, LocationID, or Adcode
  - `city` (optional): Search within a given city
  - `number` (optional): Number of results (1-20, default 10)
  - `lang` (optional): Response language

#### **POI Range** (`qweather_geo_poi_range`)
- **Description**: Query POI information within a specified area
- **Endpoint**: `/geo/v2/poi/range`
- **Parameters**:
  - `type` (required): POI type (`scenic` or `TSTA`)
  - `location` (required): Coordinates (longitude,latitude)
  - `radius` (optional): Search radius in kilometers (1-50, default 5)
  - `number` (optional): Number of results (1-20, default 10)
  - `lang` (optional): Response language

---

### Weather (City)

#### **Real-time Weather** (`qweather_weather_now`)
- **Description**: Get real-time weather data for a city or coordinate
- **Endpoint**: `/v7/weather/now`
- **Parameters**:
  - `location` (required): LocationID or coordinates
  - `lang` (optional): Response language
  - `unit` (optional): Unit system (`m` for metric, `i` for imperial)

#### **Daily Weather Forecast** (`qweather_weather_daily_forecast`)
- **Description**: Daily weather forecast for the next 3-30 days
- **Endpoint**: `/v7/weather/{days}`
- **Available Days**: 3d, 7d, 10d, 15d, 30d
- **Parameters**:
  - `days` (required): Forecast days (3d/7d/10d/15d/30d)
  - `location` (required): LocationID or coordinates
  - `lang` (optional): Response language
  - `unit` (optional): Unit system (`m` for metric, `i` for imperial)

#### **Hourly Weather Forecast** (`qweather_weather_hourly_forecast`)
- **Description**: Hourly weather forecast for the next 24-168 hours
- **Endpoint**: `/v7/weather/{hours}`
- **Available Hours**: 24h, 72h, 168h
- **Parameters**:
  - `hours` (required): Forecast hours (24h/72h/168h)
  - `location` (required): LocationID or coordinates
  - `lang` (optional): Response language
  - `unit` (optional): Unit system (`m` for metric, `i` for imperial)

---

### Weather (Grid)

#### **Grid Weather Real-time** (`qweather_grid_weather_now`)
- **Description**: Grid-based real-time weather for coordinates (3-5km resolution)
- **Endpoint**: `/v7/grid-weather/now`
- **Parameters**:
  - `location` (required): Coordinates (longitude,latitude)
  - `lang` (optional): Response language
  - `unit` (optional): Unit system (`m` for metric, `i` for imperial)

#### **Grid Weather Daily Forecast** (`qweather_grid_weather_daily_forecast`)
- **Description**: Grid weather daily forecast for the next 3-7 days (3-5km resolution)
- **Endpoint**: `/v7/grid-weather/{days}`
- **Available Days**: 3d, 7d
- **Parameters**:
  - `days` (required): Forecast days (3d/7d)
  - `location` (required): Coordinates (longitude,latitude)
  - `lang` (optional): Response language
  - `unit` (optional): Unit system (`m` for metric, `i` for imperial)

#### **Grid Weather Hourly Forecast** (`qweather_grid_weather_hourly_forecast`)
- **Description**: Grid weather hourly forecast for the next 24-72 hours (3-5km resolution)
- **Endpoint**: `/v7/grid-weather/{hours}`
- **Available Hours**: 24h, 72h
- **Parameters**:
  - `hours` (required): Forecast hours (24h/72h)
  - `location` (required): Coordinates (longitude,latitude)
  - `lang` (optional): Response language
  - `unit` (optional): Unit system (`m` for metric, `i` for imperial)

---

### Minutely Forecast

#### **Minutely Precipitation** (`qweather_minutely_precipitation`)
- **Description**: Minute-level precipitation forecast every 5 minutes for the next 2 hours (China only)
- **Endpoint**: `/v7/minutely/5m`
- **Parameters**:
  - `location` (required): Coordinates (longitude,latitude)
  - `lang` (optional): Response language

---

### Weather Indices

#### **Weather Indices Forecast** (`qweather_indices_forecast`)
- **Description**: Get weather lifestyle indices forecast data for cities in China and worldwide
- **Endpoint**: `/v7/indices/{days}`
- **Available Days**: 1d, 3d
- **Parameters**:
  - `days` (required): Forecast days (1d/3d)
  - `type` (required): Weather indices type IDs (comma-separated)
  - `location` (required): LocationID or coordinates
  - `lang` (optional): Response language

---

### Astronomy

#### **Sunrise and Sunset** (`qweather_astronomy_sun`)
- **Description**: Get sunrise and sunset times for the next 60 days at any location worldwide
- **Endpoint**: `/v7/astronomy/sun`
- **Parameters**:
  - `location` (required): LocationID or coordinates
  - `date` (required): Date in yyyyMMdd format (up to 60 days)

#### **Moon and Moon Phase** (`qweather_astronomy_moon`)
- **Description**: Get moonrise, moonset and hourly moon phase data for the next 60 days
- **Endpoint**: `/v7/astronomy/moon`
- **Parameters**:
  - `location` (required): LocationID or coordinates
  - `date` (required): Date in yyyyMMdd format (up to 60 days)
  - `lang` (optional): Response language

#### **Solar Elevation Angle** (`qweather_astronomy_solar_elevation_angle`)
- **Description**: Get global solar elevation angle and azimuth at any time point
- **Endpoint**: `/v7/astronomy/solar-elevation-angle`
- **Parameters**:
  - `location` (required): Coordinates (longitude,latitude)
  - `date` (required): Date in yyyyMMdd format
  - `time` (required): Time in HHmm format (24-hour)
  - `tz` (required): Time zone (e.g., 0800 or -0530)
  - `alt` (required): Altitude in meters

---

### Warning

#### **Weather Alert** (`qweather_weather_alert_current`)
- **Description**: Get officially issued real-time severe weather alerts by coordinates
- **Endpoint**: `/weatheralert/v1/current/{lat}/{lon}`
- **Parameters**:
  - `latitude` (required): Latitude (decimal, up to 2 decimal places)
  - `longitude` (required): Longitude (decimal, up to 2 decimal places)
  - `localTime` (optional): Return local time (true) or UTC time (false, default)
  - `lang` (optional): Response language

---

### Air Quality

#### **Current Air Quality** (`qweather_air_quality_current`)
- **Description**: Current air quality (AQI) by coordinates
- **Endpoint**: `/airquality/v1/current/{lat}/{lon}`
- **Parameters**:
  - `latitude` (required): Latitude (decimal, up to 2 decimal places)
  - `longitude` (required): Longitude (decimal, up to 2 decimal places)
  - `lang` (optional): Response language

#### **Air Quality Hourly Forecast** (`qweather_air_quality_hourly_forecast`)
- **Description**: Air quality hourly forecast for the next 24 hours
- **Endpoint**: `/airquality/v1/hourly/{lat}/{lon}`
- **Parameters**:
  - `latitude` (required): Latitude (decimal, up to 2 decimal places)
  - `longitude` (required): Longitude (decimal, up to 2 decimal places)
  - `localTime` (optional): Return local time (true) or UTC time (false, default)
  - `lang` (optional): Response language

#### **Air Quality Daily Forecast** (`qweather_air_quality_daily_forecast`)
- **Description**: Air quality daily forecast for the next 3 days
- **Endpoint**: `/airquality/v1/daily/{lat}/{lon}`
- **Parameters**:
  - `latitude` (required): Latitude (decimal, up to 2 decimal places)
  - `longitude` (required): Longitude (decimal, up to 2 decimal places)
  - `localTime` (optional): Return local time (true) or UTC time (false, default)
  - `lang` (optional): Response language

#### **Monitoring Station Data** (`qweather_air_quality_station`)
- **Description**: Get pollutant concentration values from air quality monitoring stations
- **Endpoint**: `/airquality/v1/station/{LocationID}`
- **Parameters**:
  - `location_id` (required): LocationID of the monitoring station
  - `lang` (optional): Response language

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

## Installation (For Developers)

> **Note**: This section is for plugin developers only. Regular users can install the plugin directly from the Dify Marketplace and do not need to follow these steps.

### Remote Debug (recommended for development)

1. Copy `.env.example` to `.env`
2. Fill in the values from Dify "Plugin Debug" (Remote Debug) page
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

## License

MIT

