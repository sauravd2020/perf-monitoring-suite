import os
import random
import requests
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

# Load environment variables
metrics_url = os.environ.get("GRAFANA_CLOUD_METRICS_URL")
api_key = os.environ.get("GRAFANA_CLOUD_API_KEY")

# Prepare registry and custom metrics
registry = CollectorRegistry()
tps = Gauge('jmeter_tps', 'Transactions per second from JMeter', registry=registry)
sla = Gauge('lrc_sla_percentage', 'LRC SLA success percentage', registry=registry)
response_time = Gauge('lrc_response_time_ms', 'Average response time in ms', registry=registry)

# Generate dummy values for demo
tps.set(random.uniform(10, 100))
sla.set(random.uniform(90, 100))
response_time.set(random.uniform(200, 800))

# Push metrics
print("Pushing metrics to:", metrics_url)
push_to_gateway(
    gateway=metrics_url,
    job='perf-monitoring',
    registry=registry,
    handler=lambda url, method, timeout, headers, data: requests.request(
        method, url, data=data, headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/x-www-form-urlencoded"
        }, timeout=timeout)
)
