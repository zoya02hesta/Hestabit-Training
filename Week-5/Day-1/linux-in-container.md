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
Node server process is running inside the container.

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
Logs show server startup message.