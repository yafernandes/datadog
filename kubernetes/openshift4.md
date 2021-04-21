# Red Hat OpenShift Container Platform v4

All yaml snippets below are expected to be **propertly merged** into the main `values.yaml`.

Notes based on:

- OpenShift 4.7.6
- Agent 7.27.0
- Cluster Agent 1.11.0

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

Openshift kubelet [requires clients to authenticate](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet-tls-bootstrapping/#client-and-serving-certificates) with a certificate. It can be achieved with the snippet below.

```yaml
datadog:
  kubelet:
    hostCAPath: /etc/kubernetes/kubelet-ca.crt
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

## Control Plane

OpenShift uses the same image for different components of the Control Plane. Datadog's default Control Plane monitoring uses image names to detect services, which presents a challenge here. It might be possible to update OpenShift's Control Plane deployment to include [Autodiscovery annotations](https://docs.datadoghq.com/agent/kubernetes/integrations/?tab=kubernetes#configuration) to automatically detect and start monitoring control plane services. However, many organizations do not want to change their Control Plane deployment.
OpenShift exposes the Kubernetes API as a service we can monitor using [cluster checks](https://docs.datadoghq.com/agent/cluster_agent/clusterchecks/#static-configurations-in-files) for simplicity.

```yaml
clusterAgent:
  confd:
    etcd.yaml: |-
      cluster_check: true
      init_config:
      instances:
        - use_preview: true
          prometheus_url: https://metrics.openshift-etcd-operator/metrics
          ssl_verify: false
          bearer_token_auth: true
    kube_controller_manager.yaml: |-
      cluster_check: true
      init_config:
      instances:
        - prometheus_url: https://kube-controller-manager.openshift-kube-controller-manager/metrics
          ssl_verify: false
          bearer_token_auth: true
          leader_election: false
    kube_scheduler.yaml: |-
      cluster_check: true
      init_config:
      instances:
        - prometheus_url: https://scheduler.openshift-kube-scheduler/metrics
          ssl_verify: false
          bearer_token_auth: true
    kube_apiserver_metrics.yaml: |-
      cluster_check: true
      init_config:
      instances:
        - prometheus_url: https://apiserver.openshift-kube-apiserver/metrics
          ssl_verify: false
          bearer_token_auth: true
    coredns.yaml: |-
      cluster_check: true
      init_config:
      instances:
        - prometheus_url: https://dns-default.openshift-dns:9154/metrics
          ssl_verify: false
          bearer_token_auth: true
```
