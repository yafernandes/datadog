# Kubernetes basic  monitoring

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
  env:
    - name: DD_ENV
      value: <ENVIRONMENT>
agents:
  # This toleartion allows the agent to be deployed to every node.
  tolerations:
    - operator: Exists
```

Check distribution specific notes:

- [kubeadm/vanilla](kubeadm.md)
- [AKS](aks.md)

 Deploy with the command below.

```bash
helm install datadog datadog/datadog -n datadog -f values.yaml
```