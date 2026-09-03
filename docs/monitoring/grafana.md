# Grafana Monitoring

## Overview

Grafana is the visualization and observability layer of the homelab monitoring infrastructure.

It uses Prometheus as a metrics data source and provides dashboards for understanding the health and performance of the TrueNAS environment, Docker services, storage infrastructure, and monitoring stack.

The monitoring architecture is:

```text
Infrastructure
      │
      ▼
   Exporters
      │
      ▼
  Prometheus
      │
      │ PromQL
      ▼
   Grafana
      │
      ├── Dashboards
      ├── Visualization
      ├── Alerts
      └── Analysis
```

Grafana transforms raw time-series metrics into information that can be quickly understood by an administrator.

---

# Deployment

Grafana runs as a containerized application on TrueNAS.

Current image:

```text
grafana/grafana:13.2.1
```

The application is managed as part of the TrueNAS application infrastructure.

Grafana uses persistent storage for its configuration, dashboards, users, and other application data.

---

# Role in the Infrastructure

Grafana is responsible for the visualization layer of the observability platform.

Its primary responsibilities are:

* Infrastructure dashboards
* Docker monitoring
* CPU visualization
* Memory visualization
* Network monitoring
* Storage monitoring
* Disk health visualization
* Prometheus monitoring
* Alert visualization
* Historical trend analysis

Grafana does not normally collect the metrics itself.

Instead:

```text
Exporter → Prometheus → Grafana
```

Prometheus remains the metrics collection and time-series storage layer.

---

# Prometheus Data Source

Prometheus is configured as the primary metrics data source.

The relationship is:

```text
                 Prometheus
                     │
                     │ PromQL
                     ▼
                  Grafana
                     │
            ┌────────┼────────┐
            ▼        ▼        ▼
          Panels   Alerts   Variables
```

Grafana queries Prometheus using PromQL.

This separation between collection and visualization allows the monitoring architecture to evolve independently.

---

# Dashboard Architecture

Dashboards should be organized according to infrastructure responsibilities rather than individual applications.

Recommended dashboard structure:

```text
Grafana
│
├── Infrastructure
│   ├── Overview
│   ├── CPU
│   ├── Memory
│   └── Network
│
├── Storage
│   ├── ZFS
│   ├── Disks
│   └── SMART
│
├── Docker
│   ├── Containers
│   ├── CPU
│   ├── Memory
│   └── Network
│
├── Monitoring
│   ├── Prometheus
│   └── Exporters
│
└── Applications
    ├── Media Services
    └── Other Services
```

---

# Infrastructure Overview Dashboard

The infrastructure overview should be the first dashboard opened when checking system health.

Recommended panels:

* Overall system status
* CPU utilization
* Memory utilization
* Storage utilization
* Network throughput
* System load
* Number of active containers
* Monitoring target availability
* Critical alerts

A conceptual layout:

```text
┌─────────────────────────────────────────────┐
│              INFRASTRUCTURE                 │
├──────────────┬──────────────┬───────────────┤
│ CPU          │ Memory       │ Storage       │
│              │              │               │
├──────────────┼──────────────┼───────────────┤
│ Network      │ Containers   │ Targets       │
│              │              │               │
├──────────────┴──────────────┴───────────────┤
│              Active Alerts                   │
└─────────────────────────────────────────────┘
```

The purpose is to provide a rapid health assessment rather than detailed troubleshooting.

---

# CPU Dashboard

CPU monitoring helps identify:

* Sustained system load
* Unexpected processes
* Container resource consumption
* Performance bottlenecks
* AI workload impact

Useful PromQL:

```promql
100 - (avg by(instance) (
  rate(node_cpu_seconds_total{mode="idle"}[5m])
) * 100)
```

A five-minute rate provides a more stable view than instantaneous CPU utilization.

---

# Memory Dashboard

Memory utilization is particularly important because the homelab hosts multiple containerized services.

Useful PromQL:

```promql
100 * (
  1 -
  node_memory_MemAvailable_bytes /
  node_memory_MemTotal_bytes
)
```

Recommended panels:

