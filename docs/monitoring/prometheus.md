# Prometheus Monitoring

## Overview

Prometheus is the central metrics collection and time-series monitoring platform used by the homelab.

It collects infrastructure metrics from the TrueNAS host and supporting exporters and provides the data source used by Grafana for visualization and analysis.

The monitoring architecture is designed to provide visibility into:

* Host resource utilization
* CPU usage
* Memory usage
* Network activity
* Disk health
* Storage infrastructure
* Application infrastructure
* Exporter health
* Service availability

Prometheus also provides the foundation for future AI-assisted infrastructure monitoring and anomaly detection.

---

# Monitoring Architecture

The current monitoring architecture is based on Prometheus, Grafana, and several exporters.

```text
                         TrueNAS SCALE
                              │
                              │
                  ┌───────────┴───────────┐
                  │                       │
                  ▼                       ▼
             Node Exporter          SMART Exporter
                  │                       │
                  │                       │
                  └───────────┬───────────┘
                              │
                              ▼
                       ┌─────────────┐
                       │ Prometheus  │
                       │             │
                       │ Time Series │
                       └──────┬──────┘
                              │
                              ▼
                       ┌─────────────┐
                       │   Grafana   │
                       │ Dashboards  │
                       └─────────────┘
```

Additional exporters and monitoring integrations can be added as the infrastructure evolves.

---

# Prometheus Deployment

Prometheus runs as a containerized application on TrueNAS.

Current image:

```text
prom/prometheus:v3.14.0
```

The container is managed as part of the TrueNAS application infrastructure.

The Prometheus service is configured with:

* Global scrape interval
* Scrape timeout
* Evaluation interval
* Data retention
* Storage limits
* Target definitions

---

# Data Storage

Prometheus stores time-series data on persistent storage.

The monitoring data is associated with the TrueNAS monitoring storage infrastructure.

Persistent storage is important because container replacement should not result in loss of historical monitoring data.

The monitoring storage architecture is documented separately in:

```text
docs/infrastructure/storage.md
```

---

# Scrape Model

Prometheus uses a pull-based monitoring model.

```text
Exporter
   │
   │ HTTP /metrics
   ▼
Prometheus
   │
   │ Time Series
   ▼
Prometheus Database
   │
   ▼
Grafana
```

Prometheus periodically requests metrics from configured targets.

A typical exporter endpoint looks like:

```text
http://<target>:<port>/metrics
```

The `/metrics` endpoint exposes metrics in Prometheus exposition format.

---

# Exporters

## Node Exporter

Container:

```text
prom/node-exporter:latest
```

Node Exporter exposes operating-system-level metrics.

Typical metrics include:

* CPU utilization
* Memory utilization
* Filesystem usage
* Network statistics
* System load
* Disk statistics
* Kernel information

Node Exporter is one of the primary sources of infrastructure metrics.

---

# Smartctl Exporter

Container:

```text
prometheuscommunity/smartctl-exporter:latest
```

Smartctl Exporter provides hardware storage health information through SMART data.

This is particularly important for a NAS environment.

Potential monitoring data includes:

* Disk temperature
* SMART attributes
* Drive health
* Read/write errors
* Disk identity information
* SMART availability

Disk health metrics can be used to detect potential hardware problems before a drive completely fails.

---

# Graphite Exporter

Container:

```text
prom/graphite-exporter:latest
```

Graphite Exporter provides compatibility between Graphite-formatted metrics and Prometheus.

This allows existing or future applications that produce Graphite metrics to integrate with the Prometheus monitoring architecture.

---

# Monitoring Targets

Prometheus targets should be considered healthy when:

```text
UP = 1
```

An unavailable target normally results in:

```text
UP = 0
```

Target health is one of the first indicators to check when troubleshooting monitoring problems.

---

# Target Troubleshooting

Prometheus target availability can be inspected through its web interface.

The basic troubleshooting workflow is:

```text
Target Down
    │
    ▼
Check target address
    │
    ▼
Check exporter container
    │
    ▼
Check exporter logs
    │
    ▼
Test /metrics endpoint
    │
    ▼
Check network connectivity
    │
    ▼
Check permissions
```

From the TrueNAS host, an exporter can be tested using:

```bash
curl http://<target>:<port>/metrics
```

A working exporter should return Prometheus-formatted metrics.

For example:

```text
# HELP go_gc_duration_seconds
# TYPE go_gc_duration_seconds summary
go_gc_duration_seconds{quantile="0"} ...
```

---

# Prometheus Configuration

The Prometheus configuration defines global monitoring behavior and scrape targets.

A simplified configuration structure is:

```yaml
global:
  scrape_interval: 1m
  scrape_timeout: 10s
  evaluation_interval: 1m

scrape_configs:

  - job_name: prometheus
    static_configs:
      - targets:
          - localhost:9090

  - job_name: node
    static_configs:
      - targets:
          - <node-exporter>:9100

  - job_name: smartctl
    static_configs:
      - targets:
          - <smartctl-exporter>:9633
```

