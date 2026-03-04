import loadApp from "./loaders/app.js";
import logger from "./utils/logger.js";
import { v4 as uuidv4 } from "uuid";

// Request Tracing Middleware
export const requestTracer = (req, res, next) => {
  const requestId = uuidv4();
  req.requestId = requestId;
  res.setHeader("X-Request-ID", requestId);

  logger.info({
    message: "Incoming request",
    method: req.method,
    url: req.url,
    requestId,
  });

  next();
};

// Start App
try {
  loadApp();
  logger.info("Server initialization successful");
} catch (error) {
  logger.error({
    message: "Server failed to start",
    error: error.message,
  });
}