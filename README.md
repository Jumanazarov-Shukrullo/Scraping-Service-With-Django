# Django Application Deployment with Docker, Docker Compose, and Kubernetes

This repository contains a Django application that is containerized using Docker and can be deployed using Docker Compose and Kubernetes (Minikube and standard Kubernetes).

## Table of Contents
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [Docker](#docker)
  - [Docker Compose](#docker-compose)
- [Running Locally with Docker Compose](#running-locally-with-docker-compose)
- [Deploying to Minikube (k7s)](#deploying-to-minikube-k7s)
  - [Step 1: Start Minikube](#step-1-start-minikube)
  - [Step 2: Build Docker Images](#step-2-build-docker-images)
  - [Step 3: Apply Kubernetes Manifests](#step-3-apply-kubernetes-manifests)
- [Deploying to Kubernetes (k8s)](#deploying-to-kubernetes-k8s)
  - [Step 1: Apply Kubernetes Manifests](#step-1-using-kubectl-command)
- [Accessing the Application](#accessing-the-application)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- Docker
- Docker Compose
- Minikube
- kubectl

## Setup

### Docker

Ensure you have Docker installed on your local machine. You can download and install Docker from [here](https://www.docker.com/get-started).

### Docker Compose

Docker Compose should also be installed. It typically comes with Docker Desktop, but you can install it separately if needed. Instructions can be found [here](https://docs.docker.com/compose/install/).

## Running Locally with Docker Compose

Build and Start Services:

    docker-compose up --build

Access the Application:

Open your browser and navigate to `http://localhost:8000`.

## Deploying to Minikube (k7s)

### Step 1: Start Minikube

Start Minikube if it is not already running:

    minikube start

### Step 2: Build Docker Images

Configure your shell to use Minikube's Docker daemon:

    eval $(minikube docker-env)

Build the Docker image within Minikube:

    docker build -t my-django-app .
    docker compose up

### Step 3: Apply Kubernetes Manifests

Navigate to the `k7s` directory containing your Minikube-specific Kubernetes manifests and apply them:

    kubectl apply -f k7s/

## Deploying to Kubernetes (k8s)

### Step 1: Using kubectl command

### Just one command 
    kubectl apply -f k8s/

## Accessing the Application

### Minikube

Find the Minikube IP address:

    minikube ip

Access the application at `http://<minikube-ip>:30100`.

### Standard Kubernetes

Depending on your Kubernetes setup, you might use a LoadBalancer or Ingress to access your application. Check the service details:

    kubectl get services

Access the application using the external IP and port provided.

## Troubleshooting

If you encounter any issues, check the logs of the failing pods:

    kubectl logs <pod-name>

You can delete a pod to force Kubernetes to recreate it:

    kubectl delete pod <pod-name>

Verify the status of your pods and services:

    kubectl get pods
    kubectl get services

If you continue to experience issues, consult the logs and descriptions for more details:

    kubectl describe pod <pod-name>

Feel free to raise an issue if you need further assistance!
