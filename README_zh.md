# Dify 和风天气工具插件

[English Documentation](./README.md)

这是一个 Dify **工具插件（Tool Plugin）**，提供了一组精选的工具用于调用 **和风天气（QWeather）** API，让你可以在 Chatflow / Workflow / Agent 中获取天气和地理位置数据。

本插件被设计为和风天气官方 API 的薄包装层：它将请求转发给和风天气，并 **原样** 返回响应。

---

## 概述

- **插件类型**：工具插件（Python）
- **包含工具**：20 个（天气 / 地理 API / 分钟级降水 / 生活指数 / 天文 / 预警 / 空气质量）
- **输出**：
  - `json`：和风天气原始 JSON 响应
  - `text`：与 `json` 相同的内容（格式化的 JSON 字符串）
  - `files`：不使用
- **和风天气响应码**：`code=204` 表示"成功但无数据"，被视为成功（返回而不抛出异常）

> Dify 目前不支持多级工具菜单。本插件使用工具标签前缀如 `Weather -` / `GeoAPI -` 进行轻量级分组。

---

## 安装

### 远程调试（推荐用于开发）

1. 复制 `.env.example` 为 `.env`
2. 填入 Dify "插件调试"（远程调试）页面的值
3. 启动插件进程（保持运行）：

```bash
source .venv/bin/activate
set -a
source .env
set +a
.venv/bin/python main.py
```

### 打包（用于上传）

```bash
dify plugin package .
```

---

## 配置（Provider Credentials）

在 Dify 中安装插件后，配置提供商凭证：

- `qweather_api_key`（必填）：你的和风天气 API Key
- `qweather_base_url`（必填）：你的 **和风天气 API Host**（例如 `https://xxxxxx.qweatherapi.com`）

在哪里找到 **API Host**：
- 和风天气控制台 → 设置：https://console.qweather.com/setting

注意事项：
- **本插件中的所有端点都使用 API Host**（`qweather_base_url`）。不会回退到 `devapi.qweather.com` / `geoapi.qweather.com`。
- 你可以不输入协议；插件会将其规范化为 `https://...` 并去除末尾的 `/`。

---

## 工具

### 地理 API（GeoAPI）

- `qweather_geo_city_lookup`：城市搜索（`/geo/v2/city/lookup`）
- `qweather_geo_top_city`：热门城市（`/geo/v2/city/top`）
- `qweather_geo_poi_lookup`：POI 搜索（`/geo/v2/poi/lookup`）
- `qweather_geo_poi_range`：POI 范围搜索（`/geo/v2/poi/range`）

### 天气（城市）

- `qweather_weather_now`：实时天气（`/v7/weather/now`）
- `qweather_weather_daily_forecast`：逐天预报（`/v7/weather/{days}`：3d/7d/10d/15d/30d）
- `qweather_weather_hourly_forecast`：逐小时预报（`/v7/weather/{hours}`：24h/72h/168h）

### 天气（格点）

- `qweather_grid_weather_now`：格点实时天气（`/v7/grid-weather/now`）
- `qweather_grid_weather_daily_forecast`：格点逐天预报（`/v7/grid-weather/{days}`：3d/7d）
- `qweather_grid_weather_hourly_forecast`：格点逐小时预报（`/v7/grid-weather/{hours}`：24h/72h）

### 分钟级降水

- `qweather_minutely_precipitation`：分钟级降水（`/v7/minutely/5m`）

### 天气指数

- `qweather_indices_forecast`：生活指数预报（`/v7/indices/{days}`：1d/3d）

### 天文

- `qweather_astronomy_sun`：日出日落（`/v7/astronomy/sun`）
- `qweather_astronomy_moon`：月升月落和月相（`/v7/astronomy/moon`）
- `qweather_astronomy_solar_elevation_angle`：太阳高度角（`/v7/astronomy/solar-elevation-angle`）

### 预警

- `qweather_weather_alert_current`：天气灾害预警（v1，按坐标）（`/weatheralert/v1/current/{lat}/{lon}`）

### 空气质量

- `qweather_air_quality_current`：实时空气质量（v1）（`/airquality/v1/current/{lat}/{lon}`）
- `qweather_air_quality_hourly_forecast`：逐小时空气质量预报（v1）（`/airquality/v1/hourly/{lat}/{lon}`）
- `qweather_air_quality_daily_forecast`：逐天空气质量预报（v1）（`/airquality/v1/daily/{lat}/{lon}`）
- `qweather_air_quality_station`：空气质量监测站（v1）（`/airquality/v1/station/{LocationID}`）

---

## 故障排除

1. **已安装但没有操作 / `plugin runtime not found`**
   - 远程调试需要本地插件进程持续运行（`.venv/bin/python main.py`）。
   - 确保 `.env` 与最新的 Dify 调试页面值匹配（host/port/key）。

2. **Dify 重启改变了调试密钥**
   - 更新 `.env`（`REMOTE_INSTALL_KEY`，以及 host/port 如果有变化）。
   - 重启本地插件进程，然后在 Dify 中重新安装/刷新插件。

3. **凭证验证失败**
   - 确保 `qweather_base_url` 是你的 **API Host**（`*.qweatherapi.com`），来自 https://console.qweather.com/setting。

---

## 隐私

插件本身不存储用户数据。它向和风天气发送请求并返回响应。

详见 `PRIVACY.md`。

---

## 贡献

欢迎提交 PR 和 issue。添加新工具时：

1. 添加 `tools/<name>.py`（工具实现）
2. 添加 `tools/<name>.yaml`（工具模式：标签/描述/参数）
3. 在 `qweather.yaml` 中注册该 YAML
4. 返回输出为 `json` + `text`（字符串化的 JSON）

---

## 支持 / 参考

- Dify 工具插件文档：https://docs.dify.ai/zh-hans/develop-plugin/dev-guides-and-walkthroughs/tool-plugin
- 和风天气开发文档：https://dev.qweather.com/
- 和风天气文档仓库：https://github.com/qwd/dev-site
- 和风天气控制台（API Host）：https://console.qweather.com/setting

---

## 许可证

MIT

