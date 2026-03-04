import express from "express";
import helmet from "helmet";
import cors from "cors";
import rateLimit from "express-rate-limit";
import xss from "xss-clean";
import mongoSanitize from "express-mongo-sanitize";
import hpp from "hpp";

export const applySecurityMiddleware = (app) => {

  // Payload size limit
  app.use(express.json({ limit: "10kb" }));

  // Secure HTTP headers
  app.use(helmet());

  //  CORS Policy
  app.use(
    cors({
      origin: "http://localhost:3000",
      methods: ["GET", "POST", "PUT", "DELETE"],
      credentials: true,
    })
  );

  //  Rate Limiting
  const limiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 100,
    standardHeaders: true,
    legacyHeaders: false,
    message: {
      success: false,
      message: "Too many requests. Try again later.",
    },
  });

  app.use(limiter);

  //Prevent NoSQL Injection
  app.use(mongoSanitize());

  //  Prevent Parameter Pollution
  app.use(hpp());

  // Prevent XSS
  app.use(xss());
};