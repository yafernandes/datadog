# [Secrets Management](https://docs.datadoghq.com/agent/guide/secrets-management/?tab=linux)

## Implementation example

This Python code is an implementation example of a secret backend. It expects URIs as secret handles. It supports a custom [kms](#kms-scheme) scheme and the standard [file](https://en.wikipedia.org/wiki/File_URI_scheme) scheme.

### kms scheme

It has the format `ksm://<AWS_REGION>/<SECRET_NAME>#<SECRET_KEY>`.

### Hashicorp Vault

Vault can be easily integrated in Kubernetes environments [Injecting Vault Secrets Into Kubernetes Pods via a Sidecar](https://www.hashicorp.com/blog/injecting-vault-secrets-into-kubernetes-pods-via-a-sidecar) and then referencing them using the [file](https://en.wikipedia.org/wiki/File_URI_scheme) scheme.

## Datadog agent images

This example can be easily added to a custom image using this [Dockerfile](Dockerfile) example.