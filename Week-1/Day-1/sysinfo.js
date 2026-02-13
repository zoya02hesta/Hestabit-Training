// const os = require("os");
// const { execSync } = require("child_process");
// const fs = require("fs");
// const path = require("path");

// // 1️⃣ Hostname
// const hostname = os.hostname();

// // 2️⃣ Available Disk Space (GB)
// const diskSpace = execSync("df -BG / | tail -1 | awk '{print $4}'")
//   .toString()
//   .trim();

// // 3️⃣ Open Ports (Top 5)
// const openPorts = execSync(
//   "lsof -i -P -n | grep LISTEN | head -5"
// )
//   .toString()
//   .trim();

// // 4️⃣ Default Gateway
// const defaultGateway = execSync(
//   "ip route | grep default | awk '{print $3}'"
// )
//   .toString()
//   .trim();

// // 5️⃣ Logged-in users count
// const loggedInUsers = execSync("who | wc -l")
//   .toString()
//   .trim();

// // Print everything
// console.log("Hostname:", hostname);
// console.log("Available Disk Space:", diskSpace);
// console.log("Open Ports (Top 5):\n", openPorts);
// console.log("Default Gateway:", defaultGateway);
// console.log("Logged-in Users:", loggedInUsers);

// // 6️⃣ Runtime metrics
// // const metrics = {
// //   cpuUsage: process.cpuUsage(),
// //   resourceUsage: process.resourceUsage(),
// //   timestamp: new Date().toISOString()
// // };

// // // Ensure logs folder exists
// // const logDir = path.join(__dirname, "logs");
// // if (!fs.existsSync(logDir)) {
// //   fs.mkdirSync(logDir);
// // }

// // // Save metrics to JSON file
// // fs.writeFileSync(
// //   path.join(logDir, "day1-sysmetrics.json"),
// //   JSON.stringify(metrics, null, 2)
// // );


const os = require("os");
const { execSync } = require("child_process");

// 1. Hostname
const hostname = os.hostname();

// 2. Available Disk Space (GB)
const diskOutput = execSync("df -BG --output=avail / | tail -1").toString().trim();
const availableDiskGB = diskOutput.replace("G", "");

// 3. Open Ports (top 5)
const openPorts = execSync(
  "ss -tuln | awk 'NR>1 {print $5}' | cut -d: -f2 | sort -n | uniq | head -5"
)
  .toString()
  .trim()
  .split("\n");

// 4. Default Gateway
const defaultGateway = execSync(
  "ip route | grep default | awk '{print $3}'"
)
  .toString()
  .trim();

// 5. Logged-in users count
const loggedInUsers = execSync("who | wc -l")
  .toString()
  .trim();

console.log("System Information");
console.log("------------------");
console.log("Hostname:", hostname);
console.log("Available Disk Space (GB):", availableDiskGB);
console.log("Open Ports (Top 5):", openPorts);
console.log("Default Gateway:", defaultGateway);
console.log("Logged-in Users Count:", loggedInUsers);
