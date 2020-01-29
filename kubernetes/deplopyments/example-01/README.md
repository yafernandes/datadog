* Not mounting:
  * `/var/run/docker.sock`
  * `/host/proc`
  * `/host/sys/fs/cgroup`
  * `/var/run/s6`
* Proxy setup
* Log compression
* Namespaced RBAC (No ClusterRole)
* **Infra is not a priority.  Multiple metrics missing.*
* Disk integration disabled.
  * Disk integration was causing error `FileNotFoundError: [Errno 2] No such file or directory: '/host/proc/filesystems'`