The actual production configuration should remain environment-specific and should not contain credentials or sensitive network information.

---

# Scrape Interval

The current monitoring architecture uses a one-minute global scrape interval.

```text
scrape_interval: 1m
```

A one-minute interval provides a reasonable balance between:

* Monitoring resolution
* Storage consumption
* CPU usage
* Network traffic

Higher-frequency monitoring can be introduced for specific services where required.

For example, critical infrastructure could eventually use:

```text
15s
```

while less important targets could use:

```text
60s
```

or longer.

---

# Retention

Prometheus retention determines how long historical metrics remain available.

Retention should be balanced against:

* Available storage
* Number of metrics
* Scrape frequency
* Number of targets
* Monitoring requirements

Longer retention provides more historical data for:

* Capacity planning
* Performance analysis
* Trend analysis
* Anomaly detection
* Infrastructure optimization

---

# PromQL

Prometheus Query Language (PromQL) is used to retrieve and analyze time-series data.

Examples of useful queries include:

## CPU Usage

```promql
100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

This estimates CPU utilization over a five-minute window.

---

## Memory Usage

```promql
100 * (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)
```

This calculates approximate memory utilization.

---

## Filesystem Usage

```promql
100 * (
  1 -
  node_filesystem_avail_bytes{fstype!~"tmpfs|overlay"}
  /
  node_filesystem_size_bytes{fstype!~"tmpfs|overlay"}
)
```

This can be used to identify filesystems approaching capacity.

---

## Target Availability

```promql
up
```

This is one of the simplest and most useful infrastructure health queries.

---

# Alerting

Prometheus can evaluate alert rules based on metric conditions.

A conceptual alert might look like:

```yaml
groups:
  - name: infrastructure
    rules:

      - alert: HighCPUUsage
        expr: cpu_usage > 90
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: High CPU utilization detected
```

Alert rules should avoid excessive sensitivity.

For example, a short CPU spike may be normal.

A sustained condition is usually more useful:

```text
CPU > 90%
for 10 minutes
```

rather than:

```text
CPU > 90%
for 5 seconds
```

---

# Recommended Alert Categories

As the monitoring system develops, alerts can be organized into categories.

## Host

* High CPU
* High memory
* High load
* Filesystem nearly full
* Network interface problems

## Storage

* SMART failure
* Increasing disk errors
* High disk temperature
* ZFS pool degradation
* Resilver activity
* Scrub errors

## Containers

* Container unavailable
* Container repeatedly restarting
* Exporter unavailable
* Excessive CPU usage
* Excessive memory usage

## Monitoring

* Prometheus unavailable
* Grafana unavailable
* Exporter unavailable
* Scrape failures
* Missing metrics

---

# Grafana Integration

Grafana uses Prometheus as a primary metrics data source.

```text
                    Prometheus
                        │
                        │ PromQL
                        ▼
                    Grafana
                        │
             ┌──────────┼──────────┐
             ▼          ▼          ▼
           CPU        Memory      Storage
             │          │          │
             └──────────┼──────────┘
                        ▼
                    Dashboard
```

Grafana dashboards should provide both high-level infrastructure status and detailed troubleshooting information.

---

# Dashboard Strategy

A useful monitoring environment should have multiple dashboard levels.

## Infrastructure Overview

Displays:

* Overall system status
* CPU
* Memory
* Storage
* Network
* Critical alerts

## Storage

Displays:

* ZFS pools
* Capacity
* Disk health
* SMART information
* Scrub/resilver status

## Containers

Displays:

* Running containers
* CPU usage
* Memory usage
* Network traffic
* Restart behavior

## Monitoring

Displays:

* Prometheus health
* Scrape success
* Target availability
* Exporter status
* Query performance

---

# Monitoring and ZFS

ZFS is a critical part of this environment because the TrueNAS platform provides the storage layer for applications and infrastructure data.

Prometheus monitoring should complement native ZFS administration.

Important ZFS events include:

```text
ONLINE
DEGRADED
FAULTED
OFFLINE
RESILVER
SCRUB
```

Monitoring should make it possible to detect changes in storage health before they become service-impacting failures.

---

# Monitoring and Docker

Docker metrics provide another important observability layer.

The objective is to correlate:

```text
Container
   │
   ├── CPU
   ├── Memory
   ├── Network
   └── Restart behavior
           │
           ▼
      Prometheus
           │
           ▼
        Grafana
```

This allows application problems to be analyzed together with infrastructure behavior.

For example:

```text
Application becomes slow
        │
        ▼
Container CPU increases
        │
        ▼
Host CPU increases
        │
        ▼
Prometheus records event
        │
        ▼
