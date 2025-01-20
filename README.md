# Resource Injector

## Overview
The Resource Injector is a Kubernetes-native tool designed to ensure all Pods and Deployments have resource requests and limits defined. It leverages a Mutating Admission Webhook to inject default resource values where missing.

## Features
- Monitors Kubernetes API for new Pods/Deployments.
- Injects default resource requests/limits.
- Logs actions and exposes metrics via Prometheus.

## Configuration
Default resource values can be set via:
1. Environment variables.
2. ConfigMap or Helm chart values.

### Environment Variables
- `DEFAULT_CPU_REQUEST`: Default CPU request (e.g., `500m`).
- `DEFAULT_MEMORY_REQUEST`: Default memory request (e.g., `512Mi`).
- `DEFAULT_CPU_LIMIT`: Default CPU limit (e.g., `1000m`).
- `DEFAULT_MEMORY_LIMIT`: Default memory limit (e.g., `1Gi`).

## Deployment
1. Build the Docker image:
   ```bash
   docker build -t resource-injector:latest .
2. Deploy using Helm:
   ```bash
    Copy
    Edit
    helm install resource-injector ./charts/resource-injector
3. Apply manifests:
   ```bash
    Copy
    Edit
    kubectl apply -f manifests/