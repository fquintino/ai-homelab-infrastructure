# Infrastructure Diagnostics

A Python-based diagnostic tool for the AI Homelab Infrastructure project.

The project is being developed incrementally as a practical Python and infrastructure engineering project.

## Objectives

The diagnostic tool will eventually collect and analyze information from:

* Operating system
* CPU
* Memory
* Storage
* Network
* Docker
* Prometheus
* Infrastructure services

The long-term goal is to evolve the tool into an AI-assisted infrastructure monitoring system.

## Current Version

**v0.1.0**

Current capabilities:

* Hostname detection
* Operating system detection
* Architecture detection
* Python version detection
* CPU information
* Memory information
* Root filesystem usage

## Requirements

* Python 3
* pip
* psutil

## Installation

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r python/diagnostics/requirements.txt
```

## Usage

Run:

```bash
python python/diagnostics/diagnostic.py
```

## Development Roadmap

### v0.1

Basic system diagnostics.

### v0.2

Network diagnostics:

* Network interfaces
* IP configuration
* Connectivity tests
* DNS resolution
* Default gateway

### v0.3

Docker diagnostics:

* Running containers
* Container status
* Restart counts
* CPU usage
* Memory usage

### v0.4

Prometheus integration:

* Query Prometheus
* Retrieve infrastructure metrics
* Analyze historical metrics

### v0.5

Structured output:

* JSON
* Machine-readable reports
* Exit codes
* Logging

### v0.6

FastAPI:

* REST API
* Diagnostic endpoints
* Health endpoint
* JSON responses

### v0.7

AI integration:

* Local LLM
* Infrastructure analysis
* Natural-language explanations

### v0.8

RAG:

* Qdrant
* Infrastructure documentation
* Troubleshooting knowledge base

### v1.0

AI Infrastructure Monitoring Agent.

Potential capabilities:

* Infrastructure health analysis
* Anomaly detection
* Metric analysis
* Container analysis
* Log analysis
* Troubleshooting recommendations
* Natural-language infrastructure queries

## Architecture

```text
Python Diagnostics
       │
       ├── System
       ├── CPU
       ├── Memory
       ├── Storage
       ├── Network
       └── Docker
              │
              ▼
          Prometheus
              │
              ▼
          AI Analysis
              │
              ▼
           Local LLM
```

## Portfolio Purpose

This project demonstrates practical experience with:

* Python
* Linux
* Infrastructure
* Networking
* Docker
* Monitoring
* Prometheus
* APIs
* AI
* RAG
* Observability
* MLOps

The project is developed against a real homelab environment rather than a purely theoretical example.