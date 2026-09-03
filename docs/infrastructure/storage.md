# Storage Architecture

## Overview

The homelab uses **OpenZFS** as its primary storage technology, managed through TrueNAS SCALE.

The storage architecture is designed around:

- Data integrity
- Disk redundancy
- Dataset isolation
- Capacity management
- Backup separation
- Monitoring
- Recovery
- Future automation

The current TrueNAS environment contains two primary data pools and one boot pool:

```text
                    TrueNAS Storage
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
       antioch        papyri        boot-pool
          │              │              │
          │              │              └── TrueNAS OS
          │              │
          │              └── Secondary Media
          │
          ├── Applications
          ├── NAS Data
          ├── Media
          ├── Backups
          ├── Monitoring
          └── AI Storage

Storage Technology

The storage platform is based on ZFS, providing:

Copy-on-write
End-to-end checksumming
Storage redundancy
Scrubbing
Resilvering
Snapshots
Replication
Dataset-level management
Compression support
Quotas and reservations
Detailed storage statistics

ZFS is particularly well suited to a homelab because it combines filesystem and storage-management functionality in a single architecture.

Storage Pools

The current TrueNAS system contains:

Pool	Purpose	Layout	Status
antioch	Primary NAS and applications	Mirror	ONLINE
papyri	Secondary media storage	Mirror	ONLINE
boot-pool	TrueNAS operating system	Boot device	ONLINE
Pool: antioch

antioch is the primary storage pool.

Pool: antioch
Layout: mirror
Status: ONLINE
Used: approximately 5.67 TB
Available: approximately 3.29 TB

The pool currently reports:

READ:   0
WRITE:  0
CKSUM:  0

and:

No known data errors

The pool is configured as a two-disk mirror.

              antioch
                 │
             mirror-0
             ┌────┴────┐
             │         │
          Disk A     Disk B

The mirror provides redundancy for the pool.

If one disk fails, the pool can continue operating while the failed disk is replaced.

antioch Capacity

Current approximate capacity:

Used:      5.67 TB
Available: 3.29 TB

This means the pool still has significant free capacity, but capacity monitoring is important because several workloads have high growth rates.

The primary growth areas include:

Media
Backups
Monitoring data
AI datasets
Knowledge-base content
Application data
antioch Dataset Architecture

The primary pool is divided into logical datasets.

antioch
│
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

Dataset separation allows different workloads to have independent:

Permissions
Snapshots
Replication
Backup policies
Quotas
Compression settings
Retention policies
Application Storage

TrueNAS Apps use:

antioch/ix-apps

The major application datasets are:

antioch/ix-apps/app_configs
antioch/ix-apps/app_mounts
antioch/ix-apps/docker
antioch/ix-apps/truenas_catalog

The application storage hierarchy is intentionally separated from the main NAS data.

This reduces the risk of mixing application runtime data with user data and makes storage management easier.

NAS Storage

General NAS data is stored under:

antioch/nas

The dataset contains several specialized workloads.

AIStorage
antioch/nas/AIStorage

This dataset is reserved for AI-related storage.

Potential workloads include:

AI datasets
Documents
AI application data
RAG source material
Embedding data
Generated artifacts
Model-related data

The dedicated dataset provides a foundation for future AI infrastructure.

KnowledgeBase
antioch/nas/KnowledgeBase

The KnowledgeBase dataset is intended to store information that can be consumed by future RAG systems.

Possible content includes:

Technical documentation
Homelab documentation
Configuration references
Troubleshooting guides
Manuals
Structured knowledge
Research material

Future architecture:

Documents
    │
    ▼
KnowledgeBase
    │
    ▼
Document Processing
    │
    ▼
Chunking
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
Local LLM
Media Storage

The main media dataset is:

antioch/nas/media

This dataset contains the primary media collection.

The media automation infrastructure includes:

Plex
Sonarr
Radarr
Prowlarr
qBittorrent
Bazarr
Seerr

Media storage represents one of the largest consumers of capacity in the primary pool.

For this reason, monitoring media growth is an important part of capacity management.

Backup Storage

Backup data is stored under:

antioch/nas/Backups

A dedicated location exists for the AI server:

antioch/nas/Backups/macmini-ai

Keeping backups in a separate dataset allows backup-specific policies to be implemented independently.

Future improvements include:

Automated backup verification
Snapshot-based backups
Restore testing
Off-site replication
Backup monitoring
Disaster recovery automation
Monitoring Storage

Monitoring data is stored under:

antioch/nas/Monitoring

This separates monitoring data from application and media data.

Monitoring workloads include:

Prometheus
Grafana
Node Exporter
Smartctl Exporter
Graphite Exporter

Future improvements include retention policies based on workload and capacity.

Network Service Storage

Nginx Proxy Manager uses:

antioch/nas/npm

with:

npm
├── data
└── letsencrypt

The separation allows proxy configuration and certificate-related data to remain independent from other NAS workloads.

Certificate Authority Storage

The internal Step-CA service uses:

antioch/nas/stepca

This dataset contains data associated with the internal Certificate Authority.

Because certificate infrastructure is security-sensitive, this dataset should receive appropriate permissions, backup protection, and recovery planning.

Pool: papyri

papyri is the secondary storage pool.

Pool: papyri
Layout: mirror
Status: ONLINE
Used: approximately 2.81 TB
Available: approximately 2.52 TB

The pool is configured as:

              papyri
                 │
             mirror-0
             ┌────┴────┐
             │         │
          Disk A     Disk B

The pool currently reports no known data errors.

papyri Dataset Architecture

The primary data hierarchy is:

papyri
└── nas2
    └── media2

The media2 dataset provides additional storage for media workloads.

This creates a separation between the primary media dataset on antioch and the secondary media storage on papyri.

Boot Storage

The TrueNAS operating system is installed on:

boot-pool

The boot pool is separate from the primary data pools.

Its purpose is to store:

TrueNAS operating system
System configuration
Boot environments
System files
Logs

The current system version is:

TrueNAS SCALE 25.10.7

Multiple boot environments are maintained, providing rollback capability during system upgrades.

ZFS Mirror Design

Both primary storage pools use mirrored VDEVs.

A mirror can be represented as:

                 ZFS Pool
                    │
                 Mirror
                /      \
               /        \
          Disk A        Disk B

Data is written redundantly across the mirror.

Advantages include:

Disk redundancy
Continued operation after a single disk failure
Straightforward disk replacement
Good read performance
Simple storage topology

The primary trade-off is usable capacity.

A two-disk mirror provides approximately the capacity of one disk rather than the combined capacity of both disks.

Resilvering

When a disk is replaced in a mirror, ZFS performs a resilver operation.

A recent antioch resilver completed with:

Data resilvered: approximately 5.61 TB
Duration: approximately 12 hours 19 minutes
Errors: 0

The successful resilver demonstrates that the mirror was able to reconstruct the required data without reporting errors.

Resilver operations should be monitored because the pool operates in a degraded state while redundancy is being restored.

ZFS Scrubbing

ZFS scrubbing periodically verifies stored data against filesystem checksums.

A scrub can detect:

Silent data corruption
Disk read errors
Checksum mismatches
Data inconsistencies

Recent results include:

antioch

The pool recently completed a resilver successfully:

Resilvered: approximately 5.61 TB
Errors: 0
papyri

The latest scrub reported:

Repaired: approximately 369 MB
Errors: 0

Although no unrecoverable errors were reported, repaired data should be investigated and monitored.

boot-pool

The latest scrub reported:

Repaired: 0 B
Errors: 0
Storage Integrity

ZFS uses checksums to detect corrupted data.

The basic integrity model is:

Application
    │
    ▼
Filesystem
    │
    ▼
ZFS Checksum
    │
    ▼
Storage Device

When data is read, ZFS can verify that the retrieved data matches its expected checksum.

With redundant storage, ZFS can use another copy to recover corrupted data when possible.

This is one of the major advantages of ZFS compared with traditional filesystems.

Snapshots

Snapshots are an important component of the future storage strategy.

A snapshot captures the state of a ZFS dataset at a specific point in time without requiring a traditional full copy.

Potential snapshot targets include:

antioch/nas/AIStorage
antioch/nas/KnowledgeBase
antioch/nas/Backups
antioch/nas/Monitoring
antioch/nas/npm
antioch/nas/stepca

Snapshot policies should be based on workload importance and recovery requirements.

For example:

Critical Configuration
    │
    ├── Frequent snapshots
    ├── Longer retention
    └── Replication

General Data
    │
    ├── Daily snapshots
    └── Moderate retention

Large Media
    │
    ├── Lower snapshot frequency
    └── Shorter retention
Backup vs Snapshot

Snapshots and backups serve different purposes.

Snapshot

A snapshot protects against:

Accidental deletion
Configuration mistakes
File corruption
Short-term recovery
Backup

A backup protects against:

Pool failure
Hardware failure
Disaster
Accidental pool destruction
Major infrastructure failure

A snapshot should therefore not be considered a replacement for an independent backup.

Backup Strategy

The current architecture includes:

Active Data
    │
    ▼
ZFS Storage
    │
    ├── Snapshots
    │
    └── Backups
             │
             ▼
        Backup Storage

Future improvements should follow the principle that important data should have more than one independent copy.

The eventual goal is to implement a strategy based on:

Production Data
      │
      ├── Local Snapshot
      │
      ├── Local Backup
      │
      └── Off-site Backup
Capacity Management

Storage capacity is monitored because the environment contains high-growth workloads.

The primary capacity consumers are:

Media
Application data
Backups
Monitoring data
AI datasets

Capacity monitoring should consider both current usage and growth rate.

For example:

Current Usage
      │
      ▼
Historical Growth
      │
      ▼
Growth Rate
      │
      ▼
Capacity Forecast
      │
      ▼
Alert Before Critical Threshold

Future monitoring should provide alerts before a pool reaches critical utilization.

Recommended Capacity Thresholds

The exact thresholds should be adjusted according to workload.

A practical starting point is:

< 70%     Normal
70–80%    Monitor
80–90%    Planning required
> 90%     Immediate action

The purpose is to avoid reaching a situation where storage exhaustion becomes an operational incident.

Storage Monitoring

The storage architecture is integrated with the monitoring stack.

                     ZFS
                      │
          ┌───────────┴───────────┐
          │                       │
       Pool Health             Disk Health
          │                       │
          ▼                       ▼
     zpool status             SMART data
          │                       │
          └───────────┬───────────┘
                      ▼
                 Prometheus
                      │
                      ▼
                   Grafana

Important metrics include:

Pool state
Dataset capacity
Disk temperature
SMART health
Read errors
Write errors
Checksum errors
Scrub status
Resilver status
Storage growth
Operational Commands
Check pool health
sudo zpool status
List pools
sudo zpool list
List datasets
sudo zfs list
Check pool capacity
sudo zpool list
Get detailed ZFS properties
sudo zfs get all <dataset>
Check pool history
sudo zpool history
Storage Troubleshooting

The recommended troubleshooting sequence is:

Pool Health
    │
    ▼
VDEV Health
    │
    ▼
Disk Health
    │
    ▼
Dataset Health
    │
    ▼
Permissions
    │
    ▼
Application Mount
    │
    ▼
Application

For storage-related problems:

1. Check pool status
sudo zpool status

Look for:

DEGRADED
FAULTED
UNAVAIL
READ errors
WRITE errors
CHECKSUM errors
2. Check capacity
sudo zpool list
sudo zfs list
3. Check disk health

Use SMART monitoring and:

sudo smartctl -a /dev/<device>
4. Check dataset
sudo zfs list
5. Check application mounts

Verify that the container has access to the expected dataset.

Failure Scenarios
Single Disk Failure

With a two-disk mirror:

       Mirror
       /    \
      X      ✓
   Failed   Online

The pool can continue operating in a degraded state.

The failed disk should be replaced as soon as practical.

Two Disk Failures

If both members of a two-disk mirror fail:

       Mirror
       /    \
      X      X

The pool cannot provide normal access to the data.

This demonstrates why redundancy alone is not a backup.

Recovery Strategy

The storage recovery strategy should eventually document:

Identify failed disk.
Confirm pool state.
Replace failed disk.
Start resilver.
Monitor resilver progress.
Confirm pool returns to ONLINE.
Run or schedule a scrub.
Verify application functionality.
Verify backups.

Example:

Disk Failure
     │
     ▼
Pool DEGRADED
     │
     ▼
Replace Disk
     │
     ▼
Resilver
     │
     ▼
Pool ONLINE
     │
     ▼
Scrub
     │
     ▼
Verify Data
Storage Security

Storage security includes:

Dataset permissions
Restricted administrative access
Internal network access
Backup protection
Certificate protection
Separation of workloads
Avoidance of credentials in Git

Sensitive storage information is intentionally excluded from this public repository.

The repository does not contain:

Disk UUIDs
Encryption keys
Passwords
API tokens
Private keys
Authentication secrets
Sensitive network configuration
Storage and AI

The storage architecture is designed to support future AI workloads.

The relationship between storage and AI is:

TrueNAS
   │
   ▼
AIStorage
   │
   ├── Documents
   ├── Datasets
   └── Artifacts
   │
   ▼
KnowledgeBase
   │
   ▼
Document Processing
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
Local LLM

This provides a persistent storage foundation for AI applications.

Storage and MLOps

The storage infrastructure can eventually support MLOps workloads including:

Dataset versioning
Model artifacts
Training data
Evaluation datasets
Experiment results
Feature data
RAG documents
Embeddings
Model deployment artifacts

A future architecture may look like:

                  TrueNAS
                     │
          ┌──────────┴──────────┐
          │                     │
      AIStorage            KnowledgeBase
          │                     │
          ▼                     ▼
      Datasets              Documents
          │                     │
          └──────────┬──────────┘
                     ▼
                  Python
                     │
                     ▼
              AI / ML Pipeline
                     │
          ┌──────────┼──────────┐
          │          │          │
          ▼          ▼          ▼
       Training   Evaluation   RAG
          │          │          │
          └──────────┼──────────┘
                     ▼
                  MLOps
Design Principles

The storage architecture follows these principles:

Redundancy

Important storage pools use mirrored VDEVs.

Integrity

ZFS checksumming and scrubbing provide protection against silent corruption.

Separation

Different workloads are separated into datasets.

Observability

Storage health is integrated into Prometheus and Grafana.

Recovery

Backups, snapshots, boot environments, and redundancy provide multiple recovery mechanisms.

Security

Sensitive storage information is not stored in the public repository.

Automation

Storage monitoring and operational tasks are candidates for Python and API-based automation.

Future Improvements
 Define formal snapshot policies
 Implement automated snapshot management
 Implement backup verification
 Test restoration procedures
 Implement off-site replication
 Improve ZFS monitoring
 Add pool capacity alerts
 Add dataset growth monitoring
 Add capacity forecasting
 Improve SMART alerting
 Document disk replacement procedures
 Document disaster recovery
 Automate storage health reports
 Integrate ZFS data with AI diagnostics
 Integrate storage documentation into RAG
 Develop AI-assisted storage troubleshooting
Current Status

Status: Active Development

The current storage infrastructure consists of:

TrueNAS SCALE 25.10.7
        │
        ├── antioch
        │     └── Mirror
        │
        ├── papyri
        │     └── Mirror
        │
        └── boot-pool

The primary storage architecture is operational and currently reports healthy pools with no known unrecoverable data errors.

The storage layer is continuously evolving toward greater:

Reliability
Observability
Automation
Recoverability
Security
AI integration
Related Documentation
TrueNAS Infrastructure
Docker Infrastructure
Architecture Overview
Network Architecture
AI Stack
Prometheus Monitoring
Grafana Monitoring
