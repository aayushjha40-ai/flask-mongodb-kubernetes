# Flask + MongoDB on Kubernetes (Minikube)

## Project Overview

This project demonstrates deploying a Python Flask application connected to a MongoDB database on a Kubernetes cluster using Minikube.
The application is containerized using Docker and deployed with proper Kubernetes resources such as Deployments, StatefulSets, Services, Persistent Volumes, Secrets, and Horizontal Pod Autoscaling (HPA).

The purpose of this assignment is to demonstrate understanding of Kubernetes fundamentals, database persistence, service discovery, autoscaling, and basic security practices.

---

## Technologies Used

* Python 3
* Flask
* MongoDB
* Docker
* Kubernetes (Minikube)
* kubectl
* Horizontal Pod Autoscaler (HPA)

---

## Architecture Overview

```
User Browser
     |
Flask Service (NodePort)
     |
Flask Pods (Deployment, 2–5 replicas)
     |
MongoDB Service (ClusterIP)
     |
MongoDB StatefulSet (Persistent Volume)
```

* Flask runs in multiple replicas for availability.
* MongoDB runs as a StatefulSet to ensure stable identity and persistent storage.
* Kubernetes internal DNS is used for service-to-service communication.

---

## Project Structure

```
flask-k8s-project/
├── app.py
├── requirements.txt
├── Dockerfile
├── README.md
├── k8s/
│   ├── mongo-secret.yaml
│   ├── mongo-pvc.yaml
│   ├── mongo-service.yaml
│   ├── mongo-statefulset.yaml
│   ├── flask-deployment.yaml
│   ├── flask-service.yaml
│   └── hpa.yaml
```

---

## Flask Application

The Flask application provides the following endpoints:

### `/`

Returns a welcome message with the current date and time.

### `/data`

* **POST**: Inserts JSON data into MongoDB
* **GET**: Retrieves all stored documents from MongoDB

MongoDB connection details are provided through environment variables.

---

## Docker Image Build

The Flask application is containerized using Docker.

Build the image using Minikube’s Docker environment:

```bash
eval $(minikube docker-env)
docker build -t flask-mongo-app .
```

---

## Kubernetes Deployment Steps

### 1. Start Minikube

```bash
minikube start
```

---

### 2. Apply Kubernetes Manifests

```bash
kubectl apply -f k8s/
```

This deploys:

* MongoDB Secret
* Persistent Volume Claim
* MongoDB StatefulSet
* Flask Deployment
* Kubernetes Services
* Horizontal Pod Autoscaler

---

### 3. Verify Running Pods

```bash
kubectl get pods
```

Expected pods:

* `mongo-0`
* `flask-app` pods (minimum 2 replicas)

---

### 4. Access the Flask Application

```bash
minikube service flask-service
```

The application will open in the browser.

---

## MongoDB Authentication

MongoDB authentication is enabled using Kubernetes Secrets.

* Username and password are stored in a Secret.
* MongoDB reads credentials from environment variables.
* Flask connects using a secure connection string provided via environment variables.

This ensures credentials are not hardcoded in the application code.

---

## Kubernetes DNS Resolution

Kubernetes provides internal DNS resolution using CoreDNS.

* Each Service is assigned a DNS name.
* Flask connects to MongoDB using the service name `mongo-service` instead of pod IPs.
* This ensures reliable communication even if MongoDB pods restart or change IPs.

Service-based DNS is a recommended Kubernetes best practice.

---

## Resource Requests and Limits

Resource requests and limits are configured for Flask pods to ensure stable resource usage.

### Example Configuration

**Requests**

* CPU: 0.2
* Memory: 250Mi

**Limits**

* CPU: 0.5
* Memory: 500Mi

### Purpose

* Requests guarantee minimum resources.
* Limits prevent excessive resource usage.
* Helps Kubernetes schedule and manage pods efficiently.

---

## Autoscaling (HPA)

Horizontal Pod Autoscaler is configured for the Flask application.

* Minimum replicas: 2
* Maximum replicas: 5
* Scaling based on CPU utilization above 70%

### Verification

```bash
kubectl get hpa
kubectl get pods
```

Load was generated using a BusyBox pod to test autoscaling behavior.
In the local Minikube environment, CPU usage did not exceed the threshold, so replicas remained at the minimum.
The HPA configuration and metrics collection were verified successfully.


<img width="939" height="117" alt="image" src="https://github.com/user-attachments/assets/49434fcd-a959-46d6-b7a8-dcd09bec928e" />

<img width="930" height="118" alt="image" src="https://github.com/user-attachments/assets/efb3d463-230c-4644-9ad2-50468e675086" />


---

## Security Considerations

* The application code does not contain any hardcoded credentials, secrets, or tokens.
* MongoDB credentials are managed using Kubernetes Secrets.
* The database connection string is injected into the Flask application via environment variables.
* Secrets are used only inside the Kubernetes cluster and are not exposed in the source code.
* The GitHub repository does not contain any real passwords, personal access tokens, or production credentials.
* A `.gitignore` file is used to prevent accidental commits of environment files or sensitive local data.

This approach follows standard security practices used in Kubernetes-based applications.

---

## Design Choices

* MongoDB is deployed as a StatefulSet to support persistent storage and stable identity.
* Flask is deployed using a Deployment to allow horizontal scaling.
* ClusterIP service is used for MongoDB to restrict access within the cluster.
* NodePort service is used for Flask to allow external access.
* Minikube is used to keep the setup local and reproducible.

---

## Screenshots

### 1. Kubernetes Pods Running

MongoDB StatefulSet pod and Flask application pods running successfully.

<img width="939" height="117" alt="Kubernetes Pods Running" src="https://github.com/user-attachments/assets/49434fcd-a959-46d6-b7a8-dcd09bec928e" />

---

### 2. Horizontal Pod Autoscaler Status

HPA configuration showing minimum replicas set to 2 and maximum replicas set to 5.

<img width="930" height="118" alt="HPA Status" src="https://github.com/user-attachments/assets/efb3d463-230c-4644-9ad2-50468e675086" />

---

### 3. Flask Application Access via Browser

Flask application accessed using the Minikube NodePort service.

<img width="946" height="368" alt="Flask Application in Browser" src="https://github.com/user-attachments/assets/20fe11da-7d38-40eb-87c3-b362f637ea20" />

---

### 4. Autoscaling Load Test

Load generation using a BusyBox pod making continuous requests to the Flask service.

<img width="941" height="764" alt="Autoscaling Load Test" src="https://github.com/user-attachments/assets/34635f80-a334-40f7-84ca-b21592761025" />

---
