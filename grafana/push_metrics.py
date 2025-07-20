import os
import requests
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

# Get environment variables
metrics_url = os.environ["GRAFANA_CLOUD_METRICS_URL"]
api_key = os.environ["GRAFANA_CLOUD_API_KEY"]

print("Pushing metrics to:", metrics_url)

# Create Prometheus registry and metric
registry = CollectorRegistry()
g = Gauge('sample_lrc_test_latency_seconds', 'LRC latency in seconds', registry=registry)
g.set(1.23)  # Example value

# Define a valid HTTP handler
def bearer_auth_handler(url, method, timeout, headers, data):
    str_headers = {
        key: str(value)  # Convert everything to string to avoid ValueError
        for key, value in headers
    }
    str_headers["Authorization"] = f"Bearer {api_key}"
    return lambda: requests.request(
        method=method,
        url=url,
        headers=str_headers,
        data=data,
        timeout=timeout
    )

# Push metrics
push_to_gateway(
    gateway=metrics_url,
    job="lrc_test",
    registry=registry,
    handler=bearer_auth_handler
)
