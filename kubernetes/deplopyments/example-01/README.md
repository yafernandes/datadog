
* Environment
  * Agent 7.16.1
  * Kubernetes 1.16.6
* **Infra is not a priority here.  Multiple metrics missing.**
* Not mounting:
  * `/var/run/docker.sock`
  * `/host/proc`
  * `/host/sys/fs/cgroup`
  * `/var/run/s6`
* Namespaced RBAC (No ClusterRole)
* Proxy setup
* Log compression
* Disk integration disabled.
  * Error `FileNotFoundError: [Errno 2] No such file or directory: '/host/proc/filesystems'`
* Kubernetes API Server integrations disabled.
  * Error `403 Client Error: Forbidden for url: https://10.0.1.64:6443/metrics`
* etcd integrations disabled.
  * Error `could not invoke 'etcd' python check constructor.`