* Memory used
* Memory available
* Memory percentage
* Swap usage
* Memory utilization over time

Memory trends are especially important when introducing AI workloads.

Local LLM inference, vector databases, embeddings, and data processing can significantly increase memory consumption.

---

# Network Dashboard

Network dashboards can display:

* Receive throughput
* Transmit throughput
* Packets
* Errors
* Dropped packets
* Network utilization

Example receive-rate query:

```promql
rate(node_network_receive_bytes_total[5m])
```

Example transmit-rate query:

```promql
rate(node_network_transmit_bytes_total[5m])
```

Network monitoring becomes increasingly important when infrastructure contains:

* NAS workloads
* Media streaming
* Backup operations
* AI model transfers
* Container-to-container communication
* Remote administration

---

# Storage Dashboard

Storage is one of the most important monitoring areas in a NAS environment.

The dashboard should provide visibility into:

* Pool capacity
* Filesystem capacity
* Disk activity
* Disk health
* SMART information
* Storage trends

A storage dashboard should make it possible to answer:

```text
How much storage is available?

Which filesystem is growing?

Are any disks reporting problems?

Is disk activity unusually high?

Is storage approaching a critical threshold?
```

---

# ZFS Monitoring

The TrueNAS storage infrastructure uses ZFS.

Grafana should eventually provide visibility into important ZFS conditions such as:

```text
ONLINE
DEGRADED
FAULTED
OFFLINE
SCRUB
RESILVER
```

ZFS monitoring is particularly important because storage problems can affect many services simultaneously.

For example:

```text
ZFS problem
     │
     ├── Docker storage
     ├── Media services
     ├── Backups
     ├── Monitoring data
     └── AI datasets
```

A single storage failure can therefore have a broad infrastructure impact.

---

# SMART Dashboard

SMART data can be exposed through Smartctl Exporter.

Current exporter:

```text
prometheuscommunity/smartctl-exporter:latest
```

Potential dashboard information includes:

* Drive temperature
* SMART health
* SMART attributes
* Read errors
* Write errors
* Reallocated sectors
* Pending sectors
* Power-on hours

The dashboard should emphasize trends rather than isolated values.

For example, an increasing error count can be more significant than a single warning.

---

# Docker Dashboard

A dedicated Docker dashboard can provide visibility into containerized workloads.

Recommended panels:

* Running containers
* CPU usage
* Memory usage
* Network traffic
* Restart behavior
* Container availability
* Resource consumption

Conceptual architecture:

```text
Docker
  │
  ├── Container A
  ├── Container B
  ├── Container C
  └── Container D
        │
        ▼
      Metrics
        │
        ▼
    Prometheus
        │
        ▼
      Grafana
```

---

# Container Resource Analysis

Container-level monitoring allows infrastructure administrators to identify resource-intensive applications.

Questions that can be answered include:

```text
Which container is using the most CPU?

Which container is consuming the most memory?

Which service generates the most network traffic?

Which containers restart frequently?

When did resource consumption increase?
```

This can help distinguish application problems from infrastructure problems.

---

# Monitoring Dashboard

Grafana should also monitor the monitoring system itself.

Important metrics include:

* Prometheus availability
* Scrape success
* Scrape failures
* Target availability
* Query performance
* Exporter availability
* Time-series ingestion

This follows an important observability principle:

> The monitoring system must be monitored too.

If the monitoring platform fails silently, infrastructure problems may go undetected.

---

# Alerting

Grafana can provide visualization and alerting based on Prometheus metrics.

Useful alert categories include:

### Infrastructure

* High CPU
* High memory
* High load
* Low storage capacity
* Network errors

### Storage

* ZFS pool degraded
* Disk failure
* SMART warning
* Increasing disk errors
* High disk temperature

### Docker

* Container unavailable
* Container restarting
* Excessive CPU
* Excessive memory

### Monitoring

* Prometheus unavailable
* Exporter unavailable
* Scrape failure
* Target down

---

# Alert Design

Alerts should be actionable.

Bad alert:

```text
CPU = 91%
```

Better alert:

```text
CPU utilization has remained above 90%
for more than 10 minutes.
```

Even better:

```text
CPU utilization has remained above 90% for
10 minutes and is approximately 3x above the
normal workload for this time period.
```

The final example introduces context, which becomes particularly useful when integrating AI-based anomaly detection.

---

# Time Ranges

Grafana dashboards should support common investigation periods:

```text
Last 5 minutes
Last 15 minutes
Last 1 hour
Last 6 hours
Last 24 hours
Last 7 days
Last 30 days
```

Different time ranges answer different questions.

### Short range

Useful for:

* Current incidents
* Container failures
* Performance problems

### Medium range

Useful for:

* Daily workload patterns
* Backup operations
* Media activity
* Resource spikes

### Long range

Useful for:

* Capacity planning
* Storage growth
* Performance trends
* Infrastructure optimization

---

# Variables

Grafana dashboard variables can make dashboards reusable.

Examples:

```text
$instance
$device
$filesystem
$container
$job
```

Instead of creating a separate dashboard for every service, a variable can allow the administrator to select the target dynamically.

Example:

```text
Container:
[ Sonarr ▼ ]
```

The same dashboard can then be used for:

```text
Sonarr
Radarr
Plex
Prometheus
Grafana
qBittorrent
```

---

# Dashboard Design Principles

Dashboards should follow several principles.

## 1. Start With the Big Picture

The first screen should show overall system health.

## 2. Use Consistent Units

Examples:

```text
CPU → %
Memory → GB / %
Storage → TB / %
Network → Mbps / Gbps
Temperature → °C
```

## 3. Show Trends

A value without historical context is often less useful.

## 4. Avoid Excessive Panels

A dashboard should communicate information rather than overwhelm the administrator.

## 5. Highlight Exceptions

Problems should be visually obvious.

## 6. Keep Troubleshooting Separate

Overview dashboards should remain simple.

Detailed troubleshooting dashboards can contain more information.

---

# Operational Workflow

A typical infrastructure investigation can begin with the Grafana overview dashboard.

```text
                    Alert / Problem
                           │
                           ▼
                  Infrastructure Overview
                           │
                 ┌─────────┼─────────┐
                 ▼         ▼         ▼
               CPU      Memory    Storage
                 │         │         │
                 └─────────┼─────────┘
                           ▼
                       Docker
                           │
                           ▼
                      Application
                           │
                           ▼
                         Logs
```

This workflow helps move from symptoms to probable causes.

---

# Grafana and AI

Grafana provides an important visual interface for the future AI Infrastructure Monitoring Agent.

The long-term architecture is:

```text
                         Infrastructure
                               │
                               ▼
                          Prometheus
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
                 Grafana              Python API
                    │                     │
                    │                     ▼
                    │                 AI Agent
                    │                     │
                    │              ┌──────┼──────┐
                    │              ▼      ▼      ▼
                    │           Metrics   RAG   Tools
                    │                     │
                    └─────────────────────┘
                                          │
                                          ▼
                                      Local LLM
```

Grafana remains the human-facing visualization layer while the AI agent becomes an additional analysis interface.

---

# Natural Language Infrastructure Queries

A future AI interface could allow users to ask questions such as:

```text
What is the current health of the NAS?
```

```text
Which container consumed the most memory today?
```

```text
Why did CPU usage increase yesterday?
```

```text
Has storage utilization been increasing unusually fast?
```

```text
Are there any signs of disk failure?
```

The AI agent could translate these questions into PromQL queries and combine the results with historical knowledge stored in a vector database.

---

# AI-Assisted Incident Analysis

A future implementation could combine metrics, logs, and documentation.

```text
             Incident
                 │
                 ▼
              Metrics
                 │
                 ├───────────────┐
                 ▼               ▼
            Prometheus         Logs
                 │               │
                 └───────┬───────┘
                         ▼
                     AI Agent
                         │
                 ┌───────┴────────┐
                 ▼                ▼
             Knowledge          Analysis
               Base                │
                 │                 │
                 └───────┬─────────┘
                         ▼
                  Incident Report
```

The resulting report could contain:

