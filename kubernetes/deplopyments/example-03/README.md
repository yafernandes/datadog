
Example of Config Map with Datadog configuration

### Usage
```
volumeMounts:
    - name: dd-confd
      mountPath: /conf.d
```
```
volumes:
- name: dd-confd
    configMap:
    name: dd-agent-confd
```