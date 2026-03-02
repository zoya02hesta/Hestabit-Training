import dotenv from "dotenv";
import path from "path";
import { fileURLToPath } from "url";

// Needed for __dirname in ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Decide environment
const env = process.env.NODE_ENV || "local";

// Load correct env file
dotenv.config({
  path: path.resolve(__dirname, `../../.env.${env}`)
});

const config = {
  port: process.env.PORT || 5000,
  mongoUri: process.env.MONGO_URI
};

export default config;