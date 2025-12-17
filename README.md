Flask + MongoDB on Kubernetes (Minikube)



Project Overview



This project demonstrates deploying a Python Flask application connected to a MongoDB database on a Kubernetes cluster using Minikube.

The application is containerized using Docker and deployed with Kubernetes resources such as Deployments, StatefulSets, Services, Persistent Volumes, Secrets, and Horizontal Pod Autoscaling (HPA).



The purpose of this assignment is to demonstrate understanding of Kubernetes fundamentals, database persistence, service discovery, autoscaling, and basic security practices.



Technologies Used



Python 3

Flask

MongoDB

Docker

Kubernetes (Minikube)

kubectl

Horizontal Pod Autoscaler (HPA)



Architecture Overview



User Browser

|

Flask Service (NodePort)

|

Flask Pods (Deployment, 2–5 replicas)

|

MongoDB Service (ClusterIP)

|

MongoDB StatefulSet (Persistent Volume)



Flask runs in multiple replicas for availability.

MongoDB runs as a StatefulSet to ensure stable identity and persistent storage.

Kubernetes internal DNS is used for service-to-service communication.



Project Structure



flask-k8s-project

|-- app.py

|-- requirements.txt

|-- Dockerfile

|-- README.md

|-- k8s

|-- mongo-secret.yaml

|-- mongo-pvc.yaml

|-- mongo-service.yaml

|-- mongo-statefulset.yaml

|-- flask-deployment.yaml

|-- flask-service.yaml

|-- hpa.yaml



Flask Application



The Flask application provides the following endpoints:



/

Returns a welcome message with the current date and time.



/data

POST: Inserts JSON data into MongoDB

GET: Retrieves all stored documents from MongoDB



MongoDB connection details are provided through environment variables.



Docker Image Build



The Flask application is containerized using Docker.



Build the image using Minikube’s Docker environment:



eval $(minikube docker-env)

docker build -t flask-mongo-app .



Kubernetes Deployment Steps



Step 1: Start Minikube



minikube start



Step 2: Apply Kubernetes Manifests



kubectl apply -f k8s/



This deploys:

MongoDB Secret

Persistent Volume Claim

MongoDB StatefulSet

Flask Deployment

Kubernetes Services

Horizontal Pod Autoscaler



Step 3: Verify Running Pods



kubectl get pods



Expected pods:

mongo-0

flask-app pods (minimum 2 replicas)



Step 4: Access the Flask Application



minikube service flask-service



MongoDB Authentication



MongoDB authentication is enabled using Kubernetes Secrets.



Username and password are stored in a Kubernetes Secret.

MongoDB reads credentials from environment variables.

Flask connects using a secure connection string provided via environment variables.



This ensures credentials are not hardcoded in the application code.



Kubernetes DNS Resolution



Kubernetes provides internal DNS resolution using CoreDNS.



Each Service is assigned a DNS name.

Flask connects to MongoDB using the service name mongo-service instead of pod IPs.

This ensures reliable communication even if MongoDB pods restart or change IPs.



Resource Requests and Limits



Resource requests and limits are configured for Flask pods.



Requests:

CPU: 0.2

Memory: 250Mi



Limits:

CPU: 0.5

Memory: 500Mi



Requests guarantee minimum resources.

Limits prevent excessive resource usage.

This helps Kubernetes schedule and manage pods efficiently.



Autoscaling (HPA)



Horizontal Pod Autoscaler is configured for the Flask application.



Minimum replicas: 2

Maximum replicas: 5

Scaling based on CPU utilization above 70 percent.



Verification commands:



kubectl get hpa

kubectl get pods



Load was generated using a BusyBox pod.

In the local Minikube environment, CPU usage did not exceed the threshold, so replicas remained at the minimum.

The HPA configuration and metrics collection were verified successfully.



File: screenshots/hpa-status.png

File: screenshots/pods-running.png



Security Considerations



The application code does not contain hardcoded credentials, secrets, or tokens.

MongoDB credentials are managed using Kubernetes Secrets.

The database connection string is injected into the Flask application via environment variables.

Secrets are used only inside the Kubernetes cluster and are not exposed in the source code.

The GitHub repository does not contain any real passwords, personal access tokens, or production credentials.

A .gitignore file is used to prevent accidental commits of environment files or sensitive local data.



Design Choices



MongoDB is deployed as a StatefulSet to support persistent storage and stable identity.

Flask is deployed using a Deployment to allow horizontal scaling.

ClusterIP service is used for MongoDB to restrict access within the cluster.

NodePort service is used for Flask to allow external access.

Minikube is used to keep the setup local and reproducible.





Screenshots



1\. Kubernetes Pods Running

Screenshot showing MongoDB StatefulSet pod and Flask application pods running successfully.

File: screenshots/pods-running.png



2\. Horizontal Pod Autoscaler Status

Screenshot showing HPA configuration with minimum replicas set to 2 and maximum replicas set to 5.

File: screenshots/hpa-status.png



3\. Flask Application Access via Browser

Screenshot showing the Flask application accessed using the Minikube NodePort service.

File: screenshots/flask-browser.png



4\. Autoscaling Load Test

Screenshot showing load generation using a BusyBox pod making continuous requests to the Flask service.

File: screenshots/load-test.png





