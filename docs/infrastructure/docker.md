# Docker Infrastructure

## Overview

This document describes the containerized application infrastructure running on the TrueNAS SCALE homelab.

The environment uses Docker-based applications to provide infrastructure services, monitoring, media management, reverse proxy, internal PKI, and supporting services.

The architecture is designed around:

* Containerized applications
* Persistent storage on ZFS
* Service isolation
* Health monitoring
* Centralized metrics
* Internal networking
* Infrastructure automation
* Reproducible configuration
* Security and controlled access

The Docker environment is an important component of the homelab's infrastructure and serves as a practical foundation for future AI, MLOps, and automation projects.

---

## Platform

### TrueNAS

* Platform: TrueNAS SCALE
* Current version: 25.10.7
* Storage backend: ZFS
* Primary application pool: `antioch`
* Application datasets: `antioch/ix-apps`
* Application configuration and persistent data are stored on ZFS datasets.

TrueNAS provides the underlying storage, application management, networking, and infrastructure platform.

---

## Container Architecture

The environment consists of several groups of containerized services.

```text
                         ┌──────────────────────┐
                         │      TrueNAS SCALE   │
                         │       25.10.7        │
                         └──────────┬───────────┘
                                    │
                              Docker Runtime
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          │                         │                         │
          ▼                         ▼                         ▼
   Monitoring Stack            Media Stack              Infrastructure
          │                         │                         │
   ┌──────┼───────┐        ┌────────┼─────────┐       ┌───────┼────────┐
   │      │       │        │        │         │       │       │        │
Prometheus Grafana Exporters  Plex  Sonarr  Radarr   NPM   Step-CA  Seerr
                              │       │        │
                              ├── Prowlarr
                              ├── Bazarr
                              ├── qBittorrent
                              └── FlareSolverr
```

The architecture separates application responsibilities while maintaining centralized storage and monitoring.

---

# Running Services

The following services are currently deployed in the TrueNAS environment.

## Monitoring

| Service           | Image                                          | Purpose                                     |
| ----------------- | ---------------------------------------------- | ------------------------------------------- |
| Prometheus        | `prom/prometheus:v3.14.0`                      | Metrics collection and time-series database |
| Grafana           | `grafana/grafana:13.2.1`                       | Metrics visualization and dashboards        |
| Node Exporter     | `prom/node-exporter:latest`                    | Host operating system metrics               |
| Smartctl Exporter | `prometheuscommunity/smartctl-exporter:latest` | Disk health and SMART metrics               |
| Graphite Exporter | `prom/graphite-exporter:latest`                | Graphite-to-Prometheus metrics integration  |

The monitoring stack provides infrastructure visibility and forms the basis for future automated anomaly detection.

---

# Media Services

The media environment is composed of several specialized services.

| Service      | Image                                         | Purpose                       |
| ------------ | --------------------------------------------- | ----------------------------- |
| Plex         | `plexinc/pms-docker:plexpass`                 | Media server                  |
| Sonarr       | `ghcr.io/home-operations/sonarr:4.0.19.3009`  | TV series management          |
| Radarr       | `ghcr.io/home-operations/radarr:6.4.3.10645`  | Movie management              |
| Prowlarr     | `ghcr.io/home-operations/prowlarr:2.6.3.5592` | Indexer management            |
| qBittorrent  | `ghcr.io/home-operations/qbittorrent:5.2.3`   | Download client               |
| Bazarr       | `ghcr.io/home-operations/bazarr:1.6.0`        | Subtitle management           |
| FlareSolverr | `flaresolverr/flaresolverr:v3.5.0`            | Cloudflare challenge handling |
| Seerr        | `ghcr.io/seerr-team/seerr:v3.4.1`             | Media request management      |

The services form an integrated media automation pipeline.

```text
                    ┌──────────────┐
                    │    Seerr    │
                    │ Media       │
                    │ Requests    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │    Sonarr    │
                    │    Radarr    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Prowlarr  │
                    │   Indexers   │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ qBittorrent  │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │    Media     │
                    │   Storage    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │     Plex     │
                    └──────────────┘
```

Bazarr provides subtitle automation and FlareSolverr supports services that require browser challenge handling.

---

# Infrastructure Services

## Nginx Proxy Manager

Container:

```text
jc21/nginx-proxy-manager:2.15.1
```

Nginx Proxy Manager provides reverse-proxy functionality for internal applications.

Responsibilities include:

* Reverse proxy
* HTTPS termination
* Internal application routing
* Certificate integration
* Centralized access to web applications

The proxy layer prevents individual applications from needing to expose their services directly to the network.

---

## Step CA

Container:

```text
smallstep/step-ca:latest
```

Step CA provides internal certificate authority functionality.

The internal PKI is used to support HTTPS for services inside the homelab.

This allows the environment to use trusted internal certificates without exposing infrastructure services to the public Internet.

