# Dify 和风天气工具插件

**作者**：[Ayi1337](https://github.com/Ayi1337)  
**项目地址**：[dify-plugin-qweather](https://github.com/Ayi1337/dify-plugin-qweather)

[English Documentation](https://github.com/Ayi1337/dify-plugin-qweather/blob/main/README.md) | [日本語ドキュメント](https://github.com/Ayi1337/dify-plugin-qweather/blob/main/readme/README_ja_JP.md) | [Documentação em Português](https://github.com/Ayi1337/dify-plugin-qweather/blob/main/readme/README_pt_BR.md)

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

#### **城市搜索** (`qweather_geo_city_lookup`)
- **描述**：提供全球城市搜索与坐标反查，支持多语言与模糊搜索
- **接口**：`/geo/v2/city/lookup`
- **参数**：
  - `location`（必填）：地区名称（支持模糊搜索）、经度,纬度坐标、LocationID 或 Adcode（仅中国城市）
  - `adm`（可选）：上级行政区划过滤
  - `range`（可选）：搜索范围（ISO 3166 国家/地区代码）
  - `number`（可选）：返回结果的数量（1-20，默认10）
  - `lang`（可选）：返回语言

#### **热门城市查询** (`qweather_geo_top_city`)
- **描述**：获取全球各国热门城市列表
- **接口**：`/geo/v2/city/top`
- **参数**：
  - `range`（可选）：国家/地区（ISO 3166 代码）
  - `number`（可选）：返回结果的数量（1-20，默认10）
  - `lang`（可选）：返回语言

#### **POI 搜索** (`qweather_geo_poi_lookup`)
- **描述**：使用关键字和坐标查询 POI 信息（景点、潮汐站点等）
- **接口**：`/geo/v2/poi/lookup`
- **参数**：
  - `type`（必填）：POI类型（`scenic` 景点 或 `TSTA` 潮汐站点）
  - `location`（必填）：关键字（支持模糊搜索）、经度,纬度坐标、LocationID 或 Adcode（仅中国城市）
  - `city`（可选）：限定在某个城市内搜索
  - `number`（可选）：返回结果的数量（1-20，默认10）
  - `lang`（可选）：返回语言

#### **POI 范围搜索** (`qweather_geo_poi_range`)
- **描述**：查询指定区域范围内的 POI 信息
- **接口**：`/geo/v2/poi/range`
- **参数**：
  - `type`（必填）：POI类型（`scenic` 景点 或 `TSTA` 潮汐站点）
  - `location`（必填）：经度,纬度坐标（十进制，最多支持小数点后两位）
  - `radius`（可选）：搜索半径（公里，1-50，默认 5 公里）
  - `number`（可选）：返回结果的数量（1-20，默认10）
  - `lang`（可选）：返回语言

---

### 天气预报（城市）

#### **实时天气** (`qweather_weather_now`)
- **描述**：获取指定地区的实时天气数据
- **接口**：`/v7/weather/now`
- **参数**：
  - `location`（必填）：LocationID 或以英文逗号分隔的经度,纬度坐标
  - `lang`（可选）：返回语言
  - `unit`（可选）：单位制（`m` 公制，`i` 英制）

#### **每日天气预报** (`qweather_weather_daily_forecast`)
- **描述**：提供未来3-30天天气预报数据
- **接口**：`/v7/weather/{days}`
- **可用天数**：3d、7d、10d、15d、30d
- **参数**：
  - `days`（必填）：预报天数（3d/7d/10d/15d/30d）
  - `location`（必填）：LocationID 或以英文逗号分隔的经度,纬度坐标
  - `lang`（可选）：返回语言
  - `unit`（可选）：单位制（`m` 公制，`i` 英制）

#### **逐小时天气预报** (`qweather_weather_hourly_forecast`)
- **描述**：提供未来24-168小时逐小时天气预报数据
- **接口**：`/v7/weather/{hours}`
- **可用小时数**：24h、72h、168h
- **参数**：
  - `hours`（必填）：预报小时数（24h/72h/168h）
  - `location`（必填）：LocationID 或以英文逗号分隔的经度,纬度坐标
  - `lang`（可选）：返回语言
  - `unit`（可选）：单位制（`m` 公制，`i` 英制）

---

### 天气预报（格点）

#### **格点实时天气** (`qweather_grid_weather_now`)
- **描述**：基于数值预报模型，提供指定坐标的实时天气（分辨率3-5公里）
- **接口**：`/v7/grid-weather/now`
- **参数**：
  - `location`（必填）：经度,纬度坐标（十进制，最多两位小数）
  - `lang`（可选）：返回语言
  - `unit`（可选）：单位制（`m` 公制，`i` 英制）

#### **格点每日天气预报** (`qweather_grid_weather_daily_forecast`)
- **描述**：提供指定坐标未来3-7天每日天气预报（分辨率3-5公里）
- **接口**：`/v7/grid-weather/{days}`
- **可用天数**：3d、7d
- **参数**：
  - `days`（必填）：预报天数（3d/7d）
  - `location`（必填）：经度,纬度坐标（十进制，最多两位小数）
  - `lang`（可选）：返回语言
  - `unit`（可选）：单位制（`m` 公制，`i` 英制）

#### **格点逐小时天气预报** (`qweather_grid_weather_hourly_forecast`)
- **描述**：提供指定坐标未来24-72小时逐小时天气预报（分辨率3-5公里）
- **接口**：`/v7/grid-weather/{hours}`
- **可用小时数**：24h、72h
- **参数**：
  - `hours`（必填）：预报小时数（24h/72h）
  - `location`（必填）：经度,纬度坐标（十进制，最多两位小数）
  - `lang`（可选）：返回语言
  - `unit`（可选）：单位制（`m` 公制，`i` 英制）

---

### 分钟预报

#### **分钟级降水** (`qweather_minutely_precipitation`)
- **描述**：未来2小时每5分钟降水预报数据（仅支持中国）
- **接口**：`/v7/minutely/5m`
- **参数**：
  - `location`（必填）：经度,纬度坐标（十进制，最多两位小数）
  - `lang`（可选）：返回语言

---

### 天气指数

#### **天气指数预报** (`qweather_indices_forecast`)
- **描述**：获取中国和全球城市天气生活指数预报数据
- **接口**：`/v7/indices/{days}`
- **可用天数**：1d、3d
- **参数**：
  - `days`（必填）：预报天数（1d/3d）
  - `type`（必填）：天气指数类型 ID，多个用英文逗号分隔
  - `location`（必填）：LocationID 或以英文逗号分隔的经度,纬度坐标
  - `lang`（可选）：返回语言

---

### 天文

#### **日出日落** (`qweather_astronomy_sun`)
- **描述**：获取未来60天全球任意地点日出日落时间
- **接口**：`/v7/astronomy/sun`
- **参数**：
  - `location`（必填）：LocationID 或以英文逗号分隔的经度,纬度坐标
  - `date`（必填）：日期格式 yyyyMMdd，最多未来60天（包含今天）

#### **月升月落和月相** (`qweather_astronomy_moon`)
- **描述**：获取未来60天全球任意地点月升月落和逐小时月相数据
- **接口**：`/v7/astronomy/moon`
- **参数**：
  - `location`（必填）：LocationID 或以英文逗号分隔的经度,纬度坐标
  - `date`（必填）：日期格式 yyyyMMdd，最多未来60天（包含今天）
  - `lang`（可选）：返回语言

#### **太阳高度角** (`qweather_astronomy_solar_elevation_angle`)
- **描述**：任意时间点的全球太阳高度及方位角
- **接口**：`/v7/astronomy/solar-elevation-angle`
- **参数**：
  - `location`（必填）：经度,纬度坐标（十进制，最多两位小数）
  - `date`（必填）：日期格式 yyyyMMdd
  - `time`（必填）：时间格式 HHmm（24小时制）
  - `tz`（必填）：查询地区所在时区（例如 0800 或 -0530）
  - `alt`（必填）：海拔高度（米）

---

### 预警

#### **实时天气预警** (`qweather_weather_alert_current`)
- **描述**：根据经纬度坐标查询正在生效的官方天气预警信息
- **接口**：`/weatheralert/v1/current/{lat}/{lon}`
- **参数**：
  - `latitude`（必填）：所需位置的纬度（十进制，最多支持小数点后两位）
  - `longitude`（必填）：所需位置的经度（十进制，最多支持小数点后两位）
  - `localTime`（可选）：是否返回查询地点的本地时间（true 返回本地时间，false 返回UTC时间，默认）
  - `lang`（可选）：返回语言

---

### 空气质量

#### **实时空气质量** (`qweather_air_quality_current`)
- **描述**：实时空气质量（按经纬度坐标查询，空气质量API v1）
- **接口**：`/airquality/v1/current/{lat}/{lon}`
- **参数**：
  - `latitude`（必填）：所需位置的纬度（十进制，最多支持小数点后两位）
  - `longitude`（必填）：所需位置的经度（十进制，最多支持小数点后两位）
  - `lang`（可选）：返回语言

#### **空气质量小时预报** (`qweather_air_quality_hourly_forecast`)
- **描述**：空气质量小时预报（未来24小时，按经纬度坐标查询，空气质量API v1）
- **接口**：`/airquality/v1/hourly/{lat}/{lon}`
- **参数**：
  - `latitude`（必填）：所需位置的纬度（十进制，最多支持小数点后两位）
  - `longitude`（必填）：所需位置的经度（十进制，最多支持小数点后两位）
  - `localTime`（可选）：是否返回查询地点的本地时间（true 返回本地时间，false 返回UTC时间，默认）
  - `lang`（可选）：返回语言

#### **空气质量每日预报** (`qweather_air_quality_daily_forecast`)
- **描述**：空气质量每日预报（未来3天，按经纬度坐标查询，空气质量API v1）
- **接口**：`/airquality/v1/daily/{lat}/{lon}`
- **参数**：
  - `latitude`（必填）：所需位置的纬度（十进制，最多支持小数点后两位）
  - `longitude`（必填）：所需位置的经度（十进制，最多支持小数点后两位）
  - `localTime`（可选）：是否返回查询地点的本地时间（true 返回本地时间，false 返回UTC时间，默认）
  - `lang`（可选）：返回语言

#### **监测站数据** (`qweather_air_quality_station`)
- **描述**：获取空气质量监测站的污染物浓度值
- **接口**：`/airquality/v1/station/{LocationID}`
- **参数**：
  - `location_id`（必填）：空气质量监测站的 LocationID
  - `lang`（可选）：返回语言

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

## 安装（仅供开发者）

> **提示**：本部分仅供插件开发者使用。普通用户可直接从 Dify 插件市场安装插件，无需执行以下步骤。

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

## 许可证

MIT



