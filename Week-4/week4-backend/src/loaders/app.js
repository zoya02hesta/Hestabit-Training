import express from "express";
import config from "../config/index.js";
import logger from "../utils/logger.js";
import connectDB from "./db.js";

import productRoutes from "../routes/product.routes.js";
import authRoutes from "../routes/auth.routes.js";

import errorMiddleware from "../middlewares/error.middleware.js";
import { applySecurityMiddleware } from "../middlewares/security.js";
import { requestTracer } from "../utils/tracing.js";

import accountRoutes from "../routes/account.routes.js";
import { protect } from "../middlewares/auth.middleware.js";

const app = express();

const loadApp = async () => {

  app.use(express.json({ limit: "10kb" }));
  // Database connection
  app.use("/api/auth", authRoutes);

  app.use("/api/accounts", accountRoutes);
  app.use(protect);

  await connectDB();

  // Request tracing
  app.use(requestTracer);

  


  // Body parser




  // Security middleware
  applySecurityMiddleware(app);

  logger.info("✔ Middlewares loaded");

  // Health route
  app.get("/health", (req, res) => {
    res.json({ status: "OK" });
  });

  // Routes
  app.use("/api/products", productRoutes);

  logger.info("✔ Routes mounted");

  // Error handler
  app.use(errorMiddleware);

  // Start server
  app.listen(config.port, () => {
    logger.info(`✔ Server started on port ${config.port}`);
  });
};

export default loadApp;