The internal domain architecture uses:

```text
*.lab.home.arpa
```

Private keys, certificates, CA credentials, and other sensitive PKI material are intentionally excluded from this repository.

---

# Persistent Storage

Containerized applications should be treated as ephemeral compute resources.

Important application data is stored outside the container filesystem using persistent ZFS datasets.

The primary application storage hierarchy is:

```text
antioch
└── ix-apps
    ├── app_configs
    ├── app_mounts
    │   ├── bazarr
    │   ├── plex
    │   ├── prowlarr
    │   ├── qbittorrent
    │   ├── radarr
    │   └── sonarr
    ├── docker
    └── truenas_catalog
```

Additional application and infrastructure data is stored under:

```text
antioch/nas
├── AIStorage
├── Backups
├── KnowledgeBase
├── Monitoring
├── media
├── npm
└── stepca
```

This separation provides several advantages:

* Container replacement does not destroy application data.
* ZFS snapshots can protect persistent data.
* Storage can be monitored independently from containers.
* Application data can be backed up.
* Containers can be recreated from their configuration.

---

# Container Lifecycle

A container should be considered replaceable.

The general lifecycle is:

```text
Configuration
     │
     ▼
Container Creation
     │
     ▼
Persistent Storage
     │
     ▼
Health Monitoring
     │
     ├───────────────┐
     ▼               ▼
Normal Operation   Failure
     │               │
     │               ▼
     │          Troubleshooting
     │               │
     │               ▼
     │          Replacement
     │               │
     └───────────────┘
```

Persistent configuration and data should therefore never depend exclusively on the writable layer of a container.

---

# Health Monitoring

Container health is monitored at multiple levels.

## Container Level

Docker provides container state and health information.

Useful commands:

```bash
sudo docker ps
```

```bash
sudo docker ps -a
```

```bash
sudo docker inspect <container>
```

To check a specific container:

```bash
sudo docker inspect --format='{{.State.Status}}' <container>
```

For health-enabled containers:

```bash
sudo docker inspect --format='{{.State.Health.Status}}' <container>
```

---

# Logs

Container logs are one of the first troubleshooting resources.

```bash
sudo docker logs <container>
```

Follow logs in real time:

```bash
sudo docker logs -f <container>
```

Show recent logs:

```bash
sudo docker logs --tail 100 <container>
```

Show logs with timestamps:

```bash
sudo docker logs -t <container>
```

A practical troubleshooting sequence is:

```text
Service unavailable
       │
       ▼
Check container state
       │
       ▼
Check health status
       │
       ▼
Check logs
       │
       ▼
Check storage
       │
       ▼
Check network
       │
       ▼
Check dependencies
```

---

# Resource Monitoring

Docker resource consumption can be inspected using:

```bash
sudo docker stats
```

This provides real-time information about:

* CPU usage
* Memory usage
* Network traffic
* Block I/O
* Process count

Resource monitoring is particularly important for an AI-capable homelab because AI workloads can consume significantly more CPU, memory, storage, and network resources than traditional services.

---

# Networking

The containerized environment uses internal networking.

Services communicate with each other according to their application requirements while external access is controlled through the reverse-proxy layer.

The architecture follows the principle:

```text
Internal Services
       │
       ▼
Container Network
       │
       ▼
Reverse Proxy
       │
       ▼
HTTPS
       │
       ▼
Internal Users
```

Internal services should not be unnecessarily exposed directly.

Public IP addresses, internal IP addresses, credentials, API tokens, private keys, and other infrastructure secrets are intentionally excluded from this repository.

---

# Security Principles

The Docker environment follows several security principles.

## 1. Minimize Exposure

Only services that need network access should expose ports.

## 2. Use HTTPS

Web applications should use HTTPS whenever practical.

## 3. Protect Credentials

Credentials and secrets must never be committed to Git.

Examples:

```text
.env
*.key
*.pem
*.crt
secrets/
credentials/
```

## 4. Persistent Data Separation

Application data is separated from container images and writable container layers.

## 5. Regular Updates

Containers should be periodically reviewed for:

* Security updates
* Application updates
* Image updates
* Configuration changes

## 6. Backup Application Data

Critical application configuration should be included in the homelab backup strategy.

---

# Image Management

Container images should be managed carefully.

There are two common strategies.

### Floating Tags

Example:

```text
latest
```

Advantages:

* Simple
* Automatically tracks the newest image

Disadvantages:

* Version changes can be unexpected
* Reproducibility is reduced
* Updates may introduce breaking changes

### Versioned Tags

Example:

```text
grafana/grafana:13.2.1
```

Advantages:

* Reproducibility
* Predictable deployments
* Easier troubleshooting
* Easier rollback

Disadvantages:

* Requires manual version management

For production-like infrastructure, version pinning is generally preferable for critical services.

---

# Update Strategy

Before updating an important service:

