import os
import time
import requests
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

# Get environment variables
metrics_url = os.environ["GRAFANA_CLOUD_METRICS_URL"]
api_key = os.environ["GRAFANA_CLOUD_API_KEY"]

print("Pushing metrics to:", metrics_url)

# Create registry and sample metric
registry = CollectorRegistry()
g = Gauge('sample_lrc_test_latency_seconds', 'LRC latency in seconds', registry=registry)
g.set(1.5)

# Define a custom handler for basic auth
def bearer_auth_handler(url, method, timeout, headers, data):
    return requests.request(
        method=method,
        url=url,
        headers={
            **dict(headers),
            "Authorization": f"Bearer {api_key}",
        },
        data=data,
        timeout=timeout,
    )

# Push to Grafana Cloud Pushgateway
push_to_gateway(
    gateway=metrics_url,
    job="lrc_test",
    registry=registry,
    handler=bearer_auth_handler
)
