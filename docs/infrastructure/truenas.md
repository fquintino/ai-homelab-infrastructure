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
