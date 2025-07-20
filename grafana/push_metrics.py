
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import random
import os

# Grafana Cloud
GATEWAY = "https://prometheus-prod-43-prod-ap-south-1.grafana.net/api/prom/push"
TOKEN = os.getenv("GRAFANA_CLOUD_API_TOKEN")

registry = CollectorRegistry()
Gauge('jmeter_tps', 'Transactions per second', registry=registry).set(random.uniform(50, 150))
Gauge('lrc_sla_percentage', 'LRC SLA %', registry=registry).set(random.uniform(90, 99.9))

push_to_gateway(
    GATEWAY,
    job="perf-monitoring",
    registry=registry,
    handler=lambda url, method, timeout, headers, data: __import__('requests').request(
        method, url, data=data,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/octet-stream"
        },
        timeout=timeout
    )
)
print("✅ Metrics pushed")

import os
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import requests

# Get environment variables
GATEWAY = os.getenv("GRAFANA_CLOUD_METRICS_URL")
TOKEN = os.getenv("GRAFANA_CLOUD_API_KEY")

if not GATEWAY or not TOKEN:
    raise ValueError("Both GRAFANA_CLOUD_METRICS_URL and GRAFANA_CLOUD_API_KEY must be set")

# Correct handler without headers_override
def bearer_auth_handler(url, method, timeout, headers, data):
    headers_dict = {key: value for key, value in headers}
    headers_dict["Authorization"] = f"Bearer {TOKEN}"
    response = requests.request(
        method=method,
        url=url,
        data=data,
        headers=headers_dict,
        timeout=timeout
    )
    response.raise_for_status()

# Create a registry and metric
registry = CollectorRegistry()
g = Gauge('lrc_test_duration_seconds', 'Duration of LRC test run', registry=registry)
g.set(5.2)  # Example value

# Push metrics
push_to_gateway(
    GATEWAY,
    job='lrc_performance_test',
    registry=registry,
    handler=bearer_auth_handler
)
 b8f6f97c0abb98f6b57229ecc2105bda031605ff
