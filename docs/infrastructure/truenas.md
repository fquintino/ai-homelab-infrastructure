# TrueNAS Infrastructure

## Overview

The homelab storage infrastructure is based on **TrueNAS SCALE 25.10.7**, providing centralized storage, ZFS data protection, containerized applications, monitoring infrastructure, media services, backups, and supporting services for the AI homelab.

TrueNAS is used as the primary storage and application platform within the homelab architecture.

The infrastructure is designed around:

- ZFS storage
- Mirrored storage pools
- Containerized applications
- Infrastructure monitoring
- Centralized application data
- Backup storage
- Internal PKI and reverse proxy services
- Media services
- AI and knowledge-base storage

---

## Platform

| Component | Configuration |
|---|---|
| Operating System | TrueNAS SCALE |
| Version | 25.10.7 |
| Filesystem | OpenZFS / ZFS |
| Storage Pools | `antioch`, `papyri`, `boot-pool` |
| Application Platform | TrueNAS Apps / Docker |
| Monitoring | Prometheus + Grafana |
| Metrics Exporters | Node Exporter, Smartctl Exporter, Graphite Exporter |
| Reverse Proxy | Nginx Proxy Manager |
| Internal PKI | Smallstep Step-CA |

---

# Storage Architecture

The TrueNAS system contains two primary data pools using mirrored VDEV layouts.

```text
                         TrueNAS SCALE
                              │
               ┌──────────────┴──────────────┐
               │                             │
           ZFS Storage                  Application Layer
               │                             │
       ┌───────┴────────┐          ┌─────────┴─────────┐
       │                │          │                   │
    antioch           papyri    ix-apps            Docker Apps
       │                │
       │                │
    mirror-0         mirror-0
    ┌────┴────┐      ┌────┴────┐
    │         │      │         │
   Disk      Disk   Disk      Disk

ZFS Storage Architecture

The TrueNAS system uses ZFS storage pools with mirrored VDEVs.

Mirroring provides disk redundancy and allows the system to continue operating when a member disk of a mirror fails.

The environment currently contains three ZFS pools:

antioch
papyri
boot-pool
Storage Pool: antioch

antioch is the primary data and application storage pool.

Current status:

State: ONLINE
Layout: mirror-0
Used: approximately 5.67 TB
Available: approximately 3.29 TB

The pool currently reports:

Errors: No known data errors

The most recent resilver operation completed successfully:

Data resilvered: approximately 5.61 TB
Duration: approximately 12 hours 19 minutes
Errors: 0

The antioch pool contains both application infrastructure and primary NAS data.

antioch Dataset Structure

The main structure is:

antioch
├── ix-apps
│   ├── app_configs
│   ├── app_mounts
│   ├── docker
│   └── truenas_catalog
│
└── nas
    ├── AIStorage
    ├── Backups
    │   └── macmini-ai
    ├── KnowledgeBase
    ├── Monitoring
    ├── homes
    │   └── fquin
    ├── media
    ├── npm
    │   ├── data
    │   └── letsencrypt
    └── stepca

This organization separates application infrastructure from general NAS data.

Application Storage

TrueNAS Apps use the following storage hierarchy:

antioch/ix-apps

Important application datasets include:

antioch/ix-apps/app_configs
antioch/ix-apps/app_mounts
antioch/ix-apps/docker
antioch/ix-apps/truenas_catalog

These datasets contain application configuration, application mount points, container runtime data, and the TrueNAS application catalog.

Application-specific data is separated from the primary NAS datasets whenever appropriate.

NAS Data Storage

The main NAS data hierarchy is:

antioch/nas

The major workloads are separated into dedicated datasets.

AIStorage
antioch/nas/AIStorage

Dedicated storage for AI-related workloads.

Potential uses include:

AI application data
Documents
Datasets
Embedding data
RAG-related content
AI experiments
Generated artifacts
Backups
antioch/nas/Backups

Dedicated backup storage.

The environment currently includes a dedicated backup location for the AI server:

antioch/nas/Backups/macmini-ai

Backup storage is kept separate from active application and media workloads.

KnowledgeBase
antioch/nas/KnowledgeBase

Dedicated storage for knowledge-base content.

This dataset is intended to support future AI/RAG infrastructure.

Possible workloads include:

Documentation
Technical references
Homelab documentation
Indexed documents
RAG source material
Embedding pipelines
AI knowledge repositories
Monitoring
antioch/nas/Monitoring

Dedicated storage for monitoring-related data.

This separation makes it possible to manage monitoring data independently from media and general NAS storage.

homes
antioch/nas/homes

User home directories are stored separately from application and media data.

media
antioch/nas/media

The primary media dataset.

This dataset contains the main media collection used by the media-server infrastructure.

npm
antioch/nas/npm

Storage used by Nginx Proxy Manager.

The dataset contains:

npm
├── data
└── letsencrypt
stepca
antioch/nas/stepca

Storage associated with the internal Smallstep Certificate Authority.

Storage Pool: papyri

papyri is a secondary ZFS storage pool.

Current status:

State: ONLINE
Layout: mirror-0
Used: approximately 2.81 TB
Available: approximately 2.52 TB

The pool currently reports:

Errors: No known data errors

The primary data hierarchy is:

papyri
└── nas2
    └── media2

The media2 dataset provides additional media storage.

Boot Pool

TrueNAS uses a dedicated ZFS boot pool:

boot-pool

Current status:

State: ONLINE

The boot pool contains the TrueNAS operating system and boot environments.

The current active TrueNAS version is:

25.10.7

Previous boot environments are retained as part of the TrueNAS upgrade and rollback mechanism.

This allows previous system environments to remain available if a rollback is required after an upgrade.

ZFS Health and Maintenance

ZFS provides several important data-integrity mechanisms:

Copy-on-write
End-to-end checksumming
Mirrored storage
Scrubbing
Resilvering
Snapshots
Replication
Dataset-level management

Pool health is checked using:

sudo zpool status

Dataset usage is checked using:

sudo zfs list
ZFS Scrubbing

ZFS scrubs are used to verify stored data against filesystem checksums.

Recent scrub results include:

antioch

The pool recently completed a successful resilver:

Resilvered: approximately 5.61 TB
Duration: approximately 12 hours 19 minutes
Errors: 0
papyri

The most recent scrub reported:

Repaired: approximately 369 MB
Errors: 0

Although the final result reported no unrecoverable errors, repaired data should be investigated when detected.

boot-pool

The most recent scrub reported:

Repaired: 0 B
Errors: 0
Container Infrastructure

TrueNAS Apps are backed by a Docker-based application environment.

The currently running containers include infrastructure, monitoring, security, and media services.

Current application architecture:

                    TrueNAS
                       │
                 TrueNAS Apps
                       │
                    Docker
                       │
       ┌───────────────┼────────────────┐
       │               │                │
   Monitoring       Security          Media
       │               │                │
 Prometheus        Nginx Proxy       Plex
 Grafana           Manager           Sonarr
 Node Exporter     Step-CA            Radarr
 Smartctl                             Prowlarr
 Graphite                            qBittorrent
                                     Bazarr
                                     Seerr
                                     FlareSolverr
Monitoring Stack

The monitoring architecture consists of Prometheus, Grafana, and several exporters.

                     TrueNAS
                        │
        ┌───────────────┼────────────────┐
        │               │                │
        ▼               ▼                ▼
 Node Exporter    Smartctl Exporter   Applications
        │               │                │
        └───────────────┼────────────────┘
                        │
                        ▼
                   Prometheus
                        │
                        ▼
                     Grafana
                        │
                        ▼
                  Dashboards
Prometheus

Prometheus is the primary time-series monitoring system.

Current image:

prom/prometheus:v3.14.0

Prometheus is responsible for collecting metrics from infrastructure and application exporters.

The monitoring architecture is designed to provide visibility into:

CPU utilization
Memory utilization
Network traffic
Filesystem usage
Disk health
ZFS health
Application availability
Container health
Infrastructure performance
Grafana

Grafana provides visualization and dashboards for Prometheus metrics.

Current image:

grafana/grafana:13.2.1

Grafana is used to visualize:

System performance
Storage utilization
Disk health
Container status
Application metrics
Infrastructure trends
Monitoring alerts
Node Exporter

Node Exporter exposes host-level operating-system metrics to Prometheus.

Current image:

prom/node-exporter:latest

Typical metrics include:

CPU usage
Memory usage
Filesystem usage
Network statistics
Disk statistics
System load
Operating-system metrics
Smartctl Exporter

Smartctl Exporter exposes SMART disk information to Prometheus.

Current image:

prometheuscommunity/smartctl-exporter:latest

This provides visibility into physical disk health.

Potential monitored indicators include:

Disk temperature
SMART health
Reallocated sectors
Read/write errors
Device statistics
Power-on information
Other SMART attributes

Monitoring SMART data is particularly important for a storage server because disk health directly affects ZFS redundancy.

Graphite Exporter

Graphite Exporter provides compatibility with metrics using the Graphite protocol.

Current image:

prom/graphite-exporter:latest

It allows Graphite-formatted metrics to be integrated into the Prometheus monitoring ecosystem.

Reverse Proxy

The homelab uses Nginx Proxy Manager as the reverse proxy layer.

Current image:

jc21/nginx-proxy-manager:2.15.1

The reverse proxy provides:

Service routing
HTTPS termination
Internal hostname access
Certificate management
Centralized application access

The architecture allows services to be accessed through consistent hostnames rather than requiring users to remember individual application ports.

Internal Certificate Authority

The environment includes Smallstep Step-CA.

Current image:

smallstep/step-ca:latest

Step-CA provides an internal Certificate Authority for the homelab.

This infrastructure is used to support trusted TLS certificates for internal services.

The internal PKI architecture allows the homelab to provide HTTPS services without depending entirely on publicly issued certificates.

Media Infrastructure

TrueNAS hosts a complete media automation stack.

The architecture can be represented as:

                  User Request
                       │
                       ▼
                     Seerr
                       │
                       ▼
                    Prowlarr
                       │
                       ▼
                   Indexers
                       │
                       ▼
                 Sonarr / Radarr
                       │
                       ▼
                  qBittorrent
                       │
                       ▼
                    Storage
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
          Sonarr               Radarr
             │                   │
             └─────────┬─────────┘
                       │
                       ▼
                     Plex
                       │
                       ▼
                    Clients

Additional services provide subtitle management and compatibility with indexers.

Media Applications
Plex

Image:

plexinc/pms-docker:plexpass

Plex provides media library management and streaming.

Sonarr

Image:

ghcr.io/home-operations/sonarr:4.0.19.3009

Sonarr manages television-series acquisition and organization.

Radarr

Image:

ghcr.io/home-operations/radarr:6.4.3.10645

Radarr manages movie acquisition and organization.

Prowlarr

Image:

ghcr.io/home-operations/prowlarr:2.6.3.5592

Prowlarr provides centralized indexer management for applications such as Sonarr and Radarr.

qBittorrent

Image:

ghcr.io/home-operations/qbittorrent:5.2.3

qBittorrent provides the download layer used by the media automation stack.

Bazarr

Image:

ghcr.io/home-operations/bazarr:1.6.0

Bazarr manages subtitles for supported media libraries.

Seerr

Image:

ghcr.io/seerr-team/seerr:v3.4.1

Seerr provides a user-facing media request interface.

FlareSolverr

Image:

flaresolverr/flaresolverr:v3.5.0

FlareSolverr provides browser challenge handling functionality for compatible services.

Application Health

The current application environment uses Docker health checks where supported.

Healthy application status is important because container availability alone does not necessarily indicate that an application is functioning correctly.

The monitoring strategy therefore considers:

Container Running
       │
       ▼
Container Health
       │
       ▼
Application Endpoint
       │
       ▼
Application Metrics
       │
       ▼
User Experience
Backup Architecture

The primary backup dataset is:

antioch/nas/Backups

A dedicated backup location exists for the AI server:

antioch/nas/Backups/macmini-ai

The backup architecture is intended to separate backup data from active workloads.

Future improvements include:

Automated backup verification
Backup monitoring
Snapshot automation
Off-site backup
Disaster recovery documentation
Restore testing
Backup integrity verification
Configuration backup automation

A backup strategy should ultimately be validated through regular restoration tests.

AI Infrastructure Storage

The TrueNAS infrastructure already includes dedicated storage for future AI workloads.

antioch/nas/AIStorage
antioch/nas/KnowledgeBase

These datasets provide the foundation for local AI applications.

Potential architecture:

                    AIStorage
                       │
          ┌────────────┼────────────┐
          │            │            │
      Documents     Datasets     Artifacts
          │
          ▼
                   KnowledgeBase
                       │
                       ▼
                    Embeddings
                       │
                       ▼
                  Vector Database
                       │
                       ▼
                       RAG
                       │
                       ▼
                     LLM
                       │
                       ▼
                  AI Assistant

This architecture will eventually connect the NAS storage layer to the local AI platform.

Infrastructure Observability

The monitoring strategy is organized into several layers.

Host

Monitor:

CPU
Memory
Load
Network
Filesystems
Storage

Monitor:

ZFS pool health
Pool capacity
Dataset utilization
Disk health
SMART information
Scrub status
Resilver operations
Containers

Monitor:

Container availability
Health status
Restarts
Resource utilization
Application endpoints
Applications

Monitor:

Service availability
Application metrics
Errors
Logs
Performance
Troubleshooting Methodology

Troubleshooting follows a layered approach.

Hardware
   │
   ▼
ZFS / Storage
   │
   ▼
TrueNAS
   │
   ▼
Docker Runtime
   │
   ▼
Container
   │
   ▼
Application
   │
   ▼
Network
   │
   ▼
Reverse Proxy
   │
   ▼
Client

When troubleshooting an application, the first step is to determine which layer is failing.

For example, if an application cannot access a file:

Verify the ZFS pool.
Verify the dataset.
Verify the mount point.
Verify permissions.
Verify the container.
Verify the container mount.
Verify the application configuration.
Inspect application logs.
Verify network connectivity if applicable.
Verify reverse-proxy configuration if the service is accessed through a proxy.

This approach prevents application-level troubleshooting when the actual problem exists at the storage or infrastructure layer.

Useful Administrative Commands
Check TrueNAS version
sudo midclt call system.version
Check ZFS pools
sudo zpool status
List ZFS datasets
sudo zfs list
List running containers
sudo docker ps
List containers with useful information
sudo docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"
Check Docker logs
sudo docker logs <container>
Follow Docker logs
sudo docker logs -f <container>
Security

The TrueNAS environment is designed primarily as an internal homelab infrastructure.

Security principles include:

Internal-only services where possible
HTTPS for internal applications
Reverse proxy architecture
Internal Certificate Authority
Restricted administrative access
Separation of application and data storage
Monitoring and observability
Regular system updates
Backup and recovery planning
Avoiding secrets in source control

The public GitHub repository intentionally does not contain:

Passwords
API tokens
Private keys
TLS private keys
Authentication secrets
Disk UUIDs
Sensitive network information
Personal credentials
Private application configuration

Sensitive values should always be stored outside Git.

Infrastructure as Code Direction

The current environment contains a mixture of declarative configuration, TrueNAS-managed applications, Docker configuration, and manual administration.

A long-term objective is to increase reproducibility through:

Docker Compose
Version-controlled configuration
Python automation
Shell scripts
API-based administration
Infrastructure-as-Code practices
Automated deployment
Configuration validation
CI/CD

The goal is to progressively reduce manual configuration.

Automation Opportunities

The TrueNAS infrastructure provides several opportunities for automation.

Potential Python automation projects include:

Python
  │
  ├── ZFS health checker
  ├── Disk health analyzer
  ├── Dataset capacity monitor
  ├── Docker health checker
  ├── Backup verification
  ├── Prometheus API client
  ├── Infrastructure report generator
  └── AI diagnostic assistant

These projects provide practical opportunities to combine existing infrastructure knowledge with Python development.

AI-Assisted Infrastructure Monitoring

A major future project for this homelab is an AI Infrastructure Monitoring Agent.

The planned architecture is:

                     TrueNAS
                        │
                        ▼
                  Infrastructure
                      Metrics
                        │
                        ▼
                   Prometheus
                        │
                        ▼
                  Python Service
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
       Metrics        Logs       Documentation
          │             │             │
          └─────────────┼─────────────┘
                        ▼
                    RAG System
                        │
                        ▼
                  Local LLM
                        │
                        ▼
                AI Infrastructure
                     Agent
                        │
              ┌─────────┼─────────┐
              │         │         │
              ▼         ▼         ▼
           Analyze   Diagnose   Recommend

The system is intended to eventually:

Detect abnormal infrastructure metrics
Identify potential failures
Correlate multiple events
Analyze application logs
Query infrastructure documentation
Explain possible root causes
Generate diagnostic recommendations
Assist with incident investigation
Produce infrastructure health reports

This project connects traditional infrastructure engineering with AI Engineering and MLOps.

Reliability Principles

The infrastructure follows several reliability principles.

Redundancy

Important storage pools use mirrored VDEVs.

Integrity

ZFS checksumming and scrubbing are used to detect data corruption.

Observability

Prometheus and Grafana provide centralized infrastructure monitoring.

Isolation

Application, backup, media, monitoring, and AI workloads are logically separated.

Recovery

Boot environments and backup infrastructure provide recovery mechanisms.

Documentation

Infrastructure decisions and operational procedures are documented in version control.

Automation

Repeated manual operations are candidates for automation.

Capacity Management

Storage capacity is actively monitored because the environment contains several high-growth workloads, particularly media storage.

The main capacity areas are:

antioch
├── media
├── application data
├── backups
├── monitoring
└── AI workloads

papyri
└── media2

Future monitoring improvements should include:

Dataset growth rate
Pool capacity thresholds
Forecasted capacity exhaustion
Alerting for low free space
Media growth monitoring
Backup growth monitoring
AI dataset growth monitoring
Disaster Recovery

A complete disaster recovery procedure is a future development item.

The intended recovery process will document:

Hardware Recovery
       │
       ▼
TrueNAS Installation
       │
       ▼
Pool Import
       │
       ▼
Configuration Recovery
       │
       ▼
Application Recovery
       │
       ▼
Data Recovery
       │
       ▼
Monitoring Recovery
       │
       ▼
Service Validation

Future documentation will include:

TrueNAS configuration backup
ZFS pool recovery
Dataset recovery
Application recovery
Docker recovery
Reverse proxy recovery
Certificate authority recovery
Monitoring recovery
AI infrastructure recovery
Operational Philosophy

This homelab is treated as a real infrastructure environment rather than only a collection of applications.

The main objectives are:

Reliability
Observability
Security
Reproducibility
Automation
Documentation
Continuous learning

The infrastructure provides a practical environment for developing skills in:

Linux administration
Storage administration
ZFS
Networking
Docker
Monitoring
Observability
Python
Automation
Cloud concepts
AI infrastructure
RAG
LLMs
MLOps
Technology Evolution

The homelab follows a progressive technology path:

IT Infrastructure
       │
       ▼
Linux Administration
       │
       ▼
Networking
       │
       ▼
Storage / ZFS
       │
       ▼
Docker
       │
       ▼
Monitoring
       │
       ▼
Python Automation
       │
       ▼
Cloud Infrastructure
       │
       ▼
AI Applications
       │
       ▼
LLMs / RAG
       │
       ▼
AI Agents
       │
       ▼
MLOps
       │
       ▼
AI Infrastructure

The goal is to use the homelab as a practical environment for continuously developing and demonstrating these skills.

Future Improvements

Planned improvements include:

 Expand Prometheus monitoring
 Create dedicated Grafana dashboards
 Add ZFS-specific dashboards
 Improve SMART monitoring
 Monitor dataset growth
 Add storage capacity forecasting
 Monitor container resources
 Improve application health monitoring
 Automate backup verification
 Implement restore testing
 Document disaster recovery procedures
 Improve infrastructure configuration management
 Automate common maintenance tasks
 Develop Python infrastructure tools
 Develop an AI infrastructure monitoring agent
 Integrate Prometheus with AI analysis
 Integrate the KnowledgeBase with RAG
 Implement infrastructure documentation retrieval
 Add CI/CD for infrastructure tools
 Introduce Infrastructure-as-Code practices
 Expand MLOps capabilities
Current Status

Status: Active Development

The TrueNAS infrastructure is operational and continuously evolving.

Current major capabilities include:

ZFS mirrored storage
Multiple storage pools
NAS services
Docker applications
Media automation
Prometheus monitoring
Grafana dashboards
SMART monitoring
Node-level monitoring
Reverse proxy
Internal PKI
Backup storage
AI storage
Knowledge-base storage

The next phase is focused on increasing automation, observability, reproducibility, and AI integration.

Related Documentation
Architecture Overview
Network Architecture
AI Stack
Storage Architecture
Docker Infrastructure
Prometheus Monitoring
Grafana Monitoring
Repository

This documentation is part of the:

AI Homelab Infrastructure

repository.

The purpose of the repository is to document the evolution of a real-world homelab from traditional IT infrastructure toward automation, AI Engineering, and MLOps.
