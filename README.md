# Flask + MongoDB on Kubernetes

##  Project Overview

This project demonstrates deploying a **Python Flask application** connected to a **MongoDB database** on a **Kubernetes cluster** using **Minikube**.
The application is containerized using Docker and deployed with proper Kubernetes resources including **Deployments, StatefulSets, Services, Persistent Volumes, Secrets, and Horizontal Pod Autoscaling (HPA)**.

The goal of this assignment is to showcase understanding of:

* Kubernetes core concepts
* Database persistence and authentication
* Service discovery (DNS)
* Resource management
* Autoscaling based on CPU usage

---

##  Tools & Technologies Used

* **Python 3**
* **Flask** – Backend web framework
* **MongoDB** – NoSQL database
* **Docker** – Containerization
* **Kubernetes (Minikube)** – Container orchestration
* **kubectl** – Kubernetes CLI
* **Horizontal Pod Autoscaler (HPA)** – Autoscaling
* **Persistent Volumes & PVC** – Data persistence

---

##  Architecture Overview

```
User Browser
     ↓
Flask Service (NodePort)
     ↓
Flask Pods (2–5 replicas, autoscaled)
     ↓
MongoDB Service (ClusterIP)
     ↓
MongoDB StatefulSet (Persistent Storage)
```

* Flask application runs in multiple replicas for high availability.
* MongoDB runs as a StatefulSet with persistent storage.
* Internal Kubernetes DNS enables service-to-service communication.

---

##  Project Structure

```
flask-k8s-project/
│
├── app.py
├── requirements.txt
├── Dockerfile
│
├── k8s/
│   ├── mongo-secret.yaml
│   ├── mongo-pvc.yaml
│   ├── mongo-service.yaml
│   ├── mongo-statefulset.yaml
│   ├── flask-deployment.yaml
│   ├── flask-service.yaml
│   └── hpa.yaml
│
└── README.md
```

---

##  Docker Image Build

Build the Flask application Docker image using Minikube’s Docker daemon:

```bash
eval $(minikube docker-env)
docker build -t flask-mongo-app .
```

*(Image is used locally by Minikube for this assignment.)*

---

##  Kubernetes Deployment Steps

### 1️ Start Minikube

```bash
minikube start
```

---

### 2️ Apply Kubernetes Manifests

```bash
kubectl apply -f k8s/
```

This deploys:

* MongoDB Secret
* Persistent Volume Claim
* MongoDB StatefulSet
* Flask Deployment (2 replicas)
* Services
* Horizontal Pod Autoscaler

---

### 3️ Verify Pods

```bash
kubectl get pods
```

Expected output:

* `mongo-0` → Running
* `flask-app-*` → Running (2 replicas)

---

### 4️ Access Flask Application

```bash
minikube service flask-service
```

Open the browser URL and you should see:

```
Welcome to the Flask app! The current time is: <date & time>
```

---

##  MongoDB Authentication

MongoDB is secured using **username and password**, stored in a Kubernetes **Secret**.

* Credentials are injected into MongoDB via environment variables.
* Flask connects using the following URI:

```
mongodb://admin:password@mongo-service:27017/flask_db?authSource=admin
```

This ensures secure database access.

---

##  Kubernetes DNS Resolution (Explanation)

Kubernetes provides built-in DNS via **CoreDNS**.

* Each Service gets a DNS name:

  ```
  <service-name>.<namespace>.svc.cluster.local
  ```
* Flask connects to MongoDB using:

  ```
  mongo-service
  ```
* This avoids using Pod IPs, which can change.
* If MongoDB pod restarts, DNS ensures connectivity remains intact.

---

##  Resource Requests & Limits

Both Flask and MongoDB pods are configured with resource constraints.

### Why Resource Requests & Limits?

* **Requests** ensure guaranteed minimum resources.
* **Limits** prevent a pod from consuming excessive resources.
* Helps Kubernetes schedule pods efficiently and maintain cluster stability.

### Configuration Used:

```yaml
requests:
  cpu: "0.2"
  memory: "250Mi"
limits:
  cpu: "0.5"
  memory: "500Mi"
```

---

##  Autoscaling (HPA)

### HPA Configuration

* **Minimum replicas:** 2
* **Maximum replicas:** 5
* **CPU threshold:** 70%

### HPA Status Command

```bash
kubectl get hpa
```

Sample output:

```
TARGETS: cpu 0%/70%
REPLICAS: 2
```

### Autoscaling Testing

Load was generated using a BusyBox pod:

```bash
kubectl run load --rm -it --image=busybox -- sh
```

```sh
while true; do wget -q -O- http://flask-service; done
```

Although CPU usage did not exceed 70% in this environment, the HPA was verified to be correctly configured and monitoring the deployment.

<img width="1105" height="411" alt="Screenshot 2025-12-16 234616" src="https://github.com/user-attachments/assets/89403311-d0cb-4566-bd66-6405bfe96e27" />


---

##  API Testing

### POST Data

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"name":"test"}' http://<minikube-ip>:<port>/data
```

### GET Data

```bash
curl http://<minikube-ip>:<port>/data
```

---

##  Design Choices

* **StatefulSet for MongoDB:** Ensures stable network identity and persistent storage.
* **Deployment for Flask:** Enables horizontal scaling.
* **ClusterIP for MongoDB:** Restricts database access inside cluster.
* **NodePort for Flask:** Allows external access from browser.
* **HPA:** Demonstrates scalability and production readiness.

Alternative cloud-managed Kubernetes was considered but Minikube was chosen to keep the setup local and reproducible.

---
