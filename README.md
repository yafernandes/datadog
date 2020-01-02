# Information Scrubbing
[Logs](https://docs.datadoghq.com/agent/logs/advanced_log_collection/?tab=exclude_at_match#scrub-sensitive-data-from-your-logs)

[Process](https://docs.datadoghq.com/graphing/infrastructure/process/?tab=linuxwindows#process-arguments-scrubbing)

[APM](https://docs.datadoghq.com/security/tracing/#filtering-baseline)

# OpenShift
OpenShift [metrics](https://docs.datadoghq.com/integrations/openshift/#metrics) are all around quotes.  The statment below must return something for metrics to show up.

`oc get clusterresourcequotas --all-namespaces`

# Log processing

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

# Helm

Check local version of Datadog chart on Helm

`helm search repo Datadog`

[Latest updates](https://github.com/helm/charts/commits/master/stable/datadog/Chart.yaml)


# Misc

Enable/Disable specific AWS integrations/resources on Datadog
https://gist.github.com/DanielLanger/c04c2d79ef97c1d242e19781250d428d



After a certain period of time metrics, tags, and hosts no longer appear in the Datadog UI.
https://docs.datadoghq.com/graphing/faq/historical-data


Token for login to Kubernetes Dashboard

`kubectl get secret -o json -A | jq '.items[] | select(.type == "kubernetes.io/service-account-token") | select(.metadata.name | contains("kubernetes-dashboard")) | .data.token' -r | base64 -d | pbcopy`