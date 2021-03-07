# Datadog integrations

## [Network](https://docs.datadoghq.com/integrations/network/)

If you want to capture the stats from `conntrack -S`, you will need to provide its path.

```yaml
datadog:
  confd:
    network.yaml: |-
      init_config:
      instances:
        - collect_connection_state: false
          conntrack_path: /usr/sbin/conntrack
          use_sudo_conntrack: false
```

The default Datadog agent image does not contain `conntrack`.  We recommend you creating a custom image with it.

```Dockerfile
FROM datadog/agent:latest
RUN apt update && apt install -y conntrack
```

Don't forget to update your values to use the new image.

```yaml
agents:
  image:
    repository: <IMAGE>
    doNotCheckTag: true
    tag: <TAG>
```

In order to properly run it, you will also need to allow some extra capabilities.

```yaml
agents:
  useHostNetwork: true
  containers:
    agent:
      securityContext:
        capabilities:
          add: ["CAP_NET_ADMIN"]
```
