import { Worker } from "bullmq";
import Redis from "ioredis";

const connection = new Redis();

const worker = new Worker(
  "emailQueue",
  async (job) => {
    console.log("Processing Email Job:", job.data);

    // Simulate email sending
    await new Promise((resolve) => setTimeout(resolve, 2000));

    console.log("Email Sent to:", job.data.email);
  },
  { connection }
);

worker.on("completed", (job) => {
  console.log(`Job ${job.id} completed`);
});

worker.on("failed", (job, err) => {
  console.error(`Job ${job.id} failed:`, err.message);
});