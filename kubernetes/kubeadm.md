# Kubeadm installs

All the yaml snippets below are expected to be **propertly merged** into the main `values.yaml`.

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
