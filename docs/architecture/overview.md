# Homelab Architecture Overview

## Purpose

This document provides a high-level overview of the AI Homelab infrastructure.

The environment is designed to provide a practical platform for infrastructure administration, containerized services, monitoring, automation and artificial intelligence experimentation.

## Main Infrastructure Components

The environment is composed of:

* Network infrastructure
* Firewall
* Storage
* Linux systems
* Docker containers
* Monitoring services
* AI services
* Automation services

## Logical Architecture

```text
                         CLIENTS
                            │
                            ▼
                    NETWORK / FIREWALL
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
          INFRASTRUCTURE            AI PLATFORM
                │                       │
        ┌───────┴───────┐       ┌───────┴────────┐
        │               │       │                │
      Storage        Services  LLM            Vector DB
        │               │       │                │
      NAS          Docker      Ollama           Qdrant
                        │
              ┌─────────┼─────────┐
              │         │         │
             n8n    Open WebUI  Monitoring
                                  │
                           Prometheus/Grafana
```

## Design Principles

The homelab follows several principles:

1. Services should be isolated whenever practical.
2. Infrastructure should be reproducible.
3. Configuration should be documented.
4. Sensitive information must never be committed to the repository.
5. Monitoring should be implemented for important services.
6. AI services should be deployable independently from infrastructure services.
7. Changes should be tracked using Git.

## Current Status

The infrastructure is continuously evolving.

This repository documents the current state and the changes made during the development of the environment.

