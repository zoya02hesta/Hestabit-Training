# NGINX Reverse Proxy with Load Balancing (Docker)

## Overview

This project demonstrates how to use **NGINX as a reverse proxy** inside Docker to route requests to multiple backend containers.
The setup also simulates **load balancing** using **round-robin distribution**.

The system contains:

* NGINX Reverse Proxy
* Two Node.js backend containers

All services run using **Docker Compose**.

---

## Architecture

Client → NGINX Reverse Proxy → Backend Containers

* NGINX receives incoming requests
* It forwards `/api` requests to backend containers
* Requests are distributed using **round-robin load balancing**

---

## Services

### 1. NGINX Reverse Proxy

* Runs inside a Docker container
* Listens on **port 8080**
* Routes `/api` requests to backend services

Example:

http://localhost:8080/api

---

### 2. Backend Containers

Two backend services are deployed:

* **backend1**
* **backend2**

Both run a **Node.js Express server** on **port 3000**.

Each backend returns its container hostname so we can identify which container handled the request.

Example response:

Response from backend container: backend1

---

## NGINX Configuration

NGINX uses an **upstream block** to define backend servers.

Example:

```
upstream backend_servers {
    server backend1:3000;
    server backend2:3000;
}
```

Requests to `/api` are forwarded using:

```
location /api {
    proxy_pass http://backend_servers;
}
```

---

## Load Balancing

NGINX uses **round-robin load balancing by default**.

This means requests are distributed evenly:

Request 1 → backend1
Request 2 → backend2
Request 3 → backend1
Request 4 → backend2

Refreshing the browser will show responses from different backend containers.

---

## Running the Application

Start all services using:

```
docker-compose up -d --build
```

This command will:

1. Build backend Docker images
2. Start two backend containers
3. Start the NGINX reverse proxy
4. Connect containers using Docker networking

---

## Testing

Open the browser:

http://localhost:8080/api

Refresh multiple times to see responses from different backend containers.

This confirms **load balancing is working correctly**.

---

## Conclusion

This project demonstrates:

* Running **NGINX inside Docker**
* Using **reverse proxy routing**
* Deploying **multiple backend containers**
* Implementing **round-robin load balancing**

Docker Compose simplifies the deployment by managing all services with a single command.