* What happened
* When it happened
* Affected services
* Relevant metrics
* Possible cause
* Supporting evidence
* Recommended action

This creates a practical bridge between infrastructure monitoring and AI engineering.

---

# MLOps Relevance

The Grafana/Prometheus stack also provides experience directly applicable to MLOps.

MLOps systems require monitoring of:

* Model services
* API latency
* Request volume
* Resource consumption
* GPU/CPU utilization
* Memory
* Errors
* Model performance
* Data drift
* Model drift

The same observability principles used for infrastructure can therefore be extended to AI workloads.

---

# Future AI Monitoring Project

The planned AI Infrastructure Monitoring Agent can use this environment as its real-world test platform.

Potential technology stack:

```text
Python
FastAPI
Prometheus
Grafana
Docker
Qdrant
PostgreSQL
Ollama
Local LLM
RAG
AI Agent
```

Possible project capabilities:

### Monitoring

Collect infrastructure metrics.

### Analysis

Detect unusual behavior.

### Retrieval

Retrieve relevant infrastructure documentation.

### Reasoning

Analyze metrics and logs.

### Explanation

Explain incidents in natural language.

### Recommendation

Suggest corrective actions.

### Reporting

Generate incident summaries.

---

# Backup and Reproducibility

Grafana configuration should be treated as infrastructure.

Important assets include:

* Dashboards
* Dashboard JSON
* Data source configuration
* Alert rules
* Variables
* Provisioning configuration

Whenever practical, these configurations should be version-controlled.

This allows dashboards to be recreated if the Grafana container must be replaced.

---

# Security

Grafana should be treated as an administrative application.

Security practices include:

* Strong authentication
* HTTPS
* Internal-only exposure where possible
* Least-privilege access
* Regular software updates
* Protected administrator accounts
* No credentials committed to Git

Sensitive configuration should never be stored in this repository.

---

# Troubleshooting

## Grafana Container

Check status:

```bash
sudo docker ps | grep grafana
```

Check logs:

```bash
sudo docker logs --tail 100 ix-grafana-grafana-1
```

---

## Prometheus Connection

If dashboards display no data:

1. Verify Prometheus is running.
2. Verify the Prometheus data source.
3. Test the connection.
4. Verify Prometheus targets.
5. Check the PromQL query.
6. Verify the selected time range.
7. Check whether the required metric exists.

---

## Empty Panel

If a dashboard panel displays no data:

Check:

```text
Data source
     │
     ▼
PromQL query
     │
     ▼
Metric exists?
     │
     ▼
Labels correct?
     │
     ▼
Time range correct?
```

Common causes include:

* Incorrect metric name
* Incorrect label
* Target unavailable
* Wrong time range
* Prometheus scrape failure
* Data source misconfiguration

---

# Best Practices

The Grafana environment should follow these practices:

* Keep dashboards focused.
* Monitor the monitoring stack.
* Use variables for reusable dashboards.
* Prefer trends over isolated values.
* Create actionable alerts.
* Keep dashboard configurations backed up.
* Version-control important dashboard definitions.
* Protect administrative access.
* Review dashboards as infrastructure changes.
* Build dashboards around operational questions.

---

# Future Improvements

Potential improvements include:

* Complete TrueNAS dashboard
* Detailed ZFS dashboards
* Docker container dashboard
* SMART disk dashboard
* Alertmanager integration
* Centralized logging
* Loki integration
* AI-generated dashboards
* Natural-language PromQL
* Infrastructure anomaly detection
* Capacity forecasting
* AI incident analysis
* Automated incident reports
* MLOps dashboards
* Model monitoring dashboards

---

# Related Documentation

```text
docs/architecture/overview.md
docs/infrastructure/truenas.md
docs/infrastructure/storage.md
docs/infrastructure/docker.md
docs/monitoring/prometheus.md
```

---

# Security Notice

This documentation intentionally excludes:

* Internal IP addresses
* Credentials
* API tokens
* Private keys
* Disk serial numbers
* Disk UUIDs
* Private certificates
* Authentication secrets

The objective is to document the architecture and engineering practices without exposing sensitive infrastructure information.

