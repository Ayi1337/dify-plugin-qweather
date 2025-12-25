# Plugin QWeather Tool para Dify

**Autor**: [Ayi1337](https://github.com/Ayi1337)  
**Repositório**: [dify-plugin-qweather](https://github.com/Ayi1337/dify-plugin-qweather)

[English Documentation](https://github.com/Ayi1337/dify-plugin-qweather/blob/main/README.md) | [中文文档](https://github.com/Ayi1337/dify-plugin-qweather/blob/main/readme/README_zh_Hans.md) | [日本語ドキュメント](https://github.com/Ayi1337/dify-plugin-qweather/blob/main/readme/README_ja_JP.md)

Um **Plugin de Ferramenta** do Dify que fornece um conjunto selecionado de ferramentas para chamar APIs do **QWeather (和风天气)**, permitindo que você busque dados meteorológicos e de localização no Chatflow / Workflow / Agent.

Este plugin foi projetado como um wrapper fino em torno das APIs oficiais do QWeather: ele encaminha solicitações ao QWeather e retorna a resposta **como está**.

---

## Visão Geral

- **Tipo de plugin**: Plugin de Ferramenta (Python)
- **Ferramentas incluídas**: 20 (Clima / GeoAPI / Minuto a Minuto / Índices / Astronomia / Alertas / Qualidade do Ar)
- **Saída**:
  - `json`: a resposta JSON original do QWeather
  - `text`: o mesmo conteúdo que `json` (string JSON formatada)
  - `files`: não utilizado
- **Código de resposta do QWeather**: `code=204` significa "sucesso mas sem dados", e é tratado como sucesso (retornado sem gerar exceção).

> O Dify atualmente não suporta menus de ferramentas multi-nível. Este plugin usa prefixos de rótulo de ferramenta como `Weather -` / `GeoAPI -` para agrupamento leve.

---

## Configuração (Credenciais do Provedor)

No Dify, após instalar o plugin, configure as credenciais do provedor:

- `qweather_api_key` (obrigatório): sua Chave de API do QWeather
- `qweather_base_url` (obrigatório): seu **Host da API QWeather** (por exemplo, `https://xxxxxx.qweatherapi.com`)

Onde encontrar o **Host da API**:
- Console do QWeather → Configurações: https://console.qweather.com/setting

Notas:
- **Todos os endpoints neste plugin usam o Host da API** (`qweather_base_url`). Não há fallback para `devapi.qweather.com` / `geoapi.qweather.com`.
- Você pode inserir sem o esquema; o plugin irá normalizá-lo para `https://...` e remover a `/` final.

---

## Ferramentas

### GeoAPI

#### **Busca de Cidade** (`qweather_geo_city_lookup`)
- **Descrição**: Busca de cidade e geocodificação reversa, suporta multi-idiomas e busca aproximada
- **Endpoint**: `/geo/v2/city/lookup`
- **Parâmetros**:
  - `location` (obrigatório): Palavra-chave de localização, coordenadas, LocationID ou Adcode
  - `adm` (opcional): Filtro de divisões administrativas superiores
  - `range` (opcional): Buscar dentro de país/região (código ISO 3166)
  - `number` (opcional): Número de resultados (1-20, padrão 10)
  - `lang` (opcional): Idioma da resposta

#### **Cidade Principal** (`qweather_geo_top_city`)
- **Descrição**: Obter uma lista de cidades populares ao redor do mundo
- **Endpoint**: `/geo/v2/city/top`
- **Parâmetros**:
  - `range` (opcional): País/região (código ISO 3166)
  - `number` (opcional): Número de resultados (1-20, padrão 10)
  - `lang` (opcional): Idioma da resposta

#### **Busca de POI** (`qweather_geo_poi_lookup`)
- **Descrição**: Pesquisar informações de POI (pontos turísticos, estações de maré, etc.) usando palavras-chave e coordenadas
- **Endpoint**: `/geo/v2/poi/lookup`
- **Parâmetros**:
  - `type` (obrigatório): Tipo de POI (`scenic` ou `TSTA`)
  - `location` (obrigatório): Palavra-chave de localização, coordenadas, LocationID ou Adcode
  - `city` (opcional): Buscar dentro de uma cidade específica
  - `number` (opcional): Número de resultados (1-20, padrão 10)
  - `lang` (opcional): Idioma da resposta

#### **Alcance de POI** (`qweather_geo_poi_range`)
- **Descrição**: Consultar informações de POI dentro de uma área especificada
- **Endpoint**: `/geo/v2/poi/range`
- **Parâmetros**:
  - `type` (obrigatório): Tipo de POI (`scenic` ou `TSTA`)
  - `location` (obrigatório): Coordenadas (longitude,latitude)
  - `radius` (opcional): Raio de busca em quilômetros (1-50, padrão 5)
  - `number` (opcional): Número de resultados (1-20, padrão 10)
  - `lang` (opcional): Idioma da resposta

---

### Clima (Cidade)

#### **Clima em Tempo Real** (`qweather_weather_now`)
- **Descrição**: Obter dados meteorológicos em tempo real para uma cidade ou coordenada
- **Endpoint**: `/v7/weather/now`
- **Parâmetros**:
  - `location` (obrigatório): LocationID ou coordenadas
  - `lang` (opcional): Idioma da resposta
  - `unit` (opcional): Sistema de unidade (`m` para métrico, `i` para imperial)

#### **Previsão Diária do Tempo** (`qweather_weather_daily_forecast`)
- **Descrição**: Previsão diária do tempo para os próximos 3-30 dias
- **Endpoint**: `/v7/weather/{days}`
- **Dias Disponíveis**: 3d, 7d, 10d, 15d, 30d
- **Parâmetros**:
  - `days` (obrigatório): Dias de previsão (3d/7d/10d/15d/30d)
  - `location` (obrigatório): LocationID ou coordenadas
  - `lang` (opcional): Idioma da resposta
  - `unit` (opcional): Sistema de unidade (`m` para métrico, `i` para imperial)

#### **Previsão Horária do Tempo** (`qweather_weather_hourly_forecast`)
- **Descrição**: Previsão horária do tempo para as próximas 24-168 horas
- **Endpoint**: `/v7/weather/{hours}`
- **Horas Disponíveis**: 24h, 72h, 168h
- **Parâmetros**:
  - `hours` (obrigatório): Horas de previsão (24h/72h/168h)
  - `location` (obrigatório): LocationID ou coordenadas
  - `lang` (opcional): Idioma da resposta
  - `unit` (opcional): Sistema de unidade (`m` para métrico, `i` para imperial)

---

### Clima (Grade)

#### **Clima de Grade em Tempo Real** (`qweather_grid_weather_now`)
- **Descrição**: Clima baseado em grade em tempo real para coordenadas (resolução 3-5km)
- **Endpoint**: `/v7/grid-weather/now`
- **Parâmetros**:
  - `location` (obrigatório): Coordenadas (longitude,latitude)
  - `lang` (opcional): Idioma da resposta
  - `unit` (opcional): Sistema de unidade (`m` para métrico, `i` para imperial)

#### **Previsão Diária do Clima de Grade** (`qweather_grid_weather_daily_forecast`)
- **Descrição**: Previsão diária do clima de grade para os próximos 3-7 dias (resolução 3-5km)
- **Endpoint**: `/v7/grid-weather/{days}`
- **Dias Disponíveis**: 3d, 7d
- **Parâmetros**:
  - `days` (obrigatório): Dias de previsão (3d/7d)
  - `location` (obrigatório): Coordenadas (longitude,latitude)
  - `lang` (opcional): Idioma da resposta
  - `unit` (opcional): Sistema de unidade (`m` para métrico, `i` para imperial)

#### **Previsão Horária do Clima de Grade** (`qweather_grid_weather_hourly_forecast`)
- **Descrição**: Previsão horária do clima de grade para as próximas 24-72 horas (resolução 3-5km)
- **Endpoint**: `/v7/grid-weather/{hours}`
- **Horas Disponíveis**: 24h, 72h
- **Parâmetros**:
  - `hours` (obrigatório): Horas de previsão (24h/72h)
  - `location` (obrigatório): Coordenadas (longitude,latitude)
  - `lang` (opcional): Idioma da resposta
  - `unit` (opcional): Sistema de unidade (`m` para métrico, `i` para imperial)

---

### Previsão Minutária

#### **Precipitação Minutária** (`qweather_minutely_precipitation`)
- **Descrição**: Previsão de precipitação a cada 5 minutos para as próximas 2 horas (somente China)
- **Endpoint**: `/v7/minutely/5m`
- **Parâmetros**:
  - `location` (obrigatório): Coordenadas (longitude,latitude)
  - `lang` (opcional): Idioma da resposta

---

### Índices Meteorológicos

#### **Previsão de Índices Meteorológicos** (`qweather_indices_forecast`)
- **Descrição**: Obter dados de previsão de índices de estilo de vida meteorológicos para cidades na China e em todo o mundo
- **Endpoint**: `/v7/indices/{days}`
- **Dias Disponíveis**: 1d, 3d
- **Parâmetros**:
  - `days` (obrigatório): Dias de previsão (1d/3d)
  - `type` (obrigatório): IDs de tipo de índices meteorológicos (separados por vírgula)
  - `location` (obrigatório): LocationID ou coordenadas
  - `lang` (opcional): Idioma da resposta

---

### Astronomia

#### **Nascer e Pôr do Sol** (`qweather_astronomy_sun`)
- **Descrição**: Obter horários de nascer e pôr do sol para os próximos 60 dias em qualquer local do mundo
- **Endpoint**: `/v7/astronomy/sun`
- **Parâmetros**:
  - `location` (obrigatório): LocationID ou coordenadas
  - `date` (obrigatório): Data no formato aaaammdd (até 60 dias)

#### **Nascer e Pôr da Lua e Fase Lunar** (`qweather_astronomy_moon`)
- **Descrição**: Obter nascer da lua, pôr da lua e dados de fase lunar a cada hora para os próximos 60 dias
- **Endpoint**: `/v7/astronomy/moon`
- **Parâmetros**:
  - `location` (obrigatório): LocationID ou coordenadas
  - `date` (obrigatório): Data no formato aaaammdd (até 60 dias)
  - `lang` (opcional): Idioma da resposta

#### **Ângulo de Elevação Solar** (`qweather_astronomy_solar_elevation_angle`)
- **Descrição**: Obter ângulo de elevação solar global e azimute em qualquer ponto no tempo
- **Endpoint**: `/v7/astronomy/solar-elevation-angle`
- **Parâmetros**:
  - `location` (obrigatório): Coordenadas (longitude,latitude)
  - `date` (obrigatório): Data no formato aaaammdd
  - `time` (obrigatório): Hora no formato HHmm (24 horas)
  - `tz` (obrigatório): Fuso horário (por exemplo, 0800 ou -0530)
  - `alt` (obrigatório): Altitude em metros

---

### Alertas

#### **Alerta Meteorológico** (`qweather_weather_alert_current`)
- **Descrição**: Obter alertas meteorológicos severos em tempo real emitidos oficialmente por coordenadas
- **Endpoint**: `/weatheralert/v1/current/{lat}/{lon}`
- **Parâmetros**:
  - `latitude` (obrigatório): Latitude (decimal, até 2 casas decimais)
  - `longitude` (obrigatório): Longitude (decimal, até 2 casas decimais)
  - `localTime` (opcional): Retornar hora local (true) ou hora UTC (false, padrão)
  - `lang` (opcional): Idioma da resposta

---

### Qualidade do Ar

#### **Qualidade do Ar Atual** (`qweather_air_quality_current`)
- **Descrição**: Qualidade do ar atual (IQA) por coordenadas
- **Endpoint**: `/airquality/v1/current/{lat}/{lon}`
- **Parâmetros**:
  - `latitude` (obrigatório): Latitude (decimal, até 2 casas decimais)
  - `longitude` (obrigatório): Longitude (decimal, até 2 casas decimais)
  - `lang` (opcional): Idioma da resposta

#### **Previsão Horária da Qualidade do Ar** (`qweather_air_quality_hourly_forecast`)
- **Descrição**: Previsão horária da qualidade do ar para as próximas 24 horas
- **Endpoint**: `/airquality/v1/hourly/{lat}/{lon}`
- **Parâmetros**:
  - `latitude` (obrigatório): Latitude (decimal, até 2 casas decimais)
  - `longitude` (obrigatório): Longitude (decimal, até 2 casas decimais)
  - `localTime` (opcional): Retornar hora local (true) ou hora UTC (false, padrão)
  - `lang` (opcional): Idioma da resposta

#### **Previsão Diária da Qualidade do Ar** (`qweather_air_quality_daily_forecast`)
- **Descrição**: Previsão diária da qualidade do ar para os próximos 3 dias
- **Endpoint**: `/airquality/v1/daily/{lat}/{lon}`
- **Parâmetros**:
  - `latitude` (obrigatório): Latitude (decimal, até 2 casas decimais)
  - `longitude` (obrigatório): Longitude (decimal, até 2 casas decimais)
  - `localTime` (opcional): Retornar hora local (true) ou hora UTC (false, padrão)
  - `lang` (opcional): Idioma da resposta

#### **Dados da Estação de Monitoramento** (`qweather_air_quality_station`)
- **Descrição**: Obter valores de concentração de poluentes das estações de monitoramento da qualidade do ar
- **Endpoint**: `/airquality/v1/station/{LocationID}`
- **Parâmetros**:
  - `location_id` (obrigatório): LocationID da estação de monitoramento
  - `lang` (opcional): Idioma da resposta

---

## Solução de Problemas

1. **Instalado mas sem ações / `plugin runtime not found`**
   - O Debug Remoto requer que o processo do plugin local esteja rodando continuamente (`.venv/bin/python main.py`).
   - Certifique-se de que `.env` corresponde aos valores mais recentes da página de debug do Dify (host/port/key).

2. **Reinício do Dify alterou a Chave de Debug**
   - Atualize `.env` (`REMOTE_INSTALL_KEY`, e host/port se alterados).
   - Reinicie o processo do plugin local, depois reinstale/atualize o plugin no Dify.

3. **Falha na validação de credenciais**
   - Certifique-se de que `qweather_base_url` é o seu **Host da API** (`*.qweatherapi.com`) de https://console.qweather.com/setting.

---

## Privacidade

O plugin em si não armazena dados do usuário. Ele envia solicitações ao QWeather e retorna respostas.

Veja `PRIVACY.md` para detalhes.

---

## Contribuindo

PRs e issues são bem-vindos. Ao adicionar uma nova ferramenta:

1. Adicione `tools/<name>.py` (Implementação da ferramenta)
2. Adicione `tools/<name>.yaml` (Esquema da ferramenta: label/description/parameters)
3. Registre o YAML em `qweather.yaml`
4. Retorne saídas como `json` + `text` (JSON em string)

---

## Suporte / Referências

- Documentação do Plugin de Ferramenta Dify: https://docs.dify.ai/en/develop-plugin/dev-guides-and-walkthroughs/tool-plugin
- Site de documentação do QWeather: https://dev.qweather.com/
- Repositório de documentação do QWeather: https://github.com/qwd/dev-site
- Console do QWeather (Host da API): https://console.qweather.com/setting

---

## Instalação (Para Desenvolvedores)

> **Nota**: Esta seção é apenas para desenvolvedores de plugins. Usuários regulares podem instalar o plugin diretamente do Marketplace do Dify e não precisam seguir estas etapas.

### Debug Remoto (recomendado para desenvolvimento)

1. Copie `.env.example` para `.env`
2. Preencha os valores da página "Plugin Debug" (Debug Remoto) do Dify
3. Inicie o processo do plugin (mantenha-o rodando):

```bash
source .venv/bin/activate
set -a
source .env
set +a
.venv/bin/python main.py
```

### Empacotamento (para upload)

```bash
dify plugin package .
```

---

## Licença

MIT


