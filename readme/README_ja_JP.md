# Dify用QWeather Tool Plugin

**作者**: [Ayi1337](https://github.com/Ayi1337)  
**リポジトリ**: [dify-plugin-qweather](https://github.com/Ayi1337/dify-plugin-qweather)

[English Documentation](https://github.com/Ayi1337/dify-plugin-qweather/blob/main/README.md) | [中文文档](https://github.com/Ayi1337/dify-plugin-qweather/blob/main/readme/README_zh_Hans.md) | [Documentação em Português](https://github.com/Ayi1337/dify-plugin-qweather/blob/main/readme/README_pt_BR.md)

Difyの**ツールプラグイン**で、**QWeather（和風天気）** APIを呼び出すための厳選されたツールセットを提供し、Chatflow / Workflow / Agentで天気と位置情報データを取得できます。

このプラグインはQWeather公式APIの薄いラッパーとして設計されており、リクエストをQWeatherに転送し、レスポンスを**そのまま**返します。

---

## 概要

- **プラグインタイプ**: ツールプラグイン（Python）
- **含まれるツール**: 20個（天気 / GeoAPI / 分単位 / 指数 / 天文 / 警報 / 空気質）
- **出力**:
  - `json`: QWeatherの元のJSONレスポンス
  - `text`: `json`と同じ内容（整形されたJSON文字列）
  - `files`: 未使用
- **QWeatherレスポンスコード**: `code=204`は「成功だがデータなし」を意味し、成功として扱われます（例外を発生させずに返されます）

> Difyは現在マルチレベルのツールメニューをサポートしていません。このプラグインは、軽量なグループ化のために`Weather -` / `GeoAPI -`のようなツールラベルプレフィックスを使用します。

---

## 設定（プロバイダー認証情報）

Difyでプラグインをインストールした後、プロバイダー認証情報を設定します:

- `qweather_api_key`（必須）: QWeather API Key
- `qweather_base_url`（必須）: **QWeather API Host**（例: `https://xxxxxx.qweatherapi.com`）

**API Host**の場所:
- QWeatherコンソール → 設定: https://console.qweather.com/setting

注意事項:
- **このプラグインのすべてのエンドポイントはAPI Host**（`qweather_base_url`）を使用します。`devapi.qweather.com` / `geoapi.qweather.com`へのフォールバックはありません。
- スキームなしで入力できます。プラグインは自動的に`https://...`に正規化し、末尾の`/`を削除します。

---

## ツール

### GeoAPI

#### **都市検索** (`qweather_geo_city_lookup`)
- **説明**: 都市検索と逆ジオコーディング、多言語とあいまい検索をサポート
- **エンドポイント**: `/geo/v2/city/lookup`
- **パラメータ**:
  - `location`（必須）: 位置キーワード、座標、LocationID、またはAdcode
  - `adm`（オプション）: 上位行政区画フィルター
  - `range`（オプション）: 国/地域内で検索（ISO 3166コード）
  - `number`（オプション）: 結果数（1-20、デフォルト10）
  - `lang`（オプション）: レスポンス言語

#### **人気都市** (`qweather_geo_top_city`)
- **説明**: 世界中の人気都市のリストを取得
- **エンドポイント**: `/geo/v2/city/top`
- **パラメータ**:
  - `range`（オプション）: 国/地域（ISO 3166コード）
  - `number`（オプション）: 結果数（1-20、デフォルト10）
  - `lang`（オプション）: レスポンス言語

#### **POI検索** (`qweather_geo_poi_lookup`)
- **説明**: キーワードと座標を使用してPOI情報（景勝地、潮汐観測所など）を検索
- **エンドポイント**: `/geo/v2/poi/lookup`
- **パラメータ**:
  - `type`（必須）: POIタイプ（`scenic`または`TSTA`）
  - `location`（必須）: 位置キーワード、座標、LocationID、またはAdcode
  - `city`（オプション）: 指定された都市内で検索
  - `number`（オプション）: 結果数（1-20、デフォルト10）
  - `lang`（オプション）: レスポンス言語

#### **POI範囲検索** (`qweather_geo_poi_range`)
- **説明**: 指定されたエリア内のPOI情報を照会
- **エンドポイント**: `/geo/v2/poi/range`
- **パラメータ**:
  - `type`（必須）: POIタイプ（`scenic`または`TSTA`）
  - `location`（必須）: 座標（経度,緯度）
  - `radius`（オプション）: 検索半径（km、1-50、デフォルト5）
  - `number`（オプション）: 結果数（1-20、デフォルト10）
  - `lang`（オプション）: レスポンス言語

---

### 天気（都市）

#### **リアルタイム天気** (`qweather_weather_now`)
- **説明**: 都市または座標のリアルタイム天気データを取得
- **エンドポイント**: `/v7/weather/now`
- **パラメータ**:
  - `location`（必須）: LocationIDまたは座標
  - `lang`（オプション）: レスポンス言語
  - `unit`（オプション）: 単位系（`m`メートル法、`i`ヤードポンド法）

#### **日次天気予報** (`qweather_weather_daily_forecast`)
- **説明**: 今後3〜30日間の日次天気予報
- **エンドポイント**: `/v7/weather/{days}`
- **利用可能な日数**: 3d、7d、10d、15d、30d
- **パラメータ**:
  - `days`（必須）: 予報日数（3d/7d/10d/15d/30d）
  - `location`（必須）: LocationIDまたは座標
  - `lang`（オプション）: レスポンス言語
  - `unit`（オプション）: 単位系（`m`メートル法、`i`ヤードポンド法）

#### **時間別天気予報** (`qweather_weather_hourly_forecast`)
- **説明**: 今後24〜168時間の時間別天気予報
- **エンドポイント**: `/v7/weather/{hours}`
- **利用可能な時間**: 24h、72h、168h
- **パラメータ**:
  - `hours`（必須）: 予報時間（24h/72h/168h）
  - `location`（必須）: LocationIDまたは座標
  - `lang`（オプション）: レスポンス言語
  - `unit`（オプション）: 単位系（`m`メートル法、`i`ヤードポンド法）

---

### 天気（グリッド）

#### **グリッド天気リアルタイム** (`qweather_grid_weather_now`)
- **説明**: 座標のグリッドベースのリアルタイム天気（3-5km解像度）
- **エンドポイント**: `/v7/grid-weather/now`
- **パラメータ**:
  - `location`（必須）: 座標（経度,緯度）
  - `lang`（オプション）: レスポンス言語
  - `unit`（オプション）: 単位系（`m`メートル法、`i`ヤードポンド法）

#### **グリッド天気日次予報** (`qweather_grid_weather_daily_forecast`)
- **説明**: 今後3〜7日間のグリッド天気日次予報（3-5km解像度）
- **エンドポイント**: `/v7/grid-weather/{days}`
- **利用可能な日数**: 3d、7d
- **パラメータ**:
  - `days`（必須）: 予報日数（3d/7d）
  - `location`（必須）: 座標（経度,緯度）
  - `lang`（オプション）: レスポンス言語
  - `unit`（オプション）: 単位系（`m`メートル法、`i`ヤードポンド法）

#### **グリッド天気時間別予報** (`qweather_grid_weather_hourly_forecast`)
- **説明**: 今後24〜72時間のグリッド天気時間別予報（3-5km解像度）
- **エンドポイント**: `/v7/grid-weather/{hours}`
- **利用可能な時間**: 24h、72h
- **パラメータ**:
  - `hours`（必須）: 予報時間（24h/72h）
  - `location`（必須）: 座標（経度,緯度）
  - `lang`（オプション）: レスポンス言語
  - `unit`（オプション）: 単位系（`m`メートル法、`i`ヤードポンド法）

---

### 分単位予報

#### **分単位降水量** (`qweather_minutely_precipitation`)
- **説明**: 今後2時間の5分ごとの降水量予報（中国のみ）
- **エンドポイント**: `/v7/minutely/5m`
- **パラメータ**:
  - `location`（必須）: 座標（経度,緯度）
  - `lang`（オプション）: レスポンス言語

---

### 天気指数

#### **天気指数予報** (`qweather_indices_forecast`)
- **説明**: 中国および世界中の都市の天気生活指数予報データを取得
- **エンドポイント**: `/v7/indices/{days}`
- **利用可能な日数**: 1d、3d
- **パラメータ**:
  - `days`（必須）: 予報日数（1d/3d）
  - `type`（必須）: 天気指数タイプID（カンマ区切り）
  - `location`（必須）: LocationIDまたは座標
  - `lang`（オプション）: レスポンス言語

---

### 天文

#### **日の出・日の入り** (`qweather_astronomy_sun`)
- **説明**: 世界中の任意の場所で今後60日間の日の出・日の入り時刻を取得
- **エンドポイント**: `/v7/astronomy/sun`
- **パラメータ**:
  - `location`（必須）: LocationIDまたは座標
  - `date`（必須）: yyyyMMdd形式の日付（今後60日まで）

#### **月の出・月の入りと月相** (`qweather_astronomy_moon`)
- **説明**: 今後60日間の月の出・月の入りと時間別月相データを取得
- **エンドポイント**: `/v7/astronomy/moon`
- **パラメータ**:
  - `location`（必須）: LocationIDまたは座標
  - `date`（必須）: yyyyMMdd形式の日付（今後60日まで）
  - `lang`（オプション）: レスポンス言語

#### **太陽高度角** (`qweather_astronomy_solar_elevation_angle`)
- **説明**: 任意の時点での世界の太陽高度角と方位角を取得
- **エンドポイント**: `/v7/astronomy/solar-elevation-angle`
- **パラメータ**:
  - `location`（必須）: 座標（経度,緯度）
  - `date`（必須）: yyyyMMdd形式の日付
  - `time`（必須）: HHmm形式の時刻（24時間制）
  - `tz`（必須）: タイムゾーン（例: 0800または-0530）
  - `alt`（必須）: 高度（メートル）

---

### 警報

#### **天気警報** (`qweather_weather_alert_current`)
- **説明**: 座標による公式発行のリアルタイム悪天候警報を取得
- **エンドポイント**: `/weatheralert/v1/current/{lat}/{lon}`
- **パラメータ**:
  - `latitude`（必須）: 緯度（小数点以下2桁まで）
  - `longitude`（必須）: 経度（小数点以下2桁まで）
  - `localTime`（オプション）: 現地時刻を返す（true）またはUTC時刻（false、デフォルト）
  - `lang`（オプション）: レスポンス言語

---

### 空気質

#### **現在の空気質** (`qweather_air_quality_current`)
- **説明**: 座標による現在の空気質（AQI）
- **エンドポイント**: `/airquality/v1/current/{lat}/{lon}`
- **パラメータ**:
  - `latitude`（必須）: 緯度（小数点以下2桁まで）
  - `longitude`（必須）: 経度（小数点以下2桁まで）
  - `lang`（オプション）: レスポンス言語

#### **空気質時間別予報** (`qweather_air_quality_hourly_forecast`)
- **説明**: 今後24時間の空気質時間別予報
- **エンドポイント**: `/airquality/v1/hourly/{lat}/{lon}`
- **パラメータ**:
  - `latitude`（必須）: 緯度（小数点以下2桁まで）
  - `longitude`（必須）: 経度（小数点以下2桁まで）
  - `localTime`（オプション）: 現地時刻を返す（true）またはUTC時刻（false、デフォルト）
  - `lang`（オプション）: レスポンス言語

#### **空気質日次予報** (`qweather_air_quality_daily_forecast`)
- **説明**: 今後3日間の空気質日次予報
- **エンドポイント**: `/airquality/v1/daily/{lat}/{lon}`
- **パラメータ**:
  - `latitude`（必須）: 緯度（小数点以下2桁まで）
  - `longitude`（必須）: 経度（小数点以下2桁まで）
  - `localTime`（オプション）: 現地時刻を返す（true）またはUTC時刻（false、デフォルト）
  - `lang`（オプション）: レスポンス言語

#### **監視ステーションデータ** (`qweather_air_quality_station`)
- **説明**: 空気質監視ステーションから汚染物質濃度値を取得
- **エンドポイント**: `/airquality/v1/station/{LocationID}`
- **パラメータ**:
  - `location_id`（必須）: 監視ステーションのLocationID
  - `lang`（オプション）: レスポンス言語

---

## トラブルシューティング

1. **インストール済みだがアクションがない / `plugin runtime not found`**
   - リモートデバッグでは、ローカルプラグインプロセスが継続的に実行されている必要があります（`.venv/bin/python main.py`）。
   - `.env`が最新のDifyデバッグページの値（host/port/key）と一致していることを確認してください。

2. **Difyの再起動でデバッグキーが変更された**
   - `.env`を更新します（`REMOTE_INSTALL_KEY`、および変更された場合はhost/port）。
   - ローカルプラグインプロセスを再起動し、Difyでプラグインを再インストール/更新します。

3. **認証情報の検証に失敗した**
   - `qweather_base_url`が**API Host**（`*.qweatherapi.com`）であることを確認してください。https://console.qweather.com/setting から取得できます。

---

## プライバシー

プラグイン自体はユーザーデータを保存しません。QWeatherにリクエストを送信し、レスポンスを返します。

詳細は`PRIVACY.md`を参照してください。

---

## 貢献

PRとissueを歓迎します。新しいツールを追加する場合:

1. `tools/<name>.py`を追加（ツール実装）
2. `tools/<name>.yaml`を追加（ツールスキーマ: ラベル/説明/パラメータ）
3. `qweather.yaml`にYAMLを登録
4. 出力を`json` + `text`（文字列化されたJSON）として返す

---

## サポート / リファレンス

- Difyツールプラグインドキュメント: https://docs.dify.ai/en/develop-plugin/dev-guides-and-walkthroughs/tool-plugin
- QWeatherドキュメントサイト: https://dev.qweather.com/
- QWeatherドキュメントリポジトリ: https://github.com/qwd/dev-site
- QWeatherコンソール（API Host）: https://console.qweather.com/setting

---

## インストール（開発者向け）

> **注意**: このセクションはプラグイン開発者専用です。一般ユーザーはDifyマーケットプレイスから直接プラグインをインストールでき、これらの手順に従う必要はありません。

### リモートデバッグ（開発に推奨）

1. `.env.example`を`.env`にコピー
2. Dify「プラグインデバッグ」（リモートデバッグ）ページの値を入力
3. プラグインプロセスを開始（実行し続ける）:

```bash
source .venv/bin/activate
set -a
source .env
set +a
.venv/bin/python main.py
```

### パッケージング（アップロード用）

```bash
dify plugin package .
```

---

## ライセンス

MIT


