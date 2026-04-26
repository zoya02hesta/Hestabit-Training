# Deployment Notes

## Steps:

1. Train model
2. Save model + feature list
3. Run API:
   uvicorn src.deployment.api:app --reload

## Features:

* Input validation
* Logging
* Request tracking
* Model versioning

## Future Improvements:

* Cloud deployment
* Monitoring dashboards
