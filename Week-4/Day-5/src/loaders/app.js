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
  app.use("/api/auth", authRoutes);

  app.use("/api/accounts", accountRoutes);
  app.use(protect);

  await connectDB();

  app.use(requestTracer);

  






  applySecurityMiddleware(app);

  logger.info("✔ Middlewares loaded");

  app.get("/health", (req, res) => {
    res.json({ status: "OK" });
  });

  app.use("/api/products", productRoutes);

  logger.info("✔ Routes mounted");

  app.use(errorMiddleware);

  app.listen(config.port, () => {
    logger.info(`✔ Server started on port ${config.port}`);
  });
};

export default loadApp;