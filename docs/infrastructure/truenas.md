# TrueNAS Infrastructure

## Overview

TrueNAS is used as the primary storage and infrastructure platform in the homelab.

The system provides centralized storage, ZFS management, application hosting and supporting infrastructure services.

The TrueNAS environment is also used as a platform for experimentation with containers, monitoring and infrastructure automation.

## Main Responsibilities

The TrueNAS server provides:

* ZFS storage
* Network file storage
* Application hosting
* Docker-based services
* Backup storage
* Monitoring services
* Infrastructure experimentation

## Storage

The storage environment is based on ZFS.

ZFS provides:

* Data integrity
* Storage pools
* Datasets
* Snapshots
* Compression
* Redundancy
* Storage monitoring

The main storage pool is used to organize application data, configuration files, monitoring data and other homelab resources.

Sensitive storage details such as physical disk serial numbers and private configuration information are intentionally excluded from this repository.

## Applications

The TrueNAS environment hosts several services used by the homelab.

Examples include:

* Media management
* Download services
* Monitoring
* Storage-related services
* Network services
* Supporting infrastructure applications

Applications are isolated and managed independently whenever practical.

## Containerized Services

Containerized applications are used to simplify deployment, upgrades and service management.

The environment uses Docker-based workloads for services such as:

* Prometheus
* Grafana
* Node Exporter
* Smartctl Exporter
* ZFS Exporter
* Media applications
* Other infrastructure services

## Monitoring

The TrueNAS environment is monitored using Prometheus and Grafana.

Monitoring includes infrastructure and application metrics.

The monitoring architecture includes:

```text
                    TrueNAS
                       │
            ┌──────────┼──────────┐
            │          │          │
            ▼          ▼          ▼
          Node       Smartctl     ZFS
        Exporter     Exporter   Exporter
            │          │          │
            └──────────┼──────────┘
                       ▼
                  Prometheus
                       │
                       ▼
                    Grafana
```

## Backup Strategy

Backup procedures are designed to protect important application data and configurations.

The backup strategy will be documented separately as the infrastructure evolves.

Important considerations include:

* ZFS snapshots
* Configuration backups
* Application data backups
* Recovery procedures
* Off-system backups

## Security

The TrueNAS environment is protected by the homelab network firewall.

Security practices include:

* Restricted network access
* Authentication for administrative services
* Regular updates
* Limited service exposure
* Backup protection
* Monitoring
* No credentials stored in Git

## Troubleshooting

Infrastructure problems are documented as they are identified and resolved.

Future documentation will include practical troubleshooting procedures for:

* ZFS
* Docker
* Storage
* Networking
* Applications
* Monitoring
* Permissions
* Backup and recovery

## Future Improvements

Planned improvements include:

* Improved backup automation
* Infrastructure-as-Code
* Automated monitoring
* Security monitoring
* Better service isolation
* Automated configuration management
* AI-assisted infrastructure monitoring

