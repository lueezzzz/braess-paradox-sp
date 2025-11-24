import dotenv from "dotenv";
import { MAP_COORDINATES } from "./coordinates.js";

dotenv.config();

const API_KEY = process.env.MAPS_API_KEY;

async function computeRoute(origin, destination) {
  const url = "https://routes.googleapis.com/directions/v2:computeRoutes";

  const request = {
    origin: {
      location: {
        latLng: {
          latitude: origin.latitude,
          longitude: origin.longitude,
        },
      },
    },
    destination: {
      location: {
        latLng: {
          latitude: destination.latitude,
          longitude: destination.longitude,
        },
      },
    },
    travelMode: "DRIVE",
    routingPreference: "TRAFFIC_AWARE",
    computeAlternativeRoutes: false,
    routeModifiers: {
      avoidTolls: false,
      avoidHighways: false,
      avoidFerries: false,
    },
    languageCode: "en-US",
    units: "METRIC",
  };

  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Goog-Api-Key": API_KEY,
      "X-Goog-FieldMask":
        "routes.duration,routes.distanceMeters",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`HTTP ${response.status}: ${text}`);
  }

  const data = await response.json();
  const route = data.routes?.[0];

  if (!route) {
    console.log("No route found");
    return;
  }

  console.log("Distance (meters):", route.distanceMeters);
  console.log("Duration:   ", route.duration);

  
}

const origin = MAP_COORDINATES[0];
const destination = MAP_COORDINATES[1];

computeRoute(origin, destination).catch((err) => {
  console.error("Error computing route:", err);
});
