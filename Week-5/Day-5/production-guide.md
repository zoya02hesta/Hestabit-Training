# Production Deployment Guide

## Overview
This project is a full-stack Dockerized application with:
- NGINX reverse proxy (HTTPS)
- React frontend
- Node.js backend
- MongoDB database

## Architecture
Client → NGINX → Backend → MongoDB

## Features
- HTTPS using self-signed certificates
- HTTP to HTTPS redirection
- Persistent storage using Docker volumes
- Health checks for MongoDB
- Log rotation for containers
- Restart policies for reliability

## Deployment

Run:
./deploy.sh

## Access

https://localhost

## Notes
- Environment variables are stored in .env
- Volumes ensure data persistence
- NGINX handles SSL termination