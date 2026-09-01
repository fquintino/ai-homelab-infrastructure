# Network Architecture

## Overview

The homelab network is designed to provide a controlled environment for infrastructure services, local AI applications, storage, monitoring and experimentation.

The network uses a dedicated firewall/router as the primary gateway and security layer.

## High-Level Architecture

```text
                         INTERNET
                            │
                            ▼
                       ISP / WAN
                            │
                            ▼
                       pfSense
                   Firewall / Router
                            │
                            ▼
                         LAN
                            │
                    ┌───────┴───────┐
                    │               │
                    ▼               ▼
                 Switch          Wi-Fi
                    │
          ┌─────────┼──────────┐
          │         │          │
          ▼         ▼          ▼
       TrueNAS    Mac Mini   Clients
          │         │
          │         │
          ▼         ▼
       Storage    Docker
                    │
        ┌───────────┼────────────┐
        │           │            │
        ▼           ▼            ▼
      Ollama      Qdrant        n8n
        │
        ▼
    Open WebUI

                    Monitoring
                        │
                ┌───────┴───────┐
                ▼               ▼
            Prometheus        Grafana
```

## Network Components

### Firewall

The firewall provides:

* Internet gateway
* Network routing
* Firewall rules
* NAT
* DHCP
* DNS integration
* VPN access

### Core Infrastructure

The main infrastructure systems include:

* TrueNAS storage server
* Mac mini AI server
* Docker services
* Network clients
* Monitoring services

### AI Infrastructure

The local AI environment includes:

* Ollama
* Open WebUI
* Qdrant
* n8n
* Python-based applications

### Monitoring

Infrastructure monitoring is provided by:

* Prometheus
* Grafana
* Node Exporter
* Smartctl Exporter
* ZFS Exporter

## Network Services

The homelab provides several internal services, including:

* DNS
* DHCP
* HTTP/HTTPS services
* SSH
* Docker networking
* VPN access
* Storage services
* Monitoring endpoints
* AI services

## Remote Access

Remote access is provided through a VPN connection.

Internal services are accessed using the homelab's internal DNS infrastructure.

Sensitive network information such as public IP addresses, credentials, private keys and authentication tokens is intentionally excluded from this repository.

## Security Considerations

The infrastructure follows basic security principles:

* Firewall-based network protection
* Restricted service exposure
* Internal DNS
* VPN for remote access
* Separation of services
* Container isolation
* Authentication where required
* No credentials stored in Git
* Sensitive configuration excluded from public documentation

## Future Improvements

Planned improvements include:

* Network segmentation
* VLAN implementation
* Improved firewall policies
* Centralized authentication
* Infrastructure-as-Code
* Automated backups
* Improved monitoring
* Security monitoring
* AI-assisted infrastructure monitoring

