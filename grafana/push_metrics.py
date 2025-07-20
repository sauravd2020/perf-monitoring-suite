import os
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

# Load environment variables
GATEWAY = os.environ.get("METRICS_URL")
TOKEN = os.environ.get("GRAFANA_CLOUD_TOKEN")

if not GATEWAY or not TOKEN:
    raise ValueError("Environment variables METRICS_URL and GRAFANA_CLOUD_TOKEN must be set")

registry = CollectorRegistry()
g = Gauge('example_metric', 'Example metric pushed to Grafana Cloud', registry=registry)
g.set(5.6)

# Correct handler — returns the response (not calls it)
def custom_handler(url, method, timeout, headers, data):
    import requests
    response = requests.request(
        method=method,
        url=url,
        headers=dict(headers + [('Authorization', f'Bearer {TOKEN}')] ),
        data=data,
        timeout=timeout
    )
    if not response.ok:
        raise Exception(f"Push failed: {response.status_code} {response.text}")
    return response

# Push metrics
push_to_gateway(
    GATEWAY,
    job='my_push_job',
    registry=registry,
    handler=custom_handler
)
