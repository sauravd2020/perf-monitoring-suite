# grafana/push_metrics.py

from prometheus_client import Gauge, CollectorRegistry, push_to_gateway
import random
import time
import os

# Set your Grafana Cloud details
PUSHGATEWAY = "https://prometheus-prod-01-eu-west-0.grafana.net/api/prom/push"
JOB_NAME = "lrc-jmeter"
BEARER_TOKEN = os.getenv("GRAFANA_API_TOKEN")


# Create a new registry for each push
registry = CollectorRegistry()

# Define sample metrics
sla = Gauge('lrc_sla_percentage', 'LRC SLA %', registry=registry)
tps = Gauge('jmeter_tps', 'Transactions Per Second', registry=registry)
resp_time = Gauge('jmeter_response_time_ms', 'Response Time (ms)', registry=registry)

# Generate dummy data
sla.set(random.uniform(95.0, 100.0))
tps.set(random.uniform(50, 120))
resp_time.set(random.uniform(300, 1200))

# Push metrics
push_to_gateway(
    PUSHGATEWAY,
    job=JOB_NAME,
    registry=registry,
    handler=lambda url, method, timeout, headers, data: (
        __import__('requests').request(
            method,
            url,
            data=data,
            headers={"Authorization": f"Bearer {BEARER_TOKEN}", **headers},
            timeout=timeout,
        )
    )
)

print("✅ Pushed sample metrics to Grafana Cloud Prometheus.")