Grafana displays correlation
```

This is much more useful than looking at an application in isolation.

---

# Observability Philosophy

The monitoring architecture follows three fundamental observability concepts:

### Metrics

Numerical measurements describing system behavior.

Examples:

* CPU
* Memory
* Disk
* Network
* Request rates

### Logs

Detailed events generated by applications and infrastructure.

### Traces

Request-level information showing how operations move through distributed services.

The current environment is primarily metrics-based.

Future development can add centralized logging and distributed tracing where appropriate.

---

# Prometheus as an AI Data Source

One of the most important future goals is to make Prometheus data available to an AI agent.

Conceptually:

```text
                  Prometheus
                      │
                      ▼
                 Metrics API
                      │
                      ▼
                  Python API
                      │
                      ▼
                  AI Agent
                      │
              ┌───────┼────────┐
              ▼       ▼        ▼
           Analysis  RAG     Tools
              │       │        │
              └───────┼────────┘
                      ▼
                  Local LLM
```

The AI system could ask Prometheus questions such as:

```text
What happened to CPU usage during the last hour?
```

```text
Which containers consumed the most memory?
```

```text
Did disk activity increase before the application became unavailable?
```

```text
Are there any abnormal infrastructure trends?
```

---

# AI-Assisted Anomaly Detection

Future versions of the monitoring system could analyze historical metrics to identify abnormal behavior.

For example:

```text
Normal CPU
   │
   │
   │
   ├───────────────┐
                   │
                   ▼
              Unusual spike
                   │
                   ▼
             Anomaly detector
                   │
                   ▼
               AI analysis
                   │
                   ▼
          Human-readable alert
```

Instead of simply reporting:

```text
CPU = 95%
```

the system could eventually report:

```text
CPU utilization has remained above 90% for
14 minutes, approximately 3.2x higher than the
normal workload observed during the previous
24 hours.

The largest contributor appears to be container X.
```

This is the direction of the future AI Infrastructure Monitoring Agent project.

---

# Infrastructure Monitoring Agent

A future project can integrate:

* Prometheus
* Grafana
* Docker
* TrueNAS
* Python
* Qdrant
* Ollama
* Local LLMs
* RAG
* AI Agents

Potential architecture:

```text
                    User
                      │
                      ▼
                 AI Assistant
                      │
             ┌────────┼────────┐
             │        │        │
             ▼        ▼        ▼
        Prometheus  Qdrant   Docker API
             │        │        │
             │        │        │
             ▼        ▼        ▼
          Metrics   Knowledge  Runtime
             │       Base       State
             └────────┼─────────┘
                      ▼
                 Python Agent
                      │
                      ▼
                  Local LLM
```

This project would transform the homelab monitoring system into a practical AI engineering and MLOps project.

---

# Troubleshooting Checklist

When Prometheus is not collecting metrics:

### 1. Check the container

```bash
sudo docker ps | grep prometheus
```

### 2. Check logs

```bash
sudo docker logs --tail 100 ix-prometheus-prometheus-1
```

### 3. Check exporter

```bash
sudo docker ps | grep exporter
```

### 4. Test exporter endpoint

```bash
curl http://<exporter>:<port>/metrics
```

### 5. Check network connectivity

```bash
ping <target>
```

### 6. Check Prometheus targets

Use the Prometheus Targets page and verify that the target reports:

```text
UP
```

### 7. Check configuration

Verify:

* Target hostname
* Port
* Job name
* Scrape interval
* Network accessibility
* Exporter availability

---

# Operational Best Practices

The monitoring system should follow these practices:

* Keep monitoring configuration version-controlled.
* Avoid storing credentials in Git.
* Monitor Prometheus itself.
* Monitor exporter availability.
* Keep critical dashboards documented.
* Use alerts for actionable conditions.
* Avoid excessive alert noise.
* Retain enough historical data for troubleshooting.
* Regularly review storage consumption.
* Validate monitoring after infrastructure changes.

---

# Future Improvements

Planned or potential improvements include:

* More TrueNAS-specific metrics
* Expanded ZFS monitoring
* More container-level metrics
* Centralized logging
* Alertmanager integration
* Automated alert notifications
* Infrastructure anomaly detection
* Capacity forecasting
* AI-assisted troubleshooting
* AI-generated incident summaries
* Natural-language PromQL queries
* Automated remediation with safeguards
* MLOps monitoring
* Model performance monitoring

---

# Related Documentation

Related files:

```text
docs/architecture/overview.md
docs/infrastructure/truenas.md
docs/infrastructure/storage.md
docs/infrastructure/docker.md
docs/monitoring/grafana.md
```

---

# Security

This documentation intentionally excludes:

* Internal IP addresses
* Credentials
* API tokens
* Private keys
* Disk UUIDs
* Disk serial numbers
* Authentication secrets
* Private certificates

Monitoring infrastructure should provide visibility without becoming a source of sensitive information leakage.

