# AKS - Azure Kubernetes Service

All the yaml snippets below are expected to be **propertly merged** into the main `values.yaml`.

Notes based on AKS 1.19.6.

Recently [AKS adopted containerd](https://docs.microsoft.com/en-us/azure/aks/cluster-configuration?utm_source=thenewstack&utm_medium=website&utm_campaign=platform#container-runtime-configuration) as its default container runtime. The default container runtime for Datadog is Docker.  We need to configure the path for the containerd socket with the snippet below.

```yaml
datadog:
  criSocketPath: /var/run/containerd/containerd.sock
```

AKS kubelet [requires clients to authenticate](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet-tls-bootstrapping/#client-and-serving-certificates) with a certificate. We need to mount it and set it with the snippet below.

```yaml
datadog:
  env:
    - name: DD_KUBELET_CLIENT_CA
      value: "/host/etc/kubernetes/certs/kubeletserver.crt"
agents:
  volumeMounts:
    - mountPath: /host/etc/kubernetes/certs
      name: kubernetes-certs
  volumes:
    - name: kubernetes-certs
      hostPath:
        path: /etc/kubernetes/certs
        type: DirectoryOrCreate
```

AKS certificate requires us to connect to the kubelet using the node name, instead of just its ip address. It can be achiece with the snippet below.

```yaml
datadog:
  env:
    - name: DD_KUBERNETES_KUBELET_HOST
      valueFrom:
        fieldRef:
          fieldPath: spec.nodeName
```

## Control Plane

PassS services like AKS do not give us access to control plane nodes. Since we cannot deploy agents to control plane nodes, we cannot leverage [Auto Discovery](https://docs.datadoghq.com/agent/kubernetes/integrations/?tab=kubernetes) to automatically detect and start monitoring control plane services.
AKS exposes Kubernetes API and CoreDNS as services ans we will monitor them using [cluster checks](https://docs.datadoghq.com/agent/cluster_agent/clusterchecks/#static-configurations-in-files) for simplicity.

```yaml
clusterAgent:
  confd:
    kube_apiserver_metrics.yaml: |-
      cluster_check: true
      init_config:
      instances:
        - prometheus_url: https://kubernetes.default/metrics
          ssl_ca_cert: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
          bearer_token_auth: true
    coredns.yaml: |-
      cluster_check: true
      init_config:
      instances:
        - prometheus_url: http://dns-default.openshift-dns:9153/metrics
```