1. Verify the current version.
2. Check application release notes.
3. Verify storage availability.
4. Ensure configuration is backed up.
5. Update the application.
6. Check container health.
7. Review logs.
8. Verify application functionality.
9. Monitor the service after the update.

A controlled update process is preferable to blindly updating all containers simultaneously.

---

# Troubleshooting

## Container Not Starting

Check:

```bash
sudo docker ps -a
```

Then:

```bash
sudo docker logs <container>
```

Inspect the configuration:

```bash
sudo docker inspect <container>
```

---

## Container Restarting Repeatedly

Check:

```bash
sudo docker ps -a
```

Then:

```bash
sudo docker logs --tail 200 <container>
```

Look for:

* Configuration errors
* Permission problems
* Missing files
* Database errors
* Invalid environment variables
* Port conflicts
* Dependency failures

---

## Storage Problems

Check ZFS:

```bash
zpool status
```

Check datasets:

```bash
zfs list
```

Check disk usage:

```bash
df -h
```

A container failure can sometimes be caused by a full filesystem rather than an application problem.

---

## Network Problems

Check listening ports:

```bash
sudo ss -tulpn
```

Check container networking:

```bash
sudo docker network ls
```

Inspect a network:

```bash
sudo docker network inspect <network>
```

---

# Monitoring Architecture

The Docker environment is integrated with Prometheus and Grafana.

```text
                    ┌──────────────────┐
                    │     Docker       │
                    │    Services      │
                    └────────┬─────────┘
                             │
                     Metrics / Exporters
                             │
                             ▼
                    ┌──────────────────┐
                    │    Prometheus    │
                    │   Time Series    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │     Grafana      │
                    │    Dashboards    │
                    └──────────────────┘
```

The monitoring architecture provides a foundation for future automation.

Potential future capabilities include:

* Automatic anomaly detection
* AI-assisted troubleshooting
* Predictive infrastructure alerts
* Resource optimization
* Automated incident summaries
* Natural-language infrastructure queries

---

# Docker and AI/MLOps

The Docker infrastructure is also intended to support future AI engineering projects.

Potential AI services include:

```text
              ┌───────────────────────┐
              │       AI Agent        │
              └───────────┬───────────┘
                          │
              ┌───────────┼───────────┐
              │           │           │
              ▼           ▼           ▼
         Prometheus    Qdrant      PostgreSQL
              │           │           │
              └───────────┼───────────┘
                          │
                          ▼
                     Python API
                          │
                          ▼
                       Ollama
                          │
                          ▼
                     Local LLM
```

This architecture can eventually become an AI-powered infrastructure assistant.

For example, an AI agent could:

1. Query Prometheus.
2. Detect abnormal resource usage.
3. Query historical infrastructure data.
4. Retrieve relevant troubleshooting documentation from Qdrant.
5. Analyze container logs.
6. Identify probable causes.
7. Generate a human-readable explanation.
8. Recommend corrective actions.

This project would combine:

* Linux
* Docker
* Networking
* Python
* APIs
* Prometheus
* Grafana
* Vector databases
* LLMs
* RAG
* AI agents
* Observability
* MLOps

It represents the intended evolution of this homelab from traditional infrastructure into an AI engineering platform.

---

# Operational Principles

The environment follows these general principles:

### Infrastructure as Documentation

Important infrastructure decisions should be documented.

### Persistent Data Outside Containers

Containers should be replaceable without losing application data.

### Monitoring Before Automation

Infrastructure should be observable before automated remediation is introduced.

### Security by Default

Services should remain internal unless external exposure is explicitly required.

### Reproducibility

Configurations should be version-controlled whenever possible.

### Incremental Automation

Manual procedures should gradually become scripts and eventually automated workflows.

---

# Future Improvements

Potential improvements include:

* Further standardization of container versions
* Automated image update notifications
* Automated configuration backups
* Docker resource alerting
* Expanded Prometheus exporters
* Container-level dashboards
* Centralized log management
* Automated health checks
* Git-based configuration management
* CI/CD for infrastructure scripts
* Infrastructure-as-Code
* Automated disaster recovery testing
* AI-assisted infrastructure monitoring
* AI-based log analysis
* Predictive failure detection
* MLOps monitoring

---

# Relationship With Other Documentation

Related documentation:

* `docs/infrastructure/truenas.md`
* `docs/infrastructure/storage.md`
* `docs/architecture/overview.md`
* `docs/monitoring/prometheus.md`
* `docs/monitoring/grafana.md`

---

# Security Notice

This repository intentionally does not contain:

* IP addresses
* MAC addresses
* Disk serial numbers
* Disk UUIDs
* Passwords
* API keys
* Access tokens
* Private SSH keys
* Private TLS keys
* Internal credentials
* Sensitive configuration values

The documentation describes the architecture without exposing information that could compromise the infrastructure.

