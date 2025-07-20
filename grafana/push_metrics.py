import os
import random
import requests
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

# Get environment variables
GATEWAY = os.getenv("GRAFANA_CLOUD_METRICS_URL")
TOKEN = os.getenv("GRAFANA_CLOUD_API_KEY")

if not GATEWAY or not TOKEN:
    raise ValueError("Both GRAFANA_CLOUD_METRICS_URL and GRAFANA_CLOUD_API_KEY must be set")

# Handler with Bearer token auth
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

# Create registry and metrics
registry = CollectorRegistry()
Gauge('jmeter_tps', 'Transactions per second', registry=registry).set(random.uniform(50, 150))
Gauge('lrc_sla_percentage', 'LRC SLA %', registry=registry).set(random.uniform(90, 99.9))
Gauge('lrc_test_duration_seconds', 'Duration of LRC test run', registry=registry).set(5.2)  # Static example

# Push metrics
push_to_gateway(
    GATEWAY,
    job='lrc_performance_test',
    registry=registry,
    handler=bearer_auth_handler
)

print("✅ Metrics pushed to Grafana Cloud")
