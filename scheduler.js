import cron from "node-cron";
import { MAP_COORDINATES } from "./coordinates.js";
import dotenv from "dotenv";
import { computeRoute } from "./main.js";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const resultsDir = path.join(__dirname, "results");

if (!fs.existsSync(resultsDir)) {
  fs.mkdirSync(resultsDir, { recursive: true });
}

function isCollectionPeriod() {
  const now = new Date();
  const start = new Date(2025, 10, 25);
  const end = new Date(2025, 11, 2);

  return now >= start && now < end;
}

async function collectAllRoutes(timeWindow) {
  console.log(
    `[${new Date().toISOString()}] Starting ${timeWindow} data collection...`
  );
  const results = [];
  const dayOfWeek = new Date().toLocaleDateString("en-US", {
    weekday: "long",
  });

  for (let i = 0; i < MAP_COORDINATES.length - 1; i++) {
    const origin = MAP_COORDINATES[i];
    const destination = MAP_COORDINATES[i + 1];

    try {
      const result = await computeRoute(origin, destination);

      if (result) {
        const record = {
          origin: origin.intersection,
          destination: destination.intersection,
          day_of_week: dayOfWeek,
          distance: result.distanceMeters,
          duration: result.duration,
          static_duration: result.staticDuration,
          timestamp: new Date().toISOString(),
          timeWindow: timeWindow,
        };

        results.push(record);
        console.log(`${origin.intersection} → ${destination.intersection}`);
      }
    } catch (error) {
      console.error(`Error collecting route ${i}:`, error.message);
    }

    await new Promise((resolve) => setTimeout(resolve, 500));
  }

  console.log(
    `[${new Date().toISOString()}] Collected ${results.length} routes\n`
  );
  return results;
}

function saveResults(results, timeWindow) {
  const now = new Date();
  const date = now.toISOString().split("T")[0];

  const time = now.toTimeString().slice(0, 8).replace(/:/g, "-");

  const filename = path.join(
    resultsDir,
    `results-${date}-${timeWindow}-${time}.json`
  );

  const data = JSON.stringify(results, null, 2);

  try {
    fs.writeFileSync(filename, data);
    console.log(`Saved to JSON: ${filename}`);
  } catch (error) {
    console.error(`Error saving JSON:`, error.message);
  }
}

console.log("Collection Period: Nov 25 - Dec 1, 2025");
console.log("\nScheduled Times:");
console.log("  • 7:00 AM - 8:00 am  - Peak Morning Hours");
console.log("  • 12:00 PM - 1:00 pm - Peak Noon Hours");
console.log("  • 5:00 PM - 6:00 pm - Peak Afternoon Hours");
console.log("  • 10:00 PM - 11 pm - Non-Peak Hours");
console.log("\nWaiting for scheduled times...\n");

cron.schedule("* 7 * * *", async () => {
  if (!isCollectionPeriod()) {
    return;
  }

  console.log(`\n${"=".repeat(60)}`);
  console.log(
    `MORNING COLLECTION - ${new Date().toLocaleTimeString()} (7am-8am Peak Morning Hours)`
  );
  console.log(`${"=".repeat(60)}`);

  try {
    const results = await collectAllRoutes("7am-Peak-Morning");
    saveResults(results, "7am");
  } catch (error) {
    console.error("Morning collection error:", error);
  }
});

cron.schedule("* 12 * * *", async () => {
  if (!isCollectionPeriod()) {
    return;
  }

  console.log(`\n${"=".repeat(60)}`);
  console.log(
    `NOON COLLECTION - ${new Date().toLocaleTimeString()} (12pm-1pm Peak Noon Hours)`
  );
  console.log(`${"=".repeat(60)}`);

  try {
    const results = await collectAllRoutes("12pm-Peak-Noon");
    saveResults(results, "12pm");
  } catch (error) {
    console.error("Noon collection error:", error);
  }
});

cron.schedule("* 17 * * *", async () => {
  if (!isCollectionPeriod()) {
    return;
  }

  console.log(`\n${"=".repeat(60)}`);
  console.log(
    `AFTERNOON COLLECTION - ${new Date().toLocaleTimeString()} (5pm-6pm Peak Afternoon Hours)`
  );
  console.log(`${"=".repeat(60)}`);

  try {
    const results = await collectAllRoutes("5pm-Peak-Afternoon");
    saveResults(results, "5pm");
  } catch (error) {
    console.error("Afternoon collection error:", error);
  }
});

cron.schedule("* 22 * * *", async () => {
  if (!isCollectionPeriod()) {
    return;
  }

  console.log(`\n${"=".repeat(60)}`);
  console.log(
    `NIGHT COLLECTION - ${new Date().toLocaleTimeString()} (10pm-11pm Non-Peak Hours)`
  );
  console.log(`${"=".repeat(60)}`);

  try {
    const results = await collectAllRoutes("10pm-Non-Peak");
    saveResults(results, "10pm");
  } catch (error) {
    console.error("Night collection error:", error);
  }
});
