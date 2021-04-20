# Kubeadm installs

All the yaml snippets below are expected to be **propertly merged** into the main `values.yaml`.

Notes based on:

- Kubernetes 1.21
- Agent 7.27.0
- Cluster Agent 1.11.0

Recently [Kubernetes deprecated Docker/Dockershim](https://kubernetes.io/blog/2020/12/02/dockershim-faq/). The default container runtime for Datadog Helm chart is Docker.  If using containerd as Container Runtime, we need to configure the path for the containerd socket with the snippet below.

```yaml
datadog:
  criSocketPath: /var/run/containerd/containerd.sock
```

## etcd - [etcd.d/conf.yaml](https://github.com/DataDog/integrations-core/blob/master/etcd/datadog_checks/etcd/data/conf.yaml.example)

Kubernetes etcd requires PKI certificates for authetication over TLS. The snippet below mounts the necessary certificate location and override the default config. It also assumes that the agent is being scheduled onto etcd nodes.

```yaml
datadog:
  env:
    - name: DD_IGNORE_AUTOCONF
      value: "etcd"
  confd:
    etcd.yaml: |-
      ad_identifiers:
        - etcd
      init_config:
      instances:
        - prometheus_url: https://%%host%%:2379/metrics
          ssl_ca_cert: /host/etc/kubernetes/pki/etcd/ca.crt
          ssl_cert: /host/etc/kubernetes/pki/etcd/peer.crt
          ssl_private_key: /host/etc/kubernetes/pki/etcd/peer.key
agents:
  volumeMounts:
    - mountPath: /host/etc/kubernetes/pki/etcd
      name: etcd-certs
  volumes:
    - name: etcd-certs
      hostPath:
        path: /etc/kubernetes/pki/etcd
        type: DirectoryOrCreate
```
