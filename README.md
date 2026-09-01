# AI Homelab Infrastructure

![Status](https://img.shields.io/badge/status-active-success)
![Linux](https://img.shields.io/badge/Linux-Systems-orange)
![Docker](https://img.shields.io/badge/Docker-Containers-blue)
![Python](https://img.shields.io/badge/Python-Development-yellow)
![AI](https://img.shields.io/badge/AI-LLM%20%7C%20RAG%20%7C%20Agents-purple)

## Overview

This repository documents my personal AI Homelab infrastructure, created as a practical environment for learning, experimentation and development in **IT Infrastructure, Linux, Networking, DevOps, Cloud and Artificial Intelligence**.

The goal is to build and operate real services rather than only studying them theoretically.

The environment includes infrastructure services, containerized applications, monitoring, storage, networking and locally hosted AI services.

## Objectives

* Develop practical Linux administration skills
* Build and maintain containerized services using Docker
* Improve networking and infrastructure skills
* Implement monitoring and observability
* Develop Python automation tools
* Build local AI applications
* Experiment with LLMs, RAG and AI Agents
* Develop MLOps and AI infrastructure skills
* Document infrastructure and troubleshooting procedures
* Build a professional portfolio for a career in Cloud, AI Engineering and MLOps

## Main Technologies

### Infrastructure

* TrueNAS
* Linux
* Docker
* Virtualization
* NAS / Network Storage
* Backup
* Networking
* Firewalls

### Monitoring

* Prometheus
* Grafana
* Node Exporter
* Smartctl Exporter
* ZFS Exporter

### AI

* Ollama
* Open WebUI
* Qdrant
* Large Language Models
* Embeddings
* Retrieval-Augmented Generation (RAG)
* AI Agents

### Automation & Development

* Python
* REST APIs
* n8n
* Git
* GitHub
* Docker Compose

## Architecture

The homelab is designed around several interconnected layers:

```text
                    USERS
                      │
                      ▼
                NETWORK / FIREWALL
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
      INFRASTRUCTURE          AI SERVICES
          │                       │
     ┌────┴────┐             ┌────┴─────┐
     │         │             │          │
   TrueNAS   Docker       Ollama     Qdrant
     │         │             │          │
     │     ┌───┴────┐        └────┬─────┘
     │     │        │             │
     │    n8n   Open WebUI       RAG
     │
     ▼
  STORAGE

              MONITORING
                  │
          ┌───────┴───────┐
          ▼               ▼
      Prometheus        Grafana
```

## Repository Structure

```text
docs/          Infrastructure documentation
docker/        Container configurations
python/        Python tools and AI applications
scripts/       Automation and maintenance scripts
configs/       Service configuration files
diagrams/      Infrastructure diagrams
```

## Projects

### AI Infrastructure

Coming soon.

### RAG Knowledge Base

Coming soon.

### AI Infrastructure Monitoring Agent

Coming soon.

### Python Infrastructure Tools

Coming soon.

## Documentation

Detailed documentation will be added progressively as the infrastructure evolves.

Topics include:

* Network architecture
* Storage architecture
* Docker services
* AI services
* Monitoring
* Backup
* Security
* Troubleshooting
* Automation

## Security

Sensitive information is intentionally excluded from this repository.

The repository will never contain:

* Passwords
* API keys
* Private certificates
* SSH private keys
* Authentication tokens
* Private network credentials
* Sensitive configuration data

Public documentation will use sanitized examples where necessary.

## Roadmap

* [x] Create AI Homelab repository
* [ ] Document infrastructure architecture
* [ ] Document network architecture
* [ ] Document Docker environment
* [ ] Document monitoring stack
* [ ] Document AI stack
* [ ] Create Python infrastructure tools
* [ ] Build RAG application
* [ ] Build AI Agent
* [ ] Integrate AI with infrastructure monitoring
* [ ] Deploy AI services to cloud
* [ ] Develop MLOps pipeline

## About

This project is part of my professional development in **Cloud Computing, Infrastructure, DevOps, Artificial Intelligence and MLOps**.

It represents practical, continuously evolving work performed in a real homelab environment.

---

**Author:** Fabiano Quintino
