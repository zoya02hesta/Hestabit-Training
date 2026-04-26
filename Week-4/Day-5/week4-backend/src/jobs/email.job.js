import { Queue } from "bullmq";
import Redis from "ioredis";

const connection = new Redis();

export const emailQueue = new Queue("emailQueue", {
  connection,
  defaultJobOptions: {
    attempts: 3,
    backoff: {
      type: "exponential",
      delay: 2000,
    },
  },
});

export const addEmailJob = async (data) => {
  await emailQueue.add("sendEmail", data);
};