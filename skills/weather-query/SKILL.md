---
name: weather-query
description: "Query current weather and forecast for any city via wttr.in or OpenWeatherMap API."
tags: [weather, forecast, api]
version: 1.0.0
metadata:
  {
    "openclaw":
      {
        "emoji": "🌤️",
        "requires": { "bins": ["curl"] },
        "install":
          [],
      },
  }
---

# Weather Query Skill

## 概述

通过 wttr.in 或 OpenWeatherMap API 查询任意城市的实时天气和预报信息。

支持两种模式：
- **wttr.in 模式**（默认）：无需 API Key，直接通过 curl 查询，开箱即用
- **OpenWeatherMap 模式**：需要 API Key，支持更详细的气象数据

## 前置条件

- 已安装 `curl` 和 `jq`
- 网络可访问 wttr.in 或 api.openweathermap.org

安装依赖：

```bash
# EulerOS / CentOS
sudo yum install curl jq

# Ubuntu / Debian
sudo apt install curl jq
```

## 核心命令

### wttr.in 模式（无需 API Key）

#### 查询当前天气（中文）

```bash
curl -s "wttr.in/Beijing?lang=zh"
```

#### 查询当前天气（紧凑格式）

```bash
curl -s "wttr.in/Shanghai?format=3"
```

#### 查询3天预报

```bash
curl -s "wttr.in/Guangzhou?lang=zh&format=v2"
```

#### 自定义格式输出

```bash
# 温度+风速+湿度
curl -s "wttr.in/Shenzhen?format=%t+%w+%h"
```

格式占位符：
- `%t` — 温度
- `%w` — 风向风速
- `%h` — 湿度
- `%p` — 气压
- `%c` — 天气图标
- `%C` — 天气描述

#### JSON 格式输出（便于程序解析）

```bash
curl -s "wttr.in/Beijing?format=j1" | jq '.current_condition[0] | {temp_C, humidity, weatherDesc: .weatherDesc[0].value, windspeedKmph}'
```

### OpenWeatherMap 模式（需要 API Key）

需要设置环境变量 `OWM_API_KEY`。

获取免费 API Key：https://openweathermap.org/api

#### 查询当前天气

```bash
curl -s "https://api.openweathermap.org/data/2.5/weather?q=Beijing&appid=${OWM_API_KEY}&units=metric&lang=zh_cn" | jq '{city: .name, temp: .main.temp, humidity: .main.humidity, weather: .weather[0].description, wind_speed: .wind.speed}'
```

#### 查询5天预报

```bash
curl -s "https://api.openweathermap.org/data/2.5/forecast?q=Beijing&appid=${OWM_API_KEY}&units=metric&lang=zh_cn&cnt=8" | jq '.list[] | {dt_txt, temp: .main.temp, weather: .weather[0].description}'
```

#### 按经纬度查询

```bash
curl -s "https://api.openweathermap.org/data/2.5/weather?lat=39.9&lon=116.4&appid=${OWM_API_KEY}&units=metric" | jq '{city: .name, temp: .main.temp, weather: .weather[0].description}'
```

## 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| 城市名 | 英文城市名或中文拼音 | `Beijing`, `Shanghai` |
| `lang` | 语言 | `zh`（中文）, `en`（英文） |
| `format` | wttr.in 输出格式 | `v2`（详细）, `j1`（JSON）, `3`（紧凑） |
| `units` | OWM 温度单位 | `metric`（摄氏）, `imperial`（华氏） |
| `OWM_API_KEY` | OpenWeatherMap API 密钥 | 从官网免费申请 |

## 常见用法示例

### 快速查看北京天气

```bash
curl -s "wttr.in/Beijing?lang=zh&format=v2"
```

### 获取 JSON 格式用于脚本处理

```bash
WEATHER=$(curl -s "wttr.in/Shanghai?format=j1")
TEMP=$(echo "$WEATHER" | jq -r '.current_condition[0].temp_C')
HUMIDITY=$(echo "$WEATHER" | jq -r '.current_condition[0].humidity')
echo "上海当前温度: ${TEMP}°C, 湿度: ${HUMIDITY}%"
```

### 查询多个城市

```bash
for city in Beijing Shanghai Guangzhou Shenzhen; do
  echo "=== $city ==="
  curl -s "wttr.in/${city}?format=3"
done
```

## 注意事项

- wttr.in 服务偶尔不稳定，如请求失败可重试或切换 OWM 模式
- wttr.in 有请求频率限制，避免高频调用
- OWM 免费版限制 60 次/分钟，足够日常使用
- 城市名建议使用英文，中文拼音也可识别但可能不精确

## 参考文档

- [wttr.in GitHub](https://github.com/chubin/wttr.in)
- [OpenWeatherMap API 文档](https://openweathermap.org/api)
