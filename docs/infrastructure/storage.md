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
