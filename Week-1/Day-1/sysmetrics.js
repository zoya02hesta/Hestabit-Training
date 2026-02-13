const fs = require("fs");
const path = require("path");

// Collect metrics
const metrics = {
  timestamp: new Date().toISOString(),
  cpuUsage: process.cpuUsage(),
  resourceUsage: process.resourceUsage()
};

// Ensure logs directory exists
const logsDir = path.join(__dirname, "logs");
if (!fs.existsSync(logsDir)) {
  fs.mkdirSync(logsDir);
}

// Write metrics to file
const filePath = path.join(logsDir, "day1-sysmetrics.json");
fs.writeFileSync(filePath, JSON.stringify(metrics, null, 2));

console.log("System metrics logged to:", filePath);
