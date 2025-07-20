from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import random
import os

# Grafana Cloud
GATEWAY = "https://prometheus-prod-13-prod-ap-south-1.grafana.net/api/prom/push"
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
