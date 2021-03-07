FROM datadog/agent:latest
# https://docs.datadoghq.com/developers/guide/custom-python-package/?tab=linux
RUN /opt/datadog-agent/embedded/bin/pip install boto3 uritools
COPY secret-management.py /
RUN chmod 0500 /secret-management.py
