import os
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import requests

# Get environment variables
GATEWAY = os.getenv("GRAFANA_CLOUD_METRICS_URL")
TOKEN = os.getenv("GRAFANA_CLOUD_API_KEY")

if not GATEWAY or not TOKEN:
    raise ValueError("Both METRICS_URL and GRAFANA_CLOUD_TOKEN must be set")

# Custom handler for Bearer Auth
def bearer_auth_handler(url, method, timeout, headers, data):
    response = requests.request(
        method,
        url,
        data=data,
        headers={key: value for key, value in headers},
        timeout=timeout,
        auth=None,
        headers_override={"Authorization": f"Bearer {TOKEN}"}
    )
    # Return a function to match expected callable signature
    return lambda: response.raise_for_status()

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
