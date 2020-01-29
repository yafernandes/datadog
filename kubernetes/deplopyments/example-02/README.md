
* Environment
  * Agent 7.16.1
  * Kubernetes 1.16.6
  * Helm 3.0.2
  * Datadog Chart 1.39.5
* Deploy with `helm install datadog stable/datadog -f datadog-values.yaml`
* etcd v3 configured
* Kubernetes controller integration enabled
* Kuerbetes scheduler integration enabled
* NGINX ingress controller integration enabled as a cluster check
* Sample APM obfuscation example included
* Includes broad toleration
