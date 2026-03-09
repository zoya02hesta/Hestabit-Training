#!/bin/bash

echo "Stopping old containers..."
docker-compose -f docker-compose.prod.yml down

echo "Building new containers..."
docker-compose -f docker-compose.prod.yml build

echo "Starting containers..."
docker-compose -f docker-compose.prod.yml up -d

echo "Deployment complete!"
docker ps