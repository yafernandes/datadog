# Personal notes

## Labs

### [Python application](https://github.com/yafernandes/app-python)

### [Kafka client](https://github.com/yafernandes/kafka-client)

### [Java instrumented logs](https://github.com/yafernandes/instrumented-logs)

## Information Scrubbing

[Logs](https://docs.datadoghq.com/agent/logs/advanced_log_collection/?tab=exclude_at_match#scrub-sensitive-data-from-your-logs)

[Process](https://docs.datadoghq.com/infrastructure/process/?tab=linuxwindows#process-arguments-scrubbing)

[APM](https://docs.datadoghq.com/security/tracing/#filtering-baseline)

[Profiler](https://docs.datadoghq.com/tracing/profiler/profiler_troubleshooting/#removing-sensitive-information-from-profiles)

[RUM](https://docs.datadoghq.com/real_user_monitoring/browser/advanced_configuration/?tab=npm#scrub-sensitive-data-from-your-rum-data)

## Connectivity

[The forwarder](https://docs.datadoghq.com/agent/basic_agent_usage/?tab=agentv6v7#forwarder)

[File tailing](https://docs.datadoghq.com/logs/faq/log-collection-is-the-datadog-agent-losing-logs/#file-tailing)

[datadog.yaml](https://github.com/DataDog/datadog-agent/blob/master/pkg/config/config_template.yaml#L166-L171)

## Log processing

[Latency](https://docs.datadoghq.com/agent/logs/log_transport/?tab=https#configure-the-batch-wait-time)

[OOB log parsers](https://app.datadoghq.com/logs/pipelines/pipeline/library)

[Limits applied to ingested log events](https://docs.datadoghq.com/logs/log_collection/?tab=host#custom-log-forwarding)

- For optimal use, Datadog recommends a log event should not exceed 25K bytes in size. When using the Datadog Agent, log events greater than 256KB are split into several entries. When using the Datadog TCP or HTTP API directly, log events up to 1MB are accepted.
- A log event should not have more than 100 tags, and each tag should not exceed 256 characters for a maximum of 10 million unique tags per day.
- A log event converted to JSON format should contain less than 256 attributes. Each of those attribute’s keys should be less than 50 characters, nested in less than 10 successive levels, and their respective value should be less than 1024 characters if promoted as a facet.
- Log events can be submitted up to 18h in the past and 2h in the future.

## Masking

Removing log color codes

```javascript
{
  "type": "mask_sequences",
  "name": "remove_log_color_codes",
  "replace_placeholder": "",
  "pattern" : "(\\x1B\\[[\\d;]*[JKmsu])"
}
```

## Misc

After a certain period of time metrics, tags, and hosts no longer appear in the Datadog UI.

- [Datadog docs](https://docs.datadoghq.com/graphing/faq/historical-data)
