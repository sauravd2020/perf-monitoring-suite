import os
import time
import requests
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

# Environment variables or defaults
GATEWAY = os.getenv("METRICS_URL", "https://your-prometheus-endpoint/api/v1/push")
BEARER_TOKEN = os.getenv("GRAFANA_CLOUD_TOKEN", "your-token")

registry = CollectorRegistry()

# Define a sample metric
g = Gauge('app_response_time_seconds', 'Response time in seconds', registry=registry)
g.set(0.42)

# Define a handler that returns a callable (to fix the error)
def bearer_handler(url, method, timeout, headers, data):
    response = requests.request(
        method=method,
        url=url,
        timeout=timeout,
        headers={k: v for (k, v) in headers} | {'Authorization': f"Bearer {BEARER_TOKEN}"},
        data=data
    )
    return lambda: response  # This matches what `push_to_gateway` expects

# Push the metrics
push_to_gateway(
    GATEWAY,
    job="perf-monitoring-suite",
    registry=registry,
    handler=bearer_handler,
)

print(f"Pushed metrics to: {GATEWAY}")
