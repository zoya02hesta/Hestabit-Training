import dotenv from "dotenv";
import path from "path";
import { fileURLToPath } from "url";


const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);


const env = process.env.NODE_ENV || "local";


dotenv.config({
  path: path.resolve(__dirname, `../../.env.${env}`)
});

const config = {
  port: process.env.PORT || 5000,
  mongoUri: process.env.MONGO_URI
};

export default config;