# Red Hat OpenShift Container Platform v4

All yaml snippets below are expected to be **propertly merged** into the main `values.yaml`.

Notes based on OpenShift 4.6.15.

Deploying Datadog will require an [SCC](https://docs.openshift.com/container-platform/4.5/authentication/managing-security-context-constraints.html). Use the snippet below to have our Helm chart [apply it](https://docs.datadoghq.com/integrations/openshift/?tab=helm#configuration).

```yaml
agents:
  podSecurity:
    securityContextConstraints:
      create: true
```

OpenShift 4 uses CRIO-O as its Container Runtime. The default container runtime for Datadog is Docker.  We need to configure the path for the CRI-O socket with the snippet below.

```yaml
datadog:
  criSocketPath: /var/run/crio/crio.sock
```

I currently ignore certificate validation since I could not figure out what is the correct CA<sup>1</sup>.

```yaml
datadog:
  kubelet:
    tlsVerify: false
```

If the OpenShift is running on a supported cloud provider, you should run the agent on the host network. Access to metadata servers from the PODs network is restricted. It will permit the agent to retrieve metadata information about the host from the cloud provier.

```yaml
agents:
  useHostNetwork: true
```

OpenShift comes with its own Kube State Metrics server so there is not need to deploy our own. OpenShift exposes the Kube State Metrics server as a services and we will monitor it using [cluster checks](https://docs.datadoghq.com/agent/cluster_agent/clusterchecks/#static-configurations-in-files) for simplicity.

```yaml
datadog:
  kubeStateMetricsEnabled: false
clusterAgent:
  confd:
    kubernetes_state.yaml: |-
      cluster_check: true
      init_config:
      instances:
        - kube_state_url: https://kube-state-metrics.openshift-monitoring:8443/metrics
          ssl_verify: false
          bearer_token_auth: true
```

<sup>1</sup> The CA below works for master nodes but not for workers.

```yaml
# For later...
    - name: DD_KUBELET_CLIENT_CA
      value: "/etc/kubernetes/kubelet-ca.crt"
```
