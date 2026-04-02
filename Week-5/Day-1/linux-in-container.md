# Linux Inside Docker Container

## Entering the container

Command used:

docker exec -it day1-container /bin/sh

## File structure

Command:
ls

Observation:
Application files exist inside /app directory.

## Running processes

Command:
ps aux

Observation:
The Node.js server runs as the main process (PID 1), which means if it stops, the container exits.

The container has its own process namespace, meaning processes inside the container are isolated from the host system.

## Monitoring processes

Command:
top

Observation:
Shows real-time CPU and memory usage.

## Disk usage

Command:
df -h

## Container logs

Command:
docker logs day1-container

Observation:
Docker captures logs from stdout/stderr of the main process, which can be accessed using docker logs.

The container filesystem is ephemeral—any changes are lost if the container is removed unless volumes are used.