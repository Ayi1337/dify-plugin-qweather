# Privacy Policy

Last Updated: 2025-12-21

## Overview

This privacy policy describes how the **QWeather Tool Plugin for Dify** (the “Plugin”) handles data when you use it within the Dify platform.

## Data Collection by the Plugin

**The Plugin itself does not collect, store, or retain personal information or user content.**

The Plugin only acts as a request forwarder between your Dify instance and QWeather APIs.

## Data Transmission to QWeather

When you invoke a tool, Dify sends tool parameters to the Plugin, and the Plugin sends an HTTPS request to QWeather. Depending on the tool, transmitted data may include:

- Location identifiers or coordinates (e.g. `LocationID`, `longitude,latitude`)
- Query parameters (e.g. language, unit, time, radius, etc.)
- Your QWeather credentials configured in Dify (API Key, API Host)

The Plugin does not add any additional payload beyond what is required by the QWeather API.

## Storage and Logging

- The Plugin does not implement local persistence, caching, or database storage.
- The Plugin does not intentionally log request/response bodies.
- Your Dify instance and/or hosting environment may have its own logging, monitoring, or auditing features. Please review your Dify deployment configuration.

## Data Security

- Communication to QWeather is over HTTPS.
- Credentials are stored and managed by Dify according to your Dify deployment’s security practices.

## Third-Party Policies

Your data is processed by QWeather according to their terms and privacy policies. Please refer to QWeather’s official website and console for the latest information:

- QWeather Console: https://console.qweather.com/
- QWeather Website: https://www.qweather.com/
- QWeather Developer Docs: https://dev.qweather.com/

## Your Responsibilities

You are responsible for:

1. Ensuring you have the right to transmit any data via this Plugin
2. Complying with applicable laws and regulations
3. Securing your QWeather API Key and Dify instance access

## Contact

If you have questions or concerns about this privacy policy, please open an issue in this repository.

---

# 隐私政策（中文）

更新日期：2025-12-21

## 概述

本隐私政策说明 **Dify 和风天气（QWeather）工具插件**（以下简称“插件”）在 Dify 平台中运行时如何处理数据。

## 插件的数据收集

**插件本身不会收集、存储或留存任何个人信息或用户内容。**

插件仅作为你的 Dify 实例与和风天气（QWeather）API 之间的请求转发器。

## 向 QWeather 传输的数据

当你调用工具时，Dify 会将工具参数发送给插件，插件再通过 HTTPS 请求 QWeather。根据不同接口，可能传输的数据包括：

- LocationID 或经纬度坐标（如 `LocationID`、`经度,纬度`）
- 查询参数（如语言、单位、时间、半径等）
- 你在 Dify 中配置的 QWeather 凭证（API Key、API Host）

插件不会额外添加超出 QWeather API 要求的数据载荷。

## 存储与日志

- 插件不实现本地持久化、缓存或数据库存储。
- 插件不会刻意记录请求/响应正文。
- 你的 Dify 实例或部署环境可能会有自身的日志、监控与审计能力，请以你的 Dify 部署配置为准。

## 数据安全

- 与 QWeather 的通信使用 HTTPS。
- 凭证由 Dify 按照你的 Dify 部署安全机制进行存储与管理。

## 第三方政策

你的数据会由 QWeather 按其服务条款与隐私政策处理，请以 QWeather 官方渠道为准：

- QWeather 控制台：https://console.qweather.com/
- QWeather 官网：https://www.qweather.com/
- 开发文档：https://dev.qweather.com/

## 你的责任

你需要确保：

1. 你拥有通过本插件传输相关数据的合法权利
2. 遵守适用的法律法规
3. 妥善保管 QWeather API Key 与 Dify 访问权限

## 联系方式

如对本隐私政策有疑问或顾虑，请在本仓库提交 Issue。

