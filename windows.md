# Basic Windows monitoring

## Agent - [datadog.yaml](https://github.com/DataDog/datadog-agent/blob/master/pkg/config/config_template.yaml)

```yaml
api_key: <api_key>
env: <environmen>
apm_config:
    enabled: true
logs_enabled: true
logs_config:
    compression_level: 6
    use_compression: true
    use_http: true
    container_collect_all: true
process_config:
    enabled: true
```

## IIS - [iis.d/conf.yaml](https://github.com/DataDog/integrations-core/blob/master/iis/datadog_checks/iis/data/conf.yaml.example)

Make sure that `ddagentuser` has access to IIS logs.

Datadog agent by default limits the numbers of files it can tail to 100. It is possible to [increase this number](https://docs.datadoghq.com/logs/faq/how-to-increase-the-number-of-log-files-tailed-by-the-agent/). It is recommended to clean up old logs files and adopt a rotation strategy that compresses, or renames, old logs.

```yaml
init_config:
instances:
  - 
logs:
  - type: file
    path: C:\inetpub\logs\LogFiles\*\*.log
    source: iis
```

## IIS logs parser

It assumes all standard fields selected and `x-datadog-trace-id` as a custom field.

<img src="img/iis_logging_fields.jpg" width="400px"/>

IIS outputs a line like the one below at the top of logs files. You can check what fields, and order, is included in your logs.

```text
#Fields: date time s-sitename s-computername s-ip cs-method cs-uri-stem cs-uri-query s-port cs-username c-ip cs-version cs(User-Agent) cs(Cookie) cs(Referer) cs-host sc-status sc-substatus sc-win32-status sc-bytes cs-bytes time-taken trace-id
```

### Parsing rules

```grok
iis.everything %{_date_time} %{_s_sitename} %{_s_computername} %{_s_ip} %{_cs_method} %{_cs_uri_stem} %{_cs_uri_query} %{_s_port} %{_cs_username} %{_c_ip} %{_cs_version} %{_cs_User_Agent} %{_cs_Cookie} %{_cs_Referer} %{_cs_host} %{_sc_status} %{_sc_substatus} %{_sc_win32_status} %{_sc_bytes} %{_cs_bytes} %{_time_taken} %{_trace_id}
```

### Helper rules

Their names are based on field names used by IIS.

```grok
_date_time %{date("yyyy-MM-dd HH:mm:ss"):date_access}
_s_sitename %{notSpace:iis.sitename}
_s_computername %{notSpace:network.server.name}
_s_ip %{ip:network.server.ip}
_cs_method %{word:http.method}
_cs_uri_stem %{notSpace:http.url_details.path}
_cs_uri_query %{notSpace:http.url_details.queryString:querystring}
_s_port %{integer:network.server.port}
_cs_username %{notSpace:user.name:nullIf("-")}
_c_ip %{ip:network.client.ip}
_cs_version %{notSpace:http.version}
_cs_User_Agent %{notSpace:http.useragent:decodeuricomponent}
_cs_Cookie %{notSpace:http.cookie:querystring}
_cs_Referer %{notSpace:http.referer:nullIf("-")}
_cs_host %{notSpace:http.url_details.authority}
_sc_status %{integer:http.status_code}
_sc_substatus %{integer:http.sub_status_code}
_sc_win32_status %{integer:iis.win32_status}
_sc_bytes %{integer:network.bytes_written}
_cs_bytes %{integer:network.bytes_read}
_time_taken %{integer:duration:scale(1000000)}
_trace_id %{notSpace:datadog.trace_id:nullIf("-")}
```

## MS SQLServer - [sqlserver.d/conf.yaml](https://github.com/DataDog/integrations-core/blob/master/sqlserver/datadog_checks/sqlserver/data/conf.yaml.example)

```yaml
init_config:
instances:
  - host: localhost,1433
    username: datadog
    password: <password>
    # # Required if TLS 1.0 conenctions are disabled on the server
    # # It is characterized by SECDoClientHandshake() error
    # connector: odbc
    # driver: ODBC Driver 17 for SQL Server
```

## Windows events - [win32_event_log.d/conf.yaml](https://github.com/DataDog/integrations-core/blob/master/win32_event_log/datadog_checks/win32_event_log/data/conf.yaml.example)

You can check exinting channels at C:\windows\System32\Winevt\Logs\

```yaml
instances:
  - path: Security
    legacy_mode: false
```

## Performance Counters - [pdh_check.d/conf.yaml](https://github.com/DataDog/integrations-core/blob/master/pdh_check/datadog_checks/pdh_check/data/conf.yaml.example)

Counter names are **CASE SENSITIVE**.

```yaml
init_config:
instances:
  - countersetname: Processor Information
    metrics:
      - ['% Privileged Time', pdh.processor_information.privileged_time, gauge]
```
