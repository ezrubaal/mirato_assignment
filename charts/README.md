# Resource Injector Helm Chart

## Description
This Helm chart deploys the Resource Injector application, which ensures Kubernetes pods have default CPU and memory resource requests and limits.

## Prerequisites
- Kubernetes 1.16+
- Helm 3.x

## Installation
To install the chart with the release name `my-release`:

- ```bash
- helm install my-release ./resource-injector

## Configuration
- The following table lists configurable parameters and their default values:

Parameter	                    Description	                            Default
replicaCount	                Number of replicas	                    1
image.repository	            Docker image repository	                your-docker-registry/resource-injector
image.tag	                    Image tag	                            latest
image.pullPolicy	            Image pull policy	                    IfNotPresent
defaultResources.cpuRequest	    Default CPU request for containers	    500m
defaultResources.memoryRequest	Default memory request for containers	512Mi
defaultResources.cpuLimit	    Default CPU limit for containers	    1000m
defaultResources.memoryLimit	Default memory limit for containers	    1Gi

## Uninstallation
- To uninstall the chart:

- ```bash
- Copy
- Edit
- helm uninstall my-release
