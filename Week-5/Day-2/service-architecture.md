# Multi-Container Application Architecture (Docker Compose)

## Overview

This project demonstrates a multi-container application using **Docker Compose**.
The application consists of three services:

* **Client:** React frontend
* **Server:** Node.js + Express backend
* **Database:** MongoDB

All services run in separate Docker containers and communicate using Docker's internal network.

---

## Services

### 1. Client (React)

* Built using React.js
* Runs inside a Node.js container
* Exposed on **port 3000**
* Communicates with the backend server

**Access URL**

http://localhost:3000

---

### 2. Server (Node + Express)

* Handles API requests
* Connects to MongoDB database
* Runs inside a Node.js container
* Exposed on **port 5000**

**Access URL**

http://localhost:5000

The server connects to MongoDB using the service name:

mongodb://mongo:27017/docker-demo

This works because Docker Compose automatically creates a network where services can communicate using their service names.

---

### 3. MongoDB Database

* Runs using the official MongoDB Docker image
* Stores application data
* Uses a **Docker volume** to persist data

Even if the container stops or restarts, the database data remains stored.

---

## Docker Networking

Docker Compose creates a default bridge network where each service can communicate using its service name as a hostname.

Communication flow:

Client → Server → MongoDB

* Client sends requests to Server
* Server processes requests
* Server reads/writes data to MongoDB

Containers communicate using service names:

* `mongo`
* `server`
* `client`

---

## Persistent Storage

A named Docker volume is used:

mongo-data

Purpose:

* Stores MongoDB data
* Ensures data is not lost when containers stop

Volume mapping:

mongo-data → /data/db (MongoDB container)

---

## Running the Application

The entire application can be started with a single command:

docker compose up -d

This command:

1. Builds images for client and server
2. Pulls MongoDB image
3. Creates containers
4. Connects containers through Docker networking
5. Starts all services

---

## Logs

Logs can be viewed using:

docker compose logs server

This helps monitor container activity and debug issues.

---

## Conclusion

This project demonstrates:

* Multi-container applications
* Docker Compose orchestration
* Container networking
* Persistent storage using volumes
* Easy deployment using a single command
