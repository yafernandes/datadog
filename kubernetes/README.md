# Kubernetes basic  monitoring

Notes based on:

- Kubernetes 1.21.0
- Helm Chart 2.12.3
- Agent 7.27.0
- Cluster Agent 1.12.0

## Install

Install [Datadog Helm Chart](https://github.com/DataDog/helm-charts/tree/master/charts/datadog)

```bash
helm repo add datadog https://helm.datadoghq.com
helm repo update
```

Create a namespace for Datadog

```bash
kubectl create ns datadog
```

Create a secret with the [API key](https://app.datadoghq.com/account/settings#api).

```bash
kubectl create secret generic datadog-keys -n datadog --from-literal=api-key=<API-KEY>
```

Create the `values.yaml` file.

```yaml
datadog:
  clusterName: <CLUSTER-NAME>
  apiKeyExistingSecret: datadog-keys
  apm:
    enabled: true
  logs:
    enabled: true
    containerCollectAll: true
  processAgent:
    processCollection: true
  networkMonitoring:
    enabled: true
  dogstatsd:
    useHostPort: true
  kubeStateMetricsCore:
    enabled: true
  kubeStateMetricsEnabled: false
agents:
  # This toleration allows the agent to be deployed to every node. Usually not required for managed clusters.
  tolerations:
    - operator: Exists
```

All yaml snippets presented from here are expected to be **propertly merged** into the main `values.yaml`.

Check distribution specific notes.  

- [kubeadm/vanilla](kubeadm.md)
- [AKS](aks.md)
- [Red Hat OpenShift Container Platform v4](openshift4.md)

 Deploy with the command below.

```bash
helm install datadog datadog/datadog -n datadog -f values.yaml
```

Complete values file examples can be found [here](examples).

**Note**: OpenShift [metrics](https://docs.datadoghq.com/integrations/openshift/#metrics) are all about quotas.  The statment below must return something for OpenShift specific metrics to show up.

`oc get clusterresourcequotas --all-namespaces`
