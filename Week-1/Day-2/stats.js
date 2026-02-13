#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const os = require("os");

const args = process.argv.slice(2);
const flags = args.filter(a => a.startsWith("--"));
const files = args.filter(a => !a.startsWith("--")).slice(0, 3);

if (files.length === 0) {
  console.error("❌ Please provide up to 3 files");
  process.exit(1);
}

const OUTPUT_DIR = path.join(__dirname, "output");
const LOG_DIR = path.join(__dirname, "logs");

fs.mkdirSync(OUTPUT_DIR, { recursive: true });
fs.mkdirSync(LOG_DIR, { recursive: true });

function getMemoryMB() { 
  return (process.memoryUsage().rss / 1024 / 1024).toFixed(2);
}

function analyze(content) {
  return {
    chars: content.length,
    lines: content.split("\n").length, 
    words: content.trim().split(/\s+/).filter(Boolean).length
  };
}

async function processFile(file) {
  const start = process.hrtime.bigint();
  const content = await fs.promises.readFile(file, "utf8");

  const stats = analyze(content);

  if (flags.includes("--unique")) {
    const uniqueLines = [...new Set(content.split("\n"))].join("\n");
    const outPath = path.join(
      OUTPUT_DIR,
      `unique-${path.basename(file)}`
    );
    await fs.promises.writeFile(outPath, uniqueLines);
  }

  const end = process.hrtime.bigint();
  const executionTimeMs = Number(end - start) / 1e6;

  const result = {
    file,
    executionTimeMs: Number(executionTimeMs.toFixed(2)),
    memoryMB: Number(getMemoryMB())
  };

  if (flags.includes("--chars")) console.log(`${file} → chars: ${stats.chars}`);
  if (flags.includes("--lines")) console.log(`${file} → lines: ${stats.lines}`);
  if (flags.includes("--words")) console.log(`${file} → words: ${stats.words}`);

  return result;
}

(async () => {
  try {
    const results = await Promise.all(files.map(processFile));

    const logFile = path.join(
      LOG_DIR,
      `performance-${Date.now()}.json`
    );

    await fs.promises.writeFile(
      logFile,
      JSON.stringify(results, null, 2)
    );

    console.log(`📊 Performance log saved → ${logFile}`);
  } catch (err) {
    console.error("❌ Error:", err.message);
  }
})();