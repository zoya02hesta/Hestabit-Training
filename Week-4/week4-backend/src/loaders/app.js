import express from "express";
import config from "../config/index.js";
import logger from "../utils/logger.js";
import connectDB from "./db.js";
import productRoutes from "../routes/product.routes.js";
import errorMiddleware from "../middlewares/error.middleware.js";

const app = express();

const loadApp = async () => {
  // 1. Connect DB
  await connectDB();

  // 2. Middlewares
  app.use(express.json());
  logger.info("✔ Middlewares loaded");

  // 3. Routes
  app.get("/health", (req, res) => {
    res.json({ status: "OK" });
  });

  app.use("/api/products", productRoutes);

  logger.info("✔ Routes mounted");

  // 4. Global Error Handler
  app.use(errorMiddleware);

  // 5. Start server
  const server = app.listen(config.port, () => {
    logger.info(`✔ Server started on port ${config.port}`);
  });

  // 6. Graceful shutdown
  process.on("SIGTERM", () => {
    logger.info("SIGTERM received. Shutting down...");
    server.close(() => {
      logger.info("Server closed");
      process.exit(0);
    });
  });
};

export default loadApp;