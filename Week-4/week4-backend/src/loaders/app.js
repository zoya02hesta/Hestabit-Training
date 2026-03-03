import express from "express";
import config from "../config/index.js";
import logger from "../utils/logger.js";
import connectDB from "./db.js";
import productRoutes from "../routes/product.routes.js";
import errorMiddleware from "../middlewares/error.middleware.js";
import { applySecurityMiddleware } from "../middlewares/security.js";

const app = express();

const loadApp = async () => {
  // 1️⃣ Connect DB
  await connectDB();

  // 2️⃣ Body parser (ONLY ONCE)
  app.use(express.json({ limit: "10kb" }));

  // 3️⃣ Security middleware
  applySecurityMiddleware(app);

  logger.info("✔ Middlewares loaded");

  // 4️⃣ Routes
  app.get("/health", (req, res) => {
    res.json({ status: "OK" });
  });

  app.use("/api/products", productRoutes);

  logger.info("✔ Routes mounted");

  // 5️⃣ Error handler
  app.use(errorMiddleware);

  // 6️⃣ Start server
  app.listen(config.port, () => {
    logger.info(`✔ Server started on port ${config.port}`);
  });
};

export default loadApp;