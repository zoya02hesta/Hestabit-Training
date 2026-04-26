# Backend Architecture – Week 4 Day 1

## Boot Sequence

1. Load environment configuration
2. Initialize logger
3. Connect to MongoDB
4. Load middlewares
5. Mount routes
6. Start server
7. Listen for shutdown signals

## Separation of Concerns

config/ → environment isolation  
loaders/ → boot orchestration  
utils/ → reusable utilities  
routes/ → HTTP route definitions  
controllers/ → request handling  
services/ → business logic  
repositories/ → DB access layer  

## Failure Strategy

- If database connection fails → process exits.
- Server does not start unless dependencies are ready.

## Lifecycle Control

- Handles SIGTERM
- Graceful shutdown implemented