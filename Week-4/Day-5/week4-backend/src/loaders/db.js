import mongoose from "mongoose";
import config from "../config/index.js";
import logger from "../utils/logger.js";

const connectDB = async () => {
  try {
    await mongoose.connect(config.mongoUri);
    logger.info("✔ Database connected");
  } catch (error) {
    logger.error("Database connection failed", error);
    process.exit(1);
  }
};

export default connectDB;