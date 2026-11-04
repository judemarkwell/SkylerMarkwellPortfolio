// @ts-check
import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";

// Hosted on Vercel at the root of skylermarkwell.vercel.app.
export default defineConfig({
  site: "https://skylermarkwell.vercel.app",
  trailingSlash: "always",
  vite: { plugins: [tailwindcss()] },
});
