import os
import random
import requests
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

# Load Grafana Cloud config
GATEWAY = os.getenv("GRAFANA_CLOUD_METRICS_URL")
TOKEN = os.getenv("GRAFANA_CLOUD_API_KEY")

if not GATEWAY or not TOKEN:
    raise ValueError("Both GRAFANA_CLOUD_METRICS_URL and GRAFANA_CLOUD_API_KEY must be set")

# Authentication handler for Bearer token
def bearer_auth_handler(url, method, timeout, headers, data):
    headers_dict = dict(headers)
    headers_dict["Authorization"] = f"Bearer {TOKEN}"
    response = requests.request(
        method=method,
        url=url,
        data=data,
        headers=headers_dict,
        timeout=timeout
    )
    response.raise_for_status()

# Create metrics
registry = CollectorRegistry()
Gauge('jmeter_tps', 'Transactions per second', registry=registry).set(random.uniform(50, 150))
Gauge('lrc_sla_percentage', 'LRC SLA %', registry=registry).set(random.uniform(90, 99.9))
Gauge('lrc_test_duration_seconds', 'LRC test duration in seconds', registry=registry).set(random.uniform(3, 10))

# Push to Grafana Cloud
push_to_gateway(
    GATEWAY,
    job="perf-monitoring",
    registry=registry,
    handler=bearer_auth_handler
)

print("✅ Metrics pushed successfully